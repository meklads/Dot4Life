#!/usr/bin/env python3
"""Surgical inject: deep article below Oman ROI calculator shell (Amer GO 2026-06-21)."""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "operating-system/reports/drafts/task07/oman-property-roi.md"
TARGET = ROOT / "real-estate/oman-property-roi.html"
BACKUP = ROOT / "outputs/backups/tech-build"
HERO = "/assets/images/hero-oman-property-roi.webp"
MARKER = "  <!-- RELATED TOOLS -->"

spec = importlib.util.spec_from_file_location(
    "build_draft", ROOT / "scripts/build-from-approved-draft.py"
)
build = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(build)

OMAN_CFG = {
    "id": "A-07-2",
    "lang_only": "en",
    "disclaimer_type": "financial",
    "out_en": TARGET,
}


def article_html_from_draft(md: str) -> tuple[str, list[tuple[str, str]], str]:
    """Body HTML (no FAQ), FAQ pairs, disclaimer block."""
    cut, _ = build.split_at_faq(md)
    cut = re.split(r"\n---\n|\nSources:", cut)[0]
    cut = re.split(r"\nSuggested internal links:", cut)[0].strip()
    _, body = build.md_body_html(cut, "en")
    disclaimer = build.extract_disclaimer_html(md)
    faqs = build.parse_faq(md)
    return body, faqs, disclaimer


def article_section(body: str, disclaimer: str) -> str:
    links = (
        '<p style="margin-top:24px;font-size:14px;color:var(--muted,#666)">'
        "<strong>Read also:</strong> "
        '<a href="/real-estate/rent-vs-buy-gulf-family-en.html">Rent vs buy for Gulf families</a> · '
        '<a href="/finance-wealth/investment-basics-beginners-en.html">Investment basics</a> · '
        '<a href="/blog/emergency-fund-calculator-guide-en.html">Emergency fund guide</a>'
        "</p>"
    )
    return f"""
  <!-- DFL SURGICAL ARTICLE (injected {date.today().isoformat()}) -->
  <section id="oman-roi-guide" class="card" style="margin-top:40px">
    <figure class="hero"><img src="{HERO}" alt="Muscat residential buildings and property investment guide"
           width="1200" height="750" loading="lazy"></figure>
    <h2 style="font-size:22px;font-weight:800;margin-bottom:16px">
      <span class="en">Muscat Property ROI: Complete Investor Guide</span>
      <span class="ar">دليل المستثمر: عائد العقار في مسقط</span>
    </h2>
    <div class="article-body" style="font-size:15px;line-height:1.85;color:var(--text,#333)">
      {body}
      {disclaimer}
      {links}
    </div>
  </section>
"""


def faqpage_json(faqs: list[tuple[str, str]]) -> str:
    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faqs
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def article_json(title: str, desc: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc[:300],
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": date.today().isoformat(),
        "dateModified": date.today().isoformat(),
        "image": f"https://dotforlife.com{HERO}",
        "mainEntityOfPage": "https://dotforlife.com/real-estate/oman-property-roi.html",
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def patch_head(page: str) -> str:
    title = "Oman Property ROI Guide | DOTFORLIFE"
    desc = (
        "Calculate Muscat rental yield and ROI: gross vs net yield, ITC ownership rules, "
        "costs, and a worked OMR example for Oman property investors."
    )
    page = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", page, count=1)
    page = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">',
        page,
        count=1,
    )
    if 'property="og:image"' not in page:
        page = page.replace(
            '<meta property="og:type" content="website" />',
            f'<meta property="og:type" content="article" />\n'
            f'<meta property="og:image" content="https://dotforlife.com{HERO}">',
            1,
        )
    return page


def patch_schema(page: str, faqs: list[tuple[str, str]]) -> str:
    """Replace FAQPage block; append Article schema before WebApplication."""
    art = article_json(
        "Oman Property ROI Calculator 2025: Muscat Real Estate Yield Explained",
        "Guide to Muscat rental yield, net ROI, foreign ownership in ITCs, and hidden costs.",
    )
    faq_block = faqpage_json(faqs)
    page = re.sub(
        r'<script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage"[\s\S]*?</script>',
        faq_block,
        page,
        count=1,
    )
    if '"@type":"Article"' not in page:
        page = page.replace(
            "<!-- Schema.org -->",
            f"<!-- Schema.org -->\n{art}",
            1,
        )
    return page


def main() -> None:
    if not DRAFT.exists():
        sys.exit(f"Draft missing: {DRAFT}")
    if not TARGET.exists():
        sys.exit(f"Target missing: {TARGET}")

    md = DRAFT.read_text(encoding="utf-8")
    body, faqs, disclaimer = article_html_from_draft(md)
    if len(faqs) < 4:
        sys.exit(f"FAQ parse failed: only {len(faqs)} questions")

    page = TARGET.read_text(encoding="utf-8")
    if "DFL SURGICAL ARTICLE" in page:
        print("Already injected — re-run skipped (delete marker to force)")
        return
    if MARKER not in page:
        sys.exit(f"Injection marker not found in {TARGET.name}")

    section = article_section(body, disclaimer)
    page = page.replace(MARKER, section + "\n" + MARKER, 1)
    page = patch_head(page)
    page = patch_schema(page, faqs)

    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)

    gates = build.assert_build_gates(page, "en", TARGET, OMAN_CFG, md)
    TARGET.write_text(page, encoding="utf-8")
    rel = TARGET.relative_to(ROOT)
    print(f"✅ Oman surgical inject OK — ALL GATES PASS ({', '.join(gates)}) → {rel}")


if __name__ == "__main__":
    main()
