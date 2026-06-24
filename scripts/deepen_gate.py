#!/usr/bin/env python3
"""Gate new content batches — quality-first policy (Ghost 2026-06-24)."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "operating-system/new-content-frozen.json"
AUDIT = ROOT / "operating-system/reports/quality-audit.csv"


def deepen_count() -> int:
    if not AUDIT.exists():
        return 0
    return sum(1 for r in csv.DictReader(AUDIT.open(encoding="utf-8-sig")) if "قصير" in r.get("المشاكل", ""))


def quality_pct() -> float:
    if not AUDIT.exists():
        return 0.0
    rows = list(csv.DictReader(AUDIT.open(encoding="utf-8-sig")))
    if not rows:
        return 0.0
    ok = sum(1 for r in rows if not r.get("المشاكل", "").strip())
    return round(100 * ok / len(rows), 1)


def load_policy() -> dict:
    if FROZEN.exists():
        return json.loads(FROZEN.read_text(encoding="utf-8"))
    return {"frozen": False}


def check_new_batch(batch_id: str, ghost_override: bool = False) -> tuple[bool, str]:
    policy = load_policy()
    if ghost_override:
        return True, "ghost-override"
    if not policy.get("frozen"):
        return True, "not frozen"
    allowed = policy.get("allowed_batches", [])
    if batch_id in allowed:
        return True, f"allowed batch: {batch_id}"
    deepen = deepen_count()
    unlock = policy.get("unlock_when", {})
    if (
        deepen <= unlock.get("deepen_count_max", 25)
        and quality_pct() >= unlock.get("quality_pct_min", 60)
        and not policy.get("frozen")
    ):
        return True, "unlock thresholds met"
    return False, (
        f"NEW CONTENT FROZEN — {deepen} DEEPEN pages (target ≤{unlock.get('deepen_count_max', 25)}). "
        f"See operating-system/QUALITY-FIRST-POLICY.md · Batch 03 only until backlog cleared."
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Quality-first content gate")
    p.add_argument("--check", action="store_true", help="Exit 1 if new batches blocked")
    p.add_argument("--batch", default="batch-04", help="Batch id to check")
    p.add_argument("--ghost-override", action="store_true")
    args = p.parse_args()

    policy = load_policy()
    deepen = deepen_count()
    qp = quality_pct()
    ok, msg = check_new_batch(args.batch, args.ghost_override)

    print(json.dumps({
        "frozen": policy.get("frozen", False),
        "deepen_count": deepen,
        "quality_pct": qp,
        "batch": args.batch,
        "allowed": ok,
        "message": msg,
        "policy": str(FROZEN.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))

    if args.check and not ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
