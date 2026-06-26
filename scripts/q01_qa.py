#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent QA scan for Q-01 FAQ uplift (Cursor acting QA gate).
Checks objective gates only; human reviews FAQ quality separately.
"""
import re, json, sys, os

FILES = [
    "islamic-hajj-umrah/umrah-with-kids.html",
    "islamic-hajj-umrah/hijri-new-year-children.html",
    "islamic-hajj-umrah/daily-adhkar-family-guide.html",
    "featured-stories/featured-story-gulf-family-home.html",
    "blog/family-friendly-activities-gulf-cities.html",
    "blog/daily-islamic-habits-guide.html",
    "islamic-hajj-umrah/teaching-children-allah-names.html",
    "blog/hydration-guide.html",
    "peace-capsules/beat-summer-boredom-without-screens.html",
    "finance-wealth/investment-basics-beginners.html",
    "featured-stories/saudi-father-carpentry-workshop.html",
    "featured-stories/featured-story-saudi-mother.html",
    "comparisons/gold-vs-real-estate-gulf-family.html",
    "comparisons/domestic-vs-international-travel-family.html",
    "blog/umrah-with-kids-guide.html",
]

FILLER = ["شامل ومفصل", "شامل ومتكامل", "متكامل ومتوازن", "بشكل عام", "بشكل شامل",
          "دليل شامل", "مفصل ومتكامل", "ومتوازن ومعتدل", "مفيد لتحسين"]
# institutions that commonly appear without a deep link
INST = re.compile(r"(Princeton|Harvard|Stanford|Mayo|WHO|UNICEF|American Academy|"
                  r"University of|جامعة|منظمة الصحة|الأكاديمية الأمريكية|هارفارد|"
                  r"الهيئة السعودية للسياحة|Journal of)")


def visible_faq_count(t):
    # count FAQ wrapper blocks (consistent across markup variants)
    for pat in (r'class="[^"]*faq-item[^"]*"',
                r'class="[^"]*faq-question[^"]*"',
                r'itemprop="name"'):
        c = len(re.findall(pat, t))
        if c:
            return c
    return 0


def schema_faq(t):
    counts = []
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
                         t, re.S):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except Exception:
            counts.append(("BROKEN_JSON", raw[:60]))
            continue
        objs = data if isinstance(data, list) else [data]
        for o in objs:
            if isinstance(o, dict) and o.get("@type") == "FAQPage":
                counts.append(("FAQPage", len(o.get("mainEntity", []) or [])))
    return counts


def body_text(t):
    b = re.search(r"<body.*?>(.*)</body>", t, re.S)
    b = b.group(1) if b else t
    b = re.sub(r"<script.*?</script>", " ", b, flags=re.S)
    b = re.sub(r"<style.*?</style>", " ", b, flags=re.S)
    return b


def main():
    any_fail = False
    for fp in FILES:
        if not os.path.exists(fp):
            print(f"❓ MISSING  {fp}")
            any_fail = True
            continue
        t = open(fp, encoding="utf-8", errors="ignore").read()
        bt = body_text(t)
        issues = []

        em = bt.count("—")
        if em:
            issues.append(f"em-dash={em}")
        uns = len(re.findall(r"unsplash", t, re.I))
        if uns:
            issues.append(f"unsplash={uns}")

        sch = schema_faq(t)
        broken = [s for s in sch if s[0] == "BROKEN_JSON"]
        if broken:
            issues.append("BROKEN_JSON-LD")
        faq_schema = sum(n for k, n in sch if k == "FAQPage" and isinstance(n, int))
        vis = visible_faq_count(t)
        if not any(k == "FAQPage" for k, _ in sch):
            issues.append("no-FAQPage-schema")
        elif faq_schema != vis:
            issues.append(f"schema={faq_schema}!=visible={vis}")

        fl = [f for f in FILLER if f in bt]
        if fl:
            issues.append("filler:" + "،".join(fl))

        # institution-without-nearby-href heuristic (scan paragraphs)
        inst_hits = 0
        for p in re.findall(r"<p[^>]*>(.*?)</p>", bt, re.S):
            if INST.search(p) and "href" not in p:
                inst_hits += 1
        if inst_hits:
            issues.append(f"inst-no-link≈{inst_hits}")

        status = "✅ PASS" if not issues else "❌ CHECK"
        if issues:
            any_fail = True
        print(f"{status}  {fp}  | FAQ vis={vis} schema={faq_schema}")
        for i in issues:
            print(f"        - {i}")
    print()
    print("DONE" if not any_fail else "SOME FILES NEED A LOOK")


if __name__ == "__main__":
    main()
