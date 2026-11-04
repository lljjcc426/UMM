"""CPU-only verification commands for the method feasibility package."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from .paired import read_pairs, parse_description, audit_disjoint
from .program import parse_program, save_mp4, audit_mp4, render_frames


def demo_programs():
    """Small hand-coded geometry fixtures. Not independent scholarly gold."""
    return {
        'tu': {'version': 1, 'canvas': [256, 256], 'fps': 24, 'strokes': [
            {'order': 1, 'type': 1, 'path': [[.35, .32], [.65, .32]], 'width': .038, 'frames': 12},
            {'order': 2, 'type': 2, 'path': [[.5, .28], [.5, .73]], 'width': .04, 'frames': 16},
            {'order': 3, 'type': 1, 'path': [[.2, .73], [.8, .73]], 'width': .045, 'frames': 16}
        ]},
        'shi': {'version': 1, 'canvas': [256, 256], 'fps': 24, 'strokes': [
            {'order': 1, 'type': 1, 'path': [[.2, .33], [.8, .33]], 'width': .038, 'frames': 12},
            {'order': 2, 'type': 2, 'path': [[.5, .29], [.5, .70]], 'width': .04, 'frames': 16},
            {'order': 3, 'type': 1, 'path': [[.35, .7], [.65, .7]], 'width': .045, 'frames': 16}
        ]}
    }


def build_fixtures(root):
    from PIL import Image
    root = Path(root)
    (root / 'examples' / 'media').mkdir(parents=True, exist_ok=True)
    descriptions = {'tu': ('土', '横、竖、横、土'), 'shi': ('士', '横、竖、横、士')}
    rows = []
    for name, src in demo_programs().items():
        program = parse_program(src)
        program_path = root / 'examples' / f'{name}.program.json'
        program_path.write_text(json.dumps(src, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
        character, desc = descriptions[name]
        sid = sha256(('synthetic-demo-'+name).encode()).hexdigest()[:16]
        image_file = root / 'examples' / 'media' / f'{sid}.png'
        image = Image.fromarray(list(render_frames(program))[-1])
        image.save(image_file)
        rows.append({'id': sid, 'model_inputs': {'image': f'media/{sid}.png'},
                     'training_targets': {'description': desc}})
    (root/'examples'/'synthetic_pairs.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows), encoding='utf8')
    # A DIFFERENT permutation of the same three instances produces the same end image.
    swapped = demo_programs()['tu'].copy()
    strokes = demo_programs()['tu']['strokes']
    swapped['strokes'] = [{**s, 'order': i+1} for i, s in enumerate([strokes[2], strokes[1], strokes[0]])]
    (root/'examples'/'tu_swapped.program.json').write_text(json.dumps(swapped, ensure_ascii=False, indent=2)+'\n',encoding='utf8')
    return rows


def smoke_models():
    """Run forward/backward tensor contract only; NO optimizer update and NO training."""
    import torch
    from .fusion import TinyPairedStrokeModel, stroke_sequence_loss, global_contrastive_loss, MODES
    from .paired import EOS
    torch.set_num_threads(1)
    torch.default_generator.manual_seed(20261104)
    images = torch.rand(2, 3, 64, 64)
    targets = torch.tensor([[1, 2, 1, EOS], [1, 2, 1, EOS]], dtype=torch.long)
    names = torch.tensor([ord('土'), ord('士')], dtype=torch.long)
    results = {}
    for mode in MODES:
        model = TinyPairedStrokeModel(mode=mode, width=32, heads=4)
        out = model(images, targets, names)
        assert out.logits.shape == (2, 4, 9)
        assert out.attention is None if mode in ('sft','global') else out.attention.shape == (2,4,16)
        losses = [stroke_sequence_loss(out, targets)]
        if mode != 'sft':
            losses.append(global_contrastive_loss(out))
        total = sum(losses)
        assert bool(torch.isfinite(total))
        total.backward()  # gradient plumbing only; no parameter updates
        assert any(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
        results[mode] = {'logits_shape': list(out.logits.shape),
                         'attention_shape': list(out.attention.shape) if out.attention is not None else None,
                         'forward_backward_finite': True,
                         'optimizer_steps': 0,
                         'pretrained_weights_loaded': False}
    return {'mode_checks': results, 'torch_version': torch.__version__, 'GPU_calls': 0, 'actual_model_train_steps': 0}


def cli():
    parser = argparse.ArgumentParser()
    command = parser.add_subparsers(dest='command', required=True)
    a = command.add_parser('build-fixtures')
    a.add_argument('--root', type=Path, default=Path('.'))
    a = command.add_parser('audit-pairs')
    a.add_argument('--pairs', type=Path, required=True)
    a.add_argument('--root', type=Path, required=True)
    a = command.add_parser('render')
    a.add_argument('--program', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    a = command.add_parser('smoke-models')
    a = command.add_parser('integrate')
    a.add_argument('--dataset', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    a.add_argument('--features', action='store_true', help='Use cached CPU torch for random interface checks; no optimizer')
    args = parser.parse_args()
    if args.command == 'build-fixtures':
        rows = build_fixtures(args.root)
        print(json.dumps({'built': len(rows), 'fixture_only': True},ensure_ascii=False))
    elif args.command == 'audit-pairs':
        pairs = read_pairs(args.pairs, args.root)
        print(json.dumps({'pairs':len(pairs),'stroke_counts':[len(p.strokes) for p in pairs],
                          'unique_chars':len(set(p.character for p in pairs)),
                          'gold_labels_loaded':False},ensure_ascii=False))
    elif args.command == 'render':
        program = parse_program(args.program.read_text(encoding='utf8'))
        result = save_mp4(program,args.output)
        result['decoded_audit'] = audit_mp4(args.output)
        (args.output.with_suffix('.report.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == 'integrate':
        from .integration import integrate
        print(json.dumps(integrate(args.dataset, args.output, features=args.features), ensure_ascii=False))
    elif args.command == 'smoke-models':
        print(json.dumps(smoke_models(),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    cli()
