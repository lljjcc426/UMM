"""Validate local literature structure and links; no network and no model benchmark."""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
STATUS = {"historical_record_not_rechecked","primary_sections_read","primary_abstract_read",
          "primary_metadata_only","historical_record_unresolved"}
REQUIRED = {"id","title","claim","method","problem","conclusion","gap","source_urls",
            "verification","provenance","record_type","scope","privacy"}
PRIVATE_IDS = {"C08","C09","C10","C11"}
# These owned, recorded packed-input fixtures contain training data tensors.
# Keep their exact paths explicit; model checkpoints remain excluded below.
PACKED_INPUT_FIXTURES = {
    "data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt02/packed_batches.pt",
    "data/research/runs/env01_training_reload_a10080_2026-10-27/cloud/attempt03/packed_batches.pt",
    "data/research/runs/env01_default_capacity_a10080_2026-10-27/cloud/attempt01-small/packed_joint_batch.pt",
}
def publication_files():
    # Inspect files that can enter a normal Git commit, including tracked files
    # that would otherwise match an ignore rule. Local ignored caches stay local.
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    ).decode("utf-8").split("\0")
    for name in dict.fromkeys(names):
        path = ROOT / name
        if name and path.is_file():
            yield path

def validate():
    errors, warnings = [], []
    rows = json.loads((ROOT/"data/literature.json").read_text(encoding="utf-8"))
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate record IDs")
    keys=[r.get("canonical_key") for r in rows]
    if len(keys)!=len(set(keys)):
        errors.append("Duplicate canonical literature keys")
    if PRIVATE_IDS & set(ids):
        errors.append("Private manuscript IDs included in public catalog")
    for r in rows:
        missing = REQUIRED - r.keys()
        if missing:
            errors.append(f'{r.get("id")}: missing {sorted(missing)}')
        if r.get("verification") not in STATUS:
            errors.append(f'{r.get("id")}: bad verification status')
        if r.get("verification") == "historical_record_not_rechecked" and r.get("checked_on"):
            errors.append(f'{r.get("id")}: inherited record incorrectly marked freshly checked')
        for field in ("title","claim","method","problem","conclusion","gap"):
            if not str(r.get(field,"")).strip():
                errors.append(f'{r.get("id")}: empty {field}')
        if not r.get("source_urls"):
            errors.append(f'{r.get("id")}: no source')
        for u in r.get("source_urls",[]):
            p = urlparse(u)
            if p.scheme not in {"https","http"} or not p.netloc:
                errors.append(f'{r.get("id")}: malformed URL {u}')
        if r.get("note_path") and not (ROOT/r["note_path"]).is_file():
            errors.append(f'{r["id"]}: missing note_path')
        if r.get("review_path") and not (ROOT/r["review_path"]).is_file():
            errors.append(f'{r["id"]}: missing review_path')
    resource_audit = ROOT / "data/resource_acceptance_2026-10-25.json"
    if resource_audit.exists():
        audits = json.loads(resource_audit.read_text(encoding="utf-8"))["records"]
        resource_ids = {r["id"] for r in rows if r["record_type"] == "resource"}
        if {r["id"] for r in audits} != resource_ids or len(audits) != len(resource_ids):
            errors.append("Resource audit IDs do not match catalog resources")
        for r in audits:
            if len(r["checks"]) != 5 or any(not c.get("answer") for c in r["checks"]):
                errors.append(f'{r["id"]}: resource audit requires five substantive answers')
            if not r.get("remaining_artifact_gaps"):
                errors.append(f'{r["id"]}: resource artifact boundary missing')
    # Validate relative Markdown destinations, not live external links.
    count = 0
    files=list(publication_files())
    for p in [p for p in files if p.suffix==".md"]:
        count += 1
        text = p.read_text(encoding="utf-8")
        for raw in re.findall(r"\]\(([^)\s]+)\)",text):
            if raw.startswith(("https://","http://","mailto:","#","sandbox:")):
                continue
            dest = unquote(raw.split("#",1)[0])
            if dest and not (p.parent/dest).exists():
                errors.append(f"Broken local link: {p.relative_to(ROOT)} -> {raw}")
        if "" in text or re.search(r"【turn\d",text):
            errors.append(f"Unresolved chat citation token in {p.relative_to(ROOT)}")
    forbidden_exts={".pdf",".ttf",".otf",".woff",".woff2",".pt",".pth",".ckpt",".safetensors"}
    for p in files:
        if (p.is_file() and p.suffix.lower() in forbidden_exts
                and p.relative_to(ROOT).as_posix() not in PACKED_INPUT_FIXTURES):
            errors.append(f"Excluded binary/source type included: {p.relative_to(ROOT)}")
    if any(r.get("verification")=="historical_record_unresolved" for r in rows):
        warnings.append("Some historical references remain unresolved; explicitly tagged.")
    warnings.append("External links not availability-tested by this offline validator.")
    warnings.append("No learned-model inference, accuracy benchmark, or speed test performed.")
    report={"passed":not errors,"records":len(rows),
            "papers":sum(r["record_type"]=="paper" for r in rows),
            "resources":sum(r["record_type"]=="resource" for r in rows),
            "markdown_files_checked":count,"errors":errors,"warnings":warnings}
    (ROOT/"reports").mkdir(exist_ok=True)
    (ROOT/"reports/validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

if __name__ == "__main__":
    result=validate()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result["passed"] else 1)
