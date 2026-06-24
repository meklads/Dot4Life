#!/usr/bin/env python3
"""Launch batch-03: 7 site sections × 4 tickets (Hema 5-skill charter)."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "operating-system/batch-03.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
PROMPTS_MD = ROOT / "operating-system/reports/batch-03-prompts.md"

WRITING_LAW = "operating-system/WRITING-LAW.md"
HEMA_CHARTER = "operating-system/HEMA-CHARTER.md"
WORD_TARGET = 1600

PROMPTS = {
    "gulf-father-money-lessons": "Documentary-style warm still-life photograph, Gulf father teaching children about money theme, no people. A modest home desk: an open simple budget notebook, a calculator, a ceramic coin jar (NOT a piggy bank), a small plant, and a folded children's storybook about saving. Soft natural window light, shallow depth of field, calm and trustworthy. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze/gold #b8893c accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "government-vs-private-school-gulf": "Documentary-style warm still-life photograph, Gulf family education choice theme, no people. A tidy study desk: stacked school textbooks, a sharpened pencil, an apple, a small plant, and an open notebook with two simple columns for comparison. Soft natural window light, shallow depth of field, calm and trustworthy. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent detail. No people, no faces. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "digital-minimalism-families": "Documentary-style warm still-life photograph, digital minimalism for families theme, no people. A calm home table with a single phone placed face-down in a small basket, beside an open paper book, a board game, a cup of tea, and a small plant, suggesting quiet screen-free family time. Soft natural light, shallow depth of field, peaceful. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent detail. No people, no text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "pregnancy-nutrition-first-trimester": "Documentary-style warm still-life photograph, first trimester pregnancy nutrition theme, no people. A wooden kitchen table with a basket of fresh fruits and vegetables, a glass of water, whole grains in a jar, and a small plant, healthy and gentle mood. Soft natural light, shallow depth of field. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent detail. No alcohol. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "daily-islamic-habits-guide": "Documentary-style warm still-life photograph, daily Islamic habits theme, no people. A calm home corner near a window: prayer beads, an open simple habit-tracker notebook, a small clean prayer rug folded neatly, a cup of tea, and a small plant, soft warm morning light. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, dignified soft gold #b8893c accent detail. Respect for religious symbols. No Quranic verses rendered as burned-in text. No watermark, no logos. Realistic texture, rule of thirds, gentle negative space. 3:2, crop to 1200x750.",
    "umrah-with-kids": "Documentary-style warm still-life photograph, family Umrah preparation theme, no people. On a clean surface: a compact family travel bag, prayer beads, a folded modest cap, and soft golden window light suggesting a reverent journey. Calm and dignified. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, dignified soft gold #b8893c accent detail. Respect for religious context. No text, no watermark, no logos. Realistic texture, shallow depth of field, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
    "rent-vs-buy-gulf-family": "Documentary-style warm still-life photograph, rent versus buy home for Gulf families theme, no people. On a wooden desk: a house key on a simple key ring, a folded rental contract beside a small wooden house model, a notebook with two columns, and a small plant. Balanced composition. On-brand toning: deep teal-green #054241 accents, warm cream #FAF8F4 background, olive-green #4a8a82 accent detail. No pig or piggy bank. No text, no watermark, no logos. Realistic texture, rule of thirds, breathing negative space. 3:2, crop to 1200x750.",
}

TASKS = {
    "write_deepen": f"سكيل الكتابة — {WRITING_LAW} · ≥{WORD_TARGET}w · FAQ×5–6 · 0 شرطات — ثم «انتهى من عندي»",
    "write_review": f"سكيل الكتابة — مراجعة {WRITING_LAW} + draft-gate PASS — ثم «انتهى من عندي»",
    "design_prompt": f"سكيل التصميم — VISUAL-DIRECTION.md · batch-03-prompts.md — ثم «انتهى من عندي»",
    "amer": "توليد Higgsfield → WebP 1200×750 → manifest approved → BUILD VERIFY",
    "cursor": "Autopilot: approved + slug → hero HTML → git push → «منتهي LIVE»",
}

SKILL_LABEL = {
    "writing": "Hema · سكيل الكتابة",
    "design": "Hema · سكيل التصميم",
}


def cards_for_article(a: dict, batch_num: int = 3) -> list[dict]:
    base_id = a["id"]
    slug = a["slug"]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    url_path = a.get("url_path", f"/blog/{slug}.html")
    section_ar = a.get("site_section_ar", a.get("site_section", ""))
    site_section = a.get("site_section", "")
    words = a["words_ar"]
    deepen = words < WORD_TARGET

    def base(**extra: object) -> dict:
        c = {
            "slug": slug,
            "kind": "batch3",
            "batch": batch_num,
            "batch_article": base_id,
            "owner": "جوست",
            "article": a["title_ar"],
            "reason": f"Batch 03 · {section_ar} · {words}w",
            "hero_file": a["hero_file"],
            "prompt_ref": a["prompt_ref"],
            "alt_ar": a["alt_ar"],
            "alt_en": a["alt_en"],
            "url_path": url_path,
            "ts": ts,
            "site_section": site_section,
            "law_ref": WRITING_LAW,
        }
        c.update(extra)
        return c

    write_stage = "deepen" if deepen else "review"
    write_task = TASKS["write_deepen"] if deepen else TASKS["write_review"]
    write_cmd = (
        f"{base_id}N: {slug} — "
        f"{'DEEPEN ≥'+str(WORD_TARGET)+'w per WRITING-LAW' if deepen else 'مراجعة WRITING-LAW + draft-gate'}"
    )

    return [
        base(
            id=f"{base_id}N",
            col="hema_writing",
            stage=write_stage,
            step_ar="📝 نص",
            skill="writing",
            assignee=SKILL_LABEL["writing"],
            task=write_task,
            command=write_cmd,
        ),
        base(
            id=f"{base_id}P",
            col="hema_design",
            stage="prompt",
            step_ar="🖼️ برومبت",
            skill="design",
            assignee=SKILL_LABEL["design"],
            task=TASKS["design_prompt"],
            command=f"{base_id}P: {slug} — برومبت + pending في الفهرس",
        ),
        base(
            id=f"{base_id}A",
            col="amer",
            stage="generate",
            step_ar="🎨 صورة",
            skill="generate",
            assignee="عامر",
            task=TASKS["amer"],
            command=f"{base_id}A: {slug} — Higgsfield → {a['hero_file']}",
        ),
        base(
            id=f"{base_id}C",
            col="cursor",
            stage="build",
            step_ar="⚙️ بناء",
            assignee="Cursor",
            task=TASKS["cursor"],
            command=f"{base_id}C: {slug} — بناء hero عند approved → autopilot",
        ),
    ]


def write_prompts_md(articles: list) -> None:
    lines = [
        f"# 🖼️ Batch 03 — {len(articles)} برومبتات صور",
        "",
        f"> **من:** جوست + Cursor · **إلى:** Hema سكيل التصميم · عامر (Higgsfield) · **{datetime.now().strftime('%Y-%m-%d')}**",
        f"> **القانون:** `{HEMA_CHARTER}` · `{WRITING_LAW}`",
        "> **المسار:** `assets/images/approved/hero-<slug>.webp` · 1200×750 WebP",
        "",
        "| # | قسم الموقع | slug | الملف |",
        "|---|------------|------|-------|",
    ]
    for i, a in enumerate(articles, 1):
        lines.append(
            f"| {i} | {a.get('site_section_ar', '')} | `{a['slug']}` | `{a['hero_file']}` |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, a in enumerate(articles, 1):
        slug = a["slug"]
        lines.extend([
            f"## {i}. {a['title_ar']} (`{slug}`)",
            "",
            f"**قسم الموقع:** {a.get('site_section_ar', '')} · `{a.get('site_section', '')}`",
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
            PROMPTS.get(slug, "(see VISUAL-DIRECTION.md)"),
            "```",
            "",
        ])
    PROMPTS_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    from deepen_gate import check_new_batch

    ok, msg = check_new_batch("batch-03")
    if not ok:
        print(f"BLOCKED: {msg}", file=sys.stderr)
        return 1

    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    articles = batch["articles"]
    data = json.loads(TICKETS.read_text(encoding="utf-8"))

    data["cards"] = [c for c in data["cards"] if not str(c.get("id", "")).startswith("B3-")]

    new_cards: list[dict] = []
    for a in articles:
        new_cards.extend(cards_for_article(a))

    data["cards"].extend(new_cards)
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data["batch_active"] = "batch-03"
    data["batch_size"] = batch.get("size", len(articles))
    data["batch_tickets"] = len(new_cards)
    data["rules"] = (
        "عامر = بوابة الجودة. Hema = 5 سكيلات (HEMA-CHARTER.md). Cursor = بناء. "
        "Batch 03 = 7 أقسام موقع (بدون كبسولات). جوست = مخزون."
    )

    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_prompts_md(articles)

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)

    by_col: dict[str, int] = {}
    for c in new_cards:
        by_col[c["col"]] = by_col.get(c["col"], 0) + 1
    print(f"Launched batch-03: {len(articles)} articles · {len(new_cards)} tickets")
    for col, n in sorted(by_col.items()):
        print(f"  {col}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
