"""Summarize existing P1 evidence on CPU; never modify source results or call a model."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
SERVER = ROOT / "data/research/runs/p1_full_server_2026-10-30"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


screen = load(ROOT / "data/research/runs/p1_human_feedback_2026-10-31/identified_screening.json")
requests = load(SERVER / "request_status.json")["requests"]["generation"]
codec = load(SERVER / "codec_auxiliary_evidence.json")
answers = load(SERVER / "understanding_answers_and_sampling.json")
pairs = load(SERVER / "understanding_paired_auxiliary.json")
conditions = {}
for condition in sorted({row["id"].split("-")[1] for row in requests}):
    subset = [row for row in requests if row["id"].split("-")[1] == condition]
    conditions[condition] = dict(slots=len(subset), statuses=dict(Counter(r["status"] for r in subset)),
        acceptable_video_identified_in_user_relayed_coarse_screening=screen["UMM_coarse_screening"]["readable_generally_acceptable_videos_identified"],
        formal_order_accuracy=None, interpretation="Coarse screening only; no per-facet or population claim")

event_rows = [event for row in codec for event in row["event_comparison"]]
events_identical = sum(all(event["source_" + k] == event["reconstructed_" + k]
                           for k in ("onset", "complete", "anchors")) for event in event_rows)
codec_decisions = Counter(tuple(j["decision"] for j in row["auxiliary_judgments"]) for row in codec)
integer_sequence = ", ".join(str(n) for n in range(1, 62))
text_audit = []
for row in answers:
    text = "\n".join(answer["answer"] for answer in row["raw_answer_records"])
    duration = row["duration_literal_check"]
    text_audit.append(dict(id=row["id"], raw_answer_records=row["raw_answer_records"],
        actual_container_seconds=duration["reader_nominal_container_seconds"],
        duration_literal_conflict=duration["literal_conflicts_with_container"] is True,
        contains_ascending_integer_run_1_to_61=integer_sequence in text,
        formal_event_accuracy=None, evidence_level="posthoc literal text audit, not human labels"))

result = dict(
    phase="P1", scope="limited_native_baseline_negative", analysis_device="local_CPU_no_model",
    generation=dict(conditions=conditions, playable_UMM_outputs=63, initial_attempts=64,
        engineering_failures=1, coarse_successes_identified=0, CPU_controls=8,
        human_evidence="User-relayed matching two-person coarse screening with explicit reviewer1 positive IDs",
        denominator_policy="Keep all64 initial attempts; report1 technical failure separately from63 screened outputs",
        observable_order_accuracy=None, formal_seven_facet_metrics=None),
    SO00=dict(codec_inputs=len(codec), compared_development_instances=len(event_rows),
        identical_onset_completion_anchor_records=events_identical,
        paired_auxiliary_decision_counts={"/".join(key):value for key,value in codec_decisions.items()},
        MAE_min=min(row["execution"]["mean_absolute_difference"] for row in codec),
        MAE_max=max(row["execution"]["mean_absolute_difference"] for row in codec),
        independent_human_event_gold=False, hypothesis_status="not_established_beyond_development_evidence",
        interpretation="32 instances share8 characters and one renderer; not32 independent sources. Equal unknowns do not prove events preserved."),
    SO01=dict(answers=len(answers), controlled=sum(row["source"] != "fixed_native_generation" for row in answers),
        fixed_real=sum(row["source"] == "fixed_native_generation" for row in answers),
        compared_pairs=len(pairs), identical_answer_pairs=sum(row["raw_answer_text_identical"] for row in pairs),
        identical_pairs_by_condition=dict(Counter(row["condition"] for row in pairs if row["raw_answer_text_identical"])),
        duration_conflicts=[row["id"] for row in text_audit if row["duration_literal_conflict"]],
        ascending_integer_answer_ids=[row["id"] for row in text_audit if row["contains_ascending_integer_run_1_to_61"]],
        H1_status="not_established", formal_event_accuracy=None, formal_first_error_accuracy=None,
        interpretation="Text differences do not establish correct history use. Duration conflicts and numeric runs are descriptive failures, not an event-accuracy score."),
    sources=[str(path.relative_to(ROOT)) for path in [SERVER / name for name in
        ("request_status.json", "codec_auxiliary_evidence.json", "understanding_answers_and_sampling.json",
         "understanding_paired_auxiliary.json")]] + ["data/research/runs/p1_human_feedback_2026-10-31/identified_screening.json"],
    new_model_calls=0, new_human_tasks=0)
(RUN / "existing_evidence_analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
(RUN / "SO01_text_audit.json").write_text(json.dumps(text_audit, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"generation":result["generation"], "SO00":result["SO00"], "SO01":result["SO01"]}, ensure_ascii=False, indent=2))
