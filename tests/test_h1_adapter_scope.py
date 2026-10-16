"""Verify that extending an adapter preserves its starting function and enables learning."""
from types import SimpleNamespace
import unittest

import torch
from torch import nn

from scripts.h1_train_state import add_adapter, extend_adapter_layers


class AdapterScopeTest(unittest.TestCase):
    def test_extension_preserves_old_updates_and_new_layers_receive_gradients(self):
        torch.manual_seed(13)
        layers = []
        for _ in range(4):
            attention = nn.ModuleDict({name: nn.Linear(8, 8, bias=False) for name in ('q_proj', 'v_proj')})
            attention.requires_grad_(False)
            layers.append(SimpleNamespace(self_attn=attention))
        model = SimpleNamespace(showo=SimpleNamespace(model=SimpleNamespace(layers=layers)))
        config = dict(rank=2, alpha=4, layers=[2, 3], projections=['q_proj', 'v_proj'])
        add_adapter(model, config)
        with torch.no_grad():
            for layer in layers[2:]:
                for name in config['projections']:
                    getattr(layer.self_attn, name).lora_b.normal_(std=.05)
        old_modules = [getattr(layer.self_attn, name) for layer in layers[2:] for name in config['projections']]
        x = torch.randn(3, 8)

        def forward(value):
            for layer in layers:
                value = value + layer.self_attn.q_proj(value) + layer.self_attn.v_proj(value)
            return value

        before = forward(x).detach()
        extended = extend_adapter_layers(model, config, 4)
        self.assertEqual(extended['added_layers'], [0, 1])
        self.assertEqual(extended['layers'], [0, 1, 2, 3])
        self.assertEqual(old_modules, [getattr(layer.self_attn, name) for layer in layers[2:]
                                      for name in config['projections']])
        after = forward(x)
        self.assertTrue(torch.equal(before, after.detach()))
        after.square().mean().backward()
        for layer in layers[:2]:
            for name in config['projections']:
                module = getattr(layer.self_attn, name)
                self.assertGreater(module.lora_b.grad.abs().sum().item(), 0)
                self.assertIsNone(module.base.weight.grad)


if __name__ == '__main__':
    unittest.main()
