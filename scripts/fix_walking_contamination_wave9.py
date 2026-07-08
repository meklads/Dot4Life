#!/usr/bin/env python3
"""Wave 9: fix Daily Walking template contamination.

1. Restore 16 files overwritten by commit 00255dac from parent revision.
2. Fix hero-daily-walking-benefits in og:image / JSON-LD / banners where body is correct.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESTORE_COMMIT = "00255dac^"
WALKING_HERO = "hero-daily-walking-benefits.webp"
WALKING_TITLE_MARKERS = (
    "فوائد المشي اليومي",
    "Daily Walking Benefits",
    "The Benefits of Daily Walking",
)

RESTORE_PATHS = [
    "blog/friday-night-reset-family.html",
    "blog/friday-night-reset-family-en.html",
    "comparisons/school-type-comparison-guide.html",
    "comparisons/school-type-comparison-guide-en.html",
    "featured-stories/father-quit-social-media-year.html",
    "featured-stories/father-quit-social-media-year-en.html",
    "finance-wealth/barakah-budget-family-finance.html",
    "finance-wealth/barakah-budget-family-finance-en.html",
    "health/quiet-home-family-guide.html",
    "health/quiet-home-family-guide-en.html",
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide.html",
    "islamic-hajj-umrah/makkah-medina-family-spiritual-guide-en.html",
    "peace-capsules/listening-gift.html",
    "peace-capsules/listening-gift-en.html",
    "real-estate/three-generation-table-family-meals.html",
    "real-estate/three-generation-table-family-meals-en.html",
]

HERO_BY_STEM: dict[str, str] = {
    "friday-night-reset-family": "hero-evening-rituals.webp",
    "school-type-comparison-guide": "hero-government-vs-private-school-gulf.webp",
    "father-quit-social-media-year": "hero-digital-minimalism-families.webp",
    "barakah-budget-family-finance": "hero-family-budget-plan.webp",
    "quiet-home-family-guide": "hero-peace-at-home-5-steps.webp",
    "makkah-medina-family-spiritual-guide": "hero-umrah-with-kids.webp",
    "listening-gift": "hero-art-of-apologizing.webp",
    "three-generation-table-family-meals": "hero-mindful-family-meal-faith.webp",
    "power-of-patience-marriage": "hero-art-of-apologizing.webp",
    "health-insurance-plans-gulf-families": "hero-life-insurance-gulf-families.webp",
    "hydration-guide": "hydration-hero-ar.webp",
    "hydration-guide-en": "hydration-hero-en.webp",
    "mindful-living-gulf-heat": "hero-mindful-living-gulf-heat.svg",
    "mindful-living-gulf-heat-en": "hero-mindful-living-gulf-heat.svg",
    "hydration-guide-hot-climates-families": "hydration-hero-ar.webp",
    "hydration-guide-hot-climates-families-en": "hydration-hero-en.webp",
    "pregnancy-nutrition-first-trimester": "hero-pregnancy-nutrition-first-trimester.webp",
    "building-family-reading-habit": "hero-daily-adhkar-family-guide.webp",
    "digital-minimalism-modern-families": "hero-digital-minimalism-families.webp",
    "back-pain-prevention-working-parents": "hero-body-fat-vs-weight-guide.webp",
    "screen-time-eye-health-children": "hero-managing-screen-time-children.webp",
    "preconception-checkups": "hero-preconception-checkups.webp",
    "mother-homeschooled-five-children": "hero-choosing-right-school-child-gulf.webp",
    "ramadan-calorie-calculator": "hero-daily-islamic-habits-guide.webp",
    "outdoor-vs-indoor-family-activities": "hero-family-friendly-activities-gulf-cities.webp",
    "bmi-calculator-women": "hero-bmi-calculator-women.webp",
    "pregnancy-week-by-week": "hero-pregnancy-week-by-week.webp",
}

SKIP_GLOBS = ("outputs/", "daily-walking-benefits")


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{RESTORE_COMMIT}:{path}"],
        cwd=ROOT,
        text=True,
    )


def stem_from_path(path: str) -> str:
    name = Path(path).name
    if name.endswith("-en.html"):
        return name[:-8]
    return name[:-5]


def hero_url(stem: str) -> str | None:
    fname = HERO_BY_STEM.get(stem)
    if not fname:
        # try hero-{stem}.webp in approved/
        candidate = ROOT / "assets" / "images" / "approved" / f"hero-{stem}.webp"
        if candidate.exists():
            fname = candidate.name
    if not fname:
        return None
    if fname.startswith("hero-") or fname.startswith("hydration-"):
        if (ROOT / "assets" / "images" / "approved" / fname).exists():
            return f"https://dotforlife.com/assets/images/approved/{fname}"
        if (ROOT / "assets" / "images" / fname).exists():
            return f"https://dotforlife.com/assets/images/{fname}"
    return f"https://dotforlife.com/assets/images/{fname}"


def local_hero_src(stem: str) -> str | None:
    url = hero_url(stem)
    if not url:
        return None
    return url.replace("https://dotforlife.com", "")


def extract_tag(html: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.S | re.I)
    return m.group(1).strip() if m else None


def extract_meta(html: str, name: str) -> str | None:
    m = re.search(
        rf'<meta[^>]+name=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)["\']',
        html,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{re.escape(name)}["\']',
        html,
        re.I,
    )
    return m.group(1) if m else None


def extract_og_image(html: str) -> str | None:
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']*)["\']',
        html,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']og:image["\']',
        html,
        re.I,
    )
    return m.group(1) if m else None


def extract_body_inner(html: str) -> str | None:
    m = re.search(
        r'<article[^>]*>.*?<div class="container">(.*?)</div>\s*</article>',
        html,
        re.S | re.I,
    )
    if m:
        return m.group(1).strip()
    for cls in ("container", "c"):
        m = re.search(rf'<div class="{cls}">(.*?)</div>', html, re.S | re.I)
        if m:
            return m.group(1).strip()
    return None


def first_paragraph(html: str) -> str:
    m = re.search(r"<p>(.*?)</p>", html, re.S | re.I)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()[:300]


def rebuild_sidebar_toc(html: str) -> str:
    """Replace walking TOC links with headings from restored article body."""
    article_m = re.search(
        r'<article class="article-body">(.*?)</article>',
        html,
        re.S | re.I,
    )
    if not article_m:
        return html
    body = article_m.group(1)
    headings: list[tuple[str, str]] = []
    for m in re.finditer(
        r'<h2[^>]*(?:id=["\']([^"\']*)["\'])?[^>]*>(.*?)</h2>',
        body,
        re.S | re.I,
    ):
        hid = (m.group(1) or "").strip()
        label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not label or "walking-health-benefits" in hid:
            continue
        if not hid:
            hid = label.replace(" ", "-")
        headings.append((hid, label))
    if not headings:
        return html
    toc_items = "\n".join(
        f'<a href="#{hid}" class="toc-item">{label}</a>' for hid, label in headings[:12]
    )
    patterns = [
        r'<nav class="sidebar-toc"[^>]*>.*?</nav>',
        r'<div class="sidebar-module sidebar-toc"[^>]*>.*?</div>\s*(?=<div class="sidebar-module|$)',
    ]
    for pat in patterns:
        if re.search(pat, html, re.S):
            return re.sub(
                pat,
                f'<div class="sidebar-module sidebar-toc"><h4>📑 Contents</h4> {toc_items}\n</div>',
                html,
                count=1,
                flags=re.S,
            )
    return html


def extract_banner_h1(html: str) -> str | None:
    m = re.search(
        r'<h1 class="article-banner-title"[^>]*>(.*?)</h1>',
        html,
        re.S | re.I,
    )
    return m.group(1).strip() if m else None


def remove_stuffing_block(html: str) -> str:
    return re.sub(
        r'\n*<h2 id="walking-health-benefits">.*?(?=</article>)',
        "\n",
        html,
        flags=re.S,
    )


def replace_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)


def replace_meta_description(html: str, desc: str) -> str:
    esc = desc.replace('"', "&quot;")
    if re.search(r'<meta[^>]+name=["\']description["\']', html, re.I):
        return re.sub(
            r'(<meta[^>]+name=["\']description["\'][^>]+content=["\'])([^"\']*)(["\'])',
            rf"\1{esc}\3",
            html,
            count=1,
            flags=re.I,
        )
    return html


def replace_og_image(html: str, url: str) -> str:
    return re.sub(
        r'(<meta[^>]+property=["\']og:image["\'][^>]+content=["\'])([^"\']*)(["\'])',
        rf"\1{url}\3",
        html,
        count=1,
        flags=re.I,
    )


def replace_banner_h1(html: str, h1: str) -> str:
    return re.sub(
        r'(<h1 class="article-banner-title"[^>]*>)(.*?)(</h1>)',
        rf"\1{h1}\3",
        html,
        count=1,
        flags=re.S,
    )


def replace_container(html: str, inner: str) -> str:
    return replace_article_body_container(html, inner)


def replace_article_body_container(html: str, inner: str) -> str:
    """Replace article body with restored container; drop walking tail garbage."""
    m = re.search(
        r'(<article class="article-body">)(.*?)(</article>)',
        html,
        re.S | re.I,
    )
    if not m:
        return re.sub(
            r'(<div class="container">)(.*?)(</div>)',
            rf"\1\n\n{inner}\n\n\3",
            html,
            count=1,
            flags=re.S,
        )
    hero_m = re.search(
        r'<figure class="hero">.*?</figure>\s*',
        m.group(2),
        re.S | re.I,
    )
    hero = hero_m.group(0) if hero_m else ""
    new_article = (
        f'{m.group(1)}{hero}<div class="container">\n\n{inner}\n\n</div>\n{m.group(3)}'
    )
    return html[: m.start()] + new_article + html[m.end() :]


def replace_hero_images(html: str, src: str, alt: str = "") -> str:
    html = re.sub(
        r'(<img[^>]+src=["\'])([^"\']*hero-daily-walking-benefits\.webp)(["\'])',
        rf"\1{src}\3",
        html,
    )
    return html


def update_article_json_ld(html: str, headline: str, description: str, image: str) -> str:
    out: list[str] = []
    pos = 0
    for m in re.finditer(r'<script type="application/ld\+json">\s*', html, re.I):
        out.append(html[pos : m.start()])
        start = m.end()
        end = html.find("</script>", start)
        if end == -1:
            out.append(html[m.start() :])
            return "".join(out)
        raw = html[start:end].strip()
        block = raw
        try:
            data = json.loads(raw)
            if data.get("@type") == "Article":
                data["headline"] = headline
                if description:
                    data["description"] = description
                data["image"] = image
                block = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        except json.JSONDecodeError:
            pass
        out.append(f'<script type="application/ld+json">{block}</script>')
        pos = end + len("</script>")
    out.append(html[pos:])
    return "".join(out)


def remove_walking_faq_json(html: str) -> str:
    """Drop generic/walking FAQ blocks; DEEPEN pass will rebuild proper FAQ."""

    def is_bad_faq(data: dict) -> bool:
        if data.get("@type") != "FAQPage":
            return False
        entities = data.get("mainEntity") or []
        if not entities:
            return False
        first_q = (entities[0].get("name") or "").lower()
        if "walk" in first_q or "مشي" in first_q:
            return True
        if "ما هو الموضوع الرئيسي لهذه المقالة" in (entities[0].get("name") or ""):
            return True
        return False

    out: list[str] = []
    pos = 0
    for m in re.finditer(r'<script type="application/ld\+json">\s*', html, re.I):
        out.append(html[pos : m.start()])
        start = m.end()
        end = html.find("</script>", start)
        if end == -1:
            out.append(html[m.start() :])
            return "".join(out)
        raw = html[start:end].strip()
        keep = True
        try:
            data = json.loads(raw)
            if is_bad_faq(data):
                keep = False
        except json.JSONDecodeError:
            pass
        if keep:
            out.append(f'<script type="application/ld+json">{raw}</script>')
        pos = end + len("</script>")
    out.append(html[pos:])
    return "".join(out)


def fix_share_urls(html: str, title: str) -> str:
    enc = title.replace(" ", "%20")
    html = re.sub(
        r'wa\.me/\?text=[^"&]+',
        f"wa.me/?text={enc}%20",
        html,
    )
    html = re.sub(
        r'twitter\.com/intent/tweet\?text=[^&]+',
        f"twitter.com/intent/tweet?text={enc}",
        html,
    )
    return html


def restore_file(rel: str) -> bool:
    path = ROOT / rel
    if not path.exists():
        print(f"SKIP missing {rel}")
        return False
    try:
        old = git_show(rel)
    except subprocess.CalledProcessError:
        print(f"SKIP no git parent for {rel}")
        return False

    current = path.read_text(encoding="utf-8")
    title = extract_tag(old, "title")
    desc = extract_meta(old, "description") or ""
    container = extract_body_inner(old)
    banner_h1 = extract_banner_h1(old) or extract_tag(old, "h1")
    if not title or not container:
        print(f"SKIP incomplete old content {rel}")
        return False

    body_h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", container, re.S | re.I)
    body_h1 = re.sub(r"<[^>]+>", "", body_h1_m.group(1)).strip() if body_h1_m else ""
    if body_h1 and (not title or any(m in title for m in WALKING_TITLE_MARKERS)):
        title = f"{body_h1} | DOTFORLIFE"
    if body_h1 and (not banner_h1 or any(m in banner_h1 for m in WALKING_TITLE_MARKERS)):
        banner_h1 = body_h1
    if any(m in desc for m in ("المشي اليومي", "daily walking", "half an hour of walking")):
        desc = first_paragraph(container) or desc

    stem = stem_from_path(rel)
    img = hero_url(stem) or extract_og_image(old) or ""
    src = local_hero_src(stem) or img.replace("https://dotforlife.com", "")

    out = current
    out = replace_title(out, title)
    out = replace_meta_description(out, desc)
    if img:
        out = replace_og_image(out, img)
    if banner_h1:
        out = replace_banner_h1(out, banner_h1)
    out = replace_container(out, container)
    out = remove_stuffing_block(out)
    if src:
        out = replace_hero_images(out, src)
    headline = body_h1 or banner_h1 or title.split("|")[0].strip()
    out = update_article_json_ld(out, headline, desc, img)
    out = remove_walking_faq_json(out)
    out = fix_share_urls(out, headline)
    out = rebuild_sidebar_toc(out)

    if out != current:
        path.write_text(out, encoding="utf-8")
        print(f"RESTORED {rel}")
        return True
    print(f"UNCHANGED {rel}")
    return False


def is_walking_title(html: str) -> bool:
    title = extract_tag(html, "title") or ""
    return any(m in title for m in WALKING_TITLE_MARKERS)


def fix_hero_only(rel: str) -> bool:
    if any(s in rel for s in SKIP_GLOBS):
        return False
    if rel in RESTORE_PATHS:
        return False
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if WALKING_HERO not in text:
        return False
    if is_walking_title(text):
        return False

    stem = stem_from_path(rel)
    src = local_hero_src(stem)
    img = hero_url(stem)
    if not src or not img:
        print(f"SKIP hero-only (no map) {rel}")
        return False

    out = text
    out = replace_og_image(out, img)
    out = update_article_json_ld(
        out,
        extract_tag(out, "title") or "",
        extract_meta(out, "description") or "",
        img,
    )
    # Banner + in-article hero only — keep walking thumb on links to walking article.
    out = re.sub(
        r'(<(?:section class="article-banner"|figure class="hero")[^>]*>.*?<img[^>]+src=["\'])([^"\']*hero-daily-walking-benefits\.webp)(["\'])',
        rf"\1{src}\3",
        out,
        flags=re.S,
    )
    if out != text:
        path.write_text(out, encoding="utf-8")
        print(f"HERO-FIX {rel}")
        return True
    return False


def clean_walking_faq_all() -> int:
    n = 0
    for path in ROOT.rglob("*.html"):
        rel = str(path.relative_to(ROOT))
        if any(s in rel for s in SKIP_GLOBS):
            continue
        text = path.read_text(encoding="utf-8")
        cleaned = remove_walking_faq_json(text)
        if cleaned != text:
            path.write_text(cleaned, encoding="utf-8")
            print(f"FAQ-CLEAN {rel}")
            n += 1
    return n


def main() -> int:
    restored = sum(restore_file(p) for p in RESTORE_PATHS)

    hero_fixed = 0
    for path in ROOT.rglob("*.html"):
        rel = str(path.relative_to(ROOT))
        if fix_hero_only(rel):
            hero_fixed += 1

    faq_cleaned = clean_walking_faq_all()

    print(f"\nDone: restored={restored}, hero_fixed={hero_fixed}, faq_cleaned={faq_cleaned}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
