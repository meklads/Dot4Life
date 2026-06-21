#!/usr/bin/env python3
"""Execute Amer's track-blog-triage.md: Schema-only (58) + 301 (2). Fail-closed per page."""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "operating-system/reports/track-blog-triage.md"
BACKUP = ROOT / "outputs/backups/blog-triage-20260622"
SITE = "https://dotforlife.com"

spec = importlib.util.spec_from_file_location(
    "build_draft", ROOT / "scripts/build-from-approved-draft.py"
)
build = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(build)

FINANCE_KW = re.compile(
    r"savings|budget|mortgage|zakat|invest|insurance|gold|rent|finance|financial|"
    r"ادخار|ميزانية|تمويل|زكاة|استثمار|تأمين|ذهب|إيجار|مال",
    re.I,
)
MEDICAL_KW = re.compile(
    r"pregnancy|nutrition|walking|water|bmi|health|calorie|حمل|تغذية|مشي|ماء|صحة",
    re.I,
)
SHARIA_KW = re.compile(
    r"umrah|hajj|islamic|adhkar|ramadan|prayer|عمرة|حج|إسلام|أذكار|رمضان|صلاة",
    re.I,
)

DISCLAIMERS = {
    "financial": '<div class="tip"><p><strong>Disclaimer:</strong> General educational information only, not financial advice. Consult a licensed advisor before decisions.</p></div>',
    "financial_ar": '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات تعليمية عامة وليست استشارة مالية. راجع مستشاراً مرخّصاً قبل أي قرار.</p></div>',
    "medical": '<div class="tip"><p><strong>Disclaimer:</strong> General information only, not medical advice. Consult a qualified healthcare provider.</p></div>',
    "medical_ar": '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات عامة وليست استشارة طبية. راجع طبيباً مختصاً.</p></div>',
    "sharia": '<div class="tip"><p><strong>Sharia Disclaimer:</strong> General guidance only, not a fatwa. Consult qualified scholars for religious rulings.</p></div>',
    "sharia_ar": '<div class="tip"><p><strong>إخلاء شرعي:</strong> إرشاد عام وليس فتوى. راجع أهل العلم المؤهّلين.</p></div>',
}


