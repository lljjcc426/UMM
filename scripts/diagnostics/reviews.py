"""Validate existing P1 offline exports without creating or altering human answers."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .contracts import FACETS,LABELS,save


def validate_export(export, cards):
    if export.get('schema')!='P1-human-review-v1' or export.get('package_id')!=cards['id']:
        raise ValueError('Schema/package mismatch')
    lookup={r['id']:r for r in cards['cards']};current=export['current'];versions=export['versions']
    def check(row):
        if row['id'] not in lookup or not lookup[row['id']].get('video'):
            raise ValueError('Unknown or missing-video slot cannot acquire human judgment')
        if not str(row.get('reviewer','')).strip() or not row.get('submitted_at'):
            raise ValueError('Original reviewer identifier and submission timestamp required')
        if any(row.get(k) not in LABELS for k in FACETS):raise ValueError('Seven independent facet labels required')
        if any(row[k]!='correct' for k in FACETS) and not str(row.get('reason','')).strip():
            raise ValueError('Unknown, incorrect and NA require the original reason')
        for key in ('first_error_start','first_error_end'):
            if row.get(key) is not None and (not isinstance(row[key],(int,float)) or row[key]<0):raise ValueError('Invalid error time')
        a,b=row.get('first_error_start'),row.get('first_error_end')
        if a is not None and b is not None and a>b:raise ValueError('Reversed error interval')
    last={}
    for row in versions:check(row);last[row['id']]=row
    for sid,row in current.items():
        check(row)
        if sid!=row['id'] or last.get(sid)!=row:raise ValueError('Current answer must match preserved final revision')
    reviewers={r['reviewer'] for r in versions}
    if len(reviewers)>1:raise ValueError('One package must contain one original reviewer; identities cannot be merged')
    return {'package_id':cards['id'],'slots':len(lookup),'playable':sum(bool(c.get('video')) for c in lookup.values()),
            'missing_video_slots':sum(not c.get('video') for c in lookup.values()),'current_submissions':len(current),
            'version_count':len(versions),'revision_or_duplicate_count':len(versions)-len(last),
            'remaining_playable':sum(bool(c.get('video')) for c in lookup.values())-len(current),
            'reviewer':next(iter(reviewers),None),'identity_verified':False,'independence_confirmed':False}


def compare_exports(first,second,cards1,cards2,private_mapping):
    summaries=[validate_export(first,cards1),validate_export(second,cards2)]
    if first['package_id']==second['package_id']:raise ValueError('Independent packages required')
    ids=[r['reviewer'] for r in summaries if r['reviewer']]
    if len(ids)==2 and len(set(ids))!=2:raise ValueError('Same reviewer identifier; independence not established')
    def mapped(export):
        mapping={r['blind_id']:r['source_id'] for r in private_mapping[export['package_id']]}
        return {mapping[k]:v for k,v in export['current'].items()}
    a,b=mapped(first),mapped(second);overlap=set(a)&set(b)
    disagreements=[{'source_id':sid,'facets':[k for k in FACETS if a[sid][k]!=b[sid][k]]}
                   for sid in sorted(overlap) if any(a[sid][k]!=b[sid][k] for k in FACETS)]
    return {'packages':summaries,'paired_submissions':len(overlap),'disagreements':disagreements,
            'adjudication':'pending' if disagreements else 'not_needed_for_available_pairs',
            'independence_confirmed':False,'identity_verified':False,'formal_primary_metrics':None,
            'note':'Distinct codes are not proof of two independent people. Preserve original exports and any later attestation separately.'}


def read_cards(path):
    text=Path(path).read_text();return json.loads(text.split('=',1)[1].strip().removesuffix(';'))


def main():
    p=argparse.ArgumentParser();p.add_argument('--export',required=True);p.add_argument('--cards',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();out=Path(a.output)
    if out.exists():raise ValueError('Use a new import report path; original exports are never overwritten')
    result=validate_export(json.loads(Path(a.export).read_text()),read_cards(a.cards));save(out,result);print(json.dumps(result))

if __name__=='__main__':main()
