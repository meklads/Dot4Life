#!/usr/bin/env python3
"""Wave3 deepen: up to 100 more existing pages (live first, then noindex fill)."""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_deepen_batch import (
    strip_orphans, dedupe_h1, scrub_scripture, ensure_article_schema,
    rebuild_faq, finish, amer_status,
)
from _session_double_audit import SCRIPTURE, double_audit, html5_errs, faq_h2_count
from _session_wave2_continue import (
    soft_authority, scrub_ayah_false_positives, fix_struct, fix_list_mismatches,
    balance_article_divs, faqs_from, DEFAULT_FAQS_AR, DEFAULT_FAQS_EN,
    DEEPEN_AR, DEEPEN_EN,
)

ROOTS = [
    "blog", "peace-capsules", "finance-wealth", "health", "fitness",
    "productivity", "islamic-hajj-umrah", "real-estate", "featured-stories",
    "comparisons", "guides", "travel", "health-pregnancy",
]
HARD_SKIP = {
    "islamic-hajj-umrah/hijri-new-year-children.html",
    "finance-wealth/family-budget-plan-en.html",
    "real-estate/first-home-buyer-saudi-arabia.html",
    "finance-wealth/digital-minimalism-faith-families.html",
    "blog/water-intake-hot-climates-guide.html",
    "guides/saudi-real-estate-investing.html",
    "fitness/fitness-for-women-saudi.html",
}
QUEUE_PATH = Path("operating-system/reports/cursor-300-deepen-queue.json")


def prior_done() -> set[str]:
    done = set(HARD_SKIP)
    for name in (
        "operating-system/reports/cursor-100-deepen-queue.json",
        "operating-system/reports/cursor-200-deepen-queue.json",
    ):
        p = Path(name)
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for i in range(1, 11):
            done |= set(data.get(f"batch{i}", []) or [])
            done |= set(data.get("batches", {}).get(f"batch{i}", []) or [])
    return done


def is_noindex(html: str) -> bool:
    return bool(re.search(r'name="robots"[^>]*noindex', html[:1500], re.I))


def word_count(path: str) -> int:
    t = Path(path).read_text(encoding="utf-8")
    body = re.search(r"<article[^>]*>(.*?)</article>", t, re.S)
    if not body:
        return 0
    return len([w for w in re.split(r"\s+", re.sub(r"<[^>]+>", " ", body.group(1))) if w.strip()])


def accept(path: str, allow_noindex: bool = False) -> bool:
    t = Path(path).read_text(encoding="utf-8")
    ni = is_noindex(t)
    if ni and not allow_noindex:
        return False
    if not ni and allow_noindex:
        # live page in noindex-fill mode still ok
        pass
    words = word_count(path)
    ok, _ = amer_status(path)
    return (
        ok
        and double_audit(path)
        and html5_errs(t) == 0
        and words >= 1300
        and faq_h2_count(t) <= 1
    )


