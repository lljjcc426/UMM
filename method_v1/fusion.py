"""Small CPU-only *interface* prototype; no pretrained UMM/VLM or reported capability.

This tests aligned tensor APIs and causal supervision before implementation
using actual foundation-model backbones. Never interpret random logits or
attention as evidence of stroke recognition.
"""
from dataclasses import dataclass
import torch
from torch import nn
from torch.nn import functional as F

from .paired import PAD, MASK, BOS, EOS

MODES = ('sft', 'global', 'cross', 'ordered')


@dataclass
class Output:
    logits: torch.Tensor               # (B, T, 9)
    attention: torch.Tensor | None    # (B, T, P), diagnostics only
    image_embedding: torch.Tensor
    text_embedding: torch.Tensor | None


class TinyPairedStrokeModel(nn.Module):
    """Causal image-to-sequence baseline and alternative fusion surfaces.

    target_tokens are used to create SHIFTED prefixes; the token at the
    prediction position is NEVER given to that position's sequence decoder.
    The full sequence is only read by a SEPARATE global alignment head.
    """
    def __init__(self, mode='ordered', width=64, heads=4, patch=16, max_tokens=65):
        super().__init__()
        if mode not in MODES or width % heads:
            raise ValueError('Unsupported fusion mode or width/heads')
        self.mode, self.max_tokens, self.width = mode, max_tokens, width
        self.vision = nn.Conv2d(3, width, kernel_size=patch, stride=patch)
        self.visual_position = nn.Linear(2, width, bias=False)
        self.text_tokens = nn.Embedding(9, width, padding_idx=PAD)
        self.position = nn.Embedding(max_tokens, width)
        self.ordered_slots = nn.Embedding(max_tokens, width)
        self.causal_self = nn.MultiheadAttention(width, heads, batch_first=True)
        self.cross = nn.MultiheadAttention(width, heads, batch_first=True)
        self.visual_norm = nn.LayerNorm(width)
        self.decoder_norm = nn.LayerNorm(width)
        self.classifier = nn.Linear(width, 9)
        self.image_proj = nn.Linear(width, width)
        self.full_text_proj = nn.Linear(width, width)
        self.character_embed = nn.Embedding(65536, width)
        inactive = []
        if mode in ('sft', 'global'):
            inactive.append(self.cross)
        if mode != 'ordered':
            inactive.append(self.ordered_slots)
        if mode == 'sft':
            inactive.extend((self.image_proj, self.full_text_proj, self.character_embed))
        for module in inactive:
            module.requires_grad_(False)

    def encode_image(self, images):
        if images.ndim != 4 or images.shape[1] != 3:
            raise ValueError('Expected (B,3,H,W) float RGB tensor')
        features = self.vision(images)
        height, width = features.shape[-2:]
        yy, xx = torch.meshgrid(torch.linspace(0, 1, height, device=images.device),
                                torch.linspace(0, 1, width, device=images.device), indexing='ij')
        coordinates = torch.stack((xx, yy), dim=-1).reshape(1, -1, 2)
        patches = features.flatten(2).transpose(1, 2)
        return self.visual_norm(patches + self.visual_position(coordinates))

    def decode_prefix(self, patches, prefix):
        B, T = prefix.shape
        if T > self.max_tokens or prefix.min() < 0 or prefix.max() > EOS:
            raise ValueError('Invalid prefix length or tokens')
        pos = torch.arange(T, device=prefix.device).unsqueeze(0)
        x = self.text_tokens(prefix) + self.position(pos)
        future = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1)
        x = x + self.causal_self(x, x, x, attn_mask=future, need_weights=False)[0]
        attention = None
        if self.mode in ('sft', 'global'):
            x = x + patches.mean(dim=1, keepdim=True)
        else:
            query = x if self.mode == 'cross' else x + self.ordered_slots(pos)
            spatial, attention = self.cross(query, patches, patches,
                                             need_weights=True, average_attn_weights=True)
            x = x + spatial
        return self.classifier(self.decoder_norm(x)), attention

    def forward(self, image, targets, character_unicode=None):
        if targets.ndim != 2 or targets.shape[1] < 1:
            raise ValueError('targets must be BxT including EOS')
        B, T = targets.shape
        if image.shape[0] != B:
            raise ValueError('Image/token batch mismatch')
        prefix = torch.cat((torch.full((B, 1), BOS, device=targets.device, dtype=targets.dtype),
                            targets[:, :-1]), dim=1)
        patches = self.encode_image(image)
        logits, weights = self.decode_prefix(patches, prefix)
        image_embedding = F.normalize(self.image_proj(patches.mean(1)), dim=-1)
        text_embedding = None
        if character_unicode is not None:
            if character_unicode.shape != (B,) or character_unicode.max() >= 65536 or character_unicode.min() < 0:
                raise ValueError('Expected BMP Unicode codepoints for paired text encoding')
            # Only the global contrastive branch gets the full text target.
            # It must NOT be passed into decode_prefix or image-only inference.
            full = self.text_tokens(targets)
            valid = targets.ne(PAD).unsqueeze(-1)
            encoded = (full * valid).sum(1) / valid.sum(1).clamp_min(1)
            encoded = encoded + self.character_embed(character_unicode)
            text_embedding = F.normalize(self.full_text_proj(encoded), dim=-1)
        return Output(logits, weights, image_embedding, text_embedding)

    @torch.no_grad()
    def predict_tokens(self, image, max_generated=32):
        """Run image-only autoregressive inference. There is NO gold D input."""
        patches = self.encode_image(image)
        B = image.shape[0]
        prefix = torch.full((B, 1), BOS, device=image.device, dtype=torch.long)
        out = []
        for _ in range(min(max_generated, self.max_tokens - 1)):
            logits, _ = self.decode_prefix(patches, prefix)
            token = logits[:, -1].argmax(-1)
            out.append(token)
            prefix = torch.cat((prefix, token[:, None]), 1)
            if bool(torch.all(torch.stack(out, 1).eq(EOS).any(1))):
                break
        return torch.stack(out, 1)


def stroke_sequence_loss(output: Output, targets):
    return F.cross_entropy(output.logits.reshape(-1, 9), targets.reshape(-1), ignore_index=PAD)


def global_contrastive_loss(output: Output, temperature=0.1):
    """Use only with B>=2 and distinct exact descriptions per batch.

    Identical (stroke sequence, character) pairs must not be treated as hard
    negatives. The caller is responsible for checking description identities.
    """
    if output.text_embedding is None or output.image_embedding.shape[0] < 2:
        raise ValueError('Global loss needs paired full text and at least 2 different pairs')
    score = output.image_embedding @ output.text_embedding.T / temperature
    labels = torch.arange(score.shape[0], device=score.device)
    return (F.cross_entropy(score, labels) + F.cross_entropy(score.T, labels)) / 2
