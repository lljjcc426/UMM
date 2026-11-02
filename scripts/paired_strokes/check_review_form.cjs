// One browser workflow; synthetic answers stay in a private test directory.
const {chromium} = require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const {pathToFileURL} = require('url');

(async () => {
  const root = path.resolve('private/paired_strokes_v1_2026-11-02');
  const form = path.join(root, 'S1_independent_stroke_review_form_v1/index.html');
  const output = path.join(root, 'form_ui_test');
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
  const context = await browser.newContext({acceptDownloads:true, viewport:{width:1280,height:1000}});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(pathToFileURL(form).href);
  await page.waitForSelector('.character');
  const decisions = page.locator('select[data-key]');
  const total = await decisions.count();
  assert.equal(total, 200);
  assert(await decisions.evaluateAll(elements => elements.every(e => e.value === '')));
  const assets = await page.locator('img').evaluateAll(images => images.every(i => i.complete && i.naturalWidth > 0));
  assert(assets);
  await page.fill('#reviewer', 'UI_TEST_ONLY_NOT_HUMAN');
  await page.check('#independent');
  const first = page.locator('.character').first();
  for (const select of await first.locator('select').all()) await select.selectOption('accepted');
  await first.locator('textarea').fill('Synthetic interface fixture; never a human review.');
  const downloadPromise = page.waitForEvent('download');
  await page.click('#export');
  const download = await downloadPromise;
  const exportedPath = path.join(output, 'synthetic_export.json');
  await download.saveAs(exportedPath);
  const payload = JSON.parse(fs.readFileSync(exportedPath));
  assert.equal(payload.records.length, 3);
  assert.equal(payload.pending.length, 45);
  assert.equal(payload.records.find(r => r.facet === 'E3').verdict, 'accepted');
  assert.equal(payload.records.find(r => r.facet === 'E4').verdict, 'unknown');
  assert.equal(payload.records.find(r => r.facet === 'E5').verdict, 'accepted');
  await page.reload();
  assert.equal(await first.locator('select').first().inputValue(), 'accepted');
  await first.locator('select').first().selectOption('disputed');
  const disagreementDownload = page.waitForEvent('download');
  await page.click('#export');
  const disagreement = await disagreementDownload;
  const disagreementPath = path.join(output, 'synthetic_disputed.json');
  await disagreement.saveAs(disagreementPath);
  const disputed = JSON.parse(fs.readFileSync(disagreementPath));
  assert.equal(disputed.records.find(r => r.facet === 'E3').verdict, 'disputed');
  await page.locator('#import').setInputFiles(exportedPath);
  await page.waitForFunction(() => document.getElementById('message').textContent.includes('已恢复'));
  assert.equal(await first.locator('select').first().inputValue(), 'accepted');
  await page.screenshot({path:path.join(output,'review_form.png'),fullPage:false});
  const fresh = await browser.newContext();
  const other = await fresh.newPage();
  await other.goto(pathToFileURL(form).href);
  assert(await other.locator('select[data-key]').evaluateAll(elements => elements.every(e => e.value === '')));
  assert.equal(fs.readFileSync('data/research/paired_strokes_v1/evaluation_only/reviews.jsonl','utf8'), '');
  assert.deepEqual(errors, []);
  const result = {passed:true, decision_fields:total, characters:16, strokes:54,
    checks:['all decisions initially blank','all local images load','partial export preserves pending items',
      'identity and direction export independently','single-stroke E4 stays not applicable',
      'dispute is preserved','draft survives reload','export imports back','fresh reviewer is blank'],
    actual_human_submissions:0, synthetic_exports_private:true};
  fs.writeFileSync('data/research/paired_strokes_v1/review_form_checks.json',JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
