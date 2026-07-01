#!/usr/bin/env python3
"""رصد عامر للتجميد: يعترض ويبلّغ على أي مادة جديدة أثناء تجميد المحتوى.

القاعدة (جوست 2026-06-24): بعد Batch 03 لا مواد جديدة حتى تقليص DEEPEN ≤25.
عامر = طبقة اعتراض ثانية فوق قفل Cursor: لو تسرّبت مادة جديدة، يرفع علماً.

الاستخدام: python3 scripts/amer_freeze_watch.py
يطبع OBJECTION + قائمة المخالفات إن وُجدت، وكود خروج 1؛ وإلا OK وكود 0.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "operating-system/new-content-frozen.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
MANIFEST = ROOT / "assets/images/image-manifest.json"

# دفعات مسموحة دائماً (الاستثناء الوحيد): Batch 03 + DEEPEN/معالجة قصور
ALLOWED_PREFIXES = ("B3-", "DEEPEN", "AN-", "R-", "T-0", "fix-", "deepen-")
# علامات مادة جديدة ممنوعة أثناء التجميد
NEW_CONTENT_MARKERS = ("batch-04", "batch-05", "batch-06", "new-section",
                       "new-ghost-pool", "new-site-section")

# مجلدات المحتوى التي يُرصد فيها ظهور ملفات HTML غير متتبَّعة (اكتُشفت الثغرة 2026-07-01:
# الفحص القديم كان يفحص نصوص التذاكر/تقارير فقط، لا ملفات HTML فعلية جديدة على القرص)
CONTENT_DIRS = (
    "blog", "comparisons", "featured-stories", "finance-wealth", "health",
    "islamic-hajj-umrah", "peace-capsules", "real-estate", "guides", "cities",
    "travel", "fitness",
)


def _untracked_new_content_html() -> list[str]:
    """يرجع مسارات ملفات HTML غير متتبَّعة (?? في git status) داخل مجلدات المحتوى.

    هذا يصطاد بالضبط النمط المكتشف 2026-07-01: 16 ملف جديد ظهرت على القرص
    بلا أي تذكرة/تقرير يشير إليها — freeze_watch القديم لم يكن يراها إطلاقاً.
    """
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT, capture_output=True, text=True, timeout=15, check=False,
        ).stdout
    except Exception:
        return []
    found = []
    for line in out.splitlines():
        if not line.startswith("??"):
            continue
        path = line[3:].strip()
        if not path.endswith(".html"):
            continue
        top = path.split("/", 1)[0]
        if top in CONTENT_DIRS:
            found.append(path)
    return found


def _known_slugs() -> set[str]:
    """أي slug ظهر في مصادر معروفة (تذاكر/فهرس صور/DEEPEN/inbox) = مصرَّح به على الأرجح."""
    slugs: set[str] = set()
    tk = load_json(TICKETS) or {}
    for c in tk.get("cards", []):
        blob = json.dumps(c, ensure_ascii=False)
        slugs.add(blob)
    man = load_json(MANIFEST) or {}
    for e in man.get("entries", []) if isinstance(man, dict) else []:
        s = e.get("article_slug")
        if s:
            slugs.add(s)
    return slugs


def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    frozen = load_json(FROZEN)
    if not frozen or not frozen.get("frozen"):
        print("✅ المحتوى غير مجمّد — لا رصد.")
        return 0

    violations = []
    # 1) تذاكر تشير لدفعات/أقسام جديدة ممنوعة
    tk = load_json(TICKETS) or {}
    for c in tk.get("cards", []):
        blob = json.dumps(c, ensure_ascii=False).lower()
        cid = str(c.get("id", ""))
        if cid.startswith(ALLOWED_PREFIXES):
            continue
        for mk in NEW_CONTENT_MARKERS:
            if mk in blob:
                violations.append(f"تذكرة {cid or '?'}: تشير إلى «{mk}» (مادة جديدة ممنوعة)")
                break

    # 2) ملفات تقارير إطلاق دفعات جديدة (batch-04+ launch)
    for f in (ROOT / "operating-system/reports").glob("batch-0[4-9]*"):
        violations.append(f"ملف إطلاق دفعة جديدة: {f.name}")

    # 3) ملفات HTML جديدة غير متتبَّعة في مجلدات المحتوى بلا مصدر معروف (الثغرة المُصلَحة 2026-07-01)
    known = _known_slugs()
    for path in _untracked_new_content_html():
        slug = Path(path).stem
        for suf in ("-en", "-ar"):
            if slug.endswith(suf):
                slug = slug[: -len(suf)]
                break
        traced = any(slug in k for k in known)
        if not traced:
            violations.append(f"ملف HTML جديد غير متتبَّع بلا مصدر معروف: {path}")

    if violations:
        print("⛔ OBJECTION — عامر يعترض: مادة جديدة أثناء التجميد!")
        print(f"   الشرط: DEEPEN ≤ {frozen.get('unlock_when', {}).get('deepen_count_max', 25)} + جودة ≥ "
              f"{frozen.get('unlock_when', {}).get('quality_pct_min', 60)}% + أمر جوست صريح.")
        for v in violations:
            print(f"   - {v}")
        print("   → بلّغ جوست فوراً. الاستثناء الوحيد: Batch 03 + DEEPEN/معالجة القصور.")
        return 1

    print("✅ لا مخالفات — فقط Batch 03 + DEEPEN جارٍ. التجميد محترَم.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
