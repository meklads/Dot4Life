#!/usr/bin/env python3
"""Boost archive pages toward G1–G11 via execute-blog-triage enhance_page."""
from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Long pages failing only on schema/FAQ (quality audit 2026-06-22)
DEFAULT_BOOST = [
    "blog/family-budget-planning-guide.html",
    "blog/gold-vs-savings-account-comparison-en.html",
    "guides/mecca-medina.html",
    "guides/salalah-oman.html",
    "guides/saudi-tourism.html",
    "guides/complete-life-guide.html",
]

spec = importlib.util.spec_from_file_location(
    "triage", ROOT / "scripts/execute-blog-triage.py"
)
triage = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(triage)


def main() -> None:
    paths = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_BOOST
    if paths == ["--all-long"]:
        import csv

        paths = []
        for r in csv.DictReader(
            open(ROOT / "operating-system/reports/quality-audit.csv", encoding="utf-8-sig")
        ):
            if "سليم" in r["المشاكل"]:
                continue
            if int(r["كلمات"]) >= 1350 and "قصير" not in r["المشاكل"]:
                paths.append(f"{r['القسم']}/{r['الملف']}")

    print(f"=== Archive boost ({len(paths)} pages) ===\n")
    passed = failed = 0
    log: list[str] = []
    for rel in paths:
        ok, msg = triage.enhance_page(rel)
        if ok:
            passed += 1
            print(f"  ✅ PASS {rel}")
        else:
            failed += 1
            log.append(f"{rel}: {msg}")
            print(f"  ❌ FAIL {rel}: {msg}")

    print(f"\n=== SUMMARY: {passed} PASS, {failed} FAIL ===")
    out = ROOT / "operating-system/reports/archive-boost-log.md"
    out.write_text(
        f"# Archive boost — {date.today().isoformat()}\n\n"
        f"- PASS: **{passed}/{len(paths)}**\n\n"
        "## Failures\n"
        + ("\n".join(f"- {x}" for x in log) if log else "- none")
        + "\n",
        encoding="utf-8",
    )
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
