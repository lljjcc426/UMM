"""Prepare offline independent review forms, without creating submissions."""
import argparse
from collections import defaultdict
import html
import json
from pathlib import Path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

import numpy as np
from PIL import Image, ImageDraw

from .data import NOTICE, read_jsonl, write_json
from .gold import save_png

APP = Path(__file__).with_name('review_app.js')
WORDS = {'left': '左侧', 'right': '右侧', 'above': '上方', 'below': '下方',
         'intersect': '轮廓接触或重叠', 'longer': '中线更长'}
DIRECTIONS = {'right': '右', 'down_right': '右下', 'down': '下', 'down_left': '左下',
              'left': '左', 'up_left': '左上', 'up': '上', 'up_right': '右上'}


def choice(key, label):
    return (f'<label>{html.escape(label)} <select data-key="{key}">'
            '<option value="">待核对</option><option value="accepted">符合</option>'
            '<option value="disputed">有误</option><option value="unknown">无法判断</option></select></label>')


def build_review(dataset, references, output, *, sample_ids=None,
                 revision='S1-independent-review-form-v1', include_pair=False,
                 create_archive=True):
    output.mkdir(parents=True, exist_ok=False)
    (output / 'media').mkdir()
    (output / 'official').mkdir()
    (output / 'licenses').mkdir()
    geometry = {g['id']: g for g in read_jsonl(dataset / 'evaluation_only/geometry.jsonl')}
    rows = [r for r in read_jsonl(dataset / 'manifest.jsonl')
            if (r['id'] in sample_ids if sample_ids is not None else r['split'] == 'audit_development')]
    tasks, cards, total_pairs = [], [], 0
    for row in rows:
        sid, item = row['id'], geometry[row['id']]
        shutil.copyfile(dataset / row['model_inputs']['image'], output / row['model_inputs']['image'])
        with np.load(dataset / item['mask_archive']) as archive:
            masks = archive['masks']
        full = masks.any(axis=0)
        tiles, identity_keys, direction_keys = [], [], []
        for i, path in enumerate(item['paths'], 1):
            rgb = np.full((256, 256, 3), 255, dtype='uint8')
            rgb[full] = [210, 210, 210]
            rgb[masks[i - 1]] = [25, 25, 25]
            image = Image.fromarray(rgb)
            draw = ImageDraw.Draw(image)
            for point, color in [(path[0], 'green'), (path[-1], 'red')]:
                x, y = np.asarray(point) * 256
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            image_path = f'media/{sid}-stroke-{i}.png'
            save_png(output / image_path, np.asarray(image))
            identity, directed = f'{sid}:identity:{i}', f'{sid}:direction:{i}'
            identity_keys.append(identity)
            direction_keys.append(directed)
            tiles.append(f'<div class="stroke"><h4>候选第{i}笔</h4><img src="{image_path}" alt="第{i}笔位置与起终点">'
                         + choice(identity, '实例位置与规范笔序')
                         + f'<p>绿点起、红点终；起终点位移：{DIRECTIONS[item["directions"][i - 1]["direction"]]}</p>'
                         + choice(directed, '规范起终点与方向') + '</div>')
        pairs = defaultdict(list)
        for relation in item['relations']:
            pairs[(relation['a'], relation['b'])].append(relation)
        pair_cards, pair_keys = [], []
        for (a, b), values in pairs.items():
            rgb = np.full((256, 256, 3), 255, dtype='uint8')
            rgb[full] = [210, 210, 210]
            rgb[masks[a - 1]] = [25, 85, 210]
            rgb[masks[b - 1]] = [205, 60, 25]
            rgb[masks[a - 1] & masks[b - 1]] = [135, 30, 160]
            image_path = f'media/{sid}-pair-{a}-{b}.png'
            save_png(output / image_path, rgb)
            key = f'{sid}:pair:{a}:{b}'
            pair_keys.append(key)
            claims = '；'.join(f'{WORDS[v["relation"]]}：' +
                              ('未知（容差带）' if v['answer'] is None else '是' if v['answer'] else '否') for v in values)
            pair_cards.append(f'<div class="pair"><img src="{image_path}" alt="两笔位置对照">'
                              f'<div><h4>蓝色第{a}笔，相对橙色第{b}笔</h4><p>{claims}</p>'
                              + choice(key, '以上六项候选关系') + '</div></div>')
        total_pairs += len(pairs)
        sequence_key = f'{sid}:sequence'
        note_key = f'{sid}:notes'
        tasks.append({'sample_id': sid, 'character': row['character'], 'gold_revision': item['gold_revision'],
                      'norm_reference': item['norm_reference'], 'stroke_ids': item['stroke_ids'],
                      'sequence_key': sequence_key, 'identity_keys': identity_keys,
                      'direction_keys': direction_keys, 'pair_keys': pair_keys, 'note_key': note_key})
        if include_pair:
            tasks[-1]['facets'] = ['PAIR', 'E3', 'E4', 'E5']
        page = item['norm_reference']['pdf_page']
        official = f'official/page-{page:03d}.png'
        if not (output / official).exists():
            shutil.copyfile(references / official, output / official)
        cards.append(f'<details class="character" {"open" if not cards else ""}><summary>{row["character"]}'
                     f' · {len(item["stroke_ids"])}笔 <span data-character-status="{sid}"></span></summary>'
                     f'<div class="reference"><img src="{row["model_inputs"]["image"]}" alt="完整字图">'
                     f'<div><p>规范物理页 {page}，字表序号 {item["norm_reference"]["index"]}。</p>'
                     f'<a href="{official}" target="_blank">打开规范原页，放大查阅</a>'
                     f'<p>候选五类编码：{" ".join(row["sequence"])}</p>'
                     + choice(sequence_key, '完整字图为本字，五类序列与规范原页一致') + '</div></div>'
                     '<h3>逐笔核对</h3><p>黑色是当前笔，浅灰是其余笔。先核对实例和次序，再看起终点。'
                     '“有误”或“无法判断”请在本字备注中写明笔号与原因。</p><div class="strokes">'
                     + ''.join(tiles) + '</div><h3>笔画间关系</h3>'
                     '<p>逐对阅读六项候选关系；一对中任一项有误即选“有误”，无法确认则选“无法判断”。'
                     '上下左右按质心与2%画布容差，中线长短用5%容差；接触/重叠包含相接，不等同于穿越。</p>'
                     + (''.join(pair_cards) if pair_cards else '<p>单笔字，无笔画对；E4不适用。</p>')
                     + f'<label>本字备注（指出笔号/笔画对、错误项与判断依据）<textarea data-key="{note_key}" rows="3"></textarea></label></details>')
    data = {'package_revision': revision, 'tasks': tasks}
    write_json(output / 'review_specification.json', data)
    encoded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>16字逐笔独立审核</title><style>
