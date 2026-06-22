#!/usr/bin/env python3
"""Sync handoff-tickets.json ↔ handoff-board.md + web export."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TICKETS = ROOT / "operating-system/handoff-tickets.json"
BOARD_MD = ROOT / "operating-system/handoff-board.md"
WEB_OUT = ROOT / "system/gsystem-data/handoff-tickets.json"

STAGE_LABEL = {
    "backlog": "في الانتظار",
    "waiting": "انتظار الفريق",
    "prompt": "برومبت",
    "generate": "توليد",
    "approve": "اعتماد WebP",
    "build": "بناء HTML",
    "verify": "تحقق",
    "revise": "REVISE",
    "done": "LIVE",
}

ASSIGNEE = {
    "ghost": "جوست",
    "hema": "Hema",
    "cursor": "Cursor",
    "member_done": "—",
    "done": "—",
}

SKILL_LABELS = {
    "omar": "Hema · سكيل عمر",
    "moni": "Hema · سكيل Moni",
    "amer": "Hema · سكيل عامر",
    "ruwaq": "Hema · سكيل Ruwaq",
}

SKILL_ALIASES = {"omar", "amer", "moni", "ruwaq", "hema"}

AGENT = "Hema"

ARTICLE_TITLES: dict[str, str] = {
    "investment-basics-beginners": "استثمار للمبتدئين",
    "rent-vs-buy-gulf-family": "إيجار أم تملّك للعائلة الخليجية",
    "daily-walking-benefits": "فوائد المشي اليومي",
    "pregnancy-week-by-week": "الحمل أسبوع بأسبوع",
    "preconception-checkups": "فحوصات ما قبل الحمل",
    "umrah-with-kids": "العمرة مع الأطفال",
    "hijri-new-year-children": "رأس السنة الهجرية والأطفال",
    "teaching-children-allah-names": "تعليم أسماء الله للأطفال",
    "teaching-children-prayer-with-love": "تعليم الصلاة بالحب",
    "jeddah-mortgage-calculator": "حاسبة تمويل جدة",
    "family-budget-plan": "خطة ميزانية العائلة",
    "bmi-calculator-women": "حاسبة BMI للنساء",
    "daily-adhkar-family-guide": "أذكار يومية للعائلة",
    "children-sleep-summer": "نوم الأطفال في الصيف",
    "family-friendly-activities-gulf-cities": "أنشطة عائلية في مدن الخليج",
    "best-family-destinations-gulf": "أفضل وجهات عائلية في الخليج",
    "A-09": "مسودة A-09",
    "deepen-priority-25": "DEEPEN — أولوية 25 صفحة",
    "deepen-priority-next-10": "DEEPEN — 10 صفحات تالية",
    "pregnancy-nutrition-first-trimester": "تغذية الحمل — الثلث الأول",
    "end-of-service-saudi": "مكافأة نهاية الخدمة",
    "family-time-management": "إدارة وقت العائلة",
    "saving-for-education-gulf": "ادخار التعليم للأطفال",
    "family-budget-planning-guide": "دليل ميزانية الأسرة",
    "gold-vs-savings-account-comparison": "ذهب vs حساب ادخار",
    "managing-screen-time-children": "وقت الشاشة للأطفال",
    "build-track-b-approved-thin": "BUILD — investment + rent-vs-buy thin",
    "schema-batch-1": "C-F3 Schema — دفعة 1",
    "schema-batch-2": "C-F3 Schema — دفعة 2",
    "redirect-rent-vs-buy-saudi": "301 rent-vs-buy-saudi",
    "hero-webp-batch-d4l1": "C-F6 استبدال d4l1.webp",
    "credibility-gate-blog": "بوابة مصداقية blog",
    "quality-adsense-readiness": "تقرير جودة AdSense",
}

HEMA_TASKS = {
    "T-02": "أعد REVISE في drafts/task09/ ثم ضعها في «انتهى من عندي»",
    "T-03": "DEEPEN الـ15 في hema-deepen-t03-blog-triage-15.txt — draft-gate — ثم «انتهى من عندي»",
    "T-04": "DEEPEN الـ7 في hema-deepen-t04-thin-7.txt — draft-gate — ثم «انتهى من عندي»",
}

CURSOR_TASKS = {
    "C-01": "ابدأ لما H-07..H-09 في «انتهى من عندي»: approved → HTML → push LIVE → ثم «انتهى من عندي»",
    "C-02": "ابدأ لما H-10..H-12 في «انتهى من عندي»: approved → HTML → push LIVE → ثم «انتهى من عندي»",
    "C-03": "ابدأ لما T-02..T-04 في «انتهى من عندي»: دمج مسودات → build → push LIVE → ثم «انتهى من عندي»",
    "C-04": "BUILD Track B thin (4 URLs معتمدة) → Schema → push → «انتهى من عندي»",
    "C-05": "C-F3 Schema دفعة 1 (20 blog) → verify → «انتهى من عندي»",
    "C-06": "C-F3 Schema دفعة 2 (20 blog) → verify → «انتهى من عندي»",
    "C-07": "301 rent-vs-buy-saudi duplicate → push → «انتهى من عندي»",
    "C-08": "استبدال d4l1.webp (20 صفحة) → push → «انتهى من عندي»",
    "C-09": "بوابة مصداقية blog → push → «انتهى من عندي»",
    "C-10": "تقرير جودة % + AdSense readiness → Ghost → «انتهى من عندي»",
}

CURSOR_COMMANDS = {
    "C-01": "C-01: Autopilot — H-07,H-08,H-09 approved → HTML → git push",
    "C-02": "C-02: Autopilot — H-10,H-11,H-12 approved → HTML → git push",
    "C-03": "C-03: دمج T-02,T-03,T-04 → build → git push",
    "C-04": "C-04: inject Track B thin LIVE (investment+rent-vs-buy ×4) → Schema → push",
    "C-05": "C-05: inject-article-schema.py batch 1 (20 blog) → verify JSON-LD",
    "C-06": "C-06: inject-article-schema.py batch 2 (20 blog) → verify JSON-LD",
    "C-07": "C-07: 301 blog/rent-vs-buy-saudi → real-estate/rent-vs-buy-gulf-family",
    "C-08": "C-08: replace d4l1.webp heroes (20 pages) from approved manifest",
    "C-09": "C-09: credibility gate — fabricated callouts + unverified stats sweep",
    "C-10": "C-10: quality audit CSV + AdSense readiness % → Ghost report",
}

GHOST_POOL = {
    "omar": "Hema · سكيل عمر",
    "amer": "Hema · سكيل عامر",
    "hema": "Hema · سكيل Moni",
    "moni": "Hema · سكيل Moni",
    "cursor": "Cursor · بناء",
}


def infer_skill(card: dict) -> str:
    if card.get("skill"):
        return card["skill"]
    pool = card.get("pool_for", "")
    if pool == "hema":
        return "moni"
    if pool in SKILL_LABELS:
        return pool
    cid = card.get("id", "")
    if cid.startswith("T-"):
        return "moni"
    if card.get("stage") == "generate":
        return "amer"
    if cid.startswith("H-"):
        return "omar"
    return "moni"


def skill_label(card: dict) -> str:
    return SKILL_LABELS.get(infer_skill(card), AGENT)


def normalize_col(col: str, card: dict) -> str:
    if col in SKILL_ALIASES or col in ("omar", "amer"):
        card["skill"] = "moni" if col in ("hema", "moni") else col
        return "hema"
    if col == "hema" and not card.get("skill"):
        card["skill"] = infer_skill(card)
    return col


def task_for(card: dict) -> str:
    col, stage, cid = card.get("col", "ghost"), card.get("stage", "backlog"), card.get("id", "")
    if col == "done":
        return "منتهي — على الموقع"
    if col == "member_done":
        return f"انتهى — {skill_label(card)} — بانتظار المرحلة التالية"
    if col == "ghost":
        pool = card.get("pool_for", "")
        label = GHOST_POOL.get(pool, "مخزون")
        reason = card.get("reason", "")
        return f"مخزون جوست — {label}" + (f" · {reason}" if reason else "")
    if col == "hema":
        sk = infer_skill(card)
        if sk == "omar":
            return "جهّز برومبت الصورة وضعه pending — ثم «انتهى من عندي»"
        if sk == "amer":
            return "ولّد الصورة WebP 1200×750 — ثم «انتهى من عندي»"
        return HEMA_TASKS.get(cid, "DEEPEN/كتابة — draft-gate — ثم «انتهى من عندي»")
    if col == "cursor":
        return CURSOR_TASKS.get(cid, "بناء ونشر — ثم «انتهى من عندي»")
    return card.get("task", "")



def enrich_card(card: dict) -> dict:
    slug = card.get("slug", "")
    if card.get("col") in ("omar", "amer"):
        card["skill"] = infer_skill(card)
        card["col"] = "hema"
    if card.get("col") == "hema" and not card.get("skill"):
        card["skill"] = infer_skill(card)
    if not card.get("article"):
        card["article"] = ARTICLE_TITLES.get(slug, card.get("title", slug))
    if card.get("col") in ("hema", "member_done") and card.get("skill"):
        card["owner"] = AGENT
        lbl = skill_label(card)
        card["assignee"] = lbl + (" (انتهى)" if card.get("col") == "member_done" else "")
    elif card.get("col") == "ghost" and card.get("pool_for"):
        card["assignee"] = GHOST_POOL.get(card["pool_for"], "جوست")
    else:
        card["assignee"] = card.get("owner") or ASSIGNEE.get(card.get("col", "ghost"), "—")
    card["task"] = task_for(card)
    if card.get("col") not in ("done", "ghost", "member_done") and not card.get("command"):
        card["command"] = command_for(card, card["col"])
    return card



def enrich_all(data: dict) -> dict:
    for card in data.get("cards", []):
        enrich_card(card)
    return data


def load() -> dict:
    return json.loads(TICKETS.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_for(card: dict, col: str) -> str:
    cid, slug = card["id"], card.get("slug", "")
    sk = infer_skill(card) if col == "hema" else ""
    if col == "hema" and sk == "omar":
        if card.get("stage") == "approve":
            return f"{cid}: راجع WebP → approved في الفهرس + approved/ — {slug}"
        return card.get("command") or f"{cid}: جهّز برومبت + pending في الفهرس — {slug}"
    if col == "hema" and sk == "amer":
        return f"{cid}: ولّد في Higgsfield → WebP 1200×750 → hero-{slug}.webp"
    if col == "hema":
        return card.get("command") or f"{cid}: أكمل المسودة — {slug}"
    if col == "cursor":
        return CURSOR_COMMANDS.get(cid, f"{cid}: approved جاهز — Autopilot يبني — {slug}")
    return card.get("command", "")



def advance_stage(card: dict, col: str, prev_col: str) -> str:
    if col == "ghost":
        return "backlog"
    if col == "hema":
        sk = infer_skill(card)
        if sk == "omar":
            return "approve" if card.get("stage") == "approve" else "prompt"
        if sk == "amer":
            return "generate"
        return card.get("stage", "revise")
    if col == "cursor":
        return "build" if prev_col == "cursor" else card.get("stage", "waiting")
    if col == "member_done":
        return "member_complete"
    if col == "done":
        return "done"
    return card.get("stage", "backlog")



def move_card(data: dict, card_id: str, col: str) -> dict | None:
    for card in data["cards"]:
        if card["id"] == card_id:
            prev = card.get("col", "ghost")
            card["_prev_col"] = prev
            col = normalize_col(col, card)
            card["col"] = col
            card["stage"] = advance_stage(card, col, prev)
            if prev == "ghost" and col == "hema":
                card["owner"] = AGENT
            if col not in ("done", "ghost", "member_done"):
                card["command"] = command_for(card, col)
            if col in ("done", "member_done"):
                if col == "done":
                    card["finished"] = datetime.now().strftime("%Y-%m-%d")
                card["command"] = ""
            card.pop("_prev_col", None)
            enrich_card(card)
            return card
    return None



def _esc(s: str) -> str:
    return (s or "").replace("|", "\\|")


def _rows(cards: list[dict], col: str) -> str:
    active = [c for c in cards if c.get("col") == col]
    if not active:
        return "| — | — | — | — |\n"
    lines: list[str] = []
    for c in active:
        if col == "done":
            lines.append(f"| {c['id']} | {c.get('article', '')} | {c.get('finished', '—')} |")
        else:
            lines.append(
                f"| {c['id']} | {c.get('article', '')} | {c.get('assignee', '')} | {c.get('task', '')} |"
            )
    return "\n".join(lines) + "\n"


def render_board_md(data: dict) -> str:
    cards = data["cards"]
    updated = data.get("updated", "")
    phase = data.get("phase", 1)
    rules = data.get("rules", "")
    parts = [
        f"# لوحة التسليم — المرحلة {phase}\n",
        f"> {rules}\n",
        f"> الواجهة: `system/board.html` → التسليم (Trello)\n",
        f"> آخر مزامنة: {updated}\n",
        "\n---\n",
    ]
    for col in data.get("columns", []):
        cid = col["id"]
        title = col.get("title", cid)
        sub = col.get("subtitle", "")
        if cid == "done":
            parts.append(f"\n## {title}\n\n| التذكرة | المقال | انتهى |\n|---------|--------|-------|\n")
        elif cid == "ghost":
            parts.append(
                f"\n## {title} — {sub}\n\n"
                f"| التذكرة | المقال | المسار | السبب |\n|---------|--------|--------|-------|\n"
            )
            active = [c for c in cards if c.get("col") == cid]
            if not active:
                parts.append("| — | — | — | — |\n")
            else:
                for c in active:
                    parts.append(
                        f"| {c['id']} | {c.get('article', '')} | "
                        f"{GHOST_POOL.get(c.get('pool_for', ''), '—')} | {c.get('reason', '—')} |\n"
                    )
            parts.append("\n---\n")
            continue
        else:
            parts.append(
                f"\n## {title} — {sub}\n\n| التذكرة | المقال | موجه لـ | المطلوب |\n|---------|--------|---------|----------|\n"
            )
        parts.append(_rows(cards, cid))
        parts.append("\n---\n")
    parts.append(
        "\n## تعليمات المرحلة 1\n\n"
        "1. كل عضو عنده **3 نشطة** + **7 مخزون** عند جوست.\n"
        "2. يشتغل على راحته.\n"
        "3. لما يخلص ينقل التذكرة لـ **انتهى من عندي**.\n"
        "4. جوست يقول «ابدؤوا» أو «وزّع 3 لـ عمر» من المخزون.\n"
        "5. **Cursor** يبني بعد الفريق — C-F3/C-F6/Track B للجودة وAdSense.\n"
        "6. بعد 10 → دفعة جديدة 10 حسب أولوية المنصة.\n"
    )
    return "".join(parts)


def export_web(data: dict | None = None) -> None:
    data = data or load()
    WEB_OUT.parent.mkdir(parents=True, exist_ok=True)
    WEB_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_all(write_md: bool = True) -> dict:
    data = enrich_all(load())
    save(data)
    if write_md:
        BOARD_MD.write_text(render_board_md(data), encoding="utf-8")
    export_web(data)
    return {"cards": len(data["cards"]), "updated": data.get("updated")}


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="Sync handoff tickets")
    p.add_argument("--no-md", action="store_true")
    args = p.parse_args()
    print(json.dumps(sync_all(write_md=not args.no_md), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
