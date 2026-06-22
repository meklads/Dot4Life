#!/usr/bin/env python3
"""Refresh LIVE status block in operating-system/team-board.md (hour:minute)."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "operating-system/team-board.md"
STATE = ROOT / "operating-system/.gsystem-state.json"
LOG = ROOT / "outputs/logs/gsystem-autopilot.log"
MARK_START = "<!-- TEAM-BOARD-LIVE-START -->"
MARK_END = "<!-- TEAM-BOARD-LIVE-END -->"


def _hm(iso_or_dt: str | datetime) -> str:
    if isinstance(iso_or_dt, datetime):
        return iso_or_dt.strftime("%Y-%m-%d **%H:%M**")
    s = iso_or_dt.replace("T", " ")
    if len(s) >= 16:
        return f"{s[:10]} **{s[11:16]}**"
    return s


def deepen_count() -> int:
    p = ROOT / "operating-system/reports/quality-audit.csv"
    if not p.exists():
        return 0
    return sum(1 for r in csv.DictReader(p.open(encoding="utf-8-sig")) if "قصير" in r.get("المشاكل", ""))


def quality_pct() -> str:
    p = ROOT / "operating-system/reports/quality-audit.csv"
    if not p.exists():
        return "—"
    rows = list(csv.DictReader(p.open(encoding="utf-8-sig")))
    if not rows:
        return "—"
    ok = sum(1 for r in rows if not r.get("المشاكل", "").strip())
    return f"{ok}/{len(rows)} ({round(100 * ok / len(rows))}%)"


def last_git_event() -> tuple[str, str, str] | None:
    r = subprocess.run(
        ["git", "log", "-1", "--format=%ci|%h|%s"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        return None
    when, rev, subj = r.stdout.strip().split("|", 2)
    return _hm(when), rev, subj[:80]


def last_autopilot_block() -> list[str]:
    if not LOG.exists():
        return []
    lines = LOG.read_text(encoding="utf-8").splitlines()
    block: list[str] = []
    for line in reversed(lines):
        if "=== تشغيل جديد" in line or "=== new run" in line:
            block.append(line)
            break
        if line.startswith("[") and "↳" not in line:
            block.append(line)
    block.reverse()
    return block[-8:]


def slugs_needing_build() -> list[str]:
    sys.path.insert(0, str(ROOT / "scripts"))
    from image_manifest import (
        article_slug_from_path,
        entries_by_slug,
        image_disk_path,
        image_web_path,
        is_approved,
        load_manifest,
    )

    skip_dirs = {"outputs", "node_modules", ".git", "scripts"}

    def page_has_approved_hero(path: Path, web_path: str) -> bool:
        html = path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'<figure class="hero"><img[^>]+src="([^"]+)"', html)
        return bool(m and web_path in m.group(1))

    need: list[str] = []
    for slug, e in entries_by_slug(load_manifest()).items():
        if not is_approved(e) or not image_disk_path(e).exists():
            continue
        web = image_web_path(e)
        pages = [
            p
            for p in ROOT.rglob("*.html")
            if not any(part in skip_dirs for part in p.parts)
            and article_slug_from_path(p) == slug
        ]
        if pages and any(not page_has_approved_hero(p, web) for p in pages):
            need.append(slug)
    return need


def manifest_snapshot() -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    from image_manifest import entries_by_slug, image_disk_path, is_approved, load_manifest

    by = entries_by_slug(load_manifest())
    approved = [s for s, e in by.items() if is_approved(e)]
    pending_file = [
        s for s, e in by.items() if e.get("visual_director") == "pending" and image_disk_path(e).exists()
    ]
    approved_no_file = [
        s for s, e in by.items() if is_approved(e) and not image_disk_path(e).exists()
    ]
    not_approved = [s for s, e in by.items() if not is_approved(e)]
    return {
        "approved": approved,
        "pending_file": pending_file,
        "approved_no_file": approved_no_file,
        "not_approved_count": len(not_approved),
    }


def build_live_block(now: datetime, autopilot: dict | None = None) -> str:
    autopilot = autopilot or {}
    snap = manifest_snapshot()
    need_build = slugs_needing_build()
    ran_at = autopilot.get("ran_at")
    built = autopilot.get("built_slugs") or []
    commit = autopilot.get("commit")
    deepen = deepen_count()
    a09 = (ROOT / "operating-system/reports/drafts/task09").exists()

    done_rows: list[str] = []
    progress_rows: list[str] = []
    waiting_rows: list[str] = []

    if ran_at:
        t = _hm(ran_at)
        if built:
            done_rows.append(
                f"| {t} | بُنيت صور: {', '.join(f'`{s}`' for s in built)} | Cursor | autopilot |"
            )
        elif not need_build:
            done_rows.append(
                f"| {t} | فحص autopilot — كل الصور المعتمدة على الموقع | Cursor | log `[]` |"
            )
        if autopilot.get("summary"):
            audit_note = "AUDIT PASS" if not need_build else "يحتاج بناء"
            done_rows.append(
                f"| {t} | {autopilot.get('summary')} · {audit_note} | Cursor | autopilot |"
            )
        if commit:
            done_rows.append(f"| {t} | رفع GitHub `{commit}` | Cursor | origin/main |")

    git_ev = last_git_event()
    if git_ev and (not commit or git_ev[1] != commit):
        when, rev, subj = git_ev
        done_rows.append(f"| {when} | آخر commit `{rev}` | Cursor | {subj} |")

    if not done_rows:
        done_rows.append("| — | لا نشاط جديد منذ آخر تشغيل | — | — |")

    if need_build:
        t = _hm(ran_at) if ran_at else _hm(now)
        progress_rows.append(
            f"| {t} | حقن صور في HTML: {', '.join(f'`{s}`' for s in need_build)} | Cursor | BUILD_MAP / APPLY |"
        )

    if snap["pending_file"]:
        progress_rows.append(
            f"| {_hm(now)} | **{len(snap['pending_file'])}** صورة جاهزة — بانتظار `approved` | عمر | "
            + ", ".join(f"`{s}`" for s in snap["pending_file"][:5])
            + ("…" if len(snap["pending_file"]) > 5 else "")
            + " |"
        )

    if a09:
        progress_rows.append(
            "| — | A-09 REVISE — `drafts/task09/` | Hema | تسليم لعامر بعد draft-gate |"
        )

    if snap["approved"] and not need_build:
        progress_rows.append(
            f"| {_hm(now)} | BUILD VERIFY — **{len(snap['approved'])}** صور LIVE | عامر | hero + alt + G5 |"
        )

    if not progress_rows:
        progress_rows.append(
            f"| {_hm(now)} | لا مهمة نشطة — الحلقة تنتظر مدخلات جديدة | — | عمر/كلود دفعة 2 |"
        )

    waiting_rows.append(
        f"| عمر + كلود | صور Tier 1 دفعة 2 — **{snap['not_approved_count']}** slug بلا اعتماد | منذ ٢٢ يونيو |"
    )
    waiting_rows.append(
        f"| Hema | DEEPEN — **{deepen}** صفحة قصيرة | `hema-deepen-priority.md` |"
    )
    waiting_rows.append(
        "| Cursor | وضع النشر المستمر | بانتظار «فعّل» من جوست |"
    )
    if snap["approved_no_file"]:
        waiting_rows.append(
            f"| عمر | معتمد بلا ملف: {', '.join(f'`{s}`' for s in snap['approved_no_file'][:3])} | فوري |"
        )

    log_lines = last_autopilot_block()
    events = "\n".join(f"- `{ln}`" for ln in log_lines) if log_lines else "- *(لا سجل بعد)*"

    return f"""{MARK_START}
