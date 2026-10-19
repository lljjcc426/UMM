"""Post-run T6 analysis of saved records only; no model inference or training."""
import argparse,json,time
from collections import Counter,defaultdict
import numpy as np
from PIL import Image,ImageDraw
from h1_event_data import ROOT,save
from h1_early_history_data import OUT,DATA,WEIGHTS
from h1_early_history_score import load_jsonl,mean

def oracle_timing():
    """One replay for the requested oracle latency; no learned model or tuning."""
    from h1_early_history_data import observed_truth
    from h1_event_ledger import EventLedger
    rows=[r for r in json.loads((DATA/'cases.json').read_text()) if r['split'] in ['test','diagnostic']]
    pixels=defaultdict(list)
    for r in json.loads((OUT/'pixel_states.json').read_text()):pixels[r['id']].append(r['state'])
    latency=[];ledger_latency=[]
    for row in rows:
        frames=[Image.open(ROOT/p).copy() for p in row['frames']]
        for t in [15,20,23]:
            begin=time.perf_counter();observed_truth(row,frames[:t+1]);latency.append(time.perf_counter()-begin)
        ledger=EventLedger(len(row['strokes']));previous=np.zeros(ledger.q)
        for t,s in enumerate(pixels[row['id']]):
            p=np.array(s['progress']);geometry=np.where(p>.985,2,np.where(p>.02,1,0)).tolist()
            begin=time.perf_counter();ledger.update(t,(p>.02).astype(float).tolist(),p.tolist(),geometry,s['direction'],np.maximum(p-previous,0).tolist());ledger_latency.append(time.perf_counter()-begin);previous=p
    save(OUT/'oracle_timing.json',dict(M0_pixel_query_mean_seconds=mean(latency),M0_n=len(latency),M5_oracle_ledger_update_mean_seconds=mean(ledger_latency),M5_n=len(ledger_latency),scope='Single deterministic replay, decoded observations / oracle onset state already supplied. Excludes disk decode and neural modules; M5 incremental update, M0 prefix reread. No learned model inference or training.'))

