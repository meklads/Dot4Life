#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تدقيق بنيوي شامل لكل المقالات الحيّة — يُشغَّل أسبوعياً عبر GitHub Actions (مجاناً).
يفحص أن كل <aside class="article-sidebar"> طفلٌ مباشر لـ<div class="article-layout">
(أي أن السايدبار يظهر جنب المقال لا تحته). يستخدم html5lib (سلوك المتصفّح).

عند وجود أي مكسور: يسجّل في TEAM-BUS.md ويُخرج كود 1 (تنبيه أحمر في تبويب Actions).
هذه طبقة أمان دورية فوق بوابة CI اللحظية — تمسك أي عطل تسلّل أو ملف قديم لم يمرّ بالبوابة.
"""
import glob
import os
import sys
from datetime import datetime, timezone

import html5lib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAM_BUS = os.path.join(ROOT, "operating-system", "TEAM-BUS.md")
SKIP_PREFIXES = ("outputs/", "node_modules/", ".git/")


def sidebar_broken(html):
    if "article-sidebar" not in html:
        return None  # لا سايدبار — لا فحص
    doc = html5lib.parse(html, treebuilder="dom")
    asides = []

    def walk(n):
        for ch in n.childNodes:
            if ch.nodeType == 1:
                if "article-sidebar" in (ch.getAttribute("class") or ""):
                    asides.append(ch)
                walk(ch)

    walk(doc)
    if not asides:
        return None
    p = asides[0].parentNode
    if "article-layout" in (p.getAttribute("class") or ""):
        return None  # سليم
    pc = (p.getAttribute("class") or "").split(" ")[0] or p.tagName.lower()
    return f"{p.tagName.lower()}.{pc}"


def main():
    os.chdir(ROOT)
    broken = []
    total = 0
    for f in glob.glob("**/*.html", recursive=True):
        if any(f.startswith(p) for p in SKIP_PREFIXES):
            continue
        try:
            html = open(f, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if "article-sidebar" not in html:
            continue
        total += 1
        where = sidebar_broken(html)
        if where:
            broken.append((f, where))

    print(f"فحص بنيوي: {total} مقال بسايدبار، {len(broken)} مكسور.")
    if not broken:
        print("✅ كل المقالات الحيّة سليمة بنيوياً.")
        return 0

    for f, where in broken:
        print(f"❌ {f}  (السايدبار تحت <{where}>)")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = "\n".join(f"- `{f}`: السايدبار متعشّش تحت `<{w}>`" for f, w in broken)
    note = (
        f"| {ts} | تدقيق بنيوي أسبوعي → Hermes | "
        f"**🚨 التدقيق الأسبوعي وجد {len(broken)} مقال سايدباره مكسور (يظهر تحت المقال).** "
        f"أصلِحها فوراً (أولوية 0):\\n{lines} | 🆕 |\n"
    )
    try:
        with open(TEAM_BUS, encoding="utf-8") as fh:
            bus = fh.read()
        marker = "| الوقت | من → إلى | الرسالة | الحالة |\n|-------|----------|---------|--------|\n"
        bus = bus.replace(marker, marker + note, 1) if marker in bus else bus + "\n" + note
        with open(TEAM_BUS, "w", encoding="utf-8") as fh:
            fh.write(bus)
    except Exception as e:
        print(f"(تعذّر تحديث TEAM-BUS: {e})")

    return 1


if __name__ == "__main__":
    sys.exit(main())