## 🕐 الحالة الآن — محدّث تلقائياً

**آخر تحديث:** {_hm(now)} · مصدر: autopilot + manifest + git

> **اقرأ هنا أولاً** — ثلاث حالات: **✅ تم** · **🔄 جاري** · **⏳ لسه**

| المقياس | القيمة |
|---------|--------|
| صور `approved` | **{len(snap['approved'])}** |
| تنتظر بناء HTML | **{len(need_build)}** |
| DEEPEN (قصير) | **{deepen}** |
| جودة الموقع | **{quality_pct()}** |
| آخر autopilot | {f"`{_hm(ran_at)}`" if ran_at else "—"} |

### ✅ تم — آخر ما اكتمل

| الوقت | ماذا | من | الدليل |
|-------|------|-----|--------|
{chr(10).join(done_rows)}

### 🔄 جاري العمل — الآن

| الوقت | ماذا | من | التالي |
|-------|------|-----|--------|
{chr(10).join(progress_rows)}

### ⏳ لسه — منتظر / مفتوح

| من | ماذا | ملاحظة |
|-----|------|--------|
{chr(10).join(waiting_rows)}

### 📎 آخر سطور الأوتوبايلوت

{events}

{MARK_END}"""


def refresh_team_board(autopilot_result: dict | None = None) -> Path:
    if not BOARD.exists():
        raise FileNotFoundError(BOARD)
    body = BOARD.read_text(encoding="utf-8")
    now = datetime.now()
    live = build_live_block(now, autopilot_result)

    if MARK_START in body and MARK_END in body:
        pre, rest = body.split(MARK_START, 1)
        _, post = rest.split(MARK_END, 1)
        new_body = pre.rstrip() + "\n\n" + live + "\n" + post.lstrip("\n")
    else:
        parts = body.split("---", 1)
        if len(parts) == 2:
            new_body = parts[0] + "---\n\n" + live + "\n\n" + parts[1].lstrip("\n")
        else:
            new_body = live + "\n\n" + body

    BOARD.write_text(new_body, encoding="utf-8")

    from sync_gsystem_web import sync_all

    sync_all()

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    state["team_board_refresh_at"] = now.isoformat(timespec="seconds")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return BOARD


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    ap = state.get("last_autopilot")
    path = refresh_team_board(ap)
    print(f"Refreshed {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
