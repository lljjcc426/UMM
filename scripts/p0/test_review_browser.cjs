// Actual non-holdout browser workflow. All mock labels use a separate test store.
const fs=require('fs');
const assert=require('assert');
const {chromium}=require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root='data/research/runs/p0_human_review_preparation_2026-10-28';
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1100},acceptDownloads:true});
 const page=await context.newPage(); const errors=[]; const mediaRequests=[];
 page.on('pageerror',error=>errors.push(error.message));
 page.on('request',request=>{if(request.url().includes('/media/'))mediaRequests.push(request.url());});
 const checks={}; let result;
 try{
  await page.goto('http://127.0.0.1:8767/');
  await page.waitForFunction(()=>document.querySelector('#batch').options.length===8);
  await page.fill('#reviewer','UI_TEST_ONLY'); await page.click('#load');
  await page.waitForFunction(()=>document.querySelectorAll('#facets select').length===6);
  checks.no_prefilled_decision=await page.inputValue('#decision')==='';
  checks.normative_svg_loaded=await page.locator('#media svg').count()>0;
  checks.normative_direction_endpoints=await page.locator('#media circle').count()>0;
  await page.selectOption('#decision','unverified');
  for(const select of await page.locator('#facets select').all())await select.selectOption('unknown');
  await page.fill('#notes','UI_TEST_ONLY 原始说明，不计科研标注');await page.check('#disputed');
  await page.click('#save');await page.waitForSelector('#saveState:text("已提交")');
  checks.server_save=true;
  await page.click('#next');await page.fill('#notes','UI_TEST_ONLY 未提交草稿');
  await page.reload();await page.waitForFunction(()=>document.querySelector('#notes').value==='UI_TEST_ONLY 未提交草稿');
  checks.draft_and_position_resume=true;
  await page.selectOption('#batch','practice_rgb');
  await page.waitForFunction(()=>document.querySelector('#frameInfo').textContent.includes('第1 /'));
  const frameCount=Number(await page.locator('#frame').getAttribute('max'))+1;
  const scrub=Math.min(5,frameCount-1);
  await page.locator('#frame').evaluate((el,n)=>{el.value=n;el.dispatchEvent(new Event('input'));},scrub);
  await page.waitForFunction(n=>document.querySelector('#frameInfo').textContent.includes(`第${n+1} /`),scrub);
  checks.frame_scrubbing={frame_count:frameCount,frame_label:await page.textContent('#frameInfo')};
  await page.click('#markFrame'); assert((await page.inputValue('#events')).includes(`第${scrub+1}`));
  await page.click('#start');await page.waitForFunction(()=>document.querySelector('#frameInfo').textContent.includes('第1 /'));
  // Start from the last frame to exercise single-shot end behavior without long waits.
  await page.locator('#frame').evaluate(el=>{el.value=el.max;el.dispatchEvent(new Event('input'));});
  await page.waitForFunction(n=>document.querySelector('#frameInfo').textContent.includes(`第${n} /`),frameCount);
  await page.click('#play');await page.waitForTimeout(600);
  checks.single_shot_stops_at_last_frame=Number(await page.inputValue('#frame'))===frameCount-1;
  await page.screenshot({path:root+'/review_v2_operation.png',fullPage:true});
  const request=context.request;
  const protocol=await (await request.get('http://127.0.0.1:8767/api/protocol')).json();
  const allPractice=[];
  for(const batch of ['practice_norm','practice_rgb']){
   const values=await (await request.get('http://127.0.0.1:8767/api/tasks?batch='+batch+'&reviewer=UI_TEST_ONLY')).json();
   allPractice.push(...values);
   for(const task of values){
    const annotation={protocol_id:protocol.id,blind_id:task.blind_id,type:task.type,reviewer_id:'UI_TEST_ONLY',decision:task.type==='normative'?'unverified':'unknown',facets:Object.fromEntries(Object.keys(protocol.facets[task.type]).map(key=>[key,'unknown'])),reference_consulted:false,reasons:[],disputed:false,notes:'UI_TEST_ONLY 操作测试',events:'',observed_order:'',annotated_at:new Date().toISOString()};
    const response=await request.post('http://127.0.0.1:8767/api/save',{data:{reviewer_id:'UI_TEST_ONLY',annotation,progress:{batch:'practice_rgb',index:0}}});assert(response.ok());
   }
  }
  const raw=fs.readFileSync(root+'/raw_user_export_2026-10-28.json','utf8');
  fs.writeFileSync('private/p0_human_review_ui_test_2026-10-28/input-legacy.json',raw);
  await page.locator('#importFile').setInputFiles('private/p0_human_review_ui_test_2026-10-28/input-legacy.json');
  await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('旧版38条'));
  checks.legacy_import_preserved_separate=true;
  const downloadPromise=page.waitForEvent('download');await page.click('#export');const download=await downloadPromise;
  const exportPath='private/p0_human_review_ui_test_2026-10-28/export-v2.json';await download.saveAs(exportPath);
  const exported=JSON.parse(fs.readFileSync(exportPath));assert.equal(exported.annotations.length,16);
  await page.locator('#importFile').setInputFiles(exportPath);
  await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('导入0条'));
  const conflicting=structuredClone(exported);conflicting.annotations[0].notes='UI_TEST_ONLY incoming conflict';
  const conflictResult=await (await request.post('http://127.0.0.1:8767/api/import',{data:{reviewer_id:'UI_TEST_ONLY',payload:conflicting}})).json();
  assert.equal(conflictResult.conflicts,1);
  const after=await (await request.get('http://127.0.0.1:8767/api/state?reviewer=UI_TEST_ONLY')).json();
  assert(!after.annotations.some(a=>a.notes.includes('incoming conflict')));
  checks.import_export_and_no_conflict_overwrite=true;
  const other=await (await request.get('http://127.0.0.1:8767/api/state?reviewer=UI_TEST_SECOND')).json();
  checks.reviewer_answer_separation=other.annotations.length===0;
  await page.check('#ack');await page.click('#onboard');await page.waitForFunction(()=>document.querySelector('#onboardState').textContent.includes('已确认'));
  checks.onboarding_human_action_path=true;
  const blocked=await request.get('http://127.0.0.1:8767/api/tasks?batch=holdout_rgb&reviewer=UI_TEST_ONLY');
  checks.preview_blocks_holdout=blocked.status()===400;
  const forbidden=await request.get('http://127.0.0.1:8767/data/research/runs/p0_data_eval_2026-10-27/holdout_predictions.jsonl');
  checks.raw_predictions_not_served=forbidden.status()===404;
  const forbiddenFields=['case','renderer','role','original_id','source_group_id','expected','construction_events','decision','evaluation_only'];
  checks.blind_task_allowlist=allPractice.every(t=>forbiddenFields.every(k=>!(k in t)));
  const fresh=await browser.newContext();const freshPage=await fresh.newPage();
  await freshPage.goto('http://127.0.0.1:8767/');await freshPage.waitForFunction(()=>document.querySelector('#batch').options.length===8);
  await freshPage.fill('#reviewer','UI_TEST_ONLY');await freshPage.click('#load');
  await freshPage.waitForFunction(()=>document.querySelector('#notes').value==='UI_TEST_ONLY 操作测试');
  checks.server_progress_without_browser_storage=true;await fresh.close();
  const draft=JSON.parse(fs.readFileSync(root+'/review_draft.json'));
  const holdoutIds=new Set(draft.batches.holdout_rgb.map(t=>t.blind_id));
  const holdoutMediaRequests=mediaRequests.filter(url=>[...holdoutIds].some(id=>url.includes(id)));
  result={passed:Object.values(checks).every(value=>typeof value==='object'||value===true)&&errors.length===0,checks,javascript_errors:errors,media_requests:mediaRequests.length,holdout_media_requests:holdoutMediaRequests.length,test_store:'private/p0_human_review_ui_test_2026-10-28',scientific_human_annotations_created:0,executed_at_utc:new Date().toISOString()};
 }catch(error){result={passed:false,checks,error:error.stack,javascript_errors:errors,holdout_media_requests:0,scientific_human_annotations_created:0};}
 fs.writeFileSync(root+'/ui_operation_test_attempt01.json',JSON.stringify(result,null,2)+'\n');
 if(result.passed)fs.copyFileSync(root+'/ui_operation_test_attempt01.json',root+'/ui_operation_test.json');
 console.log(JSON.stringify(result,null,2));await browser.close();if(!result.passed)process.exitCode=1;
})();
