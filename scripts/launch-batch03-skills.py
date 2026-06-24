#!/usr/bin/env python3
"""Add Batch 03 analysis (Q) + growth (L) skill tickets for Hema."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "operating-system/batch-03.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
SEO_DIR = ROOT / "operating-system/reports/batch-03-seo"
GROWTH_DIR = ROOT / "operating-system/reports/batch-03-growth"
HEMA_CHARTER = "operating-system/HEMA-CHARTER.md"

ANALYSIS_PLATFORM_TASK = """سكيل التحليل — تدقيق منصة الترافيك (قبل SEO Briefs):
1) GA4 `G-3G1XPV4F0G`: تغطية index + قوالب المقال + أدوات — gaps؟
2) Google Search Console: ملكية dotforlife.com + sitemap.xml مُرسَل
3) خط أساس (90 يوم إن وُجد وصول): top 20 صفحة · جلسات · انطباعات · CTR
4) قائمة صفحات بلا GA أو بلا canonical/hreflang
5) التقرير: `operating-system/reports/hema-analysis-traffic-baseline-2026-06-24.md`
ثم «انتهى من عندي»"""

GROWTH_PLATFORM_TASK = """سكيل النمو — خريطة العناقيد لـ 7 أقسام Batch 03:
1) جدول: قسم → مقال ركيزة B3 → 3 صفحات LIVE داعمة (URLs) → هوم/مدونة/أدوات
2) أولوية الربط: أي مقال يُربط بأيّ قبل النشر
3) الملف: `operating-system/reports/batch-03-growth/site-clusters-7sections.md`
ثم «انتهى من عندي»"""


def analysis_task(a: dict) -> str:
    aid, slug = a["id"], a["slug"]
    section = a.get("site_section_ar", "")
    report = f"operating-system/reports/batch-03-seo/{aid}-{slug}.md"
    return f"""سكيل التحليل — SEO Brief لـ {aid} ({section}) **قبل الكتابة**:
· نية البحث + كلمة ركيزة AR/EN + 3 طويلة الذيل
· SERP: 3 منافسين + فجوة المحتوى
· Title≤60 · Meta≤155 · H1 مقترح · outline H2
· 3 روابط داخلية مستهدفة (عناقيد القسم على الموقع الحالي)
· الملف: `{report}`
· أرفق ملخصاً في تذكرة {aid}N قبل أن يبدأ الكاتب
ثم «انتهى من عندي»"""


def growth_task(a: dict) -> str:
    aid, slug = a["id"], a["slug"]
    section = a.get("site_section_ar", "")
    report = f"operating-system/reports/batch-03-growth/{aid}-{slug}.md"
    return f"""سكيل النمو — ربط داخلي + SEO لـ {aid} ({section}):
