"""CPU benchmark validation/evaluation CLI; model predictions are optional and explicit."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .contracts import save,validate_manifest,validate_input
from .media import decode,validate_media
from .observer import observe_rgb,judge_execution
from .build import REGIONS,REFERENCE
from .evaluate import score_response,summarize


def audit(dataset,destination,predictions=None):
    dataset=Path(dataset);out=Path(destination);out.mkdir(parents=True,exist_ok=False)
    rows=[json.loads(s) for s in (dataset/'manifest.jsonl').read_text().splitlines()]
    validation=validate_manifest(rows);media_checks=[];cpu=[]
    for row in rows:
        p=dataset/row['input'];value=validate_input(json.loads(p.read_text()))
        if row['media_audit'] and row['media_audit']['kind']=='native_video':
            f,t=decode(p.parent/value['media'][0]);media_checks.append({'id':row['id'],**validate_media('native_video',f,t,row['media_audit']['frames'])})
            if row['source_group']=='micro-two-lines':
                observed=observe_rgb(f,t,REGIONS)
                cpu.append({'id':row['id'],'status':'completed','case':json.loads((dataset/row['evaluation']).read_text())['case'],
                            'observation':observed,'facets':judge_execution(observed,REFERENCE)})
    answers=[];index={r['id']:r for r in rows}
    if predictions is not None:
        incoming=json.loads(Path(predictions).read_text())
        if len({p['id'] for p in incoming})!=len(incoming):raise ValueError('Duplicate prediction ID')
        for pred in incoming:
            row=index[pred['id']];answer=json.loads((dataset/row['evaluation']).read_text())
            answers.append({'id':pred['id'],'track':row['track'],**score_response(row['track'],pred['response'],answer)})
    save(out/'decoded_media.json',media_checks);save(out/'CPU_pixel_observations.json',cpu)
    save(out/'response_comparisons.json',answers)
    summary={'status':'CPU_diagnostic_audit_completed',**validation,'decoded_video_count':len(media_checks),
             'microtask_count':len(cpu),'model_predictions_supplied':len(answers),'formal_primary_metrics':None,
             'new_model_calls':0,'CPU_fixture_metrics':summarize(cpu,required_facets=('stroke_order','direction','completeness','historical_ink','temporal_observability'))}
    save(out/'summary.json',summary);return summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--output',required=True);p.add_argument('--predictions')
    a=p.parse_args();r=audit(a.dataset,a.output,a.predictions)
    print(json.dumps({k:v for k,v in r.items() if k!='CPU_fixture_metrics'},ensure_ascii=False))

if __name__=='__main__':main()