def analyze():
    records=load_jsonl(OUT/'predictions.jsonl');history=load_jsonl(OUT/'history_predictions.jsonl');metrics=json.loads((OUT/'metrics.json').read_text());failure=json.loads((OUT/'failure_cases.json').read_text())
    main=[r for r in records if r['split']=='test'];by={(r['method'],r['id'],r['t']):r for r in history};families={};state={}
    for method in sorted({r['method'] for r in main}):
        fam={}
        for family in ['parallel','mixed','cross','fold','close']:
            rs=[r for r in main if r['method']==method and r['family']==family];ps=[p for p in json.loads((OUT/'paired_results.json').read_text())[method]['pairs'] if family in p['group']]
            fam[family]=dict(strict_observable=mean([r['order_correct'] for r in rs if r['truth']['event_order'] is not None]),pair=mean([p['both_correct'] for p in ps]))
        families[method]=fam
        rs=[r for r in main if r['method']==method]
        state[method]=dict(predicted_full=sum(c==2 for r in rs for c in r['prediction']['geometry_state']),full_with_raw_progress_below95=metrics['methods'][method]['predicted_full_progress_below95'])
    ledger=[]
    for r in main:
        if r['method']!='M4' or r['t']!=23 or r['variant'].startswith('merged'):continue
        true=r['truth']['onset_intervals'];pred=r['prediction']['onset_intervals']
        for j,interval in true.items():
            if pred.get(j)!=interval:ledger.append(dict(id=r['id'],group=r['group'],instance=int(j),true_interval=interval,predicted_interval=pred.get(j),source='prediction-derived first detection; cause may include shared spatial mixing or local presence detection'))
    examples=[]
    for key in ['test-00-parallel-swap2','test-04-close-swap1','test-19-close-mergedA']:
        chosen={}
        for method in ['M1','M2','M4']:
            chosen[method]={str(t):by[method,key,t] for t in [6,15,23]}
        examples.append(dict(id=key,records=chosen))
    e=json.loads((OUT/'extraction.json').read_text());timing=json.loads((OUT/'timing.json').read_text());ledgers=[len(json.dumps(r['prediction'].get('ledger',[])).encode()) for r in main if r['method']=='M4' and r['t']==23]
    resources=dict(UMM=dict(total_parameters=e['parameters'],updated_parameters=0,encoded_images=e['encoded'],encoding_seconds=e['seconds'],seconds_per_new_image=e['seconds']/e['encoded'],cache_disk_bytes=sum(p.stat().st_size for p in (WEIGHTS/'features').glob('*.pt'))),
        A_B=json.loads((OUT/'spatial_run.json').read_text()),M1=json.loads((OUT/'M1_run.json').read_text()),M2=json.loads((OUT/'M2_run.json').read_text()),
        history_payload_bytes=dict(M1_current_instance_vectors=5*196*4,M2_full24_instance_vectors=24*5*196*4,M3_K4_instance_vectors=4*5*196*4,M3_K8_instance_vectors=8*5*196*4,M4_mean_ledger_JSON=float(np.mean(ledgers)),M4_max_ledger_JSON=max(ledgers)),
        cached_query_latency_ms=dict(M1=1000*timing['M1_per_query']['mean_seconds'],M2=1000*timing['M2_per_query']['mean_seconds'],M3_K4=1000*timing['M3_K4']['mean_seconds'],M3_K8=1000*timing['M3_K8']['mean_seconds'],M4_estimated_M1_plus_incremental=1000*(timing['M1_per_query']['mean_seconds']+timing['M4_incremental_without_head']['mean_seconds'])),
        resource_scope='CPU fp32 cached heads, one pass including 108 test+diagnostic clips. Shared UMM, A+B, previous-frame scratch, hidden activations, Python overhead excluded from payload comparison. M4 latency sums two measured means, not end-to-end profiling.')
    save(OUT/'resources.json',resources)
    if (OUT/'oracle_timing.json').exists():
        resources['oracle_latency']=json.loads((OUT/'oracle_timing.json').read_text());save(OUT/'resources.json',resources)
    save(OUT/'failure_analysis.json',dict(family=families,state_progress=state,ledger_final_onset_interval_errors=ledger,failures_by_category={m:dict(Counter(c for r in failure if r['method']==m for c in r['failure_categories'])) for m in ['M2','M4']},examples=examples,early_interval_distance_seconds=dict(swap1=[(t-1)/6 for t in [15,20,23]],swap2=[(t-3)/6 for t in [15,20,23]])))
    # Render only saved observations and answers, without generating new examples.
    rows={r['id']:r for r in json.loads((DATA/'cases.json').read_text())};canvas=Image.new('RGB',(1200,760),'#eeeeee');d=ImageDraw.Draw(canvas)
    for k,example in enumerate(examples):
        key=example['id'];row=rows[key];y=k*250;d.text((10,y+8),key,fill='black')
        for i,t in enumerate([1,3,6,15,23]):
            canvas.paste(Image.open(ROOT/row['frames'][t]).resize((165,165)),(10+i*175,y+30));d.text((10+i*175,y+200),f'obs {t}',fill='black')
        for i,m in enumerate(['M2','M4']):
            r=example['records'][m]['23'];s=r['prediction'];d.text((900,y+40+65*i),m+' final '+str(s['event_order']),fill='black');d.text((900,y+60+65*i),'unknown: '+str(s.get('uncertainty_reason')),fill='black')
        d.text((900,y+195),'truth '+str(example['records']['M4']['23']['truth']['event_order']),fill='black')
        if k==2:
            r=example['records']['M4']['23'];d.text((900,y+150),'M4 groups '+str(r['prediction']['unresolved_order_groups']),fill='black');d.text((900,y+170),'truth groups '+str(r['truth']['unresolved_order_groups']),fill='black')
    canvas.save(OUT/'failure_examples.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--oracle-timing',action='store_true');args=p.parse_args()
    if args.oracle_timing:oracle_timing()
    analyze()
