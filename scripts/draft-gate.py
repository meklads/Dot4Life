#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوابة المسوّدات — يشغّلها Hema قبل تسليم أي مسوّدة لعامر.
fail-closed: إن سقط أي بند، تخرج بكود ≠0 ولا تُعتبر المسوّدة جاهزة.
الاستخدام:
  python3 scripts/draft-gate.py operating-system/reports/drafts/task10/*.md
  python3 scripts/draft-gate.py --task 10
المبدأ نفسه المطبّق على بناء Cursor: امنع العيب قبل التسليم، لا بعده.
"""
import re, sys, glob, os

SENSITIVE_HINT = re.compile(
    r"(صحة|طبي|حمل|تغذية|دواء|مال|استثمار|ميزانية|راتب|تقاعد|زكاة|صلاة|عمرة|حج|أذكار|فتوى"
    r"|health|medical|pregnan|nutrition|financ|invest|budget|salary|prayer|umrah|hajj|islam)", re.I)
DISCLAIMER = re.compile(
    r"(إخلاء|ليست\s+استشارة|ليست\s+فتوى|معلومات\s+عامة|راجع\s+(?:طبيب|مختص|أهل\s+العلم)"
    r"|disclaimer|not\s+(?:medical|financial|professional)\s+advice|not\s+a\s+fatwa|consult)", re.I)
CLICHE = ["في الختام", "علاوة على ذلك", "تجدر الإشارة", "في عالمنا السريع",
          "أصبح أولوية لكل عائلة", "في عصرنا الحالي",
          "in conclusion", "moreover,", "in today's fast"]


def prose_words(t):
    t = re.sub(r"(?m)^\s*\|.*$", "", t)          # احذف صفوف الجداول
    t = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", t)    # احذف الروابط
    t = re.sub(r"[#*>`]", " ", t)
    return len([w for w in re.split(r"\s+", t) if w.strip()])


def gate(fp):
    t = open(fp, encoding="utf-8", errors="ignore").read()
    fails = []
    w = prose_words(t)
    if w < 1200:
        fails.append(f"كلمات={w} <1200")
    em = t.count("—")
    if em:
        fails.append(f"شرطات طويلة={em} (يجب 0)")
    src = len(re.findall(r"\]\(https?://", t))
    if src < 2:
        fails.append(f"مصادر بروابط={src} <2")
    q = len(re.findall(r"\?|؟", t))
    if q < 4:
        fails.append(f"أسئلة FAQ تقديري={q} <4")
    h2 = len(re.findall(r"(?m)^##\s", t))
    if h2 < 6:
        fails.append(f"H2={h2} <6")
    table = bool(re.search(r"(?m)^\s*\|", t))
    listy = len(re.findall(r"(?m)^\s*([-*]|[0-9]+[\).])\s", t))
    if not table and listy < 3:
        fails.append("لا جدول/قائمة خطوات")
    cl = [c for c in CLICHE if c.lower() in t.lower()]
    if cl:
        fails.append("كليشيهات AI: " + "، ".join(cl))
    if SENSITIVE_HINT.search(t) and not DISCLAIMER.search(t):
        fails.append("قسم حسّاس بلا إخلاء مسؤولية/فتوى")
    return w, fails


def main():
    args = sys.argv[1:]
    files = []
    if "--task" in args:
        i = args.index("--task")
        files = sorted(glob.glob(f"operating-system/reports/drafts/task{int(args[i+1]):02d}/*.md"))
    else:
        for a in args:
            files += glob.glob(a)
    files = [f for f in files if not os.path.basename(f).startswith("_")]
    if not files:
        print("لا ملفات. الاستخدام: draft-gate.py <ملفات.md> | --task NN")
        sys.exit(2)
    any_fail = False
    for fp in sorted(files):
        w, fails = gate(fp)
        if fails:
            any_fail = True
            print(f"❌ FAIL  {os.path.basename(fp)} ({w}w)")
            for x in fails:
                print(f"        - {x}")
        else:
            print(f"✅ PASS  {os.path.basename(fp)} ({w}w)")
    print()
    if any_fail:
        print("⛔ مسوّدة واحدة أو أكثر سقطت — أصلِحها قبل التسليم لعامر. لا تُحدّث الحالة إلى AMER_REVIEW.")
        sys.exit(1)
    print("✅ كل المسوّدات مرّت البوابة الذاتية — جاهزة لتسليم عامر.")
    sys.exit(0)


if __name__ == "__main__":
    main()
