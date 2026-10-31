const $=id=>document.getElementById(id);
let catalog, tab='text', recognition=null, busy=false, imageData=null;
async function api(path,body){const r=await fetch(path,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});const value=await r.json();if(!r.ok)throw Error(value.error);return value;}
function message(text,error=false){$('status').textContent=text;$('status').className=error?'error':'';}
function update(){
 const mode=document.querySelector('input[name=mode]:checked').value;
 $('generate').textContent=mode==='preview'?'生成CPU预览':'UMM规划并生成';
 $('modeNote').textContent=mode==='preview'?'CPU预览使用已配置参考，便于检查书写过程，不调用UMM。':'UMM提出笔画计划，通过规范检查后执行；错误计划最多纠正一次。';
 $('generate').disabled=busy||(mode==='umm'&&!catalog?.backend_configured)||(tab==='image'&&(!recognition||!$('confirm').checked||!recognition.supported));
 $('recognize').disabled=busy||!catalog?.backend_configured||!imageData;
 document.querySelectorAll('#characters button').forEach(b=>b.classList.toggle('active',b.textContent===$('character').value));
}
function setTab(value){tab=value;$('textInput').hidden=value!=='text';$('imageInput').hidden=value!=='image';$('textTab').classList.toggle('selected',value==='text');$('imageTab').classList.toggle('selected',value==='image');update();}
function waitJob(id){return new Promise((resolve,reject)=>{const poll=async()=>{try{const job=await api('/api/jobs/'+id);if(job.status==='completed')resolve(job);else if(job.status==='failed')reject(Error(job.error));else setTimeout(poll,600);}catch(e){reject(e);}};poll();});}
async function run(action){busy=true;update();try{await action();}catch(e){message(e.message,true);}finally{busy=false;update();}}
$('textTab').onclick=()=>setTab('text');$('imageTab').onclick=()=>setTab('image');$('character').oninput=update;$('confirm').onchange=update;
document.querySelectorAll('input[name=mode]').forEach(el=>el.onchange=update);
$('image').onchange=async()=>{recognition=null;imageData=null;$('recognition').hidden=true;$('confirm').checked=false;$('imagePreview').hidden=true;const f=$('image').files[0];if(!f)return update();if(f.size>2_000_000){message('图片不能超过2MB',true);return update();}imageData=await new Promise(resolve=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(f);});$('imagePreview').src=imageData;$('imagePreview').hidden=false;update();};
$('recognize').onclick=()=>run(async()=>{message('UMM正在识别图片，请稍候…');const started=await api('/api/recognize',{mode:'umm',image:imageData});recognition=await waitJob(started.id);$('recognizedChar').textContent=recognition.character;$('recognition').hidden=false;message(recognition.supported?'请确认识别结果，再生成视频。':'已识别目标字，但当前字库尚不支持此字。',!recognition.supported);});
$('generate').onclick=()=>run(async()=>{
 const mode=document.querySelector('input[name=mode]:checked').value;
 const character=tab==='text'?$('character').value.trim():recognition.character;
 message(mode==='preview'?'正在生成并回读检查视频…':'UMM正在规划，随后生成并检查视频…');
 const started=await api('/api/generate',{mode,character,speed:Number($('speed').value),recognition_id:tab==='image'?recognition.id:null});
 const job=await waitJob(started.id);
 $('placeholder').hidden=true;$('video').hidden=false;$('video').src=job.video_url;$('video').poster=job.poster_url;$('result').hidden=false;
 $('resultMode').textContent=mode==='preview'?'CPU执行预览':'UMM规划＋受控执行';
 $('summary').textContent=`「${character}」 · 512 × 512 · 24帧/秒 · ${job.rendering.duration_seconds.toFixed(2)}秒`;
 $('download').href=job.video_url;$('download').download=character+'-书写.mp4';
 $('strokes').replaceChildren();for(const s of catalog.characters.find(r=>r.character===character).strokes){const li=document.createElement('li');li.textContent=s.name+' · '+s.instruction;$('strokes').append(li);}
 $('quality').textContent='MP4回读检查通过：空白起笔、逐笔行进、墨迹保留和最终完整性。规范参考仍为工程预览资格。';
 message(mode==='preview'?'CPU预览已完成，未调用UMM。':'UMM计划通过校验，视频已完成。');
});
$('replay').onclick=()=>{$('video').currentTime=0;$('video').play();};
(async()=>{try{catalog=await api('/api/catalog');$('connection').textContent=catalog.backend_configured?'UMM已配置 · 待实测验证':'UMM未连接 · CPU预览可用';for(const row of catalog.characters){const button=document.createElement('button');button.textContent=row.character;button.onclick=()=>{$('character').value=row.character;update();};$('characters').append(button);}update();}catch(e){message(e.message,true);}})();
