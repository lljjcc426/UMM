"""CPU-only supervision/replay preparation. No optimizer, tensor model, or training."""
import random
import numpy as np

NODE_MASKS={
    'correct_text':('text',1),'correct_image':('image',1),
    'policy_error_text':('text',0),'draw_error_image':('image',0),
    'reflection_text':('text',1),'redx':('image',1),
    'recovered_text':('text',1),'recovered_image':('image',1),
}


def compile_masks(nodes):
    result=[]
    for node in nodes:
        modality,weight=NODE_MASKS[node['type']]
        result.append({**node,'modality':modality,'in_context':True,
                       'CE_mask':weight if modality=='text' else 0,
                       'FM_mask':weight if modality=='image' else 0})
    return result


def normalized_loss(text_losses,text_mask,image_losses,image_mask):
    """Numeric contract check only; image losses already feature-averaged."""
    result={}
    for key,values,mask in [('CE',text_losses,text_mask),('FM',image_losses,image_mask)]:
        v=np.asarray(values,float);m=np.asarray(mask,float)
        if v.shape!=m.shape:raise ValueError('Mask shape mismatch')
        result[key]=float((v*m).sum()/m.sum()) if m.sum() else 0.0
    result['total']=result['CE']+result['FM'];return result


def recovery_nodes(branch):
    types={'draw':['correct_text','draw_error_image','reflection_text','recovered_image','correct_text'],
           'policy':['correct_image','policy_error_text','redx','recovered_text','recovered_image'],
           'positive':['correct_text','correct_image','correct_text']}
    return compile_masks([{'id':f'{branch}-{i}','type':t,'logical_step':1} for i,t in enumerate(types[branch])])


def select_replay(previous,current,keep,seed=20261101,fraction=.30):
    # Matches Algorithm1's previous-round joint subset. No hidden all-history replay claim.
    joint=[r for r in previous if r['draw_error'] and r['policy_error']]
    selected=random.Random(seed).sample(joint,int(len(joint)*fraction))
    return {'current':current,'previous_round_joint_replay':selected,'capability_keep':keep,
            'seed':seed,'previous_joint_count':len(joint),'replay_fraction':fraction,
            'paper_dropout':{'Text-Reflect':.10,'Draw-Reflect':.15},
            'dropout_implemented':False,'reason':'Node replacement requires qualified paired GT and an actual training adapter'}
