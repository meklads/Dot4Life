#!/usr/bin/env python3
"""
GSystem Autopilot — manifest approved → TECH_BUILD → push (no human GO).

Usage:
  python3 scripts/gsystem_autopilot.py           # build + notify
  python3 scripts/gsystem_autopilot.py --push    # + git commit/push
  python3 scripts/gsystem_autopilot.py --notify # inboxes only
  python3 scripts/gsystem_autopilot.py --desktop-notify
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "operating-system/.gsystem-state.json"
LOG = ROOT / "outputs/logs/gsystem-autopilot.log"
LEGEND_MARKER = "<!-- gsystem-autopilot-legend -->"

SKIP_DIRS = {"outputs", "node_modules", ".git", "scripts"}

LOG_LEGEND = """\
# سجل الأوتوبايلوت — كيف تقرأه
# GSystem Autopilot log — how to read

كل تشغيلة تبدأ بـ: === تشغيل جديد ===
Each run starts with: === new run ===

| السطر (English) | المعنى بالعربي |
|-----------------|----------------|
| slugs needing build: [] | لا مقالات تنتظر بناء — كل الصور المعتمدة على الموقع ✓ |
| slugs needing build: ['x'] | مقال/مقالات تحتاج حقن صورة البطل في HTML |
| SKIP slug: approved but file missing | معتمد في الفهرس لكن ملف WebP غير موجود في approved/ |
| WARN slug: no HTML pages found | لا توجد صفحة HTML لهذا المقال في الموقع |
| RUN scripts/... | يبني المقال من مسودة معتمدة |
| APPLY path/to/page.html | تم تحديث صورة البطل في هذه الصفحة |
| AUDIT PASS | فحص الجودة نجح — الموقع سليم |
| AUDIT FAIL | فحص الجودة فشل — راجع السطر التالي للتفاصيل |
| git: nothing to commit | لا تغييرات جديدة — لم يُرفع شيء على GitHub |
| git: pushed abc1234 | تم الرفع على GitHub بنجاح |
| ERROR: BUILD_MAP rebuild failed | فشل بناء المقال — راجع الأخطاء أعلاه |
| inboxes: ... | تم تحديث صناديق مهام الفريق (عمر، كلود، Hema، …) |

السطر الذي يبدأ بـ ↳ هو شرح عربي للسطر الذي قبله مباشرة.
Lines starting with ↳ explain the line above in Arabic.

