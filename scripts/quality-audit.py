#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فاحص جودة المقالات — DotForLife
يفحص كل مقال HTML مقابل البنود القابلة للقياس في operating-system/content-standards.md
ويُخرج تقريراً لكل قسم + CSV تفصيلي.

ملاحظة: عدد الكلمات يقاس على كامل النص الظاهر (يشمل الهيدر/الفوتر الثابتين ~150 كلمة).
لذلك العتبة العملية للجسم ≥1200 ≈ إجمالي ظاهر ≥1350.
"""
import os, re, csv, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# الأقسام التي نراجعها (مجلدات المحتوى)
SECTIONS = [
    "blog", "health", "health-pregnancy", "finance-wealth",
    "islamic-hajj-umrah", "real-estate", "travel", "productivity",
    "fitness", "comparisons", "peace-capsules", "featured-stories",
    "guides",
]
# الأقسام الحساسة التي تتطلب إخلاء مسؤولية
SENSITIVE = {"health", "health-pregnancy", "finance-wealth",
             "islamic-hajj-umrah", "fitness"}

WORD_TOTAL_THRESHOLD = 1350   # ≈ 1200 جسم + قالب
DISCLAIMER_PAT = re.compile(
    r"(إخلاء|ليست\s+استشارة|ليست\s+فتوى|معلومات\s+عامة|راجع\s+(?:أهل\s+العلم|طبيب|مختص)"
    r"|disclaimer|not\s+(?:medical|financial|professional)\s+advice|general\s+information)",
    re.I)
FAQ_PAT = re.compile(r'("@type"\s*:\s*"FAQPage"|FAQPage|<[^>]+class="[^"]*faq)', re.I)


def visible_words(html):
    h = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    h = re.sub(r"&[a-z#0-9]+;", " ", h)
    return len([w for w in re.split(r"\s+", h) if w.strip()])


def internal_links(html):
    hrefs = re.findall(r'href="([^"]+)"', html)
    return [x for x in hrefs if not re.match(r"(https?:|#|mailto:|tel:|javascript:)", x)]


def audit_file(path):
    html = open(path, encoding="utf-8", errors="ignore").read()
    words = visible_words(html)
    em = html.count("—")
    has_article = bool(re.search(r'"@type"\s*:\s*"Article"|"Article"', html))
    has_faqpage = bool(re.search(r'"@type"\s*:\s*"FAQPage"|"FAQPage"', html))
    has_faq = bool(FAQ_PAT.search(html))
    has_ldjson = "application/ld+json" in html
    has_hreflang = "hreflang" in html
    has_disc = bool(DISCLAIMER_PAT.search(html))
    ilinks = len(set(internal_links(html)))
    # صورة رئيسية
    has_hero = bool(re.search(r'(hero|banner|featured)[-_][^"\']*\.(webp|svg|jpg|png)|og:image', html, re.I))
    # title / meta
    mt = re.search(r"<title>(.*?)</title>", html, re.S)
    title_len = len(mt.group(1).strip()) if mt else 0
    md = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
    meta_len = len(md.group(1).strip()) if md else 0
    return dict(words=words, em=em, has_article=has_article, has_faqpage=has_faqpage,
                has_faq=has_faq, has_ldjson=has_ldjson, has_hreflang=has_hreflang,
                has_disc=has_disc, ilinks=ilinks, has_hero=has_hero,
                title_len=title_len, meta_len=meta_len)


def fails(sec, a):
    f = []
    if a["words"] < WORD_TOTAL_THRESHOLD: f.append("قصير(<1200)")
    if a["em"] > 0: f.append(f"شرطات×{a['em']}")
    if not (a["has_faq"] or a["has_faqpage"]): f.append("لا FAQ")
    if not a["has_article"]: f.append("لا Article-schema")
    if not a["has_faqpage"]: f.append("لا FAQPage-schema")
    if sec in SENSITIVE and not a["has_disc"]: f.append("لا إخلاء مسؤولية")
    if not a["has_hero"]: f.append("لا صورة رئيسية")
    if a["ilinks"] < 3: f.append(f"روابط داخلية<3({a['ilinks']})")
    if not a["has_hreflang"]: f.append("لا hreflang")
    if a["title_len"] == 0 or a["title_len"] > 60: f.append(f"Title({a['title_len']})")
    if a["meta_len"] == 0 or a["meta_len"] > 160: f.append(f"Meta({a['meta_len']})")
    return f


def main():
    rows = []
    section_summary = {}
    for sec in SECTIONS:
        d = os.path.join(ROOT, sec)
        if not os.path.isdir(d):
            continue
        files = sorted(glob.glob(os.path.join(d, "*.html")))
        passed = 0
        issue_counter = {}
        for fp in files:
            a = audit_file(fp)
            fl = fails(sec, a)
            if not fl:
                passed += 1
            for x in fl:
                key = re.sub(r"[×(].*", "", x)
                issue_counter[key] = issue_counter.get(key, 0) + 1
            rows.append([sec, os.path.basename(fp), a["words"], a["em"],
                         "؛ ".join(fl) if fl else "✅ سليم"])
        section_summary[sec] = dict(total=len(files), passed=passed,
                                    issues=issue_counter)
    # CSV
    out_csv = os.path.join(ROOT, "operating-system", "reports", "quality-audit.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["القسم", "الملف", "كلمات", "شرطات", "المشاكل"])
        w.writerows(rows)
    # ملخص
    print(f"{'القسم':<22}{'العدد':>6}{'سليم':>6}{'%':>6}   أبرز المشاكل")
    print("-" * 90)
    grand_t = grand_p = 0
    for sec, s in section_summary.items():
        t, p = s["total"], s["passed"]
        grand_t += t; grand_p += p
        pct = round(100 * p / t) if t else 0
        top = sorted(s["issues"].items(), key=lambda x: -x[1])[:3]
        top_s = "، ".join(f"{k}({v})" for k, v in top)
        print(f"{sec:<22}{t:>6}{p:>6}{pct:>5}%   {top_s}")
    print("-" * 90)
    gp = round(100 * grand_p / grand_t) if grand_t else 0
    print(f"{'الإجمالي':<22}{grand_t:>6}{grand_p:>6}{gp:>5}%")
    print(f"\nCSV: {out_csv}")
    # JSON summary
    out_json = os.path.join(ROOT, "operating-system", "reports", "quality-audit-summary.json")
    json.dump(section_summary, open(out_json, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
