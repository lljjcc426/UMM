"""Build a local human review queue without prefilled labels or model scores."""
import json
from pathlib import Path
import shutil

from scripts.p0.build_data import DATA, RUN, PRIVATE

templates=json.loads((DATA/'templates.json').read_text())['templates']
tasks=[]
for template in templates:
    tasks.append(dict(id='norm-'+template['template_id'],type='normative',
                      character=template['character'],role=template['role'],
                      source_group_id=template['source_group_id'],
                      official_page=template['norm_reference']['pdf_page'],
                      official_index=template['norm_reference']['index'],
                      candidate_strokes=template['strokes']))
for role in ['observer_dev','observer_holdout']:
    for line in (DATA/f'manifest_{role}.jsonl').read_text().splitlines():
        sample=json.loads(line)
        tasks.append(dict(id=sample['sample_id'],type='rgb_event',character=sample['character'],
                          role=role,source_group_id=sample['source_group_id'],
                          official_page=sample['evaluation_only']['norm_reference']['pdf_page'],
                          media='../../../../../'+sample['media_path'],
                          frame_timestamps=sample['frame_timestamps']))
review=DATA/'review'
review.mkdir(exist_ok=True)
(review/'review_data.js').write_text('window.REVIEW_TASKS='+json.dumps(tasks,ensure_ascii=False)+';\n')
shutil.copyfile('scripts/p0/review.html',review/'index.html')
shutil.copyfile(DATA/'licenses/ARPHICPL.TXT',PRIVATE/'ARPHICPL.TXT')
if not (DATA/'human_annotations.json').exists():
    (DATA/'human_annotations.json').write_text(json.dumps(dict(status='pending_no_human_reviewer_available',
        annotations=[],human_verified_normative_characters=0,human_verified_rgb_clips=0),indent=2)+'\n')
(RUN/'human_review_queue.json').write_text(json.dumps(dict(total_tasks=len(tasks),normative_tasks=len(templates),
    rgb_tasks=len(tasks)-len(templates),annotations_completed=0,predictions_visible_in_interface=False,
    construction_case_labels_visible_in_interface=False,review_entry=str(review/'index.html'),
    export_format='p0-human-annotations-v1, reviewer ID, decision, observed order, notes, timestamp',
    required_before_scientific_acceptance=['Independent per-character normative agreement/adjudication',
        'Independent RGB event audit including controlled positives, errors and ambiguity',
        'Resolve disagreements before treating construction labels as audited gold']),ensure_ascii=False,indent=2)+'\n')
print('Human review tasks',len(tasks),'completed',0)
