"""Package the remaining pilot reviews with cached official reference pages."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import html
import json
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

from .data import read_jsonl, write_json
from .review import build_review


def prepare(dataset, pdf, references, output, record_path, batch_size=20):
    rows = [r for r in read_jsonl(dataset / 'manifest.jsonl') if r['split'] != 'audit_development']
    output.mkdir(parents=True, exist_ok=False)
    official = references / 'official'
    official.mkdir(parents=True, exist_ok=True)
    pages = sorted({r['norm_reference']['pdf_page'] for r in rows})

    def render(page):
        target = official / f'page-{page:03d}.png'
        if target.exists():
            return
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1800',
                        '-singlefile', '-png', str(pdf), str(target.with_suffix(''))],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    with ThreadPoolExecutor(max_workers=4) as workers:
        list(workers.map(render, pages))
    batches, cards = [], []
    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        name = f'batch-{len(batches) + 1:02d}'
        revision = 'S1-pilot-independent-review-v1-' + name
        built = build_review(dataset, references, output / name,
                             sample_ids={r['id'] for r in batch}, revision=revision,
                             include_pair=True, create_archive=False)
        built.update(sample_ids=[r['id'] for r in batch], batch=name)
        batches.append(built)
        cards.append(f'<li><a href="{name}/index.html">第{len(batches)}批：{len(batch)}字</a>'
                     f' · {built["strokes"]}笔 · 完整选择{built["manual_decisions"]}项'
                     f' · 字符：{html.escape("".join(r["character"] for r in batch))}</li>')
    text = ('本包覆盖尚未审核的240字，分12批，每批20字；已完成的16字不在其中。\n\n'
            '解压后用Chrome或Edge打开index.html，进入各批。每批使用相同固定审核者代号。\n\n'
            '可以先只核对每字第一项：完整字图是否为本字、五类序列是否与规范原页一致。'
            '导出后可接收PAIR图文对审核记录；E3/E4/E5未填项继续待审。\n\n'
            '若继续完成逐笔真值，按每笔实例/笔序、起终点、每对关系逐项填写。全包共14772个选择项，'
            '包括240项图文序列、2189项实例/顺序、2189项方向、10154项笔画对判断。'
            '同一对需阅读六项关系，任一项无法判断可如实填未知。\n\n'
            '每批可分次导出JSON备份；草稿按批隔离。使用页面“导入”恢复此前进度。'
            '多人须各自独立填写。没有默认通过或批量通过。导出文件交回当前聊天，无需编辑JSON。\n\n'
            '规范页面仅供本地查阅，字形许可及原版权见各批licenses。候选标签与图片中的标记均待核对，'
            '程序准备这些材料不计入人工提交。\n')
    (output / '先读我.md').write_text(text)
    (output / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>S1剩余240字审核</title>'
        '<style>body{font:18px/1.8 system-ui;max-width:980px;margin:32px auto;padding:16px}li{margin:12px 0}a{color:#164ab7}</style>'
        '<h1>S1剩余240字独立审核</h1>' + ''.join(f'<p>{html.escape(p)}</p>' for p in text.split('\n\n'))
        + '<ol>' + ''.join(cards) + '</ol>')
    archive = output.with_suffix('.zip')
    with ZipFile(archive, 'x', ZIP_DEFLATED) as zipped:
        for asset in sorted(output.rglob('*')):
            if asset.is_file():
                zipped.write(asset, asset.relative_to(output))
    record = {'package_revision': 'S1-pilot-independent-review-v1', 'output': str(output),
              'zip': str(archive), 'characters': len(rows), 'batches': batches,
              'reference_pdf': str(pdf), 'reference_pages': pages,
              'manual_decisions': sum(b['manual_decisions'] for b in batches),
              'pair_only_decisions': len(rows), 'actual_submissions_created': 0}
    write_json(record_path, record)
    print(json.dumps({k: v for k, v in record.items() if k not in ('batches', 'reference_pages')}, ensure_ascii=False, indent=2))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path('data/research/paired_strokes_v1'))
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--references', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.dataset, args.pdf, args.references, args.output, args.record)


if __name__ == '__main__':
    main()
