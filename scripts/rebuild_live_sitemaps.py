#!/usr/bin/env python3
"""Rebuild sitemap index + content/main/tools for LIVE indexable pages only.

Uses apex https://dotforlife.com and extensionless paths so Cloudflare's
.html→pretty rewrite does not inflate GSC "Page with redirect".
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://dotforlife.com"
TODAY = date.today().isoformat()

CONTENT_DIRS = [
    "blog",
    "peace-capsules",
    "finance-wealth",
    "health",
    "fitness",
    "productivity",
    "islamic-hajj-umrah",
    "real-estate",
    "featured-stories",
    "comparisons",
    "guides",
    "travel",
    "health-pregnancy",
    "cities",
    "library/recipes",
    "makkah",
]

HUB_FILES = [
    "index.html",
    "health.html",
    "finance.html",
    "real-estate.html",
    "travel.html",
    "islamic.html",
    "family.html",
    "fitness.html",
    "productivity.html",
    "plants.html",
    "blog.html",
    "library.html",
    "about.html",
    "our-vision.html",
    "contact.html",
    "editorial-standards.html",
    "privacy-policy.html",
    "terms.html",
    "pregnancy-journey.html",
    "life-guide.html",
    "life-tools.html",
]

# Redirect stubs / junk never go in sitemap
SKIP_NAMES = {
    "home.html",
    "riyadh.html",
    "jeddah.html",
    "dubai.html",
    "abu-dhabi.html",
    "oman.html",
    "realestate.html",
    "404.html",
    "admin.html",
    "archive.html",
    "review.html",
    "capsule.html",
    "brand-guide.html",
    "notes.html",
    "tasks.html",
    "daily-planner.html",
    "sec1.html",
    "sec2.html",
    "sec3.html",
    "sec4.html",
    "sec5.html",
    "sec6.html",
    "privacy.html",
}


def is_noindex(html: str) -> bool:
    head = html[:2500]
    return bool(re.search(r'name=["\']robots["\'][^>]*noindex', head, re.I))


def is_redirect_stub(html: str) -> bool:
    head = html[:1200]
    return ("http-equiv=\"refresh\"" in head) or ("location.replace" in head)


def to_loc(rel_posix: str) -> str:
    if rel_posix.endswith("/index.html"):
        return BASE + "/" + rel_posix[: -len("/index.html")]
    if rel_posix == "index.html":
        return BASE + "/"
    if rel_posix.endswith(".html"):
        return BASE + "/" + rel_posix[:-5]
    return BASE + "/" + rel_posix


def url_entry(loc: str, priority: str = "0.7", changefreq: str = "monthly") -> str:
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def collect_live(paths: list[Path]) -> list[str]:
    locs: list[str] = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.name in SKIP_NAMES and path.parent == ROOT:
            continue
        if path.name == "emergency-fund-calculator.html":
            continue
        if path.name.startswith("gcc-family-budget.html") or path.name.startswith(
            "gcc-family-budget-en.html"
        ):
            # stub aliases
            if "location.replace" in path.read_text(encoding="utf-8", errors="ignore")[:800]:
                continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if is_noindex(html) or is_redirect_stub(html):
            continue
        if re.search(r'http-equiv=["\']refresh', html[:2000], re.I):
            continue
        locs.append(to_loc(rel))
    return sorted(set(locs))


def write_urlset(path: Path, locs: list[str], priority: str, changefreq: str) -> int:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n',
    ]
    for loc in locs:
        parts.append(url_entry(loc, priority=priority, changefreq=changefreq))
    parts.append("</urlset>\n")
    path.write_text("".join(parts), encoding="utf-8")
    return len(locs)


def main() -> None:
    hub_paths = [ROOT / name for name in HUB_FILES if (ROOT / name).exists()]
    content_paths: list[Path] = []
    for folder in CONTENT_DIRS:
        d = ROOT / folder
        if not d.exists():
            continue
        content_paths.extend(sorted(d.rglob("*.html")))

    tools_paths = sorted((ROOT / "tools").glob("*.html")) if (ROOT / "tools").exists() else []

    hubs = collect_live(hub_paths)
    content = collect_live(content_paths)
    tools = collect_live(tools_paths)

    n_main = write_urlset(ROOT / "sitemap-main.xml", hubs, "0.9", "weekly")
    n_content = write_urlset(ROOT / "sitemap-content.xml", content, "0.7", "monthly")
    n_tools = write_urlset(ROOT / "sitemap-tools.xml", tools, "0.6", "monthly")

    # Keep sitemap.xml as a small hub mirror for older GSC submissions
    write_urlset(ROOT / "sitemap.xml", hubs[:40], "0.9", "weekly")

    index = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <sitemap>\n"
        f"    <loc>{BASE}/sitemap-main.xml</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "  </sitemap>\n"
        "  <sitemap>\n"
        f"    <loc>{BASE}/sitemap-content.xml</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "  </sitemap>\n"
        "  <sitemap>\n"
        f"    <loc>{BASE}/sitemap-tools.xml</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "  </sitemap>\n"
        "</sitemapindex>\n"
    )
    (ROOT / "sitemap-index.xml").write_text(index, encoding="utf-8")

    print(
        json.dumps(
            {
                "sitemap-main": n_main,
                "sitemap-content": n_content,
                "sitemap-tools": n_tools,
                "total_live_urls": n_main + n_content + n_tools,
                "index": "sitemap-index.xml",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
