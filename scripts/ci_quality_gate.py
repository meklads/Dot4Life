#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوابة جودة آلية لـ GitHub Actions — تُشغَّل تلقائياً عند كل push.
تستدعي amer_gate.py على كل ملف HTML تغيّر في مجلدات المحتوى، وعند أي FAIL:
  1. تحقن <meta name="robots" content="noindex,nofollow"> في الملف (عزل عن فهرسة جوجل فوراً، بلا انتظار دورة عامر).
  2. تضيف سجلاً في operating-system/quality-log.md و TEAM-BUS.md.
  3. تُخرج كود 1 (تفشل الـ Action ليظهر تنبيه أحمر في تبويب Actions على GitHub).
لا تحذف ولا تُرجع أي commit — هذا طبقة كشف وعزل سريعة فوق مراجعة عامر البشرية/المجدولة، لا بديل عنها.
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
import amer_gate  # noqa: E402

CONTENT_DIRS = (
    "blog/", "health/", "finance-wealth/", "real-estate/", "islamic-hajj-umrah/",
    "comparisons/", "featured-stories/", "peace-capsules/", "guides/", "fitness/",
    "travel/", "health-pregnancy/",
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAM_BUS = os.path.join(ROOT, "operating-system", "TEAM-BUS.md")
QUALITY_LOG = os.path.join(ROOT, "operating-system", "quality-log.md")

NOINDEX_TAG = '<meta name="robots" content="noindex,nofollow">'


def changed_html_files(before_sha, after_sha):
    if not before_sha or before_sha == "0000000000000000000000000000000000000000":
        # أول push على الفرع أو force-push بلا تاريخ سابق — افحص كل شيء في مجلدات المحتوى بدلاً من المقارنة
        out = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout
    else:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACM", before_sha, after_sha],
            cwd=ROOT, capture_output=True, text=True,
        ).stdout
    files = [f.strip() for f in out.splitlines() if f.strip().endswith(".html")]
    return [f for f in files if any(f.startswith(d) for d in CONTENT_DIRS)]


def already_noindexed(html):
    return "noindex" in html.lower()[:2000] or 'name="robots"' in html.lower()


def quarantine(fp):
    full = os.path.join(ROOT, fp)
    with open(full, encoding="utf-8") as f:
        html = f.read()
    if already_noindexed(html):
        return False
    if "<head>" in html:
        html = html.replace("<head>", f"<head>\n  {NOINDEX_TAG}", 1)
    elif "<head " in html:
        html = re.sub(r"(<head[^>]*>)", r"\1\n  " + NOINDEX_TAG, html, count=1)
    else:
        return False
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    before_sha = os.environ.get("GH_BEFORE_SHA", "")
    after_sha = os.environ.get("GH_AFTER_SHA", "HEAD")
    files = changed_html_files(before_sha, after_sha)
    if not files:
        print("لا ملفات HTML متأثرة في مجلدات المحتوى — لا فحص مطلوب.")
        return 0

    results = [amer_gate.run(os.path.join(ROOT, f)) for f in files]
    failed = [r for r in results if r["fails"]]

    if not failed:
        print(f"✅ بوابة CI: {len(files)} ملف، 0 فاشل.")
        return 0

    quarantined = []
    lines = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for r in failed:
        rel = os.path.relpath(r["file"], ROOT)
        did = quarantine(rel)
        if did:
            quarantined.append(rel)
        fails_str = " · ".join(r["fails"])
        lines.append(f"- `{rel}`: {fails_str}")
        print(f"❌ FAIL  {rel}")
        for f in r["fails"]:
            print(f"     {f}")

    note = (
        f"\n## {ts} — 🤖 بوابة CI الآلية رفضت {len(failed)} ملف عند push\n"
        f"تشغيل تلقائي لـ `scripts/amer_gate.py` على push (`scripts/ci_quality_gate.py`)، "
        f"قبل أي دورة عامر مجدولة. تمّ عزل الملفات الفاشلة فوراً (`noindex,nofollow`) "
        f"ريثما تُصلَح وتُعاد للبوابة:\n" + "\n".join(lines) + "\n"
    )

    with open(QUALITY_LOG, "a", encoding="utf-8") as f:
        f.write(note)

    bus_entry = (
        f"| {ts} | CI الآلي → Hermes/عامر | **🚨 بوابة CI رفضت {len(failed)} ملف عند push وعزلتها (noindex) فوراً.** "
        f"التفاصيل في `quality-log.md`. ملفات: " + "، ".join(f"`{os.path.relpath(r['file'], ROOT)}`" for r in failed) +
        " | 🆕 |\n"
    )
    with open(TEAM_BUS, encoding="utf-8") as f:
        bus = f.read()
    marker = "| الوقت | من → إلى | الرسالة | الحالة |\n|-------|----------|---------|--------|\n"
    if marker in bus:
        bus = bus.replace(marker, marker + bus_entry, 1)
    else:
        bus += "\n" + bus_entry
    with open(TEAM_BUS, "w", encoding="utf-8") as f:
        f.write(bus)

    print(f"\n🚨 الإجمالي: {len(failed)}/{len(files)} ملف فاشل. عُزل {len(quarantined)} ملف (noindex). "
          f"سُجِّل في quality-log.md و TEAM-BUS.md.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
