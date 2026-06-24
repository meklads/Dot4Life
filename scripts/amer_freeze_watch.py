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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "operating-system/new-content-frozen.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"

# دفعات مسموحة دائماً (الاستثناء الوحيد): Batch 03 + DEEPEN/معالجة قصور
ALLOWED_PREFIXES = ("B3-", "DEEPEN", "AN-", "R-", "T-0", "fix-", "deepen-")
# علامات مادة جديدة ممنوعة أثناء التجميد
NEW_CONTENT_MARKERS = ("batch-04", "batch-05", "batch-06", "new-section",
                       "new-ghost-pool", "new-site-section")


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
