#!/usr/bin/env python3
"""Amer batch: fix header/footer/sidebar structure on 17 pages."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOOTER = (ROOT / "partials" / "footer.html").read_text(encoding="utf-8").strip()

THEME_SCRIPT = """<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),h=document.documentElement,l=p.get("lang")||h.getAttribute("data-lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||h.getAttribute("data-theme")||"light";h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);})()</script>"""

CSS_LINKS = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?v=20260624n">
  <link rel="stylesheet" href="/styles/home.css?v=20260617b">
  <link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
"""

TAIL_SCRIPTS = """
<script src="/scripts/global.js?v=20260625" defer></script>
<script>
(function(){
  var bar = document.getElementById('reading-progress');
  if(bar){
    window.addEventListener('scroll',function(){
      var h = document.documentElement;
      var total = h.scrollHeight - h.clientHeight;
      var pct = (h.scrollTop || document.body.scrollTop) / (total || 1) * 100;
      bar.style.width = pct + '%';
    },{passive:true});
  }
  var tocLinks = document.querySelectorAll('.toc-item');
  if(tocLinks.length){
    var headings = [];
    tocLinks.forEach(function(link){
      var id = link.getAttribute('href').replace('#','');
      var el = document.getElementById(id);
      if(el) headings.push({el:el,link:link});
    });
    window.addEventListener('scroll',function(){
      var scrollY = window.scrollY + 130;
      var current = null;
      headings.forEach(function(h){
        if(h.el.offsetTop <= scrollY) current = h;
      });
      tocLinks.forEach(function(l){ l.classList.remove('is-active'); });
      if(current) current.link.classList.add('is-active');
    },{passive:true});
  }
})();
</script>
"""

ADD_FOOTER = [
    "fitness/calorie-calculator-saudi.html",
    "fitness/fitness-for-women-saudi.html",
    "fitness/ramadan-calorie-calculator.html",
]

REMOVE_DFL_FOOTER = [
    "guides/bmi-guide-arabs-gcc.html",
    "guides/complete-life-guide.html",
    "guides/indoor-plants-saudi-arabia.html",
    "guides/mecca-medina.html",
    "guides/ramadan-nutrition-guide.html",
    "guides/salalah-oman.html",
    "guides/saudi-mortgage-guide.html",
    "guides/saudi-real-estate-investing.html",
    "guides/saudi-tourism.html",
    "guides/zakat-complete-guide.html",
]

REPLACE_FOOTER = [
    "blog/masjid-nabawi-complete-guide-en.html",
    "peace-capsules/art-of-apologizing-en.html",
]

REBUILD = {
    "productivity/family-time-management.html": "finance-wealth/barakah-budget-family-finance.html",
    "productivity/family-time-management-en.html": "finance-wealth/barakah-budget-family-finance-en.html",
    "finance-wealth/teaching-children-savings.html": "finance-wealth/barakah-budget-family-finance.html",
}

ALL_FILES = ADD_FOOTER + list(REBUILD) + REMOVE_DFL_FOOTER + REPLACE_FOOTER


def extract_between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start))
    if j < 0:
        return ""
    return text[i : j + len(end)]


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def get_robots_meta(html: str) -> str | None:
    """
    Return the exact robots content (e.g. 'noindex,nofollow') if present.
    Do not normalize; we want to detect any change.
    """
    m = re.search(
        r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']\s*/?>',
        html,
        flags=re.IGNORECASE,
    )
    return m.group(1) if m else None


def assert_robots_unchanged(before: str, after: str, rel: str) -> None:
    b = get_robots_meta(before)
    a = get_robots_meta(after)
    if b != a:
        raise RuntimeError(
            f'{rel}: robots changed (before={b!r}, after={a!r}). '
            "This batch forbids robots edits."
        )


def remove_dfl_footer(html: str) -> str:
    html = re.sub(
        r"<!--\s*DFL CANONICAL FOOTER\s*-->[\s\S]*?<footer\s+id=[\"']dfl-footer[\"'][\s\S]*?</footer>",
        "",
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"<footer\s+id=[\"']dfl-footer[\"'][\s\S]*?</footer>",
        "",
        html,
        flags=re.IGNORECASE,
    )
    return html


def replace_site_footer(html: str) -> str:
    html = re.sub(
        r"<!--\s*═+\s*UNIFIED FOOTER[\s\S]*?<!--\s*═+\s*END FOOTER\s*═+\s*-->",
        FOOTER,
        html,
        flags=re.IGNORECASE,
    )
    if 'class="site-footer"' in html:
        html = re.sub(
            r"<footer\s+class=[\"']site-footer[\"'][\s\S]*?</footer>",
            FOOTER.replace("<!-- ═══ UNIFIED FOOTER ══════════════════════════════════════ -->\n", "")
            .replace("\n<!-- ═══ END FOOTER ══════════════════════════════════════ -->", ""),
            html,
            count=1,
            flags=re.IGNORECASE,
        )
    return html


def add_missing_footer(html: str) -> str:
    if 'class="site-footer"' in html:
        return html
    insert = "\n\n" + FOOTER + "\n"
    if "global.js" not in html:
        insert += TAIL_SCRIPTS
    else:
        insert += "\n"
    return html.replace("</body>", insert + "</body>", 1)


def extract_ref_shell(ref_path: Path) -> dict[str, str]:
    ref = ref_path.read_text(encoding="utf-8")
    nav = extract_between(ref, "<div id=\"reading-progress\"", "<!-- ═══ END HEADER ══════════════════════════════════════ -->")
    sm = re.search(r'<aside class="article-sidebar">([\s\S]*?)</aside>', ref)
    sidebar = sm.group(1).strip() if sm else ""
    return {"nav": nav, "sidebar": sidebar}


def enhance_head(head: str, lang: str) -> str:
    if "data-theme" not in head and THEME_SCRIPT.strip() not in head:
        head = head.replace("<head>", "<head>\n" + THEME_SCRIPT, 1)
    if "/styles/global.css" not in head:
        head = head.replace("</head>", CSS_LINKS + "\n</head>", 1)
    if lang == "ar":
        head = re.sub(
            r"<html([^>]*)>",
            r'<html\1 data-lang="ar" data-theme="light">',
            head,
            count=1,
        )
        if 'dir="rtl"' not in head and "dir=" not in head[:200]:
            head = re.sub(r"<html([^>]*)>", r'<html lang="ar" dir="rtl"\1>', head, count=1)
    else:
        head = re.sub(
            r"<html([^>]*)>",
            r'<html lang="en" dir="ltr" data-lang="en" data-theme="light"\1>',
            head,
            count=1,
        )
    return head


def extract_body_content(html: str) -> str:
    m = re.search(r"<body[^>]*>([\s\S]*)</body>", html, flags=re.IGNORECASE)
    if not m:
        return ""
    body = m.group(1).strip()
    am = re.search(r'<article[^>]*class=["\']article-body["\'][^>]*>([\s\S]*)</article>', body, flags=re.IGNORECASE)
    if am:
        return am.group(1).strip()
    return body


def first_h1_text(content: str) -> str:
    m = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", content, flags=re.IGNORECASE)
    if not m:
        return "Article"
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def og_image(head: str, content: str) -> str:
    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', head, flags=re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content, flags=re.IGNORECASE)
    return m.group(1) if m else "/assets/images/logo1-footer.webp"


def meta_spans(content: str) -> tuple[str, str]:
    m = re.search(r'<div\s+class=["\']meta["\'][^>]*>([\s\S]*?)</div>', content, flags=re.IGNORECASE)
    if not m:
        return ("", "")
    inner = m.group(1)
    spans = re.findall(r"<span[^>]*>([\s\S]*?)</span>", inner, flags=re.IGNORECASE)
    spans = [re.sub(r"<[^>]+>", "", s).strip() for s in spans]
    date = spans[1] if len(spans) > 1 else ""
    read = spans[2] if len(spans) > 2 else ""
    return (date, read)


def rebuild_article(target_rel: str, ref_rel: str) -> str:
    target_path = ROOT / target_rel
    ref_path = ROOT / ref_rel
    original = target_path.read_text(encoding="utf-8")
    shell = extract_ref_shell(ref_path)

    head_m = re.search(r"<head[^>]*>([\s\S]*?)</head>", original, flags=re.IGNORECASE)
    head_inner = head_m.group(1) if head_m else ""
    head = "<head>" + head_inner + "</head>"
    lang = "en" if target_rel.endswith("-en.html") or 'lang="en"' in original[:500] else "ar"
    head = enhance_head(head, lang)

    content = extract_body_content(original)
    title = first_h1_text(content)
    banner_img = og_image(head, content)
    date, read_time = meta_spans(content)
    category = "إنتاجية" if "productivity" in target_rel else "المالية"
    if lang == "en":
        category = "Productivity" if "productivity" in target_rel else "Finance"

    banner = f"""
<div class="article-wrap">

<section class="article-banner" aria-label="Article banner">
  <div class="article-banner-img-wrap">
    <img src="{banner_img}" alt="" class="article-banner-img" width="1200" height="420" loading="eager" fetchpriority="high">
    <div class="article-banner-overlay">
      <div class="article-banner-cat">{category}</div>
      <h1 class="article-banner-title">{title}</h1>
      <div class="article-banner-meta">
        <span>{date or ('Jun 15, 2026' if lang == 'en' else '15 يونيو 2026')}</span>
        <span>{read_time or ('7 min read' if lang == 'en' else '٧ دقائق قراءة')}</span>
      </div>
    </div>
  </div>
</section>

<div class="article-layout">

<main class="article-main">
<article class="article-body">
<div class="container">
{content}
</div>
</article>
</main>

<aside class="article-sidebar">
{shell['sidebar']}
</aside>

</div><!-- /article-layout -->

</div><!-- /article-wrap -->
"""

    html = f"""<!DOCTYPE html>
<html>
{head}
<body data-template="article">

{shell['nav']}

{banner}

{FOOTER}

{TAIL_SCRIPTS}
</body>
</html>
"""
    return html


def validate(path: Path, html: str) -> list[str]:
    issues = []
    nav_count = count_pattern(html, r'id=["\']navbar["\']')
    footer_count = count_pattern(html, r'class=["\']site-footer["\']')
    dfl_count = count_pattern(html, r'id=["\']dfl-footer["\']')
    if nav_count != 1:
        issues.append(f"nav={nav_count} (expected 1)")
    if footer_count != 1:
        issues.append(f"site-footer={footer_count} (expected 1)")
    if dfl_count:
        issues.append(f"dfl-footer={dfl_count} (expected 0)")
    cols = len(re.findall(r'<div\s+class=["\']footer-col["\']', html))
    grid = "footer-links-grid" in html
    if footer_count == 1 and grid and cols < 4:
        issues.append(f"footer-cols={cols} (expected 4 in grid)")
    elif footer_count == 1 and not grid and cols < 4:
        issues.append(f"footer-cols={cols} (incomplete footer)")
    return issues


def process_file(rel: str) -> str:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    original_html = html
    action = "unchanged"

    if rel in REBUILD:
        html = rebuild_article(rel, REBUILD[rel])
        action = "rebuild"
    elif rel in ADD_FOOTER:
        html = add_missing_footer(html)
        action = "add-footer"
    elif rel in REMOVE_DFL_FOOTER:
        before = html
        html = remove_dfl_footer(html)
        action = "remove-dfl-footer" if html != before else "unchanged"
    elif rel in REPLACE_FOOTER:
        html = replace_site_footer(html)
        action = "replace-footer"

    issues = validate(path, html)
    if issues:
        raise RuntimeError(f"{rel}: validation failed — {', '.join(issues)}")

    assert_robots_unchanged(original_html, html, rel)
    path.write_text(html, encoding="utf-8")
    return action


def main() -> int:
    results = []
    for rel in ALL_FILES:
        action = process_file(rel)
        results.append((rel, action))
        print(f"OK  {rel}  ({action})")

    print("\n--- validation summary ---")
    for rel, action in results:
        html = (ROOT / rel).read_text(encoding="utf-8")
        issues = validate(ROOT / rel, html)
        status = "PASS" if not issues else "FAIL: " + ", ".join(issues)
        print(f"{status}  {rel}")

    print("\n--- amer_gate ---")
    cmd = ["python3", "scripts/amer_gate.py", *[str(ROOT / f) for f in ALL_FILES]]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