---
"""


def _ts() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_log_legend() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists() or LEGEND_MARKER not in LOG.read_text(encoding="utf-8"):
        LOG.write_text(f"{LEGEND_MARKER}\n{LOG_LEGEND}", encoding="utf-8")


def log(msg: str, *, meaning: str | None = None) -> None:
    ts = _ts()
    line = f"[{ts}] {msg}"
    print(line)
    if meaning:
        print(f"  ↳ {meaning}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
        if meaning:
            f.write(f"[{ts}]   ↳ {meaning}\n")


def log_run_start() -> None:
    ts = _ts()
    banner = f"[{ts}] === تشغيل جديد / new run ==="
    print(banner)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(banner + "\n")


def load_build_map() -> list[dict]:
    spec = importlib.util.spec_from_file_location(
        "build", ROOT / "scripts/build-from-approved-draft.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BUILD_MAP


def slug_to_build_id() -> dict[str, str]:
    from image_manifest import article_slug_from_path

    out: dict[str, str] = {}
    for cfg in load_build_map():
        bid = cfg["id"]
        for key in ("out_ar", "out_en"):
            p = cfg.get(key)
            if p:
                out[article_slug_from_path(p)] = bid
    out["oman-property-roi"] = "A-07-2"
    return out


def html_pages_for_slug(slug: str) -> list[Path]:
    from image_manifest import article_slug_from_path

    found: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if article_slug_from_path(p) == slug:
            found.append(p)
    return sorted(set(found))


def page_has_approved_hero(path: Path, web_path: str) -> bool:
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<figure class="hero"><img[^>]+src="([^"]+)"', html)
    return bool(m and web_path in m.group(1))


def slugs_needing_build() -> list[str]:
    from image_manifest import (
        entries_by_slug,
        image_disk_path,
        image_web_path,
        is_approved,
        load_manifest,
    )

    need: list[str] = []
    for slug, e in entries_by_slug(load_manifest()).items():
        if not is_approved(e):
            continue
        if not image_disk_path(e).exists():
            log(
                f"SKIP {slug}: approved but file missing",
                meaning=f"تخطي {slug}: معتمد في الفهرس لكن ملف الصورة غير موجود في approved/",
            )
            continue
        web = image_web_path(e)
        pages = html_pages_for_slug(slug)
        if not pages:
            log(
                f"WARN {slug}: no HTML pages found",
                meaning=f"تحذير {slug}: لا توجد صفحة HTML لهذا المقال على الموقع",
            )
            continue
        if any(not page_has_approved_hero(p, web) for p in pages):
            need.append(slug)
    return need


def run_build_ids(ids: list[str]) -> bool:
    if not ids:
        return True
    cmd = [sys.executable, str(ROOT / "scripts/build-from-approved-draft.py"), *ids]
    log(
        "RUN " + " ".join(cmd),
        meaning="تشغيل سكربت بناء المقال من المسودة المعتمدة",
    )
    return subprocess.run(cmd, cwd=ROOT).returncode == 0


def run_apply_heroes() -> int:
    spec = importlib.util.spec_from_file_location(
        "apply", ROOT / "scripts/apply-approved-heroes.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    by = mod.entries_by_slug(mod.load_manifest())
    approved = {k: v for k, v in by.items() if mod.is_approved(v)}
    done = 0
    for sec in mod.SECTIONS:
        d = ROOT / sec
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.html")):
            slug = mod.article_slug_from_path(fp)
            if slug in approved and mod.apply_path(fp, approved[slug]):
                done += 1
                rel = fp.relative_to(ROOT)
                log(
                    f"APPLY {rel}",
                    meaning=f"تم تحديث صورة البطل في: {rel}",
                )
    return done


def git_push_if_changed(message: str) -> str | None:
    import glob as _glob
    import os as _os

    # 1) Self-heal: clear any stale lock files anywhere under .git
    for _lk in _glob.glob(str(ROOT / ".git/**/*.lock"), recursive=True):
        try:
            _os.remove(_lk)
        except OSError:
            pass
    # 2) Self-heal: ensure a git identity exists so `git commit` never dies with 128
    id_check = subprocess.run(
        ["git", "config", "user.email"], cwd=ROOT, capture_output=True, text=True
    )
    if not id_check.stdout.strip():
        subprocess.run(["git", "config", "user.name", "gsystem-bot"], cwd=ROOT, check=False)
        subprocess.run(
            ["git", "config", "user.email", "gsystem-bot@users.noreply.github.com"],
            cwd=ROOT,
            check=False,
        )

    st = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    if not st.stdout.strip():
        log(
            "git: nothing to commit",
            meaning="لا تغييرات جديدة — لم يُرفع شيء على GitHub (هذا طبيعي إذا كان كل شيء محدّثاً)",
        )
        return None
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=False)
    # exclude pycache from commit if picked up
    subprocess.run(["git", "reset", "HEAD", "--", "**/__pycache__"], cwd=ROOT, check=False)
    cm = subprocess.run(
        ["git", "commit", "-m", message], cwd=ROOT, capture_output=True, text=True
    )
    if cm.returncode != 0:
        # Tolerate commit failure (e.g. nothing staged / in-progress merge); try to push what exists
        log(
            "git: commit skipped",
            meaning="تعذّر الالتزام (قد يكون لا جديد أو دمج معلّق) — أحاول الدفع بما هو موجود: "
            + (cm.stderr or "").strip()[:120],
        )
    # 3) Self-heal non-fast-forward: integrate remote (merge, no editor) before pushing
    push = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    if push.returncode != 0:
        subprocess.run(
            ["git", "pull", "--no-rebase", "--no-edit", "origin", "main"], cwd=ROOT, check=False
        )
        push = subprocess.run(
            ["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True
        )
    if push.returncode != 0:
        log(
            "git: push failed",
            meaning="فشل الدفع بعد محاولة الدمج — يدوي مطلوب: " + (push.stderr or "").strip()[:140],
        )
        return None
    rev = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
    )
    short = rev.stdout.strip()
    log(
        f"git: pushed {short}",
        meaning=f"تم الرفع على GitHub بنجاح — رقم الالتزام: {short}",
    )
    return short


def run_autopilot(*, do_build: bool, do_push: bool) -> dict:
    ran_at = datetime.now().isoformat(timespec="seconds")
    result: dict = {
        "ran_at": ran_at,
        "built_slugs": [],
        "pages_built": 0,
        "commit": None,
        "summary": "",
    }

    if do_build:
        need = slugs_needing_build()
        if need:
            log(
                f"slugs needing build: {need}",
                meaning=f"مقالات تنتظر بناء/تحديث صورة البطل: {', '.join(need)}",
            )
        else:
            log(
                "slugs needing build: []",
                meaning="لا مقالات تنتظر بناء — كل الصور المعتمدة موجودة على الموقع ✓",
            )
        slug_ids = slug_to_build_id()
        build_ids: list[str] = []
        archive_slugs: list[str] = []
        for slug in need:
            if slug in slug_ids:
                bid = slug_ids[slug]
                if bid not in build_ids:
                    build_ids.append(bid)
            else:
                archive_slugs.append(slug)

        if build_ids:
            if not run_build_ids(build_ids):
                log(
                    "ERROR: BUILD_MAP rebuild failed",
                    meaning="فشل بناء المقال — راجع سطور RUN أعلاه للتفاصيل",
                )
            else:
                result["built_slugs"].extend(
                    [s for s in need if slug_ids.get(s) in build_ids]
                )

        still = slugs_needing_build()
        archive_still = [s for s in still if s not in slug_ids or slug_ids.get(s) not in build_ids]
        if archive_still:
            n = run_apply_heroes()
            result["pages_built"] = n
            for s in archive_still:
                if s not in result["built_slugs"]:
                    result["built_slugs"].append(s)

        audit = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build-from-approved-draft.py"), "--audit"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if audit.returncode != 0:
            tail = (audit.stdout or "")[-500:]
            log(f"AUDIT FAIL:\n{tail}")
            log(
                "AUDIT FAIL (summary)",
                meaning="فحص الجودة فشل — الموقع فيه مشكلة، راجع التفاصيل في السطر السابق",
            )
        else:
            log(
                "AUDIT PASS",
                meaning="فحص الجودة نجح — المقالات LIVE سليمة",
            )

        if do_push:
            result["commit"] = git_push_if_changed(
                "GSystem autopilot: apply manifest-approved heroes.\n"
            )

    result["summary"] = (
        f"built {len(result['built_slugs'])} slug(s)"
        + (f" · {result['commit']}" if result["commit"] else "")
    )
    return result


def main() -> None:
    notify_only = "--notify" in sys.argv
    do_push = "--push" in sys.argv
    desktop = "--desktop-notify" in sys.argv

    ensure_log_legend()

    if notify_only:
        from gsystem_notify import notify_new_tasks, write_inboxes

        log_run_start()
        write_inboxes({})
        from team_board_refresh import refresh_team_board
        from sync_gsystem_web import sync_all

        refresh_team_board({})
        sync_all()
        log(
            "inboxes only (no build)",
            meaning="تحديث صناديق المهام + لوحة الفريق — بدون بناء أو رفع",
        )
        print("Inboxes updated: operating-system/inbox/")
        return

    log_run_start()
    result = run_autopilot(do_build=not notify_only, do_push=do_push)

    sys.path.insert(0, str(ROOT / "scripts"))
    from gsystem_notify import notify_new_tasks, write_inboxes

    paths = write_inboxes(result)
    log(
        "inboxes: " + ", ".join(paths),
        meaning="تم تحديث صناديق مهام الفريق (عمر، كلود، Hema، عامر، Cursor، جوست)",
    )

    from team_board_refresh import refresh_team_board
    from sync_gsystem_web import sync_all

    refresh_team_board(result)
    sync_all()
    log(
        f"team-board refreshed",
        meaning="تم تحديث لوحة الفريق بالساعة والدقيقة — operating-system/team-board.md",
    )

    if desktop:
        notify_new_tasks(result)

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    state["last_autopilot"] = result
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(result["summary"])
    raise SystemExit(0)


if __name__ == "__main__":
    main()
