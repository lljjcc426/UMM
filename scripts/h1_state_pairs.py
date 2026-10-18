"""Matched state-head continuation with endpoint and background counterfactuals."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse
import json
import math
import random
import time

import numpy as np
from PIL import Image, ImageDraw

import h1_progress_coverage as prior
import h1_endpoint_pairs as endpoint
from h1_region_state import ROOT, KINDS, CLASSES, render, make_state_head
from h1_run_showo import load_model, StateImageEncoder
from h1_spatial_probe import CACHE as SPATIAL_CACHE
from h1_state_gate import interval, read_jsonl, write_jsonl

DATA = ROOT / 'data/h1/state_pairs_v1'
RESULT = ROOT / 'results/h1/showo2_video_1_5b/state_pairs_v1'
CACHE = ROOT / 'checkpoints/h1_state_pairs_v1'
ARMS = ['replay', 'endpoint', 'paired']
GAPS = [1, 2, 4, 8, 16]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def build():
    DATA.mkdir(parents=True, exist_ok=False)
    (DATA / 'images').mkdir()
    RESULT.mkdir(parents=True, exist_ok=False)
    CACHE.mkdir(parents=True, exist_ok=False)
    images = json.loads((prior.DATA / 'images.json').read_text())
    prior_count = len(images)
    endpoint_images = json.loads((endpoint.DATA / 'images.json').read_text())
    endpoint_map = {}
    for i, row in enumerate(endpoint_images):
        if 'reused_index' in row:
            endpoint_map[i] = row['reused_index']
        else:
            endpoint_map[i] = len(images)
            images.append(row)
    reused = len(images)
    queries = json.loads((prior.DATA / 'queries.json').read_text())
    train = json.loads((prior.DATA / 'train_coverage.json').read_text())
    old_by_query = defaultdict(list)
    for r in train:
        if r['kind'] in KINDS:
            old_by_query[r['query_index']].append(r)
    targets = list(old_by_query)
    rng = random.Random(10450)
    rng.shuffle(targets)
    gap_assignment = {q: GAPS[i % len(GAPS)] for i, q in enumerate(targets)}
    supplements = {arm: [] for arm in ARMS}
    assignments = []

    def current(name, q, target_fraction, background, split):
        fractions = dict(background, **{q['target']: target_fraction})
        if all(v == 1 for v in fractions.values()):
            return q['reference_index']
        path = DATA / 'images' / f'{name}.png'
        render(q['strokes'], fractions, q['width']).save(path)
        index = len(images)
        images.append(dict(image=str(path.relative_to(ROOT)), split=split))
        return index

    def row(q, name, index, gap, background):
        length = math.dist(*q['strokes'][q['target']])
        return dict(sample_id=name, group_id=q['group_id'], kind=q['kind'],
            query_index=q['query_id'], reference_index=q['reference_index'], current_index=index,
            target=q['target'], fraction=1 - gap / length, gap_px=gap,
            background_id=background, reference_available=True, reference_pair=None,
            scene_id=name, expected='完整' if gap == 0 else '部分')

    for qi in sorted(targets):
        q = queries[qi]
        gap = gap_assignment[qi]
        length = math.dist(*q['strokes'][q['target']])
        base = {k: .5 for k in q['strokes'] if k != q['target']}
        altered = {k: rng.choice([0, .25, .75, 1]) for k in base}
        assignments.append(dict(query_index=qi, gap_px=gap, altered_background=altered))
        members = {}
        for bg, fractions in [('half', base), ('varied', altered)]:
            for g in (0, gap):
                name = f'train-q{qi:03}-{bg}-gap{g:02}'
                index = current(name, q, 1 - g / length, fractions, 'train')
                members[bg, g] = row(q, name, index, g, bg)
        complete = next(r for r in old_by_query[qi] if r['fraction'] == 1)
        partial = max((r for r in old_by_query[qi] if 0 < r['fraction'] < 1), key=lambda r: r['fraction'])
        for bg in ('half', 'varied'):
            for g in (0, gap):
                slot = f'q{qi:03}-{bg}-gap{g:02}'
                control = dict(complete if g == 0 else partial)
                control.update(sample_id=slot, family_id=qi, slot_id=slot)
                supplements['replay'].append(control)
                for arm in ('endpoint', 'paired'):
                    source_bg = 'half' if arm == 'endpoint' else bg
                    record = dict(members[source_bg, g], sample_id=slot, family_id=qi, slot_id=slot)
                    supplements[arm].append(record)

    old_endpoint = []
    for r in json.loads((endpoint.DATA / 'cases.json').read_text()):
        r = dict(r)
        r['reference_index'] = endpoint_map[r['reference_index']]
        r['current_index'] = endpoint_map[r['current_index']]
        r.update(background_id='half', reference_available=True, reference_pair=None, scene_id=r['sample_id'])
        old_endpoint.append(r)
    # New background inputs are fixed before training; geometry remains development.
    rng = random.Random(10451)
    dev_background = []
    for qi in sorted({r['query_index'] for r in old_endpoint}):
        q = queries[qi]
        length = math.dist(*q['strokes'][q['target']])
        fractions = {k: rng.choice([.15, .85]) for k in q['strokes'] if k != q['target']}
        for gap in (0, 8, 16):
            base = next(r for r in old_endpoint if r['query_index'] == qi and r['gap_px'] == gap)
            dev_background.append(dict(base))
            name = f'dev-q{qi:03}-varied-gap{gap:02}'
            index = current(name, q, 1 - gap / length, fractions, 'dev')
            dev_background.append(dict(row(q, name, index, gap, 'varied'), other_fractions=fractions))

    sets = dict(train_replay=train, dev_endpoint=old_endpoint, dev_background=dev_background,
        dev_previous=json.loads((prior.DATA / 'dev_previous.json').read_text()),
        dev_fresh=json.loads((prior.DATA / 'dev_fresh.json').read_text()))
    for arm, records in supplements.items():
        sets[f'supplement_{arm}'] = records
    for name, records in sets.items():
        save(DATA / f'{name}.json', records)
    save(DATA / 'images.json', images)
    save(DATA / 'assignments.json', assignments)
    labels = [CLASSES.index(r['expected']) for r in train]
    supplemented_labels = [CLASSES.index(r['expected']) for r in supplements['paired']]
    assert all([r['expected'] for r in supplements[arm]] == [r['expected'] for r in supplements['paired']] for arm in ARMS)
    save(RESULT / 'plan.json', dict(created_utc=datetime.now(timezone.utc).isoformat(),
        question='Do paired endpoint examples improve completion boundaries, and does changing only other strokes add background robustness?',
        model='Full frozen Show-o2-1.5B-w-video-und native visual path; original language adapter, target localizer and ink head unchanged. Only 57,764-parameter state heads continue training.',
        arms=dict(replay='Original full and highest partial state, each repeated twice per target.',
            endpoint='Full and assigned pixel gap on half-stroke background, each repeated twice.',
            paired='Same full and gap states, once on half background and once with independently varied other strokes.'),
        training=dict(steps=400, batch_size=32, original_examples_per_step=16, supplemental_families_per_step=4,
            supplemental_examples_per_family=4, lr=.0003, weight_decay=.01, seed=10452, optimizer='AdamW',
            loss='Four-class cross entropy only; no additional pair, consistency or ranking loss.',
            sampling='Same original indices and target-family indices for all arms; all four family members appear together.',
            class_weights='Inverse class probability of the 50:50 original/supplement mixture, fixed before training and identical across arms.',
            original_counts=[labels.count(i) for i in range(4)], supplement_counts=[supplemented_labels.count(i) for i in range(4)],
            initialization='Each region starts from its existing coverage head; optimizer reset. Oracle and predicted regions each run all three arms.',
            original_cases=len(train), supplement_slots=len(supplemented_labels), families=len(targets),
            training_geometry_groups=len({r['group_id'] for r in supplements['paired']}),
            gap_assignment_seed=10450, gap_counts=dict(Counter(gap_assignment.values())),
            background_levels=[0,.25,.5,.75,1]),
        evaluation=dict(previous=len(sets['dev_previous']), fresh=len(sets['dev_fresh']),
            endpoint=len(old_endpoint), background=len(dev_background), background_seed=10451,
            new_background_levels=[.15,.85], new_background_gaps=[0,8,16],
            policy='All conditions fixed before training. Final weights only; no threshold/checkpoint selection. Baseline, all arms on their own region; predicted-region arms also on oracle regions.',
            metrics='Per-gap and macro completion, full/partial pair both correct, all-gap success, background-pair both correct and answer flips, old presence/unknown/reference/target pairs, training fit. Whole-geometry bootstrap.'),
        costs=dict(prior_images=prior_count, endpoint_images=len(endpoint_images)-len([r for r in endpoint_images if 'reused_index' in r]),
            reused_images=reused, new_images=len(images)-reused),
        scope='Training geometry and development geometry remain disjoint. Development geometry was previously inspected; new backgrounds are prospective inputs, not independent acceptance. No original 130-case test, Chinese/order/H2/H3 or native-language claim.',
        interpretation='Replay versus endpoint changes both gap coverage and context; it is a combined data intervention. Endpoint versus paired isolates the replacement of duplicate half-background slots by varied backgrounds. Sample slots and update budget are matched, unique image diversity is not.'))
    draw_examples(supplements, images)
    print(json.dumps(dict(train=len(train), supplement=len(supplemented_labels), new_images=len(images)-reused)))


def draw_examples(supplements, images):
    canvas = Image.new('RGB', (5 * 216, 3 * 150), '#eeeeee')
    draw = ImageDraw.Draw(canvas)
    for i, kind in enumerate(KINDS):
        first = next(r for r in supplements['paired'] if r['kind'] == kind)
        rows = [r for r in supplements['paired'] if r['family_id'] == first['family_id']]
        indices = [first['reference_index']] + [r['current_index'] for r in rows]
        labels = [f"reference q{first['query_index']}"] + [f"{r['background_id']}, gap {r['gap_px']}" for r in rows]
        for j, (index, label) in enumerate(zip(indices, labels)):
            picture = Image.open(ROOT / images[index]['image']).crop((0,0,432,216)).resize((216,108))
            canvas.paste(picture, (216*j, 150*i+30))
            draw.text((216*j+5,150*i+8),label,fill='black')
    canvas.save(RESULT / 'training_examples.png')


def extract():
    import torch
    start = time.perf_counter()
    plan = json.loads((RESULT / 'plan.json').read_text())
    images = json.loads((DATA / 'images.json').read_text())[plan['costs']['reused_images']:]
    assets = ROOT / 'checkpoints/Show-o-assets'
    model, _, _ = load_model(ROOT/'checkpoints/Show-o-source', ROOT/'checkpoints/Show-o2-1.5B-video', assets, 'cpu')
    encoder = StateImageEncoder(model, assets, 'mps')
    values = []
    with (CACHE/'progress.jsonl').open('w') as log:
        for i, row in enumerate(images):
            values.append(encoder.encode(ROOT/row['image']).squeeze(0).cpu())
            encoder.cache.clear()
            if (i+1)%12 == 0:
                log.write(json.dumps(dict(completed=i+1, seconds=time.perf_counter()-start))+'\n')
                log.flush()
    features = torch.stack(values)
    torch.save(dict(features=features), CACHE/'new_features.pt')
    save(RESULT/'extraction.json', dict(seconds=time.perf_counter()-start, new_images=len(images), shape=list(features.shape),
        reused_images=plan['costs']['reused_images'], new_queries=0, full_model_parameters=sum(p.numel() for p in model.parameters()),
        umm_updated_parameters=0))


def prepared():
    import torch
    old = torch.load(prior.CACHE/'features.pt', map_location='cpu', weights_only=True)['features']
    ep = torch.load(endpoint.CACHE/'features.pt', map_location='cpu', weights_only=True)['features']
    ep_rows = json.loads((endpoint.DATA/'images.json').read_text())
    ep = ep[[i for i, r in enumerate(ep_rows) if 'reused_index' not in r]]
    new = torch.load(CACHE/'new_features.pt', map_location='cpu', weights_only=True)['features']
    features = torch.cat([old,ep,new])
    del old, ep, new
    stats = torch.load(SPATIAL_CACHE/'readout.pt', map_location='cpu', weights_only=True)
    mean, std = stats['mean'].to('mps'), stats['std'].to('mps')
    masks = torch.load(prior.CACHE/'masks.pt', map_location='cpu', weights_only=True)
    upper = torch.zeros(729, dtype=torch.bool)
    upper[:14*27] = True
    def inputs(rows, region):
        ref = (features[[r['reference_index'] for r in rows]].to('mps').float()-mean)/std
        cur = (features[[r['current_index'] for r in rows]].to('mps').float()-mean)/std
        mask = torch.stack([masks[region][r['query_index']] if r['reference_available'] else upper for r in rows]).to('mps')
        available = torch.tensor([float(r['reference_available']) for r in rows], device='mps')
        return ref,cur,mask,available
    return inputs


def train():
    import torch
    import torch.nn.functional as F
    inputs = prepared()
    plan = json.loads((RESULT/'plan.json').read_text())['training']
    original = json.loads((DATA/'train_replay.json').read_text())
    extra = {arm:json.loads((DATA/f'supplement_{arm}.json').read_text()) for arm in ARMS}
    original_counts = torch.tensor(plan['original_counts'], dtype=torch.float32, device='mps')
    extra_counts = torch.tensor(plan['supplement_counts'], dtype=torch.float32, device='mps')
    probabilities = .5*original_counts/original_counts.sum()+.5*extra_counts/extra_counts.sum()
    weights = 1/(4*probabilities)
    for region in ('oracle','predicted'):
        for arm in ARMS:
            torch.manual_seed(plan['seed'])
            generator = torch.Generator().manual_seed(plan['seed'])
            head = make_state_head().to('mps')
            head.load_state_dict(torch.load(prior.CACHE/f'coverage_{region}.pt',map_location='mps',weights_only=True)['state_dict'])
            optimizer = torch.optim.AdamW(head.parameters(),lr=plan['lr'],weight_decay=plan['weight_decay'])
            start = time.perf_counter()
            name = f'{arm}_{region}'
            with (RESULT/f'{name}_training.jsonl').open('w') as log:
                for step in range(plan['steps']):
                    old_ids = torch.randint(len(original),(16,),generator=generator).tolist()
                    families = torch.randint(len(extra[arm])//4,(4,),generator=generator).tolist()
                    batch = [original[i] for i in old_ids]+[extra[arm][i*4+j] for i in families for j in range(4)]
                    labels = torch.tensor([CLASSES.index(r['expected']) for r in batch],device='mps')
                    loss = F.cross_entropy(head(*inputs(batch,region)),labels,weight=weights)
                    optimizer.zero_grad();loss.backward();optimizer.step()
                    if (step+1)%25 == 0:
                        log.write(json.dumps(dict(step=step+1,loss=float(loss.detach())))+'\n');log.flush()
            torch.mps.synchronize()
            torch.save(dict(state_dict={k:v.cpu() for k,v in head.state_dict().items()}),CACHE/f'{name}.pt')
            save(RESULT/f'{name}_training.json',dict(seconds=time.perf_counter()-start,steps=plan['steps'],
                cases=len(original)+len(extra[arm]),parameters=sum(p.numel() for p in head.parameters()),
                umm_updated_parameters=0,mixture_class_probabilities=probabilities.cpu().tolist(),class_weights=weights.cpu().tolist()))


def counted(rows, field='correct'):
    groups = defaultdict(list)
    for r in rows:
        groups[r['group_id']].append(int(r[field]))
    return dict(n=len(rows),correct=sum(r[field] for r in rows),ci95=interval(groups))


def pair_metrics(rows):
    families, backgrounds = defaultdict(list),defaultdict(list)
    for r in rows:
        families[r['query_index'],r['background_id']].append(r)
        backgrounds[r['query_index'],r['gap_px']].append(r)
    pairs, all_gaps, background_pairs = [],[],[]
    for family in families.values():
        full = next(r for r in family if r['gap_px']==0)
        all_gaps.append(dict(group_id=full['group_id'],correct=all(r['correct'] for r in family)))
        for r in family:
            if r['gap_px']:
                pairs.append(dict(group_id=r['group_id'],gap_px=r['gap_px'],correct=r['correct'] and full['correct']))
    for members in backgrounds.values():
        if len(members)==2:
            background_pairs.append(dict(group_id=members[0]['group_id'],gap_px=members[0]['gap_px'],
                correct=all(r['correct'] for r in members),flip=members[0]['answer']!=members[1]['answer']))
    classes = {label:counted([r for r in rows if r['expected']==label]) for label in ('完整','部分')}
    return dict(all=counted(rows),classes=classes,macro_accuracy=sum(v['correct']/v['n'] for v in classes.values())/2,
        by_gap={str(g):dict(**counted([r for r in rows if r['gap_px']==g]),
            answers=dict(Counter(r['answer'] for r in rows if r['gap_px']==g))) for g in sorted({r['gap_px'] for r in rows})},
        pairs=counted(pairs),pairs_by_gap={str(g):counted([r for r in pairs if r['gap_px']==g]) for g in sorted({r['gap_px'] for r in pairs})},
        all_gaps=counted(all_gaps),background_pairs=counted(background_pairs),background_flips=sum(r['flip'] for r in background_pairs),
        background_by_gap={str(g):dict(**counted([r for r in background_pairs if r['gap_px']==g]),
            flips=sum(r['flip'] for r in background_pairs if r['gap_px']==g)) for g in sorted({r['gap_px'] for r in background_pairs})})


def evaluate():
    import torch
    start = time.perf_counter()
    inputs = prepared()
    datasets = {name:json.loads((DATA/f'{name}.json').read_text()) for name in
        ('train_replay','supplement_replay','supplement_endpoint','supplement_paired','dev_previous','dev_fresh','dev_endpoint','dev_background')}
    results, predictions = {},[]
    with torch.inference_mode():
        for region in ('oracle','predicted'):
            for arm in ['initial',*ARMS]:
                path = prior.CACHE/f'coverage_{region}.pt' if arm=='initial' else CACHE/f'{arm}_{region}.pt'
                head = make_state_head().to('mps').eval()
                head.load_state_dict(torch.load(path,map_location='mps',weights_only=True)['state_dict'])
                for source in [region]+(['oracle'] if region=='predicted' else []):
                    subsets = ['dev_previous','dev_fresh','dev_endpoint','dev_background']
                    if arm!='initial' and source==region:
                        subsets += ['train_replay',f'supplement_{arm}']
                    for subset in subsets:
                        records=[]
                        for offset in range(0,len(datasets[subset]),32):
                            batch=datasets[subset][offset:offset+32]
                            logits=head(*inputs(batch,source)).cpu()
                            probs=torch.softmax(logits,-1).tolist()
                            for r,p in zip(batch,probs):
                                answer=CLASSES[int(np.argmax(p))]
                                records.append(dict(**r,condition=f'{arm}_{region}/{source}',evaluation_set=subset,answer=answer,
                                    probabilities=p,correct=answer==r['expected'],presence_correct=(answer!='未出现')==(r['expected']!='未出现')))
                        predictions.extend(records)
                        results[f'{arm}_{region}/{source}/{subset}']=pair_metrics(records) if subset in ('dev_endpoint','dev_background') else prior.measures(records)
    write_jsonl(RESULT/'predictions.jsonl',predictions)
    save(RESULT/'score.json',results)
    save(RESULT/'evaluation.json',dict(seconds=time.perf_counter()-start,predictions=len(predictions),parameters_updated=0))
    compare()
    print(json.dumps({k:dict(pairs=v['pairs'],full=v['classes']['完整'],background_pairs=v['background_pairs'])
        for k,v in results.items() if k.endswith('dev_background')},indent=2))


def compare():
    records=read_jsonl(RESULT/'predictions.jsonl')
    lookup={(r['condition'],r['evaluation_set'],r['sample_id']):r for r in records}
    results={}
    for region in ('oracle','predicted'):
        for before,after in [('replay','endpoint'),('endpoint','paired'),('replay','paired')]:
            for subset in ('dev_previous','dev_fresh','dev_endpoint','dev_background'):
                rows=[r for r in records if r['condition']==f'{after}_{region}/{region}' and r['evaluation_set']==subset]
                selected={'all':rows,'full':[r for r in rows if r['expected']=='完整'],
                    'partial':[r for r in rows if r['expected']=='部分']}
                for name,group in selected.items():
                    diffs=defaultdict(list)
                    for r in group:
                        old=lookup[(f'{before}_{region}/{region}',subset,r['sample_id'])]
                        diffs[r['group_id']].append(int(r['correct'])-int(old['correct']))
                    results[f'{region}/{after}-{before}/{subset}/{name}']=dict(n=len(group),difference=sum(map(sum,diffs.values()))/len(group),paired_ci95=interval(diffs))
                if subset in ('dev_endpoint','dev_background'):
                    def paired_units(selected_rows):
                        families, backgrounds = defaultdict(list),defaultdict(list)
                        for r in selected_rows:
                            families[r['query_index'],r['background_id']].append(r)
                            backgrounds[r['query_index'],r['gap_px']].append(r)
                        units = {'endpoint_pairs':{},'background_pairs':{}}
                        for family in families.values():
                            full = next(r for r in family if r['gap_px']==0)
                            for r in family:
                                if r['gap_px']:
                                    key=(r['query_index'],r['background_id'],r['gap_px'])
                                    units['endpoint_pairs'][key]=(r['group_id'],int(r['correct'] and full['correct']))
                        for key,members in backgrounds.items():
                            if len(members)==2:
                                units['background_pairs'][key]=(members[0]['group_id'],int(all(r['correct'] for r in members)))
                        return units
                    old_rows=[lookup[(f'{before}_{region}/{region}',subset,r['sample_id'])] for r in rows]
                    old_units,new_units=paired_units(old_rows),paired_units(rows)
                    for name,units in new_units.items():
                        if not units:
                            continue
                        diffs=defaultdict(list)
                        for key,(gid,value) in units.items():
                            diffs[gid].append(value-old_units[name][key][1])
                        results[f'{region}/{after}-{before}/{subset}/{name}']=dict(n=len(units),
                            difference=sum(map(sum,diffs.values()))/len(units),paired_ci95=interval(diffs))
    save(RESULT/'paired_comparisons.json',results)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','extract','train','evaluate','compare'])
    parser.add_argument('--data',type=lambda p:ROOT/p,default=DATA)
    parser.add_argument('--output',type=lambda p:ROOT/p,default=RESULT)
    parser.add_argument('--cache',type=lambda p:ROOT/p,default=CACHE)
    args=parser.parse_args()
    DATA,RESULT,CACHE=args.data,args.output,args.cache
    globals()[args.command]()
