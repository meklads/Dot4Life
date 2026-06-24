#!/usr/bin/env python3
"""Launch DEEPEN Batch 10 — 10 thin LIVE articles → Hema / Amer / Cursor tickets."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TICKETS = ROOT / "operating-system/handoff-tickets.json"

ARTICLES = [
    ("D10-01", "best-family-destinations-gulf", "أفضل وجهات السفر العائلية في الخليج", "/travel/best-family-destinations-gulf.html", 204, "سفر"),
    ("D10-02", "featured-story-arab-father-teens", "قصة أب عربي ومراهقيه", "/featured-stories/featured-story-arab-father-teens.html", 350, "قصص مميزة"),
    ("D10-03", "featured-story-gulf-family-home", "بيت العائلة الخليجية", "/featured-stories/featured-story-gulf-family-home.html", 389, "قصص مميزة"),
    ("D10-04", "featured-story-saudi-mother", "أم سعودية — قصة ملهمة", "/featured-stories/featured-story-saudi-mother.html", 289, "قصص مميزة"),
    ("D10-05", "body-fat-vs-weight-guide", "الدهون الحشوية مقابل الوزن", "/blog/body-fat-vs-weight-guide.html", 330, "الصحة والعافية"),
    ("D10-06", "peace-at-home-5-steps", "السلام في البيت — 5 خطوات", "/peace-capsules/peace-at-home-5-steps.html", 406, "كبسولات يومية"),
    ("D10-07", "comparisons-public-vs-private-education", "تعليم حكومي أم خاص", "/comparisons/comparisons-public-vs-private-education.html", 420, "مقارنات وقرارات"),
    ("D10-08", "comparisons-ready-vs-build-home", "منزل جاهز أم بناء", "/comparisons/comparisons-ready-vs-build-home.html", 505, "مقارنات وقرارات"),
    ("D10-09", "ramadan-preparation-guide-families", "تحضير رمضان للعائلة", "/blog/ramadan-preparation-guide-families.html", 439, "الحياة الإسلامية"),
    ("D10-10", "house-affordability-single-income-guide", "قدرة تحمّل السكن بدخل واحد", "/blog/house-affordability-single-income-guide.html", 447, "العقار والمالية"),
]

TS = datetime.now().strftime("%Y-%m-%d %H:%M")


def hema_card(batch_id: str, slug: str, title: str, url_path: str, words: int, section: str) -> dict:
    n_id = f"{batch_id}N"
    return {
        "id": n_id,
        "slug": slug,
        "kind": "deepen",
        "batch": "deepen-10",
        "batch_article": batch_id,
        "col": "hema_writing",
        "stage": "revise",
        "step_ar": "📝 تعميق",
        "skill": "writing",
        "owner": "Hema",
        "article": f"DEEPEN — {title}",
        "reason": f"Batch 10 · رفيع ~{words}w · {section}",
        "url_path": url_path,
        "site_section": section,
        "law_ref": "operating-system/WRITING-LAW.md",
        "assignee": "Hema · سكيل الكتابة",
        "task": (
            f"DEEPEN D10 — تعميق `{slug}`:\n"
            f"· الهدف ≥1600w ع (+ en إن وُجد) · FAQ≥4 · Article+FAQPage\n"
            f"· 0 شرطات · مصادر https · draft-gate.py PASS\n"
            f"· الملف: `blog/` أو المسار الحيّ — لا slug جديد\n"
            f"ثم انقلي إلى «انتهى من عندي»"
        ),
        "command": f"{n_id}: deepen — {slug} → WRITING-LAW ≥1600w + FAQ",
        "ts": TS,
    }


def amer_card(batch_id: str, slug: str, title: str, url_path: str) -> dict:
    a_id = f"{batch_id}A"
    n_id = f"{batch_id}N"
    return {
        "id": a_id,
        "slug": slug,
        "kind": "deepen",
        "batch": "deepen-10",
        "batch_article": batch_id,
        "col": "amer",
        "stage": "review",
        "step_ar": "🛡️ بوابة",
        "owner": "عامر",
        "article": f"مراجعة DEEPEN — {title}",
        "url_path": url_path,
        "assignee": "عامر",
        "task": f"amer-mandate — راجع تعميق {slug} بعد تسليم هيما",
        "command": f"{a_id}: amer-mandate review — {slug}",
        "depends_on": n_id,
        "ts": TS,
    }


def cursor_card(batch_id: str, slug: str, title: str, url_path: str) -> dict:
    c_id = f"{batch_id}C"
    a_id = f"{batch_id}A"
    return {
        "id": c_id,
        "slug": slug,
        "kind": "deepen",
        "batch": "deepen-10",
        "batch_article": batch_id,
        "col": "cursor",
        "stage": "build",
        "step_ar": "⚙️ بناء",
        "owner": "Cursor",
        "article": f"TECH_BUILD — {title}",
        "url_path": url_path,
        "assignee": "Cursor",
        "task": f"بناء/نشر HTML معتمد من عامر — تمبليت موحّد + push",
        "command": f"{c_id}: TECH_BUILD — {slug} → git push",
        "depends_on": a_id,
        "ts": TS,
    }


def main() -> int:
    data = json.loads(TICKETS.read_text(encoding="utf-8"))
    existing = {c["id"] for c in data.get("cards", [])}
    added = 0
    for batch_id, slug, title, url_path, words, section in ARTICLES:
        for card in (
            hema_card(batch_id, slug, title, url_path, words, section),
            amer_card(batch_id, slug, title, url_path),
            cursor_card(batch_id, slug, title, url_path),
        ):
            if card["id"] in existing:
                continue
            data["cards"].append(card)
            existing.add(card["id"])
            added += 1
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data["deepen_batch_10"] = {
        "launched": datetime.now().strftime("%Y-%m-%d"),
        "count": 10,
        "report": "operating-system/reports/deepen-batch-10.md",
    }
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], cwd=ROOT, check=False)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], cwd=ROOT, check=False)
    print(json.dumps({"added": added, "articles": 10, "tickets_per": 3}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
