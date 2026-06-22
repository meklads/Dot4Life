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
}


def task_for(card: dict) -> str:
    col, stage = card.get("col", "ghost"), card.get("stage", "backlog")
    if col == "done":
        return "منتهي — على الموقع"
    if col == "ghost":
        return "بانتظار قرار جوست — متى تُسلَّم للفريق"
    if col == "omar" and stage == "approve":
        return "راجع الصورة وضعها approved في الفهرس ومجلد approved"
    if col == "omar":
        return "جهّز برومبت الصورة الرئيسية وضعه pending في الفهرس"
    if col == "claude":
        return "ولّد الصورة في Higgsfield WebP 1200×750 وسلّم الملف لعمر"
    if col == "cursor":
        return "تأكد Autopilot بنى الصورة على صفحات المقال"
    if col == "amer":
        return "تحقق: hero + alt + G5 على الموقع"
    if col == "hema":
        return card.get("task") or "أكمل المسودة وأرسل لعامر"
    return card.get("task", "")


def enrich_card(card: dict) -> dict:
    slug = card.get("slug", "")
    if not card.get("article"):
        card["article"] = ARTICLE_TITLES.get(slug, card.get("title", slug))
    card["assignee"] = ASSIGNEE.get(card.get("col", "ghost"), "—")
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
            if col not in ("done", "ghost"):
                card["command"] = command_for(card, col)
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
    return f"""# 👑 لوحة التسليم — Handoff Board (Trello لجوست)

> **أنت = الـ Hub.** عمود = عضو · لما يقول «انتهيت» → انقل البطاقة · انسخ الأمر.
> **الواجهة البصرية:** `system/board.html` → **🔀 التسليم (Trello)**
> **المصدر:** `handoff-tickets.json` · آخر مزامنة: {updated}

---

## 📋 عند جوست — ابدأ من هنا

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "ghost")}
---

## 🎨 عند عمر

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "omar")}
---

## 🤖 عند كلود — توليد Higgsfield

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "claude")}
---

## ✍️ عند Hema — نص

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "hema")}
---

## ⚙️ عند Cursor — بناء

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "cursor")}
---

## 🛡️ عند عامر — BUILD VERIFY

| التذكرة | المقال | موجه لـ | المطلوب |
|---------|--------|---------|---------|
{_rows(cards, "amer")}
---

## ✅ منتهي

| التذكرة | المقال | انتهى |
|---------|--------|-------|
{_rows(cards, "done")}
---

## مسار الصورة

```
جوست → عمر (برومبت) → كلود → عمر (اعتماد) → Cursor → عامر → ✅
```

## ثبّت التسليم

```bash
python3 scripts/handoff_move.py H-07 omar
```
"""


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
