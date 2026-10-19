"""Validate the 2026-10-19 provenance supplement without making network claims.

Run: python scripts/validate_research_additions.py
Checks the supplement-to-master crosswalk; does not re-run paper experiments.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "id", "title", "kind", "task", "input", "output", "data", "framework",
    "architecture", "metrics", "baselines", "experimental_conditions",
    "sources", "checked", "next", "note"
}


def validate() -> dict:
    registry = json.loads((ROOT / "data/research_additions_2026-10-19.json").read_text(encoding="utf-8"))
    rows = registry["records"]
    master = json.loads((ROOT / "data/literature.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in rows]
    master_ids = {r["id"] for r in master}
    problems = []
    warnings = []
    if len(ids) != len(set(ids)):
        problems.append("duplicate IDs in supplement")
    if set(ids) & master_ids:
        problems.append("supplement ID collides with master catalog")
    for r in rows:
        missing = REQUIRED - set(r)
        if missing:
            problems.append(f'{r.get("id")} missing {sorted(missing)}')
            continue
        for field in REQUIRED - {"sources"}:
            if not isinstance(r[field], str) or not r[field].strip():
                problems.append(f'{r["id"]} invalid {field}')
        if not isinstance(r["sources"], list) or not r["sources"]:
            problems.append(f'{r["id"]} missing URLs')
        else:
            for url in r["sources"]:
                p = urlparse(url)
                if p.scheme != "https" or not p.netloc:
                    problems.append(f'{r["id"]} invalid URL: {url}')
        if not (ROOT / r["note"]).is_file():
            problems.append(f'{r["id"]} missing note: {r["note"]}')
        if "existing_master_id" in r and r["existing_master_id"] not in master_ids:
            problems.append(f'{r["id"]} existing_master_id not found')
        if registry.get("status") == "integrated_into_master_with_stable_crosswalk":
            if r.get("integrated_master_id") not in master_ids:
                problems.append(f'{r["id"]} integrated_master_id not found')
        if "same_work_as" in r and r["same_work_as"] not in ids:
            problems.append(f'{r["id"]} same_work_as not found')
        if r["checked"] in {"repo_readme", "publisher_abstract", "hf_model_card"}:
            warnings.append(f'{r["id"]}: partial-primary-source depth; full paper/weights unverified')
    print(json.dumps({
        "passed": not problems,
        "master_entries": len(master),
        "supplement_entries": len(rows),
        "by_kind": dict(sorted(Counter(r["kind"] for r in rows).items())),
        "master_duplicates_linked": [r["id"] for r in rows if r.get("existing_master_id")],
        "supporting_artefacts_linked": [r["id"] for r in rows if r.get("same_work_as")],
        "errors": problems,
        "warnings": warnings,
        "scope": "schema and local path checks only; external URL existence and research claims not automatically verified"
    }, ensure_ascii=False, indent=2))
    return {"passed": not problems}


if __name__ == "__main__":
    raise SystemExit(0 if validate()["passed"] else 1)
