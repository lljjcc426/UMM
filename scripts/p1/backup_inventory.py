"""Inventory retained artifacts once, then verify their local backup byte for byte."""
import argparse
import json
from pathlib import Path

if __package__:
    from .full_common import sha256
else:
    from full_common import sha256


def cloud_inventory(root, pilot):
    manifest=json.loads((root/'manifest.json').read_text());records=[]
    def add(path, logical, local_scope, local_path):
        records.append(dict(path=logical,bytes=path.stat().st_size,sha256=sha256(path),
                            local_scope=local_scope,local_path=local_path))
    for phase in ['generation','understanding']:
        for row in manifest[phase]:
            reused=row.get('reused',False);origin=pilot if reused else root
            base=origin/'bundles'/row['id']
            for path in sorted(base.rglob('*')):
                if path.is_file() and not path.is_symlink():
                    rel=str(path.relative_to(base));add(path,phase+'/'+row['id']+'/'+rel,
                        'pilot' if reused else 'full','requests/'+row['id']+'/'+rel)
            archive=origin/'archives'/(row['id']+'.tar.gz')
            if archive.exists():add(archive,'archives/'+archive.name,'pilot' if reused else 'full','archives/'+archive.name)
    for row in manifest['codec']:
        base=root/'codec'/row['id']
        for path in sorted(base.rglob('*')):
            if path.is_file():
                rel=str(path.relative_to(base));add(path,'codec/'+row['id']+'/'+rel,'full','requests/'+row['id']+'/'+rel)
        archive=root/'archives'/(row['id']+'.tar.gz')
        if archive.exists():add(archive,'archives/'+archive.name,'full','archives/'+archive.name)
    excluded_dirs={'bundles','codec','archives','offline_review','__pycache__'}
    excluded_files={'artifact_inventory.json','metadata-final.tar.gz','GPU_queue.lock'}
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if (not path.is_file() or path.is_symlink() or any(p in excluded_dirs for p in rel.parts)
                or path.name in excluded_files or path.suffix=='.pyc'):
            continue
        add(path,'metadata/'+str(rel),'full','metadata_final/'+str(rel))
    for path in sorted((root/'offline_review').glob('*')):
        if path.is_file():
            local='offline_review/'+path.name if path.suffix=='.zip' else path.name
            add(path,'offline_review/'+path.name,'full',local)
    return dict(schema=1,file_count=len(records),total_bytes=sum(r['bytes'] for r in records),
                excludes=['preexisting model weights, referenced separately by pinned revision','checksum inventory itself','metadata transport tar','derived offline unpacked directories, covered by internal SHA manifests and ZIP SHA'],files=records)


def verify_local(inventory, root, pilot):
    mismatches=[]
    for row in inventory['files']:
        path=(pilot if row['local_scope']=='pilot' else root)/row['local_path']
        if not path.is_file():mismatches.append(dict(path=row['path'],reason='missing'))
        elif path.stat().st_size!=row['bytes']:mismatches.append(dict(path=row['path'],reason='size mismatch'))
        elif sha256(path)!=row['sha256']:mismatches.append(dict(path=row['path'],reason='SHA256 mismatch'))
    return dict(passed=not mismatches,files_checked=inventory['file_count'],bytes_checked=inventory['total_bytes'],
                mismatches=mismatches,method='Every listed cloud artifact checked for existence, size and SHA-256 against its local copy')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['cloud','verify']);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--pilot-root',type=Path,required=True);parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.mode=='cloud':
        result=cloud_inventory(args.root,args.pilot_root)
        args.inventory.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='files'}));return
    result=verify_local(json.loads(args.inventory.read_text()),args.root,args.pilot_root)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
