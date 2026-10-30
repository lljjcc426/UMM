// Independent SVG rasterization for prereview, no synthetic video generation.
const {chromium}=require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),zlib=require('zlib');
(async()=>{
 const templates=JSON.parse(fs.readFileSync('data/research/datasets/p0_stroke_synthetic_v1/templates.json','utf8')).templates;
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-gpu']});
 const page=await browser.newPage(),output={};
 for(let k=0;k<templates.length;k++){
  const t=templates[k];
  for(const renderer of ['outline','centerline'])output[t.template_id+'|'+renderer]=await page.evaluate(async({t,renderer})=>{
   const masks=[];const canvas=document.createElement('canvas');canvas.width=canvas.height=128;const ctx=canvas.getContext('2d',{willReadFrequently:true});
   const transform='translate(10 10) scale('+108/1024+') scale(1 -1) translate(0 -900)';
   for(let i=0;i<t.strokes.length;i++){
    const content=renderer==='outline'?`<path d="${t.strokes[i]}" fill="black"/>`:`<polyline points="${t.medians[i].map(p=>p.join(',')).join(' ')}" fill="none" stroke="black" stroke-width="${5*1024/108}" stroke-linejoin="round" stroke-linecap="round"/>`;
    const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><g transform="${transform}">${content}</g></svg>`;
    const img=new Image();img.src='data:image/svg+xml;base64,'+btoa(svg);await img.decode();ctx.clearRect(0,0,128,128);ctx.drawImage(img,0,0);
    const data=ctx.getImageData(0,0,128,128).data,indices=[];
    for(let j=0;j<128*128;j++)if(data[j*4+3]>=128)indices.push(j);
    masks.push(indices);
   }return masks;
  },{t,renderer});
  if((k+1)%100===0)process.stdout.write(`SVG reference ${k+1}/${templates.length}\n`);
 }
 fs.writeFileSync('private/p0_ai_prereview_2026-10-28/svg_masks.json.gz',zlib.gzipSync(JSON.stringify(output)));
 await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
