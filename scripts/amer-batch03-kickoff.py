#!/usr/bin/env python3
"""Kick off Amer + team for Batch 03 — manifest pending, design done, sync."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "operating-system/batch-03.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
MANIFEST = ROOT / "assets/images/image-manifest.json"
KICKOFF_MD = ROOT / "operating-system/reports/amer-batch03-kickoff.md"
PROMPTS = ROOT / "operating-system/reports/batch-03-prompts.md"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_pending_entries(articles: list[dict]) -> int:
    data = load_manifest()
    by_slug = {e["article_slug"]: e for e in data.get("entries", [])}
    added = 0
    for a in articles:
        slug = a["slug"]
        if slug in by_slug:
            continue
        data["entries"].append({
            "article_slug": slug,
            "image": f"assets/images/approved/{a['hero_file']}",
            "alt_ar": a["alt_ar"],
            "alt_en": a["alt_en"],
            "visual_director": "pending",
            "by": "عامر — Batch 03 kickoff (جوست)",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "prompt_ref": a.get("prompt_ref", "batch-03-prompts.md"),
            "ticket": f"{a['id']}A",
        })
        added += 1
    if added:
        save_manifest(data)
    return added


def advance_design_tickets(data: dict) -> int:
    moved = 0
    for card in data.get("cards", []):
        cid = card.get("id", "")
        if not (cid.startswith("B3-") and cid.endswith("P")):
            continue
        if card.get("col") in ("member_done", "done"):
            continue
        card["col"] = "member_done"
        card["stage"] = "member_complete"
        card["result"] = "برومبت جاهز — operating-system/reports/batch-03-prompts.md"
        card["finished"] = datetime.now().strftime("%Y-%m-%d")
        card.pop("command", None)
        moved += 1
    return moved


def write_kickoff_md(articles: list[dict], ts: str) -> None:
    lines = [
        f"# 🛡️ عامر — إطلاق Batch 03 · {ts}",
        "",
        "> **من:** جوست (2026-06-24) — «ابدأ العمل وشغّل الفريق وتوليد الصور»",
        "> **القانون:** `gsystem-charter.md` · `VISUAL-DIRECTION.md` · `batch-03-prompts.md`",
        "",
        "## المطلوب الآن — توليد 7 صور (Higgsfield)",
        "",
        "| # | تذكرة | slug | الملف | القسم |",
        "|---|--------|------|-------|-------|",
    ]
    for i, a in enumerate(articles, 1):
        lines.append(
            f"| {i} | `{a['id']}A` | `{a['slug']}` | `{a['hero_file']}` | {a.get('site_section_ar', '')} |"
        )
    lines += [
        "",
        "## خطوات كل صورة",
        "",
        "1. انسخ **Prompt (EN)** من `operating-system/reports/batch-03-prompts.md`",
        "2. Higgsfield → WebP **1200×750** → `assets/images/approved/hero-<slug>.webp`",
        "3. حدّث `assets/images/image-manifest.json` → `visual_director: approved`",
        "4. انقل تذكرة `B3-XXA` إلى **انتهى من عندي** على اللوحة",
        "5. Cursor Autopilot يبني HTML تلقائياً عند `approved` + ملف",
        "",
        "## أولوية التوليد (مقترحة)",
        "",
        "1. `gulf-father-money-lessons` (B3-01A)",
        "2. `government-vs-private-school-gulf` (B3-02A)",
        "3. `digital-minimalism-families` (B3-03A)",
        "4. `pregnancy-nutrition-first-trimester` (B3-04A)",
        "5. `daily-islamic-habits-guide` (B3-05A)",
        "6. `umrah-with-kids` (B3-06A)",
        "7. `rent-vs-buy-gulf-family` (B3-07A)",
        "",
        "## الفريق بالتوازي",
        "",
        "| العضو | المسار |",
        "|-------|--------|",
        "| **Hema · تحليل** | AN-00 → B3-XXQ (SEO Briefs) |",
        "| **Hema · نمو** | GR-00 → B3-XXL (بعد Q) |",
        "| **Hema · كتابة** | B3-XXN بعد Q |",
        "| **عامر** | B3-01A…07A — توليد + اعتماد manifest |",
        "| **Cursor** | بناء عند approved — لا انتظار «ابنِ» |",
        "",
        "## BUILD VERIFY (بعد كل بناء)",
        "",
        "- hero WebP + alt ع/إن + og:image",
        "- `python3 scripts/build-from-approved-draft.py --audit` للصفحة",
    ]
    KICKOFF_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    articles = batch["articles"]

    added = ensure_pending_entries(articles)
    data = json.loads(TICKETS.read_text(encoding="utf-8"))
    moved = advance_design_tickets(data)
    data["amer_kickoff"] = ts
    data["rules"] = (
        "عامر = بوابة الجودة + توليد Batch 03. Hema = 5 سكيلات. Cursor = بناء فوري عند approved. "
        "Batch 03 نشط — جوست أمر بالبدء 2026-06-24."
    )
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    batch["amer_kickoff"] = ts
    batch["amer_status"] = "images_complete"
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_kickoff_md(articles, ts)

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/team_board_refresh.py")], check=True)
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/gsystem_notify.py")],
        check=True,
        env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "scripts")},
    )

    print(f"Amer Batch 03 kickoff: {ts}")
    print(f"  manifest pending added: {added}")
    print(f"  design tickets closed: {moved}")
    print(f"  report: {KICKOFF_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
