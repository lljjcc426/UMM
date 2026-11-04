// One pilot review workflow. Synthetic exports never enter the review registry.
const {chromium} = require('/Users/cc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const {pathToFileURL} = require('url');

(async () => {
  const root = path.resolve('private/paired_strokes_v1_2026-11-02/S1_remaining_240_review_v1');
  const output = path.resolve('private/paired_strokes_v1_2026-11-02/completion_ui_check');
  fs.mkdirSync(output, {recursive:true});
  const registry = fs.readFileSync('data/research/paired_strokes_v1/evaluation_only/reviews.jsonl', 'utf8');
  const browser = await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
  const context = await browser.newContext({acceptDownloads:true, viewport:{width:1280,height:1000}});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root, 'batch-01/index.html')).href);
  const decisions = page.locator('select[data-key]');
  assert.equal(await decisions.count(), 300);
  assert(await decisions.evaluateAll(elements => elements.every(e => !e.value)));
  assert(await page.locator('img').evaluateAll(images => images.every(i => i.complete && i.naturalWidth > 0)));
  await page.fill('#reviewer', 'UI_TEST_ONLY_NOT_HUMAN');
  await page.check('#independent');
  await decisions.first().selectOption('accepted');
  const downloadWait = page.waitForEvent('download');
  await page.click('#export');
  const download = await downloadWait;
  assert(download.suggestedFilename().includes('batch-01'));
  const exported = path.join(output, 'synthetic_pair_only.json');
  await download.saveAs(exported);
  const payload = JSON.parse(fs.readFileSync(exported));
  assert.equal(payload.records.length, 1);
  assert.equal(payload.records[0].facet, 'PAIR');
  assert.equal(payload.pending.length, 79);
  await page.reload();
  assert.equal(await decisions.first().inputValue(), 'accepted');
  await decisions.first().selectOption('unknown');
  await page.locator('#import').setInputFiles(exported);
  await page.waitForFunction(() => document.getElementById('message').textContent.includes('已恢复'));
  assert.equal(await decisions.first().inputValue(), 'accepted');
  await page.screenshot({path:path.join(output, 'pilot_review.png')});
  // Another batch in the same browser must have a separate draft.
  await page.goto(pathToFileURL(path.join(root, 'batch-12/index.html')).href);
  assert.equal(await page.locator('select[data-key]').count(), 1981);
  assert(await page.locator('select[data-key]').evaluateAll(elements => elements.every(e => !e.value)));
  assert.equal(fs.readFileSync('data/research/paired_strokes_v1/evaluation_only/reviews.jsonl', 'utf8'), registry);
  assert.deepEqual(errors, []);
  const result = {passed:true, checks:['blank initial choices', 'batch-01 images load',
    'PAIR-only export leaves spatial facets pending', 'draft survives reload', 'import restores choices',
    'export filename includes batch', 'different batch has isolated draft', 'actual registry unchanged'],
    synthetic_export:exported, new_human_submissions_created:0};
  fs.writeFileSync('data/research/paired_strokes_v1/s1_completion_2026-11-02/browser_check.json', JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result,null,2));
  await browser.close();
})().catch(error => {console.error(error);process.exit(1);});
