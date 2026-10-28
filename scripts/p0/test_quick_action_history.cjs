// Real browser operation test on the separate observer_dev preview service.
const fs=require('fs');
const assert=require('assert/strict');
const {chromium}=require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const run='data/research/runs/p0_program_ai_audit_2026-10-28';
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-gpu']});
 const primary='historyPrimary03',secondary='historyOther03';const page=await browser.newPage();await page.addInitScript(id=>localStorage.setItem('umm-p0-quick-v1-identity',JSON.stringify({reviewer:id,secondary:false})),primary);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8769/');await page.waitForSelector('canvas');
 const initial=await page.evaluate(()=>({character:current.character,role:current.rgb.role,id:current.blind_id}));
 assert.equal(initial.role,undefined); // Public payload deliberately omits dataset role.
 for(let i=0;i<5;i++)await page.locator('#nextFrame').click();
 await page.waitForFunction(()=>actions.frames_visited.includes(5));
 await page.locator('#reference').click();await page.locator('#closeZoom').click();
 await page.locator('#sequenceDetails summary').click();
 await page.waitForFunction(()=>actions.candidate_sequence_opened);
 await page.reload();await page.waitForSelector('canvas');
 const restored=await page.evaluate(()=>structuredClone(actions));
 assert(restored.frames_visited.includes(5));assert(restored.official_crop_zoom_opened);assert(restored.candidate_sequence_opened);
 await page.locator('#next').click();await page.waitForSelector('canvas');
 await page.locator('#prev').click();await page.waitForSelector('canvas');
 assert(await page.evaluate(()=>actions.frames_visited.includes(5)));
 await page.locator('#agree').click();await page.waitForFunction(id=>state.annotations.some(a=>a.blind_id===id),initial.id);
 const exported=await page.evaluate(id=>api('/api/export?reviewer='+id),primary);
 const old=exported.annotations.find(x=>x.blind_id===initial.id);
 assert(old.view_actions.frames_visited.includes(5));
 // New browser has no local cache: restore only the current reviewer's save.
 const other=await browser.newPage();await other.addInitScript(id=>localStorage.setItem('umm-p0-quick-v1-identity',JSON.stringify({reviewer:id,secondary:false})),primary);await other.goto('http://127.0.0.1:8769/');await other.waitForSelector('canvas');
 await other.locator('#prev').click();await other.waitForFunction(id=>current.blind_id===id,initial.id);
 assert(await other.evaluate(()=>actions.frames_visited.includes(5)));
 await other.evaluate(async id=>{$('reviewer').value=id;await load();},secondary);await other.waitForSelector('canvas');
 assert.deepEqual(await other.evaluate(()=>actions.frames_visited),[0]);
 assert.equal(await other.evaluate(()=>actions.official_crop_zoom_opened),false);
 assert.equal(errors.length,0);
 const result={passed:true,preview_only:true,holdout_samples_used:0,actual_human_store_modified:false,
   reload_persistence:true,revisit_persistence:true,own_saved_state_restored:true,reviewer_isolation:true,
   saved_export_retains_actions:true,viewing_does_not_prove_attention:true,errors};
 fs.writeFileSync(run+'/quick_action_history_browser.json',JSON.stringify(result,null,2)+'\n');
 await page.screenshot({path:'private/p0_program_ai_audit_2026-10-28/UI_preview.png',fullPage:true});
 await browser.close();console.log(JSON.stringify(result));
})().catch(e=>{console.error(e);process.exit(1);});
