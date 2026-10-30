"""CPU-only P1 request preparation; no model import, inference or new gold labels."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

from scripts.p0.evaluate_decoupled import geometry_for, load_inputs


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build_requests(plan, audits):
    """Freeze comparable request IDs; the 16 pilot calls are part of the full64."""
    rows = []
    for stratum in plan['strata']:
        for nid in stratum['ids']:
            audit = audits[nid]
            common = dict(norm_id=nid, character=audit['character'], stratum=stratum['name'],
                reference_level='official_norm_plus_existing_global_human_and_AI_development_binding',
                formal_geometry_gold=False, status='planned_not_executed')
            for condition in plan['conditions']:
                seeds = plan['seeds'] if condition in ['T_G0_native_simple', 'T_G0_order_text'] else [plan['seeds'][0]]
                for seed in seeds:
                    rows.append(dict(common, id=f'{nid}-{condition}-s{seed}', condition=condition,
                        seed=seed, task='i2v' if condition=='T_G0_blank_i2v' else 't2v',
                        geometry_permission='G1_fixed_development_template' if condition=='T_G1_template_text' else 'G0',
                        pilot=nid in plan['pilot_ids'] and seed in plan['pilot_seeds']
                              and condition in ['T_G0_native_simple', 'T_G0_order_text']))
    return rows


def prompt_for(row, audit, geometry=None):
    prompt = (f'A fixed camera looks at a plain white canvas. Starting with a blank canvas, write the complete '
        f'Chinese character {row["character"]} in black monoline ink, one stroke at a time, '
        'following the mainland simplified Chinese stroke order in GF0023-2020. '
        'Preserve all existing ink. No hand, pen, cuts, camera movement or extra characters.')
    if row['condition'] != 'T_G0_native_simple':
        prompt += ' Required stroke types in normative order: ' + ', '.join(audit['descriptions']) + '.'
    if row['condition'] == 'T_G1_template_text':
        # Extra spatial information is explicit G1. Container order has no rank.
        by_id = {r['instance_id']:r['canonical_id'] for r in audit['review_records']}
        boxes = []
        for g in sorted(geometry, key=lambda g:g.instance_id):
            y,x = np.nonzero(g.mask)
            boxes.append(dict(instance_id=g.instance_id, canonical_id=by_id[g.instance_id],
                normalized_bbox=[round(float(x.min()/g.mask.shape[1]),3),round(float(y.min()/g.mask.shape[0]),3),
                                 round(float((x.max()+1)/g.mask.shape[1]),3),round(float((y.max()+1)/g.mask.shape[0]),3)]))
        prompt += ' Fixed development template spatial hints (unordered): ' + json.dumps(boxes)
    return prompt


def prepare(plan_path, output, private_output, upstream):
    if output.exists() or private_output.exists():
        raise ValueError('Use fresh preparation directories; preserve previous versions')
    plan = json.loads(plan_path.read_text())
    tasks,_,_=load_inputs()
    audits = json.loads(Path('data/research/runs/p0_decoupled_d1_d4_2026-10-29/static_qualification_audit.json').read_text())
    rows = build_requests(plan, audits)
    human = {r['internal_id']:r for r in csv.DictReader(Path(
        'data/research/runs/p0_human_acceptance_2026-10-29/normative_accepted_candidates.csv').open())}
    selected = {r['norm_id'] for r in rows}
    if any(n not in human or any(json.loads(human[n][f'reasons{k}']) or human[n][f'notes{k}'].strip()
                                 for k in [1,2]) for n in selected):
        raise ValueError('Selected normative references require a clean existing paired global review; no automatic gold upgrade')
    output.mkdir(parents=True)
    private_output.mkdir(parents=True)
    for row in rows:
        bundle = (private_output/row['id']).resolve()
        inputs = bundle/'inputs';inputs.mkdir(parents=True)
        prompt = prompt_for(row,audits[row['norm_id']],geometry_for(tasks[row['norm_id']])[0]
                            if row['geometry_permission']!='G0' else None)
        sample = {'0001':prompt}
        if row['task']=='i2v':
            blank=inputs/'blank.png'
            Image.new('RGB',(plan['native']['width'],plan['native']['height']),'white').save(blank)
            sample={'0001':dict(interleave_array=[prompt,str(blank)],element_dtype_array=['text','image'],istarget_in_interleave=[0,0])}
        save(inputs/(row['task']+'.json'),sample)
        native_plan=dict(plan['native'],experiment_id='BASE-01',scope='P1 proposed no-finetuning single request; actual RGB independent human evaluation',
            tasks=[row['task']],seed=row['seed'],request=row,code_revision=plan['model']['code_revision'],
            weight_revision=plan['model']['weight_revision'],approval={'user_approved':False,'scope_limit':'GPU execution requires a new explicit approval'})
        save(bundle/'plan.json',native_plan)
        (bundle/'upstream').symlink_to(upstream.resolve(),target_is_directory=True)
        row['prepared_bundle']=str(bundle.relative_to(Path.cwd()))
    save(output/'requests.json',rows)
    save(output/'summary.json',dict(status='prepared_not_executed',total_generation_requests=len(rows),
        pilot_requests=sum(r['pilot'] for r in rows),expanded_incremental_requests=sum(not r['pilot'] for r in rows),
        native_G0_t2v=48,blank_G0_i2v=8,template_G1_t2v=8,
        deterministic_geometry_controls_planned=8,SO01_understanding_calls_planned=28,
        model_imports=0,GPU_calls=0,new_human_tasks=0,new_video_files=0,
        formal_geometry_gold_created=False,source_revision='45a90c17 + current preparation code',
        future_materialization='On the approved host, relocate bundles and update upstream symlink/input absolute paths; attach explicit GPU approval before execution. No local weights assumed.'))
    save(output/'command_plan.json',dict(phase='P1_preparation_only',
        dry_run_command='python -m scripts.env01.run_interfaces --bundle PREPARED_BUNDLE --dry-run',
        future_execution_command='python -m scripts.env01.run_interfaces --bundle PREPARED_BUNDLE',
        conditions=['Obtain explicit GPU experiment approval','Materialize fixed upstream and weights on GPU host',
                    'Rebase onto approved P1 branch after P0 merge approval','Freeze actual deployment and sampling version',
                    'Set plan.approval.user_approved with approval evidence before execution'],
        output_accounting='Each native invocation creates a new run directory and preserves process/log/metrics. Join request IDs across all attempts; no best-of selection.'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,default=Path('configs/research/p1_baseline_plan.json'))
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--private-output',type=Path,required=True)
    p.add_argument('--upstream',type=Path,required=True)
    a=p.parse_args();prepare(a.plan,a.output,a.private_output,a.upstream)
