#!/usr/bin/env python3
"""Launch batch-02: inject handoff tickets + sync board."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "operating-system/batch-02.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
PROMPTS_MD = ROOT / "operating-system/reports/batch-02-prompts.md"

PROMPTS = {
    "children-education-savings-guide": "Documentary-style warm still-life photograph, saving for children's education theme, no people. On a tidy desk: a clean coin jar (NOT a piggy bank), a graduation cap miniature, a stack of children's books, a notebook with a simple savings plan, and a small plant. Soft natural light, shallow depth of field, hopeful and calm. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "daily-islamic-habits-guide": "Documentary-style warm still-life photograph, daily Islamic habits theme, no people. A calm home corner near a window: prayer beads, an open simple habit-tracker notebook, a small clean prayer rug folded neatly, a cup of tea, and a small plant, soft warm morning light. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, dignified soft gold #b8893c accent detail. Respect for religious symbols. No Quranic verses rendered as burned-in text. No watermark, no logos. Realistic texture, rule of thirds, gentle negative space. 3:2, crop to 1200x750.",
    "life-insurance-gulf-families": "Documentary-style warm still-life photograph, life insurance and family protection theme, no people. On a clean desk: a small wooden house model and a small family-figure paper cutout placed under a gently sheltering hand-drawn umbrella icon on a document, a pen, a folder, and a small plant. Soft natural light, shallow depth of field, calm and reassuring. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "building-personal-savings-system": "Documentary-style warm still-life photograph, personal savings system theme, no people. On a wooden desk: three labeled clean glass jars holding coins (NOT piggy banks), a notebook with a simple savings plan, a calculator, and a small green plant growing beside the coins. Soft natural light, shallow depth of field, organized and calm. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "family-budget-planning-guide": "Documentary-style warm still-life photograph, family budget planning guide theme, no people. On a wooden home table: an open budget planner notebook with simple columns, a calculator, a coin jar (NOT a piggy bank), neatly stacked coins, and a small plant. Soft natural window light, shallow depth of field, tidy and calm. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "end-of-service-saudi": "Documentary-style warm still-life photograph, end-of-service benefits theme, no people. On a clean office desk: a labeled document folder, a calculator, a pen, neatly stacked coins, a notebook with simple figures, and a small plant. Soft natural light, shallow depth of field, professional and calm. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "medina-hotels-near-masjid-nabawi": "Documentary-style warm photograph, Medina hotels near Masjid an-Nabawi theme, reverent. A serene wide view of the Medina skyline at golden hour with the green dome and minarets softly in the background, a tidy hotel room key and a small travel bag resting on a clean surface in the foreground, calm and dignified, softly blurred distant scene, no faces in focus. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 tones, dignified soft gold #b8893c accent detail. Respect for religious context. No text, no watermark, no logos. Realistic texture, shallow depth of field, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "umrah-visa-gulf-residents-guide": "Documentary-style warm still-life photograph, Umrah visa for Gulf residents theme, no people. On a clean surface: a passport, a travel document folder, a small modest prayer cap, a compact bag, and a softly blurred mosque silhouette through a window at golden hour. Soft natural light, shallow depth of field, calm and reverent. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, dignified soft gold #b8893c accent detail. Respect for religious context. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "family-nutrition-on-budget": "Documentary-style warm still-life photograph, affordable family nutrition theme, no people. A wooden kitchen table with a basket of fresh affordable vegetables, fruits, grains in jars, a few coins beside a simple grocery list, and a small plant, healthy and economical mood. Soft natural light, shallow depth of field. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent detail. No pig or piggy bank, no alcohol. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "managing-screen-time-children": "Documentary-style warm still-life photograph, managing children's screen time theme, no people. A calm family table with a tablet placed face-down beside a small hourglass timer, a stack of children's books, building blocks, and a small plant, suggesting balanced healthy limits. Soft natural light, shallow depth of field, peaceful. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent detail. No people, no text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
}

TASKS = {
    "hema": {
        "deepen": "DEEPEN/كتابة — ≥1300w · FAQ×4 · draft-gate — ثم «انتهى من عندي» → عامر",
        "prompt": "جهّز/راجع برومبت الصورة — batch-02-prompts.md — ثم «انتهى من عندي»",
    },
    "amer": "توليد Higgsfield → WebP 1200×750 → manifest approved → BUILD VERIFY",
    "cursor": "Autopilot: approved + slug → hero HTML → git push → «منتهي LIVE»",
}


def card_from_article(a: dict) -> dict:
    col = a["owner_col"]
    skill = a.get("skill")
    stage = a["stage"]
    slug = a["slug"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    if col == "hema":
        task = TASKS["hema"]["deepen" if stage == "deepen" else "prompt"]
        assignee = {"moni": "Hema · سكيل Moni", "ruwaq": "Hema · سكيل رواق", "omar": "Hema · سكيل عمر"}.get(
            skill or "moni", "Hema"
        )
    elif col == "amer":
        task = TASKS["amer"]
        assignee = "عامر"
    else:
        task = TASKS["cursor"]
        assignee = "Cursor"

    url = f"https://dotforlife.com/blog/{slug}.html"
    cmd = f"{a['id']}: {slug} — {a['needs']}"

    c = {
        "id": a["id"],
        "slug": slug,
        "kind": "batch2",
        "col": col,
        "stage": stage,
        "batch": 2,
        "owner": "جوست",
        "article": a["title_ar"],
        "reason": f"Batch 02 · {a['section']} · {a['words_ar']}w",
        "assignee": assignee,
        "task": task,
        "command": cmd,
        "hero_file": a["hero_file"],
        "prompt_ref": a["prompt_ref"],
        "alt_ar": a["alt_ar"],
        "alt_en": a["alt_en"],
        "url": url,
        "ts": ts,
    }
    if skill:
        c["skill"] = skill
    return c


def write_prompts_md(articles: list) -> None:
    lines = [
        "# 🖼️ Batch 02 — 10 برومبتات صور",
        "",
        "> **من:** جوست + Cursor · **إلى:** Hema (مراجعة) · عامر (توليد Higgsfield) · **2026-06-24**",
        "> **المسار:** `assets/images/approved/hero-<slug>.webp` · 1200×750 WebP",
        "",
        "| # | slug | الملف | المالك الآن |",
        "|---|------|-------|-------------|",
    ]
    for i, a in enumerate(articles, 1):
        lines.append(f"| {i} | `{a['slug']}` | `{a['hero_file']}` | {a['owner_col']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, a in enumerate(articles, 1):
        slug = a["slug"]
        lines.extend([
            f"## {i}. {a['title_ar']} (`{slug}`)",
            "",
            f"**الملف:** `assets/images/approved/{a['hero_file']}`",
            "",
            f"**alt_ar:** {a['alt_ar']}",
            "",
            f"**alt_en:** {a['alt_en']}",
            "",
            "**Prompt (EN):**",
            "",
            "```",
            PROMPTS.get(slug, "(see omar-image-table.md)"),
            "```",
            "",
        ])
    PROMPTS_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    articles = batch["articles"]
    data = json.loads(TICKETS.read_text(encoding="utf-8"))

    # Remove old batch-2 ghost backlog superseded by B2 launch
    supersede = {
        "H-16", "H-17", "H-18", "H-19", "H-20", "H-21", "H-22",
        "H-23", "H-24", "H-25", "H-26",
        "T-08", "T-09", "T-10", "T-11",
    }
    for c in data["cards"]:
        if c.get("id") in supersede and c.get("col") == "ghost":
            c["col"] = "done"
            c["stage"] = "done"
            c["task"] = "أُدمج في Batch 02"
            c["result"] = "✅ superseded by batch-02 launch 2026-06-24"

    # Drop existing B2-* if re-run
    data["cards"] = [c for c in data["cards"] if not str(c.get("id", "")).startswith("B2-")]

    new_cards = [card_from_article(a) for a in articles]
    data["cards"].extend(new_cards)
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data["batch_active"] = "batch-02"
    data["batch_size"] = 10

    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_prompts_md(articles)

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)

    print(f"Launched batch-02: {len(new_cards)} tickets")
    for c in new_cards:
        print(f"  {c['id']} → {c['col']} · {c['article']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
