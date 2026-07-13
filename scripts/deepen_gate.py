#!/usr/bin/env python3
"""Gate new content batches — quality-first policy (Ghost 2026-06-24)."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "operating-system/new-content-frozen.json"
AUDIT = ROOT / "operating-system/reports/quality-audit.csv"

CONTENT_ROOTS = [
    "blog", "peace-capsules", "finance-wealth", "health", "fitness",
    "productivity", "islamic-hajj-umrah", "real-estate", "featured-stories",
    "comparisons", "guides", "travel", "health-pregnancy",
]
HARD_SKIP = {
    "islamic-hajj-umrah/hijri-new-year-children.html",
    "finance-wealth/family-budget-plan-en.html",
    "real-estate/first-home-buyer-saudi-arabia.html",
}


def _audit_rows():
    if not AUDIT.exists():
        return []
    return list(csv.DictReader(AUDIT.open(encoding="utf-8-sig")))


def _is_ok(problems: str) -> bool:
    p = (problems or "").strip()
    return (not p) or p.startswith("✅")


def deepen_count() -> int:
    """Raw CSV flag count (includes stubs/redirects marked قصير)."""
    return sum(1 for r in _audit_rows() if "قصير" in r.get("المشاكل", ""))


def real_live_deepen_count() -> int:
    """LIVE indexed articles with <article> body under 1600 words (WRITING-LAW)."""
    n = 0
    for root in CONTENT_ROOTS:
        folder = ROOT / root
        if not folder.exists():
            continue
        for p in folder.glob("*.html"):
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if rel in HARD_SKIP or "complete-" in rel:
                continue
            html = p.read_text(encoding="utf-8", errors="ignore")
            if re.search(r'name="robots"[^>]*noindex', html[:2000], re.I):
                continue
            if re.search(r'http-equiv=["\']refresh', html[:2000], re.I):
                continue
            m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S | re.I)
            if not m:
                continue
            words = len(
                [w for w in re.split(r"\s+", re.sub(r"<[^>]+>", " ", m.group(1))) if w.strip()]
            )
            if 200 <= words < 1600:
                n += 1
    return n


def quality_pct() -> float:
    rows = _audit_rows()
    if not rows:
        return 0.0
    ok = sum(1 for r in rows if _is_ok(r.get("المشاكل", "")))
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
    real = real_live_deepen_count()
    unlock = policy.get("unlock_when", {})
    # Unlock still uses CSV deepen for conservatism + quality_pct; real count is reported.
    if (
        deepen <= unlock.get("deepen_count_max", 25)
        and quality_pct() >= unlock.get("quality_pct_min", 60)
        and not policy.get("frozen")
    ):
        return True, "unlock thresholds met"
    return False, (
        f"NEW CONTENT FROZEN — CSV قصير={deepen} · LIVE<article><1600={real} "
        f"(target ≤{unlock.get('deepen_count_max', 25)}). "
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
    real = real_live_deepen_count()
    qp = quality_pct()
    ok, msg = check_new_batch(args.batch, args.ghost_override)

    print(json.dumps({
        "frozen": policy.get("frozen", False),
        "deepen_count": deepen,
        "real_live_deepen": real,
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
