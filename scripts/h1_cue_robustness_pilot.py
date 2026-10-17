"""Small matched continuation: exact target cues versus state-independent cue jitter."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import argparse
import contextlib
import gc
import io
import json
import os
import random
import subprocess
import sys

from PIL import Image

from h1_state_gate import ROOT, DEFAULT, read_jsonl, write_jsonl, evaluate, parse
from h1_target_controls import score_different_targets, compare_different_targets
from h1_compare_state_runs import compare
from h1_target_grid import ADAPTER
from h1_cue_perturbation import paint, shifted_bounds, VARIANTS, DATA as PERTURB_DATA

DATA=ROOT/'data/h1/cue_robustness_pilot_v1'
RESULT=ROOT/'results/h1/showo2_video_1_5b/cue_robustness_pilot_v1'
CACHE=ROOT/'checkpoints/h1_cue_robustness_pilot_v1'
RAW=ROOT/'data/h1/state_target_cue_v1/raw'
TEXT=ROOT/'data/h1/state_training_v1'
CONTRAST=ROOT/'data/h1/state_target_contrast_v1'


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def select_cases(rows,labels,count,seed,include_layout=False):
    grouped=defaultdict(list);cases=defaultdict(list)
    for row in rows:cases[row['case_id']].append(row)
    for cid,case in cases.items():
        completion=next(r for r in case if r['task']=='completion')
        key=(completion['layout'],labels[completion['sample_id']]['expected']) if include_layout else labels[completion['sample_id']]['expected']
        grouped[key].append(cid)
    rng=random.Random(seed)
    buckets=list(grouped.values());rng.shuffle(buckets)
    for bucket in buckets:rng.shuffle(bucket)
    chosen=[]
    while len(chosen)<count:
        for bucket in buckets:
            if bucket and len(chosen)<count:chosen.append(bucket.pop())
    return [row for cid in chosen for row in cases[cid]]


def build():
    DATA.mkdir(parents=True,exist_ok=False);RESULT.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=False)
    source_ref=RAW/'train_reference';source_current=RAW/'train'
    ref_labels={r['sample_id']:r for r in read_jsonl(source_ref/'labels.jsonl')}
    cur_labels={r['sample_id']:r for r in read_jsonl(source_current/'labels.jsonl')}
    text_labels={r['sample_id']:r for r in read_jsonl(TEXT/'labels.jsonl')}
    ref=select_cases(read_jsonl(source_ref/'inputs.jsonl'),ref_labels,32,10423,True)
    current=select_cases([r for r in read_jsonl(source_current/'inputs.jsonl') if r['view']=='current_only'],cur_labels,16,10424)
    text=select_cases([r for r in read_jsonl(TEXT/'inputs.jsonl') if r['split']=='train' and r['view']=='oracle_text' and r['response_format']=='json'],text_labels,16,10425)
    (DATA/'text_replay').mkdir()
    write_jsonl(DATA/'text_replay/inputs.jsonl',text)
    write_jsonl(DATA/'text_replay/labels.jsonl',[text_labels[r['sample_id']] for r in text])
    scenes={r['case_id']:r for r in json.loads((CONTRAST/'scenes.json').read_text())}
    keys=sorted({(r['group_id'],r['target']) for r in ref})
    random.Random(10426).shuffle(keys)
    assigned={key:VARIANTS[i%len(VARIANTS)] for i,key in enumerate(keys)}
    for arm in ('exact','jitter'):
        directory=DATA/arm;(directory/'images').mkdir(parents=True)
        rows=[]
        for original in ref:
            row=dict(original)
            path=directory/'images'/f'{row["case_id"]}.png'
            points=scenes[row['scene_id']]['strokes'][row['target']]
            if arm=='jitter':
                variant=assigned[(row['group_id'],row['target'])]
                bounds=shifted_bounds(points,variant)
            else:
                variant='exact';xs,ys=zip(*points)
                bounds=[min(xs)-12,min(ys)-12,max(xs)+12,max(ys)+12]
            if not path.exists():paint(Image.open(source_ref/row['images'][0]).convert('RGB'),bounds).save(path)
            row.update(images=[str(path.relative_to(directory))],cue_variant=variant,cue_condition=arm)
            rows.append(row)
        for original in current:
            row=dict(original)
            row['images']=[os.path.relpath(source_current/row['images'][0],directory)]
            rows.append(row)
        write_jsonl(directory/'inputs.jsonl',rows)
        write_jsonl(directory/'labels.jsonl',[ref_labels.get(r['sample_id'],cur_labels.get(r['sample_id'])) for r in rows])
    # x_plus6 and width_plus6 were declared before intervention scores were read.
    # y_plus6 was added after that diagnosis, before training, as exploratory stress.
    for variant in ('x_plus6','width_plus6','y_plus6'):
        directory=DATA/'evaluation'/variant;directory.mkdir(parents=True)
        rows=[]
        for original in read_jsonl(PERTURB_DATA/'inputs.jsonl'):
            if original['cue_variant']!=variant:continue
            row=dict(original);row['images']=[os.path.relpath(PERTURB_DATA/row['images'][0],directory)]
            rows.append(row)
        ids={r['sample_id'] for r in rows}
        write_jsonl(directory/'inputs.jsonl',rows)
        write_jsonl(directory/'labels.jsonl',[r for r in read_jsonl(PERTURB_DATA/'labels.jsonl') if r['sample_id'] in ids])
    save(DATA/'cue_assignment.json',[dict(group_id=g,target=t,variant=v) for (g,t),v in sorted(assigned.items())])
    save(RESULT/'plan.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        role='Small matched augmentation pilot, not independent acceptance. Run after the frozen-model cue intervention establishes sensitivity.',
        arms=['exact','jitter'],initial_adapter=str(ADAPTER.relative_to(ROOT)),
        training_rows=dict(reference_current=len(ref),current_only=len(current),oracle_text=len(text)),
        reference_cases=32,current_cases=16,text_cases=16,reference_geometry_groups=len({r['group_id'] for r in ref}),
        sampling='Training data only; reference cases stratified by layout and completion class; retention cases stratified by completion class. Seeds 10423/10424/10425.',
        cue_assignment='Fixed round-robin over eight +/-6px translations/length/width changes after shuffling reference geometry+target keys, seed10426. One target uses the same perturbation across all its current states.',
        controls='Same selected questions, labels, initial weights, row order, optimizer and updates; only target-reference cues in the reference_current subset differ.',
        optimization=dict(epochs=1,steps=64,accumulation=4,learning_rate=.0001,seed=731,
                          parameters=311296,layers=list(range(20,28)),rank=8,alpha=16,
                          loss='Existing answer+EOS cross entropy; identical text and current-only replay in both arms.'),
        evaluations=['Original correct-cue target dev','Predicted-cue target dev','Fixed x_plus6 target dev','Fixed width_plus6 target dev','Original current-only dev','Original text dev'],
        additional_stress_test='y_plus6 chosen after the frozen intervention showed the largest completion drop, declared before training; an exploratory secondary condition, not an independently predeclared test.',
        localization_policy='Predicted cue images are fixed outputs from the preceding localizer and original adapter, shared by both arms. This pilot changes only the state adapter; compatibility of the new adapter with the localization head is not tested.',
        evaluation_cache='Reuse CPU embeddings of immutable evaluation images across the two language-only adapter conditions; frozen base visual weights unchanged. Language inference recomputed for each adapter. Exact arm pays first image encoding, so wall times are not a matched compute comparison.',
        evaluation_policy='Final checkpoint only. The two perturbations are fixed before reading intervention scores; they do not establish invariance to all eight. No original 130-case visual test.',
        primary='Matched-arm predicted-cue completion and different-target pair outcomes; both-wording consistency; report every regression.',
        limitation='One small update budget, one seed, three repeatedly inspected target geometries; wider geometry/character/font and temporal tests remain required.'))
    save(DATA/'selection.json',dict(reference_sample_ids=[r['sample_id'] for r in ref],current_sample_ids=[r['sample_id'] for r in current],
        text_sample_ids=[r['sample_id'] for r in text],completion_classes={name:dict(Counter(labels[r['sample_id']]['expected'] for r in rows if r['task']=='completion'))
            for name,rows,labels in [('reference',ref,ref_labels),('current',current,cur_labels),('text',text,text_labels)]}))
    print(dict(reference=len(ref),current=len(current),text=len(text),reference_targets=len(keys)))


def train(arm):
    with (CACHE/f'{arm}_training.log').open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts/h1_train_state.py'),'--data',str(DATA/arm),
            '--views','reference_current','current_only','--text-replay',str(DATA/'text_replay'),
            '--init-adapter',str(ADAPTER),'--epochs','1','--lr','.0001','--output',str(RESULT/arm/'training'),
            '--adapter',str(CACHE/arm/'adapter.pt'),'--eval-policy','Final-only matched 64-step exact/jitter pilot; six primary development/retention conditions plus exploratory y_plus6. No held-out calls.'],
            cwd=ROOT,env=dict(os.environ,PYTORCH_ENABLE_MPS_FALLBACK='1'),stdout=log,stderr=subprocess.STDOUT,check=True)


def evaluation_sources():
    return [('correct',ROOT/'data/h1/state_target_cue_v1/boxed/all_targets_dev','reference_current'),
            ('predicted',ROOT/'data/h1/predicted_target_cue_v1','reference_current'),
            ('x_plus6',DATA/'evaluation/x_plus6','reference_current'),
            ('width_plus6',DATA/'evaluation/width_plus6','reference_current'),
            ('y_plus6',DATA/'evaluation/y_plus6','reference_current'),
            ('current',DEFAULT,'current_only'),('text',TEXT,'oracle_text')]


def evaluate_arm(arm,image_cache=None):
    import torch
    from h1_run_showo import run as infer
    for name,directory,view in evaluation_sources():
        output=RESULT/arm/name
        args=argparse.Namespace(source=ROOT/'checkpoints/Show-o-source',model=ROOT/'checkpoints/Show-o2-1.5B-video',
            assets=ROOT/'checkpoints/Show-o-assets',device='mps',inputs=directory/'inputs.jsonl',output=output,
            split='dev',view=view,format='json',constrain_answers=True,adapter=CACHE/arm/'adapter.pt',
            adapter_grad_forward=False,blank_image=False,limit=None,max_tokens=32,
            chat_template='tokenizer' if view=='oracle_text' else 'official_mmu')
        with (CACHE/f'{arm}_{name}.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
            infer(args,image_cache=image_cache)
        gc.collect();torch.mps.empty_cache()
        with contextlib.redirect_stdout(io.StringIO()):
            evaluate(directory,output/'predictions.jsonl','dev','json',output/'score',view)
            if name in ('correct','predicted','x_plus6','width_plus6','y_plus6'):
                score_different_targets(directory,output,output/'score/different_target_pairs.json')


def evaluate_all():
    # The two trained adapters touch language q/v projections only. The base
    # visual modules and all evaluation image paths are identical between arms.
    image_cache={}
    for arm in ('exact','jitter'):evaluate_arm(arm,image_cache)
    save(RESULT/'evaluation_cache.json',dict(images=len(image_cache),
        policy='CPU embeddings reused across the two language-adapter conditions; identical frozen base visual modules and immutable image paths. No train/test reuse or label input.',
        timing='Exact-arm runs pay first image encoding; jitter-arm runs reuse it. Wall-clock evaluation times are not a matched compute comparison.'))
    compare_arms()
    summarize()


def compare_arms():
    with contextlib.redirect_stdout(io.StringIO()):
        for name,directory,view in evaluation_sources():
            compare(directory,RESULT/'exact'/name,RESULT/'jitter'/name,RESULT/f'{name}_jitter_vs_exact.json',view,'dev')
            if name in ('correct','predicted','x_plus6','width_plus6','y_plus6'):
                compare_different_targets(directory,RESULT/'exact'/name,RESULT/'jitter'/name,
                                          RESULT/f'{name}_pairs_jitter_vs_exact.json')
    print('Matched final-checkpoint comparisons saved.')


def summarize():
    old=ROOT/'results/h1/showo2_video_1_5b/target_cue_v1/boxed'
    perturb=json.loads((ROOT/'results/h1/showo2_video_1_5b/cue_perturbation_v1/score.json').read_text())
    def target_metrics(directory):
        score=json.loads((directory/'score/summary.json').read_text())['metrics']
        pairs=json.loads((directory/'score/different_target_pairs.json').read_text())['metrics']
        return dict(presence=score['reference_current/presence/correct']['correct'],
            completion=score['reference_current/completion/correct']['correct'],questions_per_task=56,
            completion_both_wordings=score['reference_current/completion/both_correct']['correct'],cases=28,
            completion_pairs=pairs['completion']['correct'],pairs=20)
    report=dict(role='Final matched pilot and unchanged original-adapter controls; development only.',target_conditions={},retention={},training={})
    for name in ('correct','predicted','x_plus6','width_plus6','y_plus6'):
        if name in ('correct','predicted'):
            source=old/'targets_boxed_dev' if name=='correct' else ROOT/'results/h1/showo2_video_1_5b/predicted_target_cue_v1/state_dev'
            initial=target_metrics(source)
        else:
            p=perturb['conditions'][name+'/presence'];c=perturb['conditions'][name+'/completion']
            initial=dict(presence=p['correct'],completion=c['correct'],questions_per_task=56,
                completion_both_wordings=c['both_wordings_correct'],cases=28,completion_pairs=c['target_pairs_correct'],pairs=20)
        report['target_conditions'][name]=dict(initial=initial,**{arm:target_metrics(RESULT/arm/name) for arm in ('exact','jitter')})
    for name,directory,view in evaluation_sources():
        if name not in ('current','text'):continue
        for arm in ('exact','jitter'):
            output=RESULT/f'{name}_{arm}_vs_initial.json'
            with contextlib.redirect_stdout(io.StringIO()):
                compare(directory,old/f'{name}_dev',RESULT/arm/name,output,view,'dev')
            comparison=json.loads(output.read_text())['metrics']
            report['retention'][f'{arm}/{name}']={task:{k:comparison[task][k] for k in ('n','before_correct','after_correct','paired_cluster_bootstrap_95')}
                                                 for task in ('presence','completion')}
        # Class counts on the same prompt/pixel deduplication rule as compare().
        rows=[r for r in read_jsonl(directory/'inputs.jsonl') if r['split']=='dev' and r['view']==view and r['response_format']=='json' and r['task']=='completion']
        labels={r['sample_id']:r for r in read_jsonl(directory/'labels.jsonl')}
        runs={arm:{r['sample_id']:r for r in read_jsonl((old/f'{name}_dev' if arm=='initial' else RESULT/arm/name)/'predictions.jsonl')}
              for arm in ('initial','exact','jitter')}
        pixels={};seen=set();counts={}
        for row in rows:
            for image_path in row['images']:
                if image_path not in pixels:
                    im=Image.open(directory/image_path).convert('RGB');pixels[image_path]=(im.size,im.tobytes())
            key=(row['prompt'],tuple(pixels[p] for p in row['images']))
            if key in seen:continue
            seen.add(key);lab=labels[row['sample_id']]
            cell=counts.setdefault(lab['expected'],dict(n=0,initial=0,exact=0,jitter=0));cell['n']+=1
            for arm,responses in runs.items():
                cell[arm]+=int(parse(responses[row['sample_id']]['raw_response'],'json',lab['allowed'])==lab['expected'])
        report['retention'][name+'_completion_classes']=counts
    for arm in ('exact','jitter'):
        run=json.loads((RESULT/arm/'training/run.json').read_text())
        report['training'][arm]={k:run[k] for k in ('train_rows','steps','trainable_parameters','image_preparation_seconds','elapsed_seconds')}
    save(RESULT/'summary.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','train','evaluate','evaluate-all','compare','summarize'])
    parser.add_argument('--arm',choices=['exact','jitter'])
    parser.add_argument('--data',type=Path,default=DATA);parser.add_argument('--output',type=Path,default=RESULT)
    parser.add_argument('--cache',type=Path,default=CACHE)
    args=parser.parse_args();DATA,RESULT,CACHE=args.data.resolve(),args.output.resolve(),args.cache.resolve()
    if args.command in ('train','evaluate') and args.arm is None:parser.error('--arm is required for training/evaluation')
    if args.command=='train':train(args.arm)
    elif args.command=='evaluate':evaluate_arm(args.arm)
    else:{'build':build,'evaluate-all':evaluate_all,'compare':compare_arms,'summarize':summarize}[args.command]()
