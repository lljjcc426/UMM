"""Export two isolated offline human-review packages; never create human judgments."""
import json
from pathlib import Path
import random
import shutil
import zipfile

import numpy as np
from PIL import Image

from scripts.p1.full_common import sha256


PAGE = r'''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P1独立视频审核</title>
<style>body{font:17px system-ui;max-width:1100px;margin:25px auto;padding:12px;color:#182230}button,select,input,textarea{font:inherit;padding:7px;margin:5px}video,#frame{width:min(848px,95vw);background:#eee}label{display:inline-block;min-width:240px}section{padding:14px;background:#f3f5f8;margin:12px 0}textarea{width:95%;min-height:65px}#reference{max-width:95%;max-height:240px}small{display:block;color:#475467}</style>
<h1>P1 独立实际视频审核</h1><p>仅按可见视频判断。规范参考可供核对；看不清先后或方向时选择 unknown。最终字形相似不能证明过程正确。请独立填写，提交前不查看另一位审核者答案或自动分析。</p>
<p>correct：该维度有足够可见证据支持正确；incorrect：有可指明的错误；unknown：证据不足。not_applicable 仅用于确不适用，须写明理由。时间可判性：correct=过程清晰可判，incorrect=可见时序损坏/遮挡导致缺失，unknown=无法确定。</p>
<div id="status"></div><button id="prev">上一项</button><select id="jump"></select><button id="next">下一项</button>
<h2 id="title"></h2><div id="missing"></div><video id="video" controls preload="metadata"></video>
<section><button id="back">前一帧</button><input id="slider" type="range" min="0" value="0"><button id="forward">后一帧</button><span id="frameinfo"></span><br><img id="frame" alt="实际解码帧"></section>
<details><summary>可信规范原件（展开核验）</summary><img id="reference" alt="规范原件"></details>
<section><label>审核者代号 <input id="reviewer" placeholder="自行填写"></label><div id="fields"></div><label>首错起点秒 <input id="start" type="number" min="0" step="0.001"></label><label>首错终点秒 <input id="end" type="number" min="0" step="0.001"></label><p>首错区间不适用或无法定位时留空，并说明原因。</p><textarea id="reason" placeholder="错误证据、未知原因、参考争议或不适用理由"></textarea><label><input id="disputed" type="checkbox">存在参考或判断争议</label><button id="save">保存本项</button></section>
<button id="export">导出批注JSON</button><label>导入批注 <input id="import" type="file" accept="application/json"></label><p>进度保存在本浏览器；结束时务必导出JSON。每次保存保留版本。离线直接打开 index.html 即可，无需安装软件或联网。</p>
<script src="cards.js"></script><script>
const dimensions={stroke_order:'笔顺',direction:'方向',completeness:'笔画完整性',historical_ink:'旧墨迹保留',temporal_observability:'时间可判性',final_glyph:'最终字形',task_compliance:'任务合规（目标字、空白起笔、逐笔写入等）'};
const key='P1-blind-'+PACKAGE.id;let db=JSON.parse(localStorage.getItem(key)||'{"current":{},"versions":[]}'),index=0,frameIndex=0;
const $=x=>document.getElementById(x);for(const [k,v] of Object.entries(dimensions)){let l=document.createElement('label');l.textContent=v+' ';let s=document.createElement('select');s.id=k;for(const v of ['', 'correct','incorrect','unknown','not_applicable']){let o=document.createElement('option');o.value=v;o.textContent=v||'待选择';s.append(o)}l.append(s);$('fields').append(l)}
PACKAGE.cards.forEach((c,i)=>{let o=document.createElement('option');o.value=i;o.textContent=(i+1)+' / '+PACKAGE.cards.length+' · '+c.id;$('jump').append(o)});
function persist(){localStorage.setItem(key,JSON.stringify(db))}function paintFrame(){let c=PACKAGE.cards[index];frameIndex=Math.max(0,Math.min((c.frames||[]).length-1,frameIndex));$('slider').value=frameIndex;$('frame').src=c.frames?.[frameIndex]||'';$('frameinfo').textContent=c.frames?.length?`帧 ${frameIndex} / ${c.frames.length-1} · PTS ${c.PTS[frameIndex]}秒`:''}
function show(){let c=PACKAGE.cards[index],a=db.current[c.id]||{};$('jump').value=index;$('title').textContent=(index+1)+' / '+PACKAGE.cards.length+' · '+c.id+' · 目标字 '+c.character;$('video').src=c.video||'';$('video').style.display=c.video?'block':'none';$('missing').textContent=c.video?'':'此槽位无可审核原片。保留缺失，不能代填笔顺结论。';$('reference').src=c.reference;for(const k of Object.keys(dimensions))$(k).value=a[k]||'';$('start').value=a.first_error_start??'';$('end').value=a.first_error_end??'';$('reason').value=a.reason||'';$('disputed').checked=!!a.disputed;$('reviewer').value=a.reviewer||$('reviewer').value;$('slider').max=Math.max(0,(c.frames||[]).length-1);frameIndex=0;paintFrame();$('status').textContent=`已保存 ${Object.keys(db.current).length} / ${PACKAGE.cards.filter(c=>c.video).length} 可审项；另有 ${PACKAGE.cards.filter(c=>!c.video).length} 缺失槽位，目标共 ${PACKAGE.cards.length} 槽位。请保存后再切换。`}
$('save').onclick=()=>{let c=PACKAGE.cards[index];if(!c.video){alert('无片槽位无需填写，已保留为缺失。');return}let a={id:c.id,reviewer:$('reviewer').value.trim(),submitted_at:new Date().toISOString(),reason:$('reason').value,disputed:$('disputed').checked,first_error_start:$('start').value===''?null:Number($('start').value),first_error_end:$('end').value===''?null:Number($('end').value)};for(const k of Object.keys(dimensions))a[k]=$(k).value;if(!a.reviewer||Object.keys(dimensions).some(k=>!a[k])){alert('请填写审核者代号及全部七项判断。');return}if(Object.keys(dimensions).some(k=>a[k]!=='correct')&&!a.reason.trim()){alert('错误、未知或不适用项请写明证据或理由。');return}db.current[c.id]=a;db.versions.push(a);persist();show()};
$('prev').onclick=()=>{index=Math.max(0,index-1);show()};$('next').onclick=()=>{index=Math.min(PACKAGE.cards.length-1,index+1);show()};$('jump').onchange=e=>{index=Number(e.target.value);show()};$('back').onclick=()=>{frameIndex--;paintFrame()};$('forward').onclick=()=>{frameIndex++;paintFrame()};$('slider').oninput=e=>{frameIndex=Number(e.target.value);paintFrame()};
$('export').onclick=()=>{let blob=new Blob([JSON.stringify({schema:'P1-human-review-v1',package_id:PACKAGE.id,protocol:PACKAGE.protocol,...db},null,2)],{type:'application/json'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='P1-'+PACKAGE.id+'-annotations.json';a.click();URL.revokeObjectURL(a.href)};
$('import').onchange=async e=>{let x=JSON.parse(await e.target.files[0].text());if(x.package_id!==PACKAGE.id||Object.keys(x.current).some(id=>!PACKAGE.cards.some(c=>c.id===id))){alert('批注不属于本审核包');return}db={current:{...db.current,...x.current},versions:[...db.versions,...x.versions]};persist();show()};show();
</script></html>'''


