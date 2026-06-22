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
            lines.append(f"| {c['id']} | `{c.get('slug', '')}` | {c.get('finished', '—')} |")
        elif col == "ghost":
            lines.append(
                f"| {c['id']} | `{c.get('slug', '')}` | {c.get('title', '')} | {_esc(c.get('command', ''))} |"
            )
        else:
            note = STAGE_LABEL.get(c.get("stage", ""), c.get("stage", ""))
            lines.append(
                f"| {c['id']} | `{c.get('slug', '')}` | {note} | {_esc(c.get('command', ''))} |"
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

| ID | slug | المهمة | أمر عند التسليم |
|----|------|--------|------------------|
{_rows(cards, "ghost")}
---

## 🎨 عند عمر

| ID | slug | حالة | أمر |
|----|------|------|-----|
{_rows(cards, "omar")}
---

## 🤖 عند كلود — توليد Higgsfield

| ID | slug | حالة | أمر |
|----|------|------|-----|
{_rows(cards, "claude")}
---

## ✍️ عند Hema — نص

| ID | slug | حالة | أمر |
|----|------|------|-----|
{_rows(cards, "hema")}
---

## ⚙️ عند Cursor — بناء

| ID | slug | حالة | ملاحظة |
|----|------|------|--------|
{_rows(cards, "cursor")}
---

## 🛡️ عند عامر — BUILD VERIFY

| ID | slug | حالة | أمر |
|----|------|------|-----|
{_rows(cards, "amer")}
---

## ✅ منتهي

| ID | slug | انتهى |
|----|------|-------|
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
    data = load()
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
