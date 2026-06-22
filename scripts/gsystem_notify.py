#!/usr/bin/env python3
"""GSystem team inboxes — periodic task alerts per lane owner."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "operating-system/inbox"
STATE = ROOT / "operating-system/.gsystem-state.json"
MANIFEST = ROOT / "assets/images/image-manifest.json"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deepen_count() -> int:
    p = ROOT / "operating-system/reports/quality-audit.csv"
    if not p.exists():
        return 0
    n = 0
    for r in csv.DictReader(p.open(encoding="utf-8-sig")):
        if "قصير" in r.get("المشاكل", ""):
            n += 1
    return n


def build_inboxes(autopilot_result: dict | None = None) -> dict[str, str]:
    from image_manifest import entries_by_slug, image_disk_path, is_approved, load_manifest

    autopilot_result = autopilot_result or {}
    manifest = load_manifest()
    by = entries_by_slug(manifest)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    approved_no_file = []
    pending_with_file = []
    approved_need_verify = autopilot_result.get("built_slugs", [])

    for slug, e in by.items():
        st = e.get("visual_director", "missing")
        disk = image_disk_path(e)
        if st == "approved" and not disk.exists():
            approved_no_file.append(slug)
        if st == "pending" and disk.exists():
            pending_with_file.append(slug)

    omar_lines = [
        f"# 📬 عمر — مهام الصور · {now}",
        "",
        "## 🔴 عاجل",
    ]
    if pending_with_file:
        omar_lines.append(f"- **{len(pending_with_file)}** صورة جاهزة بانتظار `approved` في الفهرس:")
        for s in pending_with_file[:10]:
            omar_lines.append(f"  - `{s}`")
    else:
        omar_lines.append("- لا شيء عاجل (ملف بلا approved).")

    omar_lines += ["", "## 📋 التالي (بلا صورة بعد)", "- راجع `omar-image-production.md` و`list-image-pending.py`"]

    claude_lines = [
        f"# 📬 كلود — توليد Higgsfield · {now}",
        "",
        "## مهام",
        "- توليد صور للـ slugs التي يجهّزها عمر برومبتات",
        f"- **{len([s for s, e in by.items() if e.get('visual_director') != 'approved'])}** slug بلا اعتماد نهائي في الفهرس",
        "- بعد التوليد: عمر يضع WebP في `approved/` ويحدّث الفهرس",
    ]

    hema_lines = [
        f"# 📬 Hema — كتابة · {now}",
        "",
        f"## DEEPEN · **{deepen_count()}** صفحة قصيرة",
        "- طابور: `hema-deepen-priority.md`",
        "- بوابة: `scripts/draft-gate.py` قبل التسليم لعامر",
    ]
    a09 = ROOT / "operating-system/reports/drafts/task09"
    if a09.exists():
        hema_lines.append("- **A-09** REVISE — راجع `drafts/task09/`")

    amer_lines = [
        f"# 📬 عامر — BUILD VERIFY · {now}",
        "",
    ]
    if approved_need_verify:
        amer_lines.append(f"## ✅ يحتاج تحقّق بعد بناء Cursor ({len(approved_need_verify)})")
        for s in approved_need_verify:
            amer_lines.append(f"- `{s}` — تحقّق hero + alt + G5")
    else:
        amer_lines.append("## لا دفعة بناء جديدة منذ آخر تشغيل")
    amer_lines += ["", "- جودة: `python3 scripts/quality-audit.py`"]

    cursor_lines = [
        f"# 📬 Cursor — أوتوبايلوت · {now}",
        "",
        f"- آخر تشغيل: {autopilot_result.get('ran_at', '—')}",
        f"- صفحات بُنيت: **{autopilot_result.get('pages_built', 0)}**",
        f"- push: {autopilot_result.get('commit', '—')}",
        "- القاعدة: `approved` + ملف → بناء فوري بدون سؤال جوست",
    ]

    ghost_lines = [
        f"# 📬 جوست — ملخص · {now}",
        "",
        f"- صور معتمدة في الفهرس: **{sum(1 for e in by.values() if is_approved(e))}**",
        f"- DEEPEN (قصير): **{deepen_count()}**",
        f"- آخر autopilot: {autopilot_result.get('summary', 'لم يُشغَّل')}",
        "- تقارير: `operating-system/reports/ghost/`",
    ]

    boxes = {
        "omar": "\n".join(omar_lines) + "\n",
        "claude": "\n".join(claude_lines) + "\n",
        "hema": "\n".join(hema_lines) + "\n",
        "amer": "\n".join(amer_lines) + "\n",
        "cursor": "\n".join(cursor_lines) + "\n",
        "ghost": "\n".join(ghost_lines) + "\n",
    }
    return boxes


def write_inboxes(autopilot_result: dict | None = None) -> list[str]:
    INBOX.mkdir(parents=True, exist_ok=True)
    boxes = build_inboxes(autopilot_result)
    written: list[str] = []
    for name, body in boxes.items():
        path = INBOX / f"{name}.md"
        path.write_text(body, encoding="utf-8")
        written.append(str(path.relative_to(ROOT)))
    return written


def desktop_notify(title: str, message: str) -> None:
    import platform
    import subprocess

    if platform.system() != "Darwin":
        return
    safe_t = title.replace('"', "'")[:60]
    safe_m = message.replace('"', "'")[:200]
    subprocess.run(
        ["osascript", "-e", f'display notification "{safe_m}" with title "{safe_t}"'],
        check=False,
    )


def notify_new_tasks(autopilot_result: dict) -> None:
    state = load_state()
    prev = set(state.get("last_alert_keys", []))
    keys: list[str] = []
    alerts: list[tuple[str, str, str]] = []

    for slug in autopilot_result.get("built_slugs", []):
        k = f"built:{slug}"
        keys.append(k)
        if k not in prev:
            alerts.append(("Cursor", f"بُني: {slug}", "GSystem Autopilot"))

    from image_manifest import entries_by_slug, image_disk_path, load_manifest

    for slug, e in entries_by_slug(load_manifest()).items():
        if e.get("visual_director") == "pending" and image_disk_path(e).exists():
            k = f"omar-approve:{slug}"
            keys.append(k)
            if k not in prev:
                alerts.append(("عمر", f"اعتمد في الفهرس: {slug}", "GSystem"))

    state["last_alert_keys"] = keys
    state["last_notify_at"] = datetime.now().isoformat(timespec="seconds")
    save_state(state)

    for title, msg, sub in alerts:
        desktop_notify(f"{sub} — {title}", msg)