body{font:16px/1.6 system-ui,sans-serif;color:#242424;max-width:1140px;margin:24px auto;padding:0 18px;background:#fafafa}
h1{font-size:26px}h3{margin-bottom:8px}h4{margin:8px 0}a{color:#164ab7}label{display:block;margin:10px 0}select,input,textarea,button{font:inherit;padding:7px;border:1px solid #aaa;border-radius:4px}
textarea{display:block;box-sizing:border-box;width:100%;max-width:900px}button{background:#17449a;color:white;cursor:pointer;margin:8px 12px 8px 0}input[type=checkbox]{width:20px;height:20px;vertical-align:middle}
.toolbar{position:sticky;top:0;background:#fff;border:1px solid #bbb;padding:10px 14px;z-index:2}.toolbar p{margin:4px 0}
.character{border:1px solid #bbb;border-radius:6px;background:white;margin:18px 0;padding:14px}summary{font-size:24px;cursor:pointer}summary span{font-size:14px;color:#555}
.reference,.pair{display:flex;gap:22px;align-items:center;flex-wrap:wrap}.reference img{width:180px}.strokes{display:flex;gap:14px;flex-wrap:wrap}.stroke{border:1px solid #ddd;padding:12px;width:280px}.stroke img{width:230px;display:block}
.pair{border-top:1px solid #ddd;padding:10px 0}.pair img{width:155px}.pair>div{flex:1;min-width:220px}.pair p{max-width:780px}.notice{font-size:13px;color:#555}#message{color:#9c2400}
@media(max-width:600px){.toolbar{position:static}.stroke{width:100%}.pair img{width:130px}}
</style><h1>16字、54笔独立审核</h1>
<p>请独立对照规范原页核对候选标签。未参与标签构建且亲自核查的审核者填写本表；多人审核时各自填写、分别导出，不先交换答案。所有选择初始为“待核对”，没有批量通过功能。</p>
<p>依次核对：规范序列 → 每笔位置与顺序 → 起终点 → 每对笔画的六项关系。无法判断可如实填写，不需要强行通过。静态图只核对规范方向。</p>
<div class="toolbar"><label>审核者代号（每人固定、互不重复） <input id="reviewer" autocomplete="off"></label>
<label><input type="checkbox" id="independent"> 我未参与这批候选标签构建，导出的已完成项目由我亲自对照规范核查。</label>
<p id="progress"></p><button id="export">导出审核结果 / 备份进度</button>
<label>继续此前导出的进度 <input type="file" id="import" accept=".json"></label><p id="message" role="status"></p></div>
<main>''' + ''.join(cards) + '</main><p class="notice">' + html.escape(NOTICE) + '''</p>
<p><a href="licenses/ARPHICPL.TXT">Arphic Public License</a> · <a href="licenses/COPYING">来源说明</a>。规范原页仅供本地查阅。</p>
<script id="review-data" type="application/json">''' + encoded + '</script><script src="review_app.js"></script></html>'
    strokes = sum(len(t['stroke_ids']) for t in tasks)
    page = page.replace('16字、54笔', f'{len(tasks)}字、{strokes}笔').replace('16字逐笔', f'{len(tasks)}字逐笔')
    if include_pair:
        page = page.replace('<div class="toolbar">',
                            '<p>可先只核对每字第一项，导出PAIR记录以完成图文对审核；逐笔与关系未填部分继续保留待审，不会自动通过。</p><div class="toolbar">')
    (output / 'index.html').write_text(page)
    shutil.copyfile(APP, output / APP.name)
    for name in ('COPYING', 'ARPHICPL.TXT'):
        shutil.copyfile(dataset / 'licenses' / name, output / 'licenses' / name)
    readme = f'''# 16字独立逐笔审核

解压整个ZIP，用Chrome或Edge打开index.html，无需联网、安装软件或编辑JSON。图片和official目录须与网页保持相对位置。

填写固定审核者代号。若多人参与，每人用自己的副本独立填写，不预先交换答案。未参与候选标签构建且亲自查阅规范的审核者勾选页面确认项。

本包共16字54笔：16项规范序列、54项实例/顺序、54项规范起终点，以及{total_pairs}个笔画对的六项关系复核。每对需读完六项候选再选择；任一项有误可选有误，不能确认可选无法判断。此处审核全部笔画对，覆盖本轮108条E4请求。

页面没有默认通过或全部通过。可分次核对，浏览器保存本地草稿；离开前点“导出审核结果 / 备份进度”保存JSON，也可在别的设备导入继续。不同审核者不要共用一份已填答案。核对错误时在本字备注写明笔号/笔画对、问题项与依据。

完成后将导出的JSON文件交还给项目负责人；负责人转交本聊天即可。无需修改JSON。导出文件包含原始逐项判断、备注、待完成项与按字/指标汇总；项目中的正式审核登记不会因准备网页或运行界面测试自动增加。

规范页中的字表序号与网页对应，可点击原页放大。黑色为当前笔、浅灰为其余笔；绿色起点、红色终点；关系图中蓝色为第一笔，橙色为第二笔，紫色为交叠。图中标记都是待核对候选。

左右/上下按轮廓质心判断，2%画布内留未知；更长按中线弧长与5%容差；轮廓接触/重叠包含相接。若无法确认这些具体定义下的候选值，请选无法判断。规范方向不代表真实书写历史。

本包为开发材料，不能使其他240字自动通过。字形许可在licenses中，规范页面仅供本地查阅。原只读审核包保留。
'''
    readme = readme.replace('16字54笔', f'{len(tasks)}字{strokes}笔').replace('16字', f'{len(tasks)}字')
    if include_pair:
        readme = readme.replace('16项规范序列、54项实例/顺序、54项规范起终点',
                                f'{len(tasks)}项规范序列、{strokes}项实例/顺序、{strokes}项规范起终点')
        readme = readme.replace('此处审核全部笔画对，覆盖本轮108条E4请求。', '此处审核本批全部笔画对，复杂字尚未新增模型请求。')
        readme = readme.replace('本包为开发材料，不能使其他240字自动通过。', '本包只覆盖所列开发字，未填的逐笔/关系项继续待审。')
        readme += '\n可先只完成每字第一项后导出：PAIR单独记录图文与规范序列核查；E3/E4/E5仍需各自逐笔完成。\n'
    (output / '先读我.md').write_text(readme)
    archive = output.with_suffix('.zip') if create_archive else None
    if create_archive:
        with ZipFile(archive, 'x', ZIP_DEFLATED) as zipped:
            for asset in sorted(output.rglob('*')):
                if asset.is_file():
                    zipped.write(asset, asset.relative_to(output))
    record = {'package_revision': data['package_revision'], 'characters': len(tasks),
              'strokes': strokes, 'pairs': total_pairs,
              'relation_claims': total_pairs * 6,
              'manual_decisions': sum(1 + len(t['identity_keys']) + len(t['direction_keys']) + len(t['pair_keys']) for t in tasks),
              'output': str(output), 'zip': str(archive) if archive else None, 'actual_submissions': 0}
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=Path, default=Path('data/research/paired_strokes_v1'))
    parser.add_argument('--references', type=Path, default=Path('private/paired_strokes_v1_2026-11-02/review'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    write_json(args.record, build_review(args.dataset, args.references, args.output))


if __name__ == '__main__':
    main()
