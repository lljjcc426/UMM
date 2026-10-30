const fs=require('fs'),assert=require('assert/strict');
const {chromium}=require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root='data/research/runs/p0_final_calibration_2026-10-28';
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-gpu']});
 const page=await browser.newPage({viewport:{width:1280,height:900}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8771/');await page.waitForFunction(()=>current?.kind==='normative');
 const tasks=await page.evaluate(()=>structuredClone(tasks));
 for(const task of tasks)for(const key of ['id','part','writer_id','nominal_case','ai_suggestion','AI_v1','AI_v2','expected','source_order','path'])assert.equal(task[key],undefined);
 assert(tasks.every(t=>/^F-[0-9a-f]{10}$/.test(t.blind_id)));
 const norm=tasks[0].blind_id;
 await page.locator('#normRef').click();await page.locator('#closeZoom').click();await page.locator('#sequenceDetails summary').click();
 await page.locator('#splitButton').click();await page.locator('[data-field="identity_order"] [data-value="pass"]').click();await page.locator('[data-field="direction"] [data-value="unknown"]').click();
 await page.locator('#notes').fill('UI_TEST_ONLY，不计科研人审');await page.reload();await page.waitForFunction(()=>values.identity_order==='pass'&&values.direction==='unknown');
 await page.locator('#splitButton').click();await page.locator('#saveDetail').click();await page.waitForFunction(()=>current?.kind==='rgb');await page.waitForSelector('canvas');
 for(let i=0;i<5;i++)await page.locator('#nextFrame').click();await page.waitForFunction(()=>actions.frames.includes(5));
 await page.reload();await page.waitForSelector('canvas');assert(await page.evaluate(()=>actions.frames.includes(5)));
 await page.locator('#no').click();await page.locator('#saveDetail').click();assert.match(await page.locator('#message').textContent(),/错误原因/);
 await page.locator('[data-reason="wrong_order"]').click();await page.locator('#saveDetail').click();await page.waitForFunction(()=>current?.kind==='record');
 await page.locator('#context').click();await page.locator('#closeZoom').click();await page.locator('#unknown').click();await page.waitForSelector('#done:not(.hidden)');
 const saved=await page.evaluate(()=>api('/api/export?reviewer=1'));
 assert.equal(saved.saved,3);assert.equal(saved.annotations.find(a=>a.blind_id===norm).judgments.direction,'unknown');
 const again=await page.evaluate(payload=>api('/api/import',{reviewer_id:'1',payload}),saved);assert.equal(again.imported,0);assert.equal(again.conflicts_preserved,0);
 await page.selectOption('#reviewer','2');await page.locator('#load').click();await page.waitForFunction(()=>reviewer==='2'&&state.saved===0);
 assert.equal(await page.evaluate(()=>state.annotations.length),0);
 const rejected=await page.evaluate(async payload=>{const r=await fetch('/api/import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({reviewer_id:'2',payload})});return r.status;},saved);assert.equal(rejected,400);
 const paths=['/api/predictions','/predictions.jsonl','/api/other_answers'];for(const path of paths){const r=await page.request.get('http://127.0.0.1:8771'+path);assert.equal(r.status(),404);}
 const second=await browser.newPage();await second.goto('http://127.0.0.1:8771/');await second.waitForSelector('#done:not(.hidden)');await second.locator('#reopen').click();await second.waitForFunction(()=>current?.kind==='normative');assert.equal(await second.evaluate(()=>values.direction),'unknown');
 await second.screenshot({path:'private/p0_final_calibration_2026-10-28/UI_verified.png',fullPage:true});
 assert.equal(errors.length,0);await browser.close();
 const result={passed:true,formal_samples_used:0,source:'Three separate operation-only tasks; no formal64calibration records',
  normative_facets_saved_without_inference:true,frame_navigation_and_reload:true,record_panel:true,reference_zoom:true,
  own_export_restore:true,duplicate_import_no_new_records:true,other_reviewer_export_import_rejected:true,
  reviewer_records_separate:true,AI_case_and_other_answers_not_served:true,opaque_ids:true,scientific_human_records_created:0,errors};
 fs.writeFileSync(root+'/browser_operation_check.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
})().catch(e=>{console.error(e);process.exit(1);});
