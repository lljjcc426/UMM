"""Local audit contact sheets from existing reference/RGB; never generate videos."""
import argparse
import gzip
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from scripts.p0.ai_prereview import PRIVATE, RUN, read_rgb
from scripts.p0.prepare_acceptance import load_existing


def normative():
    templates,_=load_existing();templates=sorted(templates,key=lambda t:t['character'])
    refs={r['template_id']:r for r in json.loads((RUN/'official_reference_extraction.json').read_text())['records']}
    with gzip.open(PRIVATE/'svg_masks.json.gz','rt') as handle:raw=json.load(handle)
    font=ImageFont.truetype('/System/Library/Fonts/STHeiti Light.ttc',16)
    index=[]
    for batch in range(0,len(templates),8):
        rows=[];mapping=[]
        for t in templates[batch:batch+8]:
            ref=refs[t['template_id']];official=Image.open(ref['diagram_path']).convert('RGB')
            official=official.resize((430,round(official.height*430/official.width)))
            candidate=Image.new('RGB',(480,((len(t['strokes'])+11)//12)*66),'white');cd=ImageDraw.Draw(candidate)
            masks=[]
            for indices in raw[t['template_id']+'|outline']:
                mask=np.zeros(128*128,bool);mask[indices]=True;masks.append(mask.reshape(128,128))
            union=np.zeros((128,128),bool)
            for i,mask in enumerate(masks):
                rgb=np.full((128,128,3),255,np.uint8);rgb[union]=[170,180,190];rgb[mask]=[30,70,160]
                image=Image.fromarray(rgb);draw=ImageDraw.Draw(image)
                points=np.asarray(t['medians'][i],float).copy();points[:,1]=900-points[:,1];points=10+points*108/1024
                for point,color in [(points[0],'green'),(points[-1],'#ff8000')]:
                    draw.ellipse((point[0]-4,point[1]-4,point[0]+4,point[1]+4),fill=color)
                candidate.paste(image.resize((40,40)),((i%12)*40,(i//12)*66+20))
                cd.text(((i%12)*40,(i//12)*66),str(i+1),fill='black');union|=mask
            height=max(official.height,candidate.height)+28
            row=Image.new('RGB',(930,height),'#f0f2f4');draw=ImageDraw.Draw(row)
            draw.text((3,2),t['character']+f' | PDF {ref["official_page"]} | 官方(左) / 源候选(右)',font=font,fill='black')
            row.paste(official,(0,28));row.paste(candidate,(444,28));rows.append(row);mapping.append(t['character'])
        sheet=Image.new('RGB',(930,sum(image.height for image in rows)),'white');y=0
        for image in rows:sheet.paste(image,(0,y));y+=image.height
        name=f'norm_{batch//8+1:02}.png';sheet.save(PRIVATE/'contact'/name)
        index.append(dict(sheet=name,characters=mapping))
    (RUN/'normative_visual_contact_index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['normative'])
    parser.parse_args();normative()