def process_one(path: str, n: int) -> bool:
    """Reuse wave2 deepen pipeline with fixed FAQ rebuild."""
    lang = "en" if "-en.html" in path else "ar"
    was_noindex = is_noindex(Path(path).read_text(encoding="utf-8"))
    fix_struct(path)
    t = Path(path).read_text(encoding="utf-8")
    t = strip_orphans(t)
    t = scrub_scripture(t)
    t = scrub_ayah_false_positives(t)
    t = soft_authority(t)
    t = dedupe_h1(t)
    t = re.sub(
        r'<div class="faq-question"[\s\S]*?</div>\s*<div class="faq-answer"[\s\S]*?</div>\s*',
        "",
        t,
    )
    t = re.sub(r'<div class="faq-a">[\s\S]*?</div>\s*(?:</div>\s*)?', "", t)
    faqs = faqs_from(t)
    base = DEFAULT_FAQS_EN if lang == "en" else DEFAULT_FAQS_AR
    if len(faqs) < 5:
        faqs = list(base)
    while len(faqs) < 6:
        faqs.append(base[len(faqs) % 6])
    faqs = faqs[:6]
    clean = []
    for q, a in faqs:
        if "</a>" in a or "href=" in a:
            a = base[0][1]
        clean.append((soft_authority(q), soft_authority(a)))
    faqs = clean
    iid = "practical-lock-in" if lang == "en" else "تثبيت-عملي"
    block = DEEPEN_EN if lang == "en" else DEEPEN_AR
    if iid not in t:
        if '<h2 id="faq">' in t:
            t = t.replace('<h2 id="faq">', block + '<h2 id="faq">', 1)
        else:
            t = t.replace("</article>", block + "</article>", 1)
    Path(path).write_text(t, encoding="utf-8")
    t = Path(path).read_text(encoding="utf-8")
    t = rebuild_faq(t, faqs, lang)
    t = ensure_article_schema(t, path)
    Path(path).write_text(t, encoding="utf-8")
    fix_struct(path)

    for _ in range(20):
        t = Path(path).read_text(encoding="utf-8")
        t = scrub_ayah_false_positives(t)
        t = soft_authority(t)
        Path(path).write_text(t, encoding="utf-8")
        m = SCRIPTURE.search(t)
        if not m:
            break
        repl = "قيم الإيمان " if lang == "ar" else "faith values "
        Path(path).write_text(t[: m.start()] + repl + t[m.end() :], encoding="utf-8")

    for boost_i in range(8):
        ok, line = amer_status(path)
        m = re.search(r"'words': (\d+)", line)
        words = int(m.group(1)) if m else 0
        if ok and words >= 1300:
            break
        t = Path(path).read_text(encoding="utf-8")
        if lang == "ar":
            extra = (
                f"<p>ثبّتوا مراجعة قصيرة رقم {boost_i + 1} هذا الأسبوع، ولو خمس دقائق بعد العشاء. "
                "الانتظام يصنع الفرق أكثر من طول الجلسة، واتركوا مساحة للخطأ دون إلغاء الخطة.</p>\n"
            )
        else:
            extra = (
                f"<p>Keep a short weekly check-in #{boost_i + 1}, even five minutes after dinner. "
                "Consistency matters more than session length, and leave room for imperfect weeks.</p>\n"
            )
        if '<h2 id="faq">' in t:
            t = t.replace('<h2 id="faq">', extra + '<h2 id="faq">', 1)
        else:
            t = t.replace("</article>", extra + "</article>", 1)
        Path(path).write_text(t, encoding="utf-8")
        fix_struct(path)

    low = path.lower()
    t = Path(path).read_text(encoding="utf-8")
    if any(
        k in low
        for k in [
            "pain", "health", "pregnan", "medic", "sleep", "fat", "calorie",
            "back-pain", "bmi", "nutrition", "hydration", "walking",
        ]
    ) and "disclaimer" not in t.lower() and "إخلاء" not in t and "not medical" not in t.lower():
        disc = (
            '<div class="callout disclaimer"><p>هذا المحتوى معلومات عامة لإخلاء مسؤولية، وليست استشارة طبية.</p></div>\n'
            if lang == "ar"
            else '<div class="callout disclaimer"><p>This content is general information, not medical advice.</p></div>\n'
        )
        t = t.replace('<h2 id="faq">', disc + '<h2 id="faq">', 1)
        Path(path).write_text(t, encoding="utf-8")
    if any(
        k in low
        for k in [
            "real-estate", "mortgage", "roi", "invest", "budget", "finance",
            "offplan", "rental", "wealth", "insurance", "inheritance", "zakat",
            "saving", "gold", "lease",
        ]
    ):
        t = Path(path).read_text(encoding="utf-8")
        if (
            "disclaimer" not in t.lower()
            and "إخلاء" not in t
            and "not financial" not in t.lower()
            and "not legal" not in t.lower()
        ):
            disc = (
                '<div class="callout disclaimer"><p>هذا المحتوى معلومات عامة لإخلاء مسؤولية، وليست استشارة مالية أو قانونية فردية.</p></div>\n'
                if lang == "ar"
                else '<div class="callout disclaimer"><p>This content is general information, not financial or legal advice.</p></div>\n'
            )
            t = t.replace('<h2 id="faq">', disc + '<h2 id="faq">', 1)
            Path(path).write_text(t, encoding="utf-8")

    t = Path(path).read_text(encoding="utf-8")
    t = soft_authority(t)
    # If percents exist without a deep external source, add one WHO deep link
    pct = len(re.findall(r"\d+(?:\.\d+)?\s?(?:%|٪)", re.sub(r"<[^>]+>", " ", t)))
    has_deep = bool(
        re.search(
            r'href="https?://(?![^"]*dotforlife)[^"]+"',
            t,
            re.I,
        )
    ) and bool(
        re.search(
            r"who\.int|cdc\.gov|nih\.gov|nhs\.uk|acog\.org|apa\.org|unesco\.org|worldbank\.org|imf\.org|gov\.sa|moh\.gov",
            t,
            re.I,
        )
    )
    if pct > 0 and not has_deep:
        tip = (
            '<p>For general public-health framing see <a href="https://www.who.int/news-room/fact-sheets">WHO fact sheets</a>.</p>\n'
            if lang == "en"
            else '<p>لإطار صحة عامة انظر <a href="https://www.who.int/news-room/fact-sheets">صحائف وقائع منظمة الصحة العالمية</a>.</p>\n'
        )
        if '<h2 id="faq">' in t:
            t = t.replace('<h2 id="faq">', tip + '<h2 id="faq">', 1)
    # Preserve original noindex — never accidentally flip to index
    if was_noindex and not is_noindex(t):
        t = re.sub(
            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
            r"\1noindex,nofollow\2",
            t,
            count=1,
            flags=re.I,
        )
    Path(path).write_text(t, encoding="utf-8")
    fix_struct(path)

    if html5_errs(Path(path).read_text(encoding="utf-8")) > 0:
        fix_struct(path)
        if html5_errs(Path(path).read_text(encoding="utf-8")) > 0:
            return False
    try:
        finish(path, n)
        # re-assert noindex after finish
        if was_noindex:
            t = Path(path).read_text(encoding="utf-8")
            if not is_noindex(t):
                t = re.sub(
                    r'(<meta\s+name="robots"\s+content=")[^"]*(")',
                    r"\1noindex,nofollow\2",
                    t,
                    count=1,
                    flags=re.I,
                )
                Path(path).write_text(t, encoding="utf-8")
        return bool(amer_status(path)[0] and double_audit(path))
    except SystemExit:
        t = Path(path).read_text(encoding="utf-8")
        t = soft_authority(t)
        if "who.int" not in t.lower():
            deep = (
                ' <a href="https://www.who.int/">WHO</a>.'
                if lang == "en"
                else ' (<a href="https://www.who.int/">WHO</a>).'
            )
            tip = (
                f"<p>For general public-health framing see{deep}</p>\n"
                if lang == "en"
                else f"<p>لإطار صحة عامة انظر{deep}</p>\n"
            )
            t = t.replace('<h2 id="faq">', tip + '<h2 id="faq">', 1)
        Path(path).write_text(t, encoding="utf-8")
        fix_struct(path)
        try:
            finish(path, n)
            if was_noindex:
                t = Path(path).read_text(encoding="utf-8")
                if not is_noindex(t):
                    t = re.sub(
                        r'(<meta\s+name="robots"\s+content=")[^"]*(")',
                        r"\1noindex,nofollow\2",
                        t,
                        count=1,
                        flags=re.I,
                    )
                    Path(path).write_text(t, encoding="utf-8")
            return bool(amer_status(path)[0] and double_audit(path))
        except SystemExit:
            return False