· 5 روابط صادرة وصفية من المقال (URLs محددة على dotforlife.com)
· 3 صفحات LIVE ترجع لهذا المقال (anchor AR طبيعي)
· hreflang ar/en + canonical + breadcrumb مقترح
· خطّاف واحد لإعادة تدوير (واتساب أو ثريد) — نص فقط
· الملف: `{report}`
· يعتمد على اكتمال {aid}Q (SEO Brief)
ثم «انتهى من عندي»"""


def cards_for_batch(articles: list[dict]) -> list[dict]:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards: list[dict] = []

    cards.append({
        "id": "AN-00",
        "slug": "traffic-baseline",
        "kind": "analysis",
        "batch": 3,
        "col": "hema_analysis",
        "stage": "audit",
        "step_ar": "📊 ترافيك",
        "skill": "analysis",
        "assignee": "Hema · سكيل التحليل",
        "owner": "جوست",
        "article": "تدقيق GA4 + Search Console + خط أساس",
        "reason": "Batch 03 · منصة التحليل",
        "law_ref": HEMA_CHARTER,
        "task": ANALYSIS_PLATFORM_TASK,
        "command": "AN-00: GA4 G-3G1XPV4F0G + GSC + baseline ترافيك → hema-analysis-traffic-baseline",
        "ts": ts,
    })

    cards.append({
        "id": "GR-00",
        "slug": "site-clusters-7sections",
        "kind": "growth",
        "batch": 3,
        "col": "hema_growth",
        "stage": "map",
        "step_ar": "🗺️ عناقيد",
        "skill": "growth",
        "assignee": "Hema · سكيل النمو",
        "owner": "جوست",
        "article": "خريطة عناقيد 7 أقسام Batch 03",
        "reason": "Batch 03 · ربط داخلي",
        "law_ref": HEMA_CHARTER,
        "task": GROWTH_PLATFORM_TASK,
        "command": "GR-00: خريطة عناقيد 7 أقسام → site-clusters-7sections.md",
        "ts": ts,
    })

    for a in articles:
        base_id = a["id"]
        slug = a["slug"]
        section_ar = a.get("site_section_ar", "")
        url_path = a.get("url_path", f"/blog/{slug}.html")
        common = {
            "slug": slug,
            "kind": "batch3",
            "batch": 3,
            "batch_article": base_id,
            "owner": "جوست",
            "article": a["title_ar"],
            "reason": f"Batch 03 · {section_ar}",
            "url_path": url_path,
            "site_section": a.get("site_section", ""),
            "law_ref": HEMA_CHARTER,
            "ts": ts,
        }
        cards.append({
            **common,
            "id": f"{base_id}Q",
            "col": "hema_analysis",
            "stage": "brief",
            "step_ar": "🔍 SEO Brief",
            "skill": "analysis",
            "assignee": "Hema · سكيل التحليل",
            "task": analysis_task(a),
            "command": f"{base_id}Q: {slug} — SEO Brief + SERP → batch-03-seo/{base_id}-{slug}.md",
            "depends_on": "AN-00",
        })
        cards.append({
            **common,
            "id": f"{base_id}L",
            "col": "hema_growth",
            "stage": "links",
            "step_ar": "🔗 ربط",
            "skill": "growth",
            "assignee": "Hema · سكيل النمو",
            "task": growth_task(a),
            "command": f"{base_id}L: {slug} — 5 صادرة + 3 واردة → batch-03-growth/{base_id}-{slug}.md",
            "depends_on": f"{base_id}Q",
        })

    return cards


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    articles = batch["articles"]
    data = json.loads(TICKETS.read_text(encoding="utf-8"))

    skill_ids = {"AN-00", "GR-00"} | {f"{a['id']}Q" for a in articles} | {f"{a['id']}L" for a in articles}
    data["cards"] = [c for c in data["cards"] if c.get("id") not in skill_ids]

    new_cards = cards_for_batch(articles)
    data["cards"].extend(new_cards)

    dist = batch.get("distribution", {})
    dist["hema_analysis"] = dist.get("hema_analysis", 0) + 1 + len(articles)
    dist["hema_growth"] = dist.get("hema_growth", 0) + 1 + len(articles)
    batch["distribution"] = dist
    batch["tickets_per_article"] = 6
    batch["ticket_total"] = len(articles) * 6 + 2
    batch["pipeline"] = "Hema تحليل → نمو → كتابة + تصميم → عامر → Cursor"
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    SEO_DIR.mkdir(parents=True, exist_ok=True)
    GROWTH_DIR.mkdir(parents=True, exist_ok=True)
    (SEO_DIR / "README.md").write_text(
        "# Batch 03 — SEO Briefs (سكيل التحليل)\n\n"
        "ملف لكل مقال: `B3-XX-<slug>.md` — يُرفق ملخص في تذكرة `B3-XXN`.\n",
        encoding="utf-8",
    )
    (GROWTH_DIR / "README.md").write_text(
        "# Batch 03 — Internal Links (سكيل النمو)\n\n"
        "ملف لكل مقال: `B3-XX-<slug>.md` + `site-clusters-7sections.md`.\n",
        encoding="utf-8",
    )

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)

    by_col: dict[str, int] = {}
    for c in new_cards:
        by_col[c["col"]] = by_col.get(c["col"], 0) + 1
    print(f"Added batch-03 skill tickets: {len(new_cards)}")
    for col, n in sorted(by_col.items()):
        print(f"  {col}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
