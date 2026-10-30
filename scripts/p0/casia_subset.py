"""Small official CASIA research subset; raw trajectories stay private.

POT preserves coordinate/pen-lift order, not native RGB or physical timing.
ZIP byte ranges avoid fetching full archives for a few writer records.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct
import time
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor
import random

RUN=Path('data/research/runs/p0_final_calibration_2026-10-28')
PRIVATE=Path('private/p0_final_calibration_2026-10-28')
BASE='https://nlpr.ia.ac.cn/databases/Download/Online/'
URLS={'pot':BASE+'CharData/Pot1.0Test.zip','wptt':BASE+'WPTTData/WPTT2.0-Test.zip'}


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


class RemoteZip:
    def __init__(self,url):
        self.url=url;self.requests=[]
        with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=30) as r:
            self.length=int(r.headers['Content-Length']);self.modified=r.headers.get('Last-Modified')
        start=max(0,self.length-65557);tail=self.read(start,self.length-1)
        end=tail.rfind(b'PK\x05\x06')
        if end<0:raise ValueError('ZIP end directory not found')
        eocd=struct.unpack('<4s4H2LH',tail[end:end+22]);size,offset=eocd[5:7]
        directory=tail[offset-start:offset-start+size] if offset>=start else self.read(offset,offset+size-1)
        self.entries=[];cursor=0
        while cursor<len(directory):
            h=struct.unpack('<4s6H3L5H2L',directory[cursor:cursor+46])
            if h[0]!=b'PK\x01\x02':raise ValueError('Invalid ZIP directory entry')
            name=directory[cursor+46:cursor+46+h[10]].decode('utf-8' if h[3]&2048 else 'cp437')
            self.entries.append(dict(name=name,method=h[4],compressed_size=h[8],size=h[9],offset=h[16]))
            cursor+=46+h[10]+h[11]+h[12]

    def read(self,start,end):
        t=time.monotonic()
        req=urllib.request.Request(self.url,headers={'Range':f'bytes={start}-{end}'})
        with urllib.request.urlopen(req,timeout=30) as r:
            if r.status!=206:raise ValueError('Server did not honor bounded ZIP range request')
            raw=r.read(end-start+2)
        if len(raw)!=end-start+1:raise ValueError('Incomplete range response')
        event=dict(start=start,end=end,bytes=len(raw),wall_seconds=time.monotonic()-t)
        self.requests.append(event)
        with (PRIVATE/'range_requests.jsonl').open('a') as f:
            f.write(json.dumps(dict(url=self.url,**event))+'\n')
        return raw

    def member(self,entry):
        raw=self.read(entry['offset'],entry['offset']+29)
        name,extra=struct.unpack('<HH',raw[26:30]);start=entry['offset']+30+name+extra
        data=self.read(start,start+entry['compressed_size']-1)
        if entry['method']==8:return zlib.decompress(data,-15)
        if entry['method']==0:return data
        raise ValueError('Unsupported ZIP compression')


def parse_pot(raw):
    """Read the official little-endian POT format, validating each record once."""
    records=[];offset=0
    while offset<len(raw):
        size,tag,count=struct.unpack_from('<HIH',raw,offset)
        if size<12 or offset+size>len(raw):raise ValueError('Invalid POT record length')
        label=(tag&65535).to_bytes(2,'big').decode('gbk')
        points=[list(p) for p in struct.iter_unpack('<hh',raw[offset+8:offset+size])]
        strokes=[];stroke=[]
        for x,y in points:
            if x==-1:
                if y==0:strokes.append(stroke);stroke=[]
                elif y==-1:break
                else:raise ValueError('Invalid POT sentinel')
            else:stroke.append([x,y])
        if len(strokes)!=count or any(not s for s in strokes) or points[-1]!=[-1,-1]:
            raise ValueError('POT stroke count or end marker mismatch')
        records.append(dict(character=label,record_offset=offset,record_bytes=size,strokes=strokes))
        offset+=size
    return records


def parse_wptt(raw):
    """Read independent text-page acquisitions and their line transcripts.

    WPTT provides line-to-stroke grouping, not per-character boundaries. No
    character segmentation or timing is invented from these transcripts.
    """
    header=struct.unpack_from('<I',raw)[0]
    if b'WPTT' not in raw[4:12]:raise ValueError('Expected WPTT header')
    sample_length,page,count=struct.unpack_from('<iii',raw,header);cursor=header+12
    strokes=[]
    for _ in range(count):
        n=struct.unpack_from('<H',raw,cursor)[0];cursor+=2
        strokes.append([list(p) for p in struct.iter_unpack('<HH',raw[cursor:cursor+n*4])]);cursor+=n*4
    lines_count=struct.unpack_from('<H',raw,cursor)[0];cursor+=2;lines=[]
    for _ in range(lines_count):
        n=struct.unpack_from('<H',raw,cursor)[0];cursor+=2
        indexes=list(struct.unpack_from('<'+'H'*n,raw,cursor));cursor+=2*n
        letters=struct.unpack_from('<H',raw,cursor)[0];cursor+=2
        tags=[raw[cursor+2*i:cursor+2*i+2] for i in range(letters)];cursor+=letters*2
        text=''.join('�' if tag==b'\xff\xff' else tag.decode('gbk') for tag in tags)
        lines.append(dict(stroke_indices=indexes,text=text))
    if cursor!=len(raw) or any(i>=len(strokes) for line in lines for i in line['stroke_indices']):
        raise ValueError('WPTT page boundary or line/stroke mismatch')
    return dict(page_index=page,declared_sample_length=sample_length,strokes=strokes,lines=lines,
                character_boundaries_available=False,physical_timestamps_available=False)


def fetch():
    if (RUN/'casia_download.json').exists():raise ValueError('Preserve completed source record')
    PRIVATE.mkdir(parents=True,exist_ok=True)
    archive=RemoteZip(URLS['pot'])
    save(PRIVATE/'pot_directory.json',archive.entries)
    # Deterministic writer selection, before looking at observer outcomes.
    entries=sorted((e for e in archive.entries if e['name'].lower().endswith('.pot')),key=lambda e:e['name'])
    chosen=[entries[0],entries[len(entries)//2]]
    inventory=[]
    for e in chosen:
        raw=archive.member(e);name=Path(e['name']).name
        (PRIVATE/name).write_bytes(raw)
        records=parse_pot(raw);writer=Path(name).stem
        save(PRIVATE/(writer+'-records.json'),records)
        inventory.append(dict(writer_id=writer,archive_member=e['name'],local_file=str(PRIVATE/name),records=len(records),
                              characters=len({r['character'] for r in records}),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    # Index text pages so independently repeated records can be checked without
    # claiming that a color/speed variant is a new handwriting acquisition.
    pages=RemoteZip(URLS['wptt']);save(PRIVATE/'wptt_directory.json',pages.entries)
    writers=[x['writer_id'] for x in inventory];text_entries=[]
    for writer in writers:
        matches=[e for e in pages.entries if Path(e['name']).name.startswith(writer.split('-')[0]) and e['name'].lower().endswith('.wptt')]
        for e in sorted(matches,key=lambda x:x['name']):
            raw=pages.member(e);path=PRIVATE/Path(e['name']).name;path.write_bytes(raw)
            text_entries.append(dict(writer_id=writer,archive_member=e['name'],local_file=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    for name,url in [('conditions','https://nlpr.ia.ac.cn/databases/handwriting/Application_form.html'),('format','https://nlpr.ia.ac.cn/databases/handwriting/Online_database.html')]:
        with urllib.request.urlopen(url,timeout=30) as r:(PRIVATE/(name+'.html')).write_bytes(r.read())
    save(RUN/'casia_download.json',dict(downloaded_at_utc=datetime.now(timezone.utc).isoformat(),purpose='Academic research only, local group use; no raw data redistribution',
        conditions='https://nlpr.ia.ac.cn/databases/handwriting/Application_form.html',acknowledgment='C.-L. Liu, F. Yin, D.-H. Wang, Q.-F. Wang, CASIA online and offline Chinese handwriting databases, ICDAR2011,37-41',
        raw_POT=inventory,text_pages=text_entries,archives=[dict(url=a.url,last_modified=a.modified,archive_bytes=a.length,requests=a.requests) for a in [archive,pages]],
        bytes_downloaded=sum(r['bytes'] for a in [archive,pages] for r in a.requests),
        writer_selection='Sorted official Pot1.0Test directory, first and middle writer; chosen before observer outputs',
        physical_timing_present=False,pressure_present=False,native_RGB_present=False,recorded_coordinate_and_penlift_order_present=True,
        prior_2752_media_modified=False,GPU_hours=0))
    print(json.dumps(dict(writers=writers,POT_records=[x['records'] for x in inventory],text_pages=len(text_entries),downloaded_bytes=sum(r['bytes'] for a in [archive,pages] for r in a.requests))))


def expand_writers():
    """Reserve16 development and64 unseen-writer calibration groups once."""
    if (RUN/'writer_source_inventory.json').exists():raise ValueError('Writer subset already fixed')
    archive=RemoteZip(URLS['pot'])
    entries=sorted((e for e in archive.entries if e['name'].lower().endswith('.pot')
                    and Path(e['name']).stem not in ['006','205']),key=lambda e:e['name'])
    random.Random(2026102804).shuffle(entries);selected=entries[:80]
    # Fix IDs/roles before inspecting their trajectories or any scorer output.
    frozen=RUN/'writer_selection_freeze.json'
    if not frozen.exists():
        save(frozen,dict(seed=2026102804,frozen_at_utc=datetime.now(timezone.utc).isoformat(),
            development=[Path(e['name']).stem for e in selected[:16]],validation=[Path(e['name']).stem for e in selected[16:]],
            prior_exposed_writers_excluded=['006','205'],selection='Uniform shuffle of the82 remaining official test writers; first16development, next64validation',
            distinct_writers=True,new_human_workload='16development +64validation characters; norm and RGB labels in one fixed bundle',
            independence_limit='Different acquisition writers; recruitment independence/representativeness is not established by directory IDs alone'))
    else:
        roster=json.loads(frozen.read_text());by_writer={Path(e['name']).stem:e for e in entries}
        selected=[by_writer[w] for w in roster['development']+roster['validation']]
    def download(e):
        path=PRIVATE/Path(e['name']).name
        if path.exists():raw=path.read_bytes()
        else:raw=archive.member(e);path.write_bytes(raw)
        records=parse_pot(raw)
        return dict(writer_id=path.stem,archive_member=e['name'],local_file=str(path),records=len(records),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    with ThreadPoolExecutor(max_workers=2) as pool:inventory=list(pool.map(download,selected))
    save(RUN/'writer_source_inventory.json',dict(writers=inventory,selected_writers=80,development_writers=16,validation_writers=64,
        archive_url=archive.url,last_modified=archive.modified,archive_bytes=archive.length,range_requests=archive.requests,
        bytes_downloaded_this_attempt=sum(r['bytes'] for r in archive.requests),
        selected_compressed_payload_bytes=sum(e['compressed_size'] for e in selected),
        prior_failed_attempt_transfer_overhead='not fully instrumented; retained local raw files reused without overwriting',
        raw_files_private=True,native_RGB=False,physical_timing=False,
        source_order_not_automatically_normative=True,original_640_and2752_unchanged=True))
    print(json.dumps(dict(writers=len(inventory),bytes_downloaded=sum(r['bytes'] for r in archive.requests))))


if __name__=='__main__':
    import sys
    (expand_writers if len(sys.argv)>1 and sys.argv[1]=='expand' else fetch)()