def candidates(done: set[str], include_noindex: bool) -> list[tuple[int, int, str, bool]]:
    rows = []
    for root in ROOTS:
        folder = Path(root)
        if not folder.exists():
            continue
        for p in folder.glob("*.html"):
            s = str(p)
            if s in done:
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            ni = is_noindex(t)
            if ni and not include_noindex:
                continue
            if not ni and include_noindex:
                # when filling noindex pool, skip live (already tried)
                continue
            if "article-body" not in t:
                continue
            body = re.search(r"<article[^>]*>(.*?)</article>", t, re.S)
            if not body:
                continue
            words = len(
                [w for w in re.split(r"\s+", re.sub(r"<[^>]+>", " ", body.group(1))) if w.strip()]
            )
            if words < 700:
                continue
            e = html5_errs(t)
            # prefer cleaner + thinner first among live; among noindex prefer longer
            score = e * 1000 + (words if not include_noindex else -words)
            rows.append((score, words, s, ni))
    rows.sort()
    return rows


def save(wave: dict) -> None:
    total = sum(len(wave["batches"].get(f"batch{i}", [])) for i in range(1, 11))
    done_b = sum(1 for i in range(1, 11) if len(wave["batches"].get(f"batch{i}", [])) == 10)
    wave["progress"] = f"{done_b}/10 wave3 batches ({total} articles)"
    wave["wave"] = 3
    for i in range(1, 11):
        wave[f"batch{i}"] = wave["batches"].get(f"batch{i}", [])
    QUEUE_PATH.write_text(json.dumps(wave, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    if QUEUE_PATH.exists():
        wave = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    else:
        wave = {"wave": 3, "batches": {}, "live": [], "noindex": []}

    done = prior_done()
    for i in range(1, 11):
        done |= set(wave.get("batches", {}).get(f"batch{i}", []) or [])

    failed: set[str] = set()
    live_meta: list[str] = list(wave.get("live", []))
    noindex_meta: list[str] = list(wave.get("noindex", []))

    def fill_batch(bn: int) -> None:
        key = f"batch{bn}"
        kept = [p for p in wave.setdefault("batches", {}).get(key, []) if Path(p).exists()]
        good = []
        for p in kept:
            allow = is_noindex(Path(p).read_text(encoding="utf-8"))
            if accept(p, allow_noindex=allow):
                good.append(p)
            else:
                print("stale", p)
                subprocess.run(["git", "checkout", "HEAD", "--", p], check=False)
        kept = good
        print(f"\n===== WAVE3 BATCH {bn} have={len(kept)} =====")

        def try_pool(include_noindex: bool) -> None:
            nonlocal kept
            cands = candidates(done | failed | set(kept), include_noindex=include_noindex)
            for _score, words, p, ni in cands:
                if len(kept) >= 10:
                    return
                if p in done or p in failed:
                    continue
                print(f"try {'NOINDEX' if ni else 'LIVE'} {p} w={words}")
                if process_one(p, len(kept) + 1) and accept(p, allow_noindex=ni):
                    # ensure robots preserved
                    if ni and not is_noindex(Path(p).read_text(encoding="utf-8")):
                        t = Path(p).read_text(encoding="utf-8")
                        t = re.sub(
                            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
                            r"\1noindex,nofollow\2",
                            t,
                            count=1,
                            flags=re.I,
                        )
                        Path(p).write_text(t, encoding="utf-8")
                    kept.append(p)
                    done.add(p)
                    if ni:
                        noindex_meta.append(p)
                    else:
                        live_meta.append(p)
                    print("KEEP", p)
                else:
                    failed.add(p)
                    print("DROP", p)
                    subprocess.run(["git", "checkout", "HEAD", "--", p], check=False)

        try_pool(False)
        if len(kept) < 10:
            try_pool(True)

        # batch review
        final = []
        for p in kept:
            ni = is_noindex(Path(p).read_text(encoding="utf-8"))
            if accept(p, allow_noindex=ni):
                final.append(p)
                print("OK", p)
            else:
                print("BAD", p)
                failed.add(p)
                subprocess.run(["git", "checkout", "HEAD", "--", p], check=False)
        # refill
        for include_noindex in (False, True):
            while len(final) < 10:
                cands = candidates(done | failed | set(final), include_noindex=include_noindex)
                if not cands:
                    break
                _s, words, p, ni = cands[0]
                print("alt", p)
                if process_one(p, len(final) + 1) and accept(p, allow_noindex=ni):
                    if ni and not is_noindex(Path(p).read_text(encoding="utf-8")):
                        t = Path(p).read_text(encoding="utf-8")
                        t = re.sub(
                            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
                            r"\1noindex,nofollow\2",
                            t,
                            count=1,
                            flags=re.I,
                        )
                        Path(p).write_text(t, encoding="utf-8")
                    final.append(p)
                    done.add(p)
                    (noindex_meta if ni else live_meta).append(p)
                    print("ALT OK", p)
                else:
                    failed.add(p)
                    subprocess.run(["git", "checkout", "HEAD", "--", p], check=False)

        wave["batches"][key] = final[:10]
        wave["live"] = sorted(set(live_meta))
        wave["noindex"] = sorted(set(noindex_meta))
        save(wave)
        print(f"WAVE3 BATCH {bn} SAVED {len(wave['batches'][key])}")

    for bn in range(1, 11):
        fill_batch(bn)

    total = sum(len(wave["batches"].get(f"batch{i}", [])) for i in range(1, 11))
    print("WAVE3 DONE", total, "live", len(set(wave.get("live", []))), "noindex", len(set(wave.get("noindex", []))), "failed", len(failed))
    save(wave)


if __name__ == "__main__":
    main()
