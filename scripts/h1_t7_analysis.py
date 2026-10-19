"""Post-test frozen evidence analysis. No fitting or method/threshold changes."""
import json
from collections import Counter,defaultdict
from importlib.metadata import version
import numpy as np
import torch
from PIL import Image,ImageDraw,ImageFont
from h1_event_data import ROOT,save
from h1_event_observe import masks_for
from h1_event_train import grid
from h1_t7_data import OUT,WEIGHTS
from h1_t7_score import estimate
from h1_early_history_score import load_jsonl

def signal_at(view,t,j):
    o=view['outputs']
    return dict(presence=float(1-o['state'][t,j].softmax(-1)[0]),start=float(o['start'][t,j].sigmoid()),new_ink=float(view['inputs'][t,j,193]))

def main():
    torch.set_num_threads(4);items=torch.load(WEIGHTS/'compact_test.pt',weights_only=False)
    records=load_jsonl(OUT/'predictions.jsonl');by={(r['method'],r['id'],r['t']):r for r in records}
    masks=json.loads((OUT/'mask_predictions.json').read_text());mask_by={(r['method'],r['group']):r for r in masks}
    metrics=json.loads((OUT/'factorial_results.json').read_text());uncertainty=json.loads((OUT/'uncertainty_results.json').read_text())
    audits=defaultdict(lambda:dict(onsets=[],absent=[],state_correct=[],progress_error=[]));events=[];oracle_false=[];confirmation_lags=defaultdict(list)
    for x in items:
        r=x['row']
        if r['variant']=='mergedB':continue
        q=len(r['strokes']);m=masks_for(r);exclusive=m&(m.sum(0)==1)[None]
        ink=np.stack([np.asarray(Image.open(ROOT/p))[:,:,0]<128 for p in r['frames']]);new=ink&~np.concatenate([np.zeros_like(ink[:1]),ink[:-1]])
        new_flat=torch.from_numpy(new.astype(np.float32)).flatten(1)
        def fine(mask):
            flat=torch.from_numpy(mask.astype(np.float32)).flatten(1)
            return new_flat@flat.T/flat.sum(-1).clamp_min(1)[None]
        fine_full,fine_unique=fine(m),fine(exclusive);mask_grid=grid(m);weights=mask_grid/mask_grid.sum(-1,keepdim=True).clamp_min(1e-6);coarse=grid(new)@weights.T
        for region,method0,method1 in [('A0','E00','E01'),('A1','E10','E11'),('Oracle','Oracle_L0','Oracle_L1')]:
            view=x['views'][region];out=view['outputs'];a=audits[region];p=1-out['state'].softmax(-1)[:,:,0];s=out['start'].sigmoid();b=view['inputs'][:,:,193];c=out['state'].argmax(-1)
            a['state_correct'].extend((c==x['state']).flatten().tolist());a['progress_error'].extend((out['progress']-x['progress']).abs().flatten().tolist())
            for t in range(24):
                for j in range(q):
                    if x['progress'][t,j]!=0:continue
                    entry=dict(id=r['id'],group=r['group'],family=r['family'],t=t,instance=j,**signal_at(view,t,j),fine_rgb_full_new=float(fine_full[t,j]),fine_rgb_unique_new=float(fine_unique[t,j]),coarse_rgb_new=float(coarse[t,j]))
                    a['absent'].append(entry)
                    if region=='Oracle' and (entry['presence']>=.5 or entry['start']>=.5 or entry['new_ink']>=.02):oracle_false.append(entry)
            final0=by[method0,r['id'],23]['prediction'];final1=by[method1,r['id'],23]['prediction']
            for j in range(q):
                true=x['truth_states'][-1]['onset_intervals'][str(j)];t=true[1];signal=signal_at(view,t,j);a['onsets'].append(signal)
                first=final1['first_detection_intervals'].get(str(j));confirm=final1['confirmation_intervals'].get(str(j));got=final1['onset_intervals'].get(str(j))
                event=dict(id=r['id'],group=r['group'],family=r['family'],q=q,region=region,instance=j,true_interval=true,
                    mask_iou=mask_by[region,r['group']]['ious'][j] if region!='Oracle' else 1.,true_onset_signal=signal,
                    true_onset_fine_rgb_new=float(fine_full[t,j]),true_onset_coarse_rgb_new=float(coarse[t,j]),L0_interval=final0['onset_intervals'].get(str(j)),
                    L1_interval=got,L1_first_detection=first,L1_confirmation=confirm,L1_status=next((e['status'] for e in final1['ledger'] if e['instance_id']==j),None),
                    first_detection_signal=signal_at(view,first[1],j) if first else None)
                events.append(event)
                if confirm:confirmation_lags[region].append(dict(group=r['group'],id=r['id'],instance=j,observations=confirm[1]-t,seconds=(confirm[1]-t)/6))
    summary={}
    for region,a in audits.items():
        true=a['onsets'];absent=a['absent']
        summary[region]=dict(onset_events=len(true),presence_recall_at_true_onset=float(np.mean([v['presence']>=.5 for v in true])),start_recall_at_true_onset=float(np.mean([v['start']>=.5 for v in true])),
            new_ink_recall_at_true_onset=float(np.mean([v['new_ink']>=.02 for v in true])),three_signals_agree_at_true_onset=float(np.mean([v['presence']>=.5 and v['start']>=.5 and v['new_ink']>=.02 for v in true])),
            absent_observations=len(absent),false_presence=sum(v['presence']>=.5 for v in absent),false_start=sum(v['start']>=.5 for v in absent),false_new=sum(v['new_ink']>=.02 for v in absent),
            all_prefix_state_accuracy=float(np.mean(a['state_correct'])),all_prefix_progress_mae=float(np.mean(a['progress_error'])),
            confirmation_lags=dict(n=len(confirmation_lags[region]),counts=dict(Counter(v['observations'] for v in confirmation_lags[region])),mean_seconds=float(np.mean([v['seconds'] for v in confirmation_lags[region]]))))
    false_new=[v for v in oracle_false if v['new_ink']>=.02]
    accounting=dict(total=len(false_new),real_shared_ink=sum(v['fine_rgb_full_new']>0 for v in false_new),native_cell_mixing=sum(v['fine_rgb_full_new']==0 and v['coarse_rgb_new']>0 for v in false_new),B_positive_without_coarse_rgb_change=sum(v['fine_rgb_full_new']==0 and v['coarse_rgb_new']==0 for v in false_new),
        interpretation='Diagnostic accounting under true areas, not mutually independent causal interventions; shared ink can be real global change without being target-instance onset.')
    mask_diffs=[]
    for r in masks:
        if r['method']!='A0':continue
        other=mask_by['A1',r['group']]
        for j,v in enumerate(r['ious']):mask_diffs.append(dict(group=r['group'],delta=float(other['ious'][j]>=.5)-float(v>=.5),identity_delta=float(other['identity_correct'][j])-float(r['identity_correct'][j])))
    paired=json.loads((OUT/'paired_results.json').read_text());base={(v['group'],v['variant'],v['t']):v for v in paired['E00']}
    net=[dict(group=v['group'],delta=float(v['both_correct'])-float(base[v['group'],v['variant'],v['t']]['both_correct'])) for v in paired['E11']]
    contrasts=dict(mask_match_A1_minus_A0=estimate(mask_diffs,lambda r:r['delta']),identity_A1_minus_A0=estimate(mask_diffs,lambda r:r['identity_delta']),E11_minus_E00=estimate(net,lambda r:r['delta']))
    examples=[]
    for method,id,t in [('E10','test-close-q5-01-correct',23),('Oracle_L1','test-mixed-q5-01-correct',23),('Oracle_L1','test-close-q5-01-correct',20),('E11','test-cross-q5-02-correct',23),('E11','test-close-q5-02-mergedA',23)]:
        r=by[method,id,t];x=next(x for x in items if x['row']['id']==id);region={'E10':'A1','E11':'A1','Oracle_L1':'Oracle'}[method]
        examples.append(dict(record=r,events=[e for e in events if e['id']==id and e['region']==region]))
    save(OUT/'failure_analysis.json',dict(signals=summary,oracle_false_new_accounting=accounting,paired_additional_diagnostics=contrasts,examples=examples,
        constraints='Read-only analysis of fixed Test outputs; no changed method, threshold, checkpoint or primary score. Geometry intervals condition on one trained seed.'))
    save(OUT/'onset_instance_evidence.json',events);save(OUT/'oracle_absent_signal_evidence.json',oracle_false);save(OUT/'confirmation_lags.json',dict(confirmation_lags))
    resources=dict(UMM=json.loads((OUT/'extraction.json').read_text()),A_training=json.loads((OUT/'training_runs.json').read_text()),
        compact_train_dev=json.loads((OUT/'compact_train_dev_inputs.json').read_text())['seconds'],formal_test=json.loads((OUT/'test_execution.json').read_text()),
        feature_cache_bytes=sum(p.stat().st_size for p in (WEIGHTS/'features').glob('*.pt')),local_weights_excluded_from_git=True,
        trainable_parameters_per_condition=2051074,B_parameters=71395,M1_parameters=1104653,UMM_updated=0,B_updated=0,M1_updated=0,
        head_sequence_mean_seconds={v:float(np.mean([x['views'][v]['head_sequence_seconds'] for x in items])) for v in ['A0','A1','Oracle']},
        RAM='M5 16GiB run completed. Unified CPU/MPS peak was not instrumented; process RSS is not total unified memory.',
        memory_limitations='Ledger JSON footprint excludes Python/runtime and common visual scratch. Audit log grows with event hypotheses; no general constant-memory or end-to-end acceleration claim.',
        plotting=dict(library='Matplotlib',version=version('matplotlib'),model_results_changed=False))
    save(OUT/'resources.json',resources)
    plots(metrics,uncertainty,json.loads((OUT/'mask_metrics.json').read_text()))
    montage(items)
    print(json.dumps(dict(signals=summary,oracle_false_new=accounting,contrasts=contrasts),indent=2))