def main():
    private=Path('private/p1_full_server_2026-10-30')
    public=Path('data/research/runs/p1_full_server_2026-10-30')
    manifest=json.loads((public/'manifest.json').read_text())
    output=private/'offline_review';output.mkdir(exist_ok=False)
    sources=[]
    for row in manifest['generation']:
        base=(Path('private/p1_native_pilot_issue3_2026-10-30/requests') if row['reused'] else private/'requests')/row['id']
        videos=list(base.glob('runs/*/'+row['task']+'/outputs/*.mp4'))
        arrays=list(base.glob('runs/*/'+row['task']+'/decoded_rgb_uint8.npz'))
        probes=list(base.glob('runs/*/'+row['task']+'/ffprobe.json'))
        sources.append(dict(id=row['id'],character=row['character'],norm_id=row['norm_id'],
                            video=videos[0] if videos else None,array=arrays[0] if arrays else None,probe=probes[0] if probes else None))
    for row in manifest['controls']:
        base=private/'diagnostics/controls'/row['id']
        sources.append(dict(id=row['id'],character=next(g['character'] for g in manifest['generation'] if g['norm_id']==row['norm_id']),
                            norm_id=row['norm_id'],video=base/'control.mp4',array=base/'decoded_RGB_12fps.npz',probe=base/'ffprobe.json'))
    mappings={};summaries=[]
    for number in [1,2]:
        rng=random.Random(202610300700+number);rows=sources.copy();rng.shuffle(rows)
        package_id=f'P1-independent-{number}';directory=output/f'reviewer_{number}';directory.mkdir()
        media=directory/'media';media.mkdir();cards=[];mapping=[]
        for row in rows:
            blind='V'+format(rng.getrandbits(56),'014x');card=dict(id=blind,character=row['character'])
            reference=media/(blind+'-reference.png')
            shutil.copy2(Path('private/p0_final_calibration_2026-10-28/reference')/(row['norm_id']+'.png'),reference)
            card['reference']='media/'+reference.name
            if row['video'] is not None and row['video'].exists() and row['array'] is not None and row['array'].exists():
                video=media/(blind+'.mp4');shutil.copy2(row['video'],video);card['video']='media/'+video.name
                frames=np.load(row['array'])['frames'];card['frames']=[]
                probe=json.loads(row['probe'].read_text())
                card['PTS']=[float(f['best_effort_timestamp_time']) for f in probe['frames'] if f['media_type']=='video']
                for i,frame in enumerate(frames):
                    path=media/f'{blind}-f{i:03}.png';Image.fromarray(frame).save(path)
                    card['frames'].append('media/'+path.name)
            else:card.update(video=None,frames=[],PTS=[])
            cards.append(card);mapping.append(dict(blind_id=blind,source_id=row['id'],
                original_MP4_sha256=sha256(row['video']) if row['video'] is not None and row['video'].exists() else None))
        (directory/'index.html').write_text(PAGE)
        (directory/'cards.js').write_text('const PACKAGE = '+json.dumps(dict(id=package_id,protocol='P1-human-review-v1',cards=cards),ensure_ascii=False)+';\n')
        checksums=[dict(path=str(p.relative_to(directory)),bytes=p.stat().st_size,sha256=sha256(p))
                   for p in sorted(directory.rglob('*')) if p.is_file()]
        (directory/'SHA256SUMS.json').write_text(json.dumps(checksums,indent=2)+'\n')
        with zipfile.ZipFile(output/(directory.name+'.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
            for path in directory.rglob('*'):
                if path.is_file():z.write(path,path.relative_to(output))
        mappings[package_id]=mapping;summaries.append(dict(package_id=package_id,slots=len(cards),playable=sum(bool(c['video']) for c in cards),
            planned_target_slots=len(cards),required_playable_video_judgments=sum(bool(c['video']) for c in cards),actual_human_submissions=0))
    (private/'review_blind_mapping_private.json').write_text(json.dumps(mappings,ensure_ascii=False,indent=2)+'\n')
    summary=dict(status='pending_human_review',reviewers=summaries,blind_to=['method','condition','seed','prompt','automatic_analysis'],
                 total_planned_video_review_slots=144,pending_playable_video_reviews=sum(r['required_playable_video_judgments'] for r in summaries),actual_human_reviews=0,understanding_review_optional_additional=56,
                 independent_mapping_outside_packages=True)
    (public/'offline_review_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
