/* Offline human decisions. No generated labels are submitted by this app. */
'use strict';
const specification = JSON.parse(document.getElementById('review-data').textContent);
const storageKey = specification.package_revision + ':draft';
const answers = JSON.parse(localStorage.getItem(storageKey) || '{}');
const reviewer = document.getElementById('reviewer');
const independent = document.getElementById('independent');
const fields = [...document.querySelectorAll('[data-key]')];
const message = document.getElementById('message');
reviewer.value = answers.reviewer_id || '';
independent.checked = answers.independent === true;
for (const field of fields) field.value = answers[field.dataset.key] || '';

function verdict(keys) {
  const values = keys.map(key => answers[key] || '');
  if (values.some(v => !v)) return 'pending';
  if (values.includes('disputed')) return 'disputed';
  if (values.includes('unknown')) return 'unknown';
  return 'accepted';
}

function reviewPayload() {
  const records = [], pending = [];
  const exportedAt = new Date().toISOString();
  for (const task of specification.tasks) {
    const identity = [task.sequence_key, ...task.identity_keys];
    for (const [facet, keys] of [
      ['E3', identity], ['E4', [...identity, ...task.pair_keys]],
      ['E5', [...identity, ...task.direction_keys]]
    ]) {
      let status = verdict(keys);
      const notApplicable = facet === 'E4' && task.pair_keys.length === 0;
      if (notApplicable && status !== 'pending') status = 'unknown';
      if (status === 'pending') {
        pending.push({sample_id: task.sample_id, facet});
        continue;
      }
      records.push({sample_id: task.sample_id, gold_revision: task.gold_revision, facet,
        reviewer_id: reviewer.value.trim(), reviewer_kind: 'human',
        independent_of_label_construction: independent.checked,
        norm_reference: task.norm_reference, stroke_ids: task.stroke_ids, verdict: status,
        not_applicable: notApplicable, annotated_at: exportedAt,
        evidence: `${specification.package_revision}; GF0023-2020 PDF p${task.norm_reference.pdf_page}; ` +
          `字表序号${task.norm_reference.index}; see item_decisions and reviewer_notes`,
        item_decisions: Object.fromEntries(keys.map(key => [key, answers[key]])),
        reviewer_notes: answers[task.note_key] || ''});
    }
  }
  return {package_revision: specification.package_revision, reviewer_id: reviewer.value.trim(),
    exported_at: exportedAt, independent_of_label_construction: independent.checked,
    records, pending, raw_answers: {...answers}};
}

function refresh() {
  const decisions = fields.filter(f => f.tagName === 'SELECT');
  const completed = decisions.filter(f => f.value).length;
  const payload = reviewPayload();
  document.getElementById('progress').textContent =
    `已填 ${completed} / ${decisions.length} 项；完成 ${payload.records.length} / 48 个字×指标记录。待填项不会导出为通过。`;
  for (const task of specification.tasks) {
    const taskKeys = [task.sequence_key, ...task.identity_keys, ...task.direction_keys, ...task.pair_keys];
    const n = taskKeys.filter(key => answers[key]).length;
    document.querySelector(`[data-character-status="${task.sample_id}"]`).textContent = `（${n}/${taskKeys.length}）`;
  }
}

function save() {
  answers.reviewer_id = reviewer.value;
  answers.independent = independent.checked;
  localStorage.setItem(storageKey, JSON.stringify(answers));
  refresh();
}

for (const field of fields) field.addEventListener('input', () => {
  answers[field.dataset.key] = field.value;
  save();
});
reviewer.addEventListener('input', save);
independent.addEventListener('change', save);
document.getElementById('export').addEventListener('click', () => {
  if (!reviewer.value.trim() || !independent.checked) {
    message.textContent = '导出前请填写审核者代号，并确认独立核查声明。';
    return;
  }
  const payload = reviewPayload();
  const blob = new Blob([JSON.stringify(payload, null, 2) + '\n'], {type: 'application/json'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'S1_stroke_review_' + reviewer.value.trim().replace(/[^\w\u3400-\u9fff-]/g, '_') + '.json';
  link.click();
  URL.revokeObjectURL(link.href);
  message.textContent = `已导出 ${payload.records.length} 条完整记录和原始进度；待完成 ${payload.pending.length} 条。`;
});
document.getElementById('import').addEventListener('change', async event => {
  const payload = JSON.parse(await event.target.files[0].text());
  if (payload.package_revision !== specification.package_revision || !payload.raw_answers) {
    message.textContent = '该文件不属于本版审核包。';
    return;
  }
  // Import is an explicit user action that replaces the current local draft.
  for (const key of Object.keys(answers)) delete answers[key];
  Object.assign(answers, payload.raw_answers);
  reviewer.value = payload.reviewer_id || '';
  independent.checked = payload.independent_of_label_construction === true;
  for (const field of fields) field.value = answers[field.dataset.key] || '';
  save();
  message.textContent = '已恢复导出文件中的审核进度。';
});
refresh();