def plots(metrics,uncertainty,masks):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'savefig.dpi':220})
    fig,axes=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
    for axis,names,data,key,title in [(axes[0],['A0','A1'],masks,'match','Instance matching'),(axes[1],['E00','E01','E10','E11'],metrics,'pair','Both histories correct')]:
        ys=[data[n][key]['value']*100 for n in names];errors=np.array([[ys[i]-data[n][key]['CI'][0]*100,data[n][key]['CI'][1]*100-ys[i]] for i,n in enumerate(names)]).T
        axis.bar(names,ys,color=['#718096','#287d9f'] if len(names)==2 else ['#718096','#a8b6c3','#56a1a6','#287d9f']);axis.errorbar(names,ys,yerr=errors,fmt='none',color='black',capsize=4)
        axis.axhline(90,color='#a84848',linestyle='--',linewidth=1);axis.set(ylim=(0,105),ylabel='Percent',title=title)
        for i,y in enumerate(ys):axis.text(i,5,f'{y:.1f}',ha='center',color='white',weight='bold')
    fig.suptitle('T7: fixed test, 30 geometry groups; 95% cluster intervals');fig.savefig(OUT/'factorial_comparison.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,4.5),layout='constrained')
    offsets={'E00':(8,7),'E01':(8,7),'E10':(-32,9),'E11':(-31,-18)}
    for name in ['E00','E01','E10','E11']:
        u=uncertainty[name];x=u['raw_answer_coverage']['value']*100;y=u['visible_wrong_acceptance']['value']*100
        ax.scatter(x,y,s=65,label=name);ax.annotate(name,(x,y),xytext=offsets[name],textcoords='offset points')
    ax.set(xlim=(70,90),ylim=(0,5),xlabel='Non-unknown answers on observable videos (%)',ylabel='Accepted wrong answers / all observable decisions (%)',title='Coverage and accepted errors at the fixed rules')
    ax.grid(alpha=.2);fig.savefig(OUT/'coverage_error.png');plt.close(fig)

def montage(items):
    ids=['test-close-q5-01-correct','test-mixed-q5-01-correct','test-close-q5-02-mergedA'];times=[[0,1,3,5,23],[13,14,17,18,20],[0,1,4,5,23]]
    im=Image.new('RGB',(1120,3*226),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
    for row,(id,ts) in enumerate(zip(ids,times)):
        x=next(x for x in items if x['row']['id']==id);y=row*226;d.text((8,y+4),id,fill='black',font=font)
        for col,t in enumerate(ts):
            image=Image.open(ROOT/x['row']['frames'][t]).resize((176,176));im.paste(image,(col*183,y+29));d.text((col*183+4,y+205),f'observation {t}',fill='black',font=font)
        if row==0:text='Higher aggregate IoU;\na local target can\nstill fail after A1.'
        elif row==1:text='Oracle area:\nmissed B change;\nfalse early presence.'
        else:text='True tied group [0,1]\nE11 infers [1,2];\nunknown hides errors.'
        d.multiline_text((923,y+65),text,fill='black',font=font,spacing=8)
    im.save(OUT/'failure_examples.png')

if __name__=='__main__':main()
