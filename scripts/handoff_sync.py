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
    "omar": "عمر",
    "claude": "كلود",
    "hema": "Hema",
    "cursor": "Cursor",
    "amer": "عامر",
    "member_done": "—",
    "done": "—",
}

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
}

HEMA_TASKS = {
    "T-02": "أعد REVISE في drafts/task09/ ثم ضعها في «انتهى من عندي»",
    "T-03": "وسّع 25 صفحة من hema-deepen-priority.md ثم «انتهى من عندي»",
    "T-04": "وسّع 10 صفحات DEEPEN تالية ثم «انتهى من عندي»",
}


def task_for(card: dict) -> str:
    col, stage, cid = card.get("col", "ghost"), card.get("stage", "backlog"), card.get("id", "")
    if col == "done":
        return "منتهي — على الموقع"
    if col == "member_done":
        who = card.get("owner", "العضو")
        return f"انتهى من جهة {who} — بانتظار المرحلة التالية"
    if col == "ghost":
        return "احتياط — دفعة قادمة"
    if col == "omar":
        return "جهّز برومبت الصورة وضعه pending — ثم انقلها لـ «انتهى من عندي»"
    if col == "claude":
        return "ولّد الصورة WebP 1200×750 (تحقق من برومبت عمر) — ثم «انتهى من عندي»"
    if col == "hema":
        return HEMA_TASKS.get(cid, "أكمل المطلوب — ثم «انتهى من عندي»")
    if col == "cursor":
        return "المرحلة 2 — Autopilot يبني بعد approved"
    if col == "amer":
        return "المرحلة 2 — BUILD VERIFY"
    return card.get("task", "")


def enrich_card(card: dict) -> dict:
    slug = card.get("slug", "")
    if not card.get("article"):
        card["article"] = ARTICLE_TITLES.get(slug, card.get("title", slug))
    card["assignee"] = card.get("owner") or ASSIGNEE.get(card.get("col", "ghost"), "—")
    if card.get("col") == "member_done" and card.get("owner"):
        card["assignee"] = card["owner"] + " (انتهى)"
    card["task"] = task_for(card)
    if card.get("col") not in ("done", "ghost") and not card.get("command"):
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
    if col == "omar":
        if card.get("stage") == "approve" or card.get("_prev_col") == "claude":
            return f"{cid}: راجع WebP → approved في الفهرس + approved/ — {slug}"
        return card.get("command") or f"{cid}: جهّز برومبت + pending في الفهرس — {slug}"
    if col == "claude":
        return f"{cid}: ولّد في Higgsfield → WebP 1200×750 → سلّم لعمر: hero-{slug}.webp"
    if col == "hema":
        return card.get("command") or f"{cid}: أكمل المسودة — {slug}"
    if col == "cursor":
        return f"{cid}: approved جاهز — Autopilot يبني؛ راقب team-board — {slug}"
    if col == "amer":
        return f"{cid}: BUILD VERIFY — hero + alt + G5 — {slug}"
    return card.get("command", "")


def advance_stage(card: dict, col: str, prev_col: str) -> str:
    if col == "ghost":
        return "backlog"
    if col == "omar":
        return "approve" if prev_col == "claude" else "prompt"
    if col == "claude":
        return "generate"
    if col == "hema":
        return card.get("stage", "revise")
    if col == "cursor":
        return "build"
    if col == "amer":
        return "verify"
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
            card["col"] = col
            card["stage"] = advance_stage(card, col, prev)
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
        else:
            parts.append(
                f"\n## {title} — {sub}\n\n| التذكرة | المقال | موجه لـ | المطلوب |\n|---------|--------|---------|----------|\n"
            )
        parts.append(_rows(cards, cid))
        parts.append("\n---\n")
    parts.append(
        "\n## تعليمات المرحلة 1\n\n"
        "1. كل عضو عنده 3 تذاكر في مربعه.\n"
        "2. يشتغل على راحته.\n"
        "3. لما يخلص ينقل التذكرة لـ **انتهى من عندي**.\n"
        "4. جوست يقول «ابدؤوا» — مو لازم يتابع كل تذكرة.\n"
        "5. المرحلة 2: نربط «انتهى من عندي» بالعضو التالي.\n"
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