def parse_triage() -> tuple[list[str], list[tuple[str, str]]]:
    text = TRIAGE.read_text(encoding="utf-8")
    schema: list[str] = []
    redirects: list[tuple[str, str]] = []
    section = None
    for line in text.splitlines():
        if "## 1)" in line:
            section = "schema"
            continue
        if "## 2)" in line:
            section = "redirect"
            continue
        if "## 3)" in line:
            section = None
            continue
        if section == "schema":
            m = re.match(r"\|\s*\d+\s*\|\s*`([^`]+)`", line)
            if m:
                schema.append(m.group(1))
        if section == "redirect":
            m = re.match(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`", line)
            if m:
                redirects.append((m.group(1), m.group(2)))
    return schema, redirects


def infer_disclaimer(path: Path, html: str) -> str:
    blob = path.as_posix() + " " + html[:8000]
    if FINANCE_KW.search(blob):
        return "financial"
    if MEDICAL_KW.search(blob):
        return "medical"
    if SHARIA_KW.search(blob):
        return "sharia"
    return "none"


def is_ar(path: Path) -> bool:
    return not path.name.endswith("-en.html")


def parse_faqs(html: str, lang: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []

    # 1) Existing FAQPage JSON-LD anywhere
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            d = json.loads(m.group(1).strip())
            if d.get("@type") == "FAQPage":
                for e in d.get("mainEntity", []):
                    q = e.get("name", "")
                    a = (e.get("acceptedAnswer") or {}).get("text", "")
                    if q and a:
                        faqs.append((q, a))
        except json.JSONDecodeError:
            pass
    if len(faqs) >= 4:
        return faqs[:8]

    # 2) microdata Question — h3 or div.faq-question
    for m in re.finditer(
        r'itemtype="https://schema.org/Question"[\s\S]*?'
        r'(?:itemprop="name"[^>]*>(.*?)</h3>|class="faq-question"[^>]*itemprop="name"[^>]*>(.*?)</div>|'
        r'class="faq-question"[^>]*>(.*?)</div>)'
        r'[\s\S]*?itemprop="text"[\s\S]*?<p>(.*?)</p>',
        html,
        re.I,
    ):
        q = next((g.strip() for g in m.groups()[:3] if g), "")
        q = re.sub(r"<[^>]+>", "", q).strip()
        a = re.sub(r"<[^>]+>", "", m.group(4)).strip()
        if q and a:
            faqs.append((q, a))

    # 3) div.faq-item / faq-question + faq-answer (no microdata)
    for m in re.finditer(
        r'<div class="faq-item">[\s\S]*?'
        r'class="faq-question"[^>]*>(.*?)</div>\s*'
        r'<div class="faq-answer"[^>]*>\s*<p>(.*?)</p>',
        html,
        re.I,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if q and a:
            faqs.append((q, a))

    # 4) guide accordion: button.faq-q with span.en / span.ar
    en = lang == "en"
    for m in re.finditer(
        r'<div class="faq-item">[\s\S]*?<button class="faq-q"[^>]*>([\s\S]*?)</button>\s*'
        r'<div class="faq-a"[^>]*>([\s\S]*?)</div>\s*</div>',
        html,
        re.I,
    ):
        qblock, ablock = m.group(1), m.group(2)
        qm = re.search(rf'<span class="{"en" if en else "ar"}">(.*?)</span>', qblock, re.S)
        am = re.search(rf'<p class="{"en" if en else "ar"}">(.*?)</p>', ablock, re.S)
        if not qm:
            qm = re.search(r"<span class=\"en\">(.*?)</span>", qblock, re.S)
        if not am:
            am = re.search(r"<p[^>]*>(.*?)</p>", ablock, re.S)
        if qm and am:
            q = re.sub(r"<[^>]+>", "", qm.group(1)).strip()
            a = re.sub(r"<[^>]+>", "", am.group(1)).strip()
            if q and a:
                faqs.append((q, a))

    # 5) h3 + p under FAQ h2 (medina style)
    sec = re.search(
        r"(أسئلة شائعة|Frequently Asked Questions|FAQ)[^<]*</h2>([\s\S]{0,15000})",
        html,
        re.I,
    )
    if sec:
        chunk = sec.group(2)
        for m in re.finditer(r"<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>", chunk, re.S):
            q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if q and a and len(q) > 8:
                faqs.append((q, a))

    # dedupe
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for q, a in faqs:
        if q not in seen:
            seen.add(q)
            out.append((q, a))
    return out[:8]


def extract_h1(html: str) -> str:
    for pat in (
        r'<h1[^>]*class="article-banner-title"[^>]*>(.*?)</h1>',
        r"<h1[^>]*>(.*?)</h1>",
    ):
        m = re.search(pat, html, re.S)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


def fix_title(html: str, h1: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    raw = m.group(1).strip() if m else h1
    suffix = build.TITLE_SUFFIX if build.TITLE_SUFFIX in raw else build.TITLE_SUFFIX
    base = raw.replace(build.TITLE_SUFFIX, "").strip(" |")
    if not base and h1:
        base = h1
    limit = build.MAX_TITLE_LEN - len(build.TITLE_SUFFIX)
    if len(base) > limit:
        chunk = base[:limit]
        if " " in chunk:
            chunk = chunk.rsplit(" ", 1)[0]
        base = chunk.rstrip("?.،,")
    title = f"{base}{build.TITLE_SUFFIX}"
    new_tag = f"<title>{title}</title>"
    if m:
        html = html.replace(m.group(0), new_tag, 1)
    else:
        html = html.replace("</head>", new_tag + "\n</head>", 1)
    return html


def fix_meta(html: str) -> str:
    import html as html_lib

    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
    if not m:
        return html
    d = html_lib.unescape(m.group(1).strip())
    if not d or len(d) <= build.MAX_META_LEN:
        return html
    chunk = d[: build.MAX_META_LEN]
    if " " in chunk:
        chunk = chunk.rsplit(" ", 1)[0]
    chunk = chunk.rstrip("?.،,")
    return html.replace(m.group(0), re.sub(r'content="[^"]*"', f'content="{chunk}"', m.group(0), 1), 1)


def ensure_hreflang(html: str, path: Path) -> str:
    html = re.sub(r'hreflang="ar-SA"', 'hreflang="ar"', html)
    if 'hreflang="ar"' in html and 'hreflang="en"' in html:
        return html
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith("-en.html"):
        en, ar = rel, rel.replace("-en.html", ".html")
    else:
        ar, en = rel, rel.replace(".html", "-en.html")
    if not (ROOT / en).exists():
        en = ar
    block = (
        f'<link rel="alternate" hreflang="ar" href="{SITE}/{ar}" />\n'
        f'<link rel="alternate" hreflang="en" href="{SITE}/{en}" />\n'
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/{en}" />'
    )
    if "hreflang" in html:
        if 'hreflang="ar"' not in html:
            html = html.replace("</head>", f'<link rel="alternate" hreflang="ar" href="{SITE}/{ar}" />\n</head>', 1)
        if 'hreflang="en"' not in html:
            html = html.replace("</head>", f'<link rel="alternate" hreflang="en" href="{SITE}/{en}" />\n</head>', 1)
        return html
    cm = re.search(r'<link rel="canonical"[^>]*>', html, re.I)
    if cm:
        return html[: cm.end()] + "\n" + block + html[cm.end() :]
    return html.replace("</head>", block + "\n</head>", 1)


def hero_path(slug: str) -> Path:
    return ROOT / "assets/images" / f"hero-{slug}.webp"


def ensure_hero(html: str, path: Path, h1: str) -> tuple[str, str]:
    slug = path.stem.replace("_", "-")
    hp = hero_path(slug)
    hp.parent.mkdir(parents=True, exist_ok=True)
    if not hp.exists():
        src_url = None
        og = re.search(r'property="og:image"[^>]+content="([^"]+)"', html, re.I)
        if og:
            src_url = og.group(1)
        if not src_url:
            img = re.search(r'class="article-banner-img"[^>]+src="([^"]+)"', html)
            if img:
                src_url = img.group(1)
        if src_url and src_url.startswith("http"):
            try:
                subprocess.run(
                    ["curl", "-sL", "-o", str(hp.with_suffix(".jpg")), src_url],
                    check=True,
                    timeout=30,
                )
                jpg = hp.with_suffix(".jpg")
                if jpg.exists() and jpg.stat().st_size > 1000:
                    subprocess.run(["cwebp", "-q", "82", str(jpg), "-o", str(hp)], check=True)
                    jpg.unlink(missing_ok=True)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass
        if not hp.exists():
            fallback = ROOT / "assets/images/d4l1.webp"
            if fallback.exists():
                shutil.copy2(fallback, hp)
            else:
                shutil.copy2(ROOT / "d4l1.webp", hp)
    webp = f"/assets/images/hero-{slug}.webp"
    alt = h1[:120] if h1 else slug.replace("-", " ")
    figure = (
        f'<figure class="hero"><img src="{webp}" alt="{alt}" '
        f'width="1200" height="750" loading="lazy"></figure>'
    )
    if '<figure class="hero">' not in html:
        html = html.replace("<article class=\"article-body\">", f"<article class=\"article-body\">\n{figure}", 1)
        if figure not in html:
            html = html.replace("<main", figure + "\n<main", 1)
    og = f'<meta property="og:image" content="{SITE}{webp}">'
    if 'property="og:image"' not in html:
        html = html.replace("</head>", og + "\n</head>", 1)
    else:
        html = re.sub(
            r'<meta property="og:image" content="[^"]*">',
            og,
            html,
            count=1,
        )
    return html, webp


def ld_json(atype: str, data: dict) -> str:
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def inject_schema(html: str, path: Path, faqs: list[tuple[str, str]], h1: str, webp: str) -> str:
    url = f"{SITE}/{path.relative_to(ROOT).as_posix()}"
    desc_m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
    desc = desc_m.group(1)[:300] if desc_m else h1[:300]
    if not ld_has_type(html, "Article"):
        art = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": h1[:120] or path.stem,
            "description": desc,
            "author": {"@type": "Organization", "name": "DOTFORLIFE"},
            "datePublished": date.today().isoformat(),
            "dateModified": date.today().isoformat(),
            "image": f"{SITE}{webp}",
            "mainEntityOfPage": url,
        }
        html = html.replace("</head>", ld_json("Article", art) + "\n</head>", 1)
    if faq_count(html) < build.MIN_FAQ_Q and faqs:
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        }
        html = html.replace("</head>", ld_json("FAQPage", faq) + "\n</head>", 1)
    return html


def add_disclaimer(html: str, dtype: str, ar: bool) -> str:
    if dtype == "none" or build.has_disclaimer(html, dtype):
        return html
    key = f"{dtype}_ar" if ar else dtype
    block = DISCLAIMERS.get(key, DISCLAIMERS[dtype])
    if '<article class="article-body">' in html:
        return html.replace("</article>", block + "\n</article>", 1)
    return html.replace("</body>", block + "\n</body>", 1)


def ld_has_type(page: str, schema_type: str) -> bool:
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        items = [d] + list(d.get("@graph") or [])
        for item in items:
            if isinstance(item, dict) and item.get("@type") == schema_type:
                return True
    return False


def faq_count(page: str) -> int:
    n = 0
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        blocks = [d] + list(d.get("@graph") or [])
        for b in blocks:
            if isinstance(b, dict) and b.get("@type") == "FAQPage":
                n += len(b.get("mainEntity") or [])
    return n


def archive_ld_blocks(page: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1).strip())
        except json.JSONDecodeError as e:
            raise build.BuildGateError("G11", Path("?"), f"invalid JSON-LD: {e}") from e
        out.append(d)
        for item in d.get("@graph") or []:
            if isinstance(item, dict):
                out.append(item)
    return out


def archive_assert_gates(page: str, lang: str, out_path: Path, dtype: str) -> None:
    """G1–G11 with @graph-aware G3/G4 for archive pages."""
    cfg = {"id": "archive", "disclaimer_type": dtype}
    if build.EM_DASH in page:
        build.gate_fail("G1", out_path, f"{page.count(build.EM_DASH)} em dash(es)")
    wc = build.visible_word_count(page)
    if wc < build.MIN_DRAFT_WORDS:
        build.gate_fail("G2", out_path, f"visible words={wc} < {build.MIN_DRAFT_WORDS}")
    ld_blocks = archive_ld_blocks(page)
    article_blocks = [b for b in ld_blocks if b.get("@type") == "Article"]
    if not article_blocks:
        build.gate_fail("G3", out_path, "Article schema missing")
    faq_blocks = [b for b in ld_blocks if b.get("@type") == "FAQPage"]
    if not faq_blocks:
        build.gate_fail("G4", out_path, "FAQPage schema missing")
    faq_q = sum(len(b.get("mainEntity") or []) for b in faq_blocks)
    if faq_q < build.MIN_FAQ_Q:
        build.gate_fail("G4", out_path, f"FAQ questions={faq_q} < {build.MIN_FAQ_Q}")
    hero = re.search(
        r'<figure class="hero"><img[^>]+src="([^"]+\.webp)"[^>]+alt="([^"]*)"', page
    )
    if not hero:
        build.gate_fail("G5", out_path, "hero WebP img missing")
    if not hero.group(2).strip():
        build.gate_fail("G5", out_path, "hero alt empty")
    if 'property="og:image"' not in page:
        build.gate_fail("G5", out_path, "og:image missing")
    tm = re.search(r"<title>(.*?)</title>", page)
    if not tm:
        build.gate_fail("G6", out_path, "no <title>")
    title = tm.group(1)
    if len(title) > build.MAX_TITLE_LEN:
        build.gate_fail("G6", out_path, f"title len={len(title)} > {build.MAX_TITLE_LEN}")
    mm = re.search(r'<meta name="description" content="(.*?)"', page)
    if not mm:
        build.gate_fail("G7", out_path, "meta description missing")
    import html as html_lib
    if len(html_lib.unescape(mm.group(1))) > build.MAX_META_LEN:
        build.gate_fail("G7", out_path, "meta too long")
    if 'hreflang="ar"' not in page or 'hreflang="en"' not in page:
        build.gate_fail("G8", out_path, "hreflang ar/en pair missing")
    if dtype != "none" and not build.has_disclaimer(page, dtype):
        build.gate_fail("G9", out_path, f"disclaimer missing (type={dtype})")
    nlinks = build.count_internal_links(page)
    if nlinks < build.MIN_INTERNAL_LINKS:
        build.gate_fail("G10", out_path, f"internal links={nlinks} < {build.MIN_INTERNAL_LINKS}")


def gate_check(html: str, path: Path, dtype: str) -> tuple[bool, str]:
    try:
        archive_assert_gates(html, "en" if path.name.endswith("-en.html") else "ar", path, dtype)
        return True, "ALL PASS"
    except build.BuildGateError as e:
        return False, str(e)


def redirect_stub(src: Path, dest: str) -> None:
    ar = src.name.endswith(".html") and not src.name.endswith("-en.html")
    lang = "ar" if ar else "en"
    dir_attr = 'rtl' if ar else 'ltr'
    if src.name.endswith("-en.html") and not dest.endswith("-en.html"):
        dest_en = dest.replace(".html", "-en.html")
        if (ROOT / dest_en).exists():
            dest = dest_en
    canon = f"{SITE}/{dest.lstrip('/')}"
    dest_url = f"/{dest.lstrip('/')}"
    html = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{dir_attr}">
<head>
<meta charset="UTF-8">
<title>Redirecting…</title>
<link rel="canonical" href="{canon}">
<meta http-equiv="refresh" content="0;url={dest_url}">
<meta name="robots" content="noindex,follow">
<script>location.replace("{dest_url}");</script>
</head>
<body><p><a href="{dest_url}">Continue</a></p></body>
</html>
"""
    BACKUP.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, BACKUP / src.name)
    src.write_text(html, encoding="utf-8")


def enhance_page(rel: str) -> tuple[bool, str]:
    path = ROOT / rel
    if not path.exists():
        return False, "MISSING"
    html = path.read_text(encoding="utf-8")
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, BACKUP / path.name)
    h1 = extract_h1(html)
    faqs = parse_faqs(html, "en" if path.name.endswith("-en.html") else "ar")
    if len(faqs) < 4:
        return False, f"FAQ<{4} ({len(faqs)})"
    html = fix_title(html, h1)
    html = fix_meta(html)
    html = ensure_hreflang(html, path)
    html, webp = ensure_hero(html, path, h1)
    html = inject_schema(html, path, faqs, h1, webp)
    dtype = infer_disclaimer(path, html)
    html = add_disclaimer(html, dtype, is_ar(path))
    ok, msg = gate_check(html, path, dtype)
    if ok:
        path.write_text(html, encoding="utf-8")
    return ok, msg


def main() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    schema, redirects = parse_triage()
    print(f"=== Blog triage execute ===\nSchema-only: {len(schema)} · 301: {len(redirects)}\n")

    for src_rel, dest_rel in redirects:
        redirect_stub(ROOT / src_rel, dest_rel)
        print(f"  301 {src_rel} → {dest_rel}")

    passed = failed = 0
    fail_log: list[str] = []
    for rel in schema:
        ok, msg = enhance_page(rel)
        if ok:
            passed += 1
            print(f"  ✅ PASS {rel}")
        else:
            failed += 1
            fail_log.append(f"{rel}: {msg}")
            print(f"  ❌ FAIL {rel}: {msg}")

    print(f"\n=== SUMMARY: {passed} PASS, {failed} FAIL (301: {len(redirects)}) ===")
    log = ROOT / "operating-system/reports/blog-triage-execute-log.md"
    log.write_text(
        f"# Blog triage execute — {date.today().isoformat()}\n\n"
        f"- Schema-only PASS: **{passed}/{len(schema)}**\n"
        f"- 301 redirects: **{len(redirects)}**\n\n"
        "## Failures\n"
        + ("\n".join(f"- {x}" for x in fail_log) if fail_log else "- none")
        + "\n",
        encoding="utf-8",
    )
    print(f"Log: {log.relative_to(ROOT)}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
