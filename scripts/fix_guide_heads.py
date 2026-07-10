#!/usr/bin/env python3
"""Fix broken guide <head> sections: raw JS, unclosed gtag scripts, og:image inside scripts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GUIDES = [
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

# Correct og:image per slug (from image-manifest or body hero)
OG_IMAGES = {
    "complete-life-guide": "https://dotforlife.com/d4l1.webp",
    "indoor-plants-saudi-arabia": "https://dotforlife.com/assets/images/approved/hero-indoor-plants-saudi-arabia.webp",
    "mecca-medina": "https://dotforlife.com/assets/images/hero-mecca-medina.webp",
    "ramadan-nutrition-guide": "https://dotforlife.com/assets/images/approved/hero-ramadan-nutrition-guide.webp",
    "salalah-oman": "https://dotforlife.com/assets/images/hero-salalah-oman.webp",
    "saudi-mortgage-guide": "https://dotforlife.com/assets/images/approved/hero-saudi-mortgage-guide.webp",
    "saudi-real-estate-investing": "https://dotforlife.com/assets/images/approved/hero-saudi-real-estate-investing.webp",
    "saudi-tourism": "https://dotforlife.com/assets/images/hero-saudi-tourism.webp",
    "zakat-complete-guide": "https://dotforlife.com/assets/images/approved/hero-zakat-complete-guide.webp",
}

THEME_BLOCK = re.compile(
    r"(?:<script>\s*)?\(function\(\)\{\s*/\*\s*theme\s*\*/.*?"
    r"document\.querySelectorAll\([\"']\.reveal[\"']\).*?\}\)\(\);(?:\s*</script>)?",
    re.DOTALL,
)

# Raw analytics block (no opening <script>) through DFL_FIX3 marker
RAW_ANALYTICS = re.compile(
    r"(?:<!-- DFL Analytics v1 -->\s*)?"
    r"(?:<script>\s*)?"
    r"window\.dataLayer=window\.dataLayer\|\|\[\];.*?;"
    r"\s*(?:<!-- DFL_FIX3_APPLIED -->\s*)?"
    r"(?:</script>\s*)?",
    re.DOTALL,
)

# gtag config line with meta tags jammed on same line
GTAG_META_INLINE = re.compile(
    r"gtag\('config',\s*'G-3G1XPV4F0G'\);\s*"
    r"(<meta property=\"og:image\"[^>]+/>)\s*"
    r"(?:<meta name=\"twitter:image\"[^>]+/>)?",
    re.DOTALL,
)

CLEAN_ANALYTICS = """<!-- DFL Analytics v1 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());
gtag('config','G-3G1XPV4F0G',{
  page_title:document.title,
  page_location:window.location.href,
  send_page_view:true,
  cookie_flags:'SameSite=None;Secure'
});
window.dflTrack=function(event,params){
  gtag('event',event,Object.assign({
    page_path:location.pathname,
    language:document.documentElement.getAttribute('data-lang')||'en'
  },params||{}));
};
</script>"""


def slug_from_path(path: str) -> str:
    return Path(path).stem


def fix_dfl_sys_css(text: str) -> str:
    """Remove stray 'nav' lines inside #dfl-sys style block."""
    return re.sub(
        r"(<style id=\"dfl-sys\">)\s*\n\s*nav\s*\n\s*nav\s*\n",
        r"\1\n",
        text,
        count=1,
    )


def ensure_og_meta(text: str, slug: str) -> str:
    og = OG_IMAGES[slug]
    twitter = og
    meta_block = (
        f'  <meta property="og:image" content="{og}"/>\n'
        f'  <meta name="twitter:image" content="{twitter}"/>\n'
        f'  <meta name="twitter:card" content="summary_large_image"/>\n'
    )
    # Remove any existing og:image / twitter:image in head
    head_end = text.find("</head>")
    if head_end == -1:
        return text
    head = text[:head_end]
    body = text[head_end:]
    head = re.sub(r'\s*<meta property="og:image"[^>]+/>\s*', "\n", head)
    head = re.sub(r'\s*<meta name="twitter:image"[^>]+/>\s*', "\n", head)
    # Insert before </head> if not already present with correct URL
    if f'content="{og}"' not in head:
        head = head.rstrip() + "\n" + meta_block
    return head + body


ORPHAN_ANALYTICS = re.compile(
    r"\n\}\s*\n"
    r"(?:gtag\('js'.*?\n)?"
    r"gtag\('config'.*?\n"
    r"(?:  [^\n]+\n)*"
    r"\}\);\s*\n"
    r"(?://[^\n]+\n)?"
    r"window\.dflTrack=function\(event,params\)\{.*?\}\);\s*"
    r"(?:<!-- DFL_FIX3_APPLIED -->\s*)?"
    r"(?:</script>\s*)?",
    re.DOTALL,
)

BROKEN_GTAG_LINE = re.compile(
    r"\n\}gtag\('js',new Date\(\)\);gtag\('config','G-3G1XPV4F0G'\);</script>\s*",
    re.MULTILINE,
)

DUPLICATE_GTAG_BLOCK = re.compile(
    r"<!-- Google tag \(gtag\.js\) -->\s*"
    r"<script>\s*"
    r"window\.dataLayer = window\.dataLayer \|\| \[\];\s*"
    r"function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*"
    r"window\.dataLayer = window\.dataLayer \|\| \[\];\s*"
    r"function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*"
    r"gtag\('js', new Date\(\)\);\s*"
    r"gtag\('config', 'G-3G1XPV4F0G'\);\s*"
    r"</script>\s*",
    re.DOTALL,
)


BROKEN_PARTIAL_ANALYTICS = re.compile(
    r"\n(?:gtag\('js',new Date\(\)\);\s*\n)?"
    r"gtag\('config','G-3G1XPV4F0G',\{.*?"
    r"<!-- DFL_FIX3_APPLIED -->\s*</script>\s*",
    re.DOTALL,
)


def scrub_orphan_analytics(text: str) -> str:
    text = BROKEN_PARTIAL_ANALYTICS.sub("\n", text)
    text = ORPHAN_ANALYTICS.sub("\n", text)
    text = BROKEN_GTAG_LINE.sub("\n", text)
    text = DUPLICATE_GTAG_BLOCK.sub("", text)
    # Lone closing brace before style/comments
    text = re.sub(
        r"(<link rel=\"stylesheet\"[^>]+>)\s*\n\}\s*\n",
        r"\1\n",
        text,
    )
    return text


def ensure_clean_analytics(text: str) -> str:
    head_end = text.find("</head>")
    if head_end == -1:
        return text
    head_only = text[:head_end]
    rest = text[head_end:]
    if (
        "window.dflTrack=function" in head_only
        and '<script async src="https://www.googletagmanager.com/gtag/js' in head_only
        and "window.dataLayer=window.dataLayer||[]" in head_only
        and "<!-- DFL_FIX3_APPLIED -->" not in head_only
    ):
        return text
    insert_at = head_only.find("<!-- ═══ PHASE 3C")
    if insert_at == -1:
        insert_at = head_only.find('<style id="dfl-sys"')
    if insert_at == -1:
        insert_at = head_only.find("<style>")
    if insert_at == -1:
        insert_at = len(head_only)
    head_only = head_only[:insert_at] + CLEAN_ANALYTICS + "\n\n" + head_only[insert_at:]
    return head_only + rest


def dedupe_dfltrack_scripts(text: str) -> str:
    """Keep one inline gtag/dflTrack script block in head."""
    head_end = text.find("</head>")
    if head_end == -1:
        return text
    head, rest = text[:head_end], text[head_end:]
    pattern = re.compile(
        r"<script>\s*function gtag\(\).*?window\.dflTrack=function.*?;\s*</script>\s*",
        re.DOTALL,
    )
    matches = list(pattern.finditer(head))
    if len(matches) <= 1:
        return text
    for m in reversed(matches[1:]):
        head = head[: m.start()] + head[m.end() :]
    return head + rest


def remove_fix3_markers(text: str) -> str:
    return (
        text.replace("}; <!-- DFL_FIX3_APPLIED -->", "};")
        .replace("<!-- DFL_FIX3_APPLIED -->", "")
    )


def dedupe_analytics_blocks(text: str) -> str:
    """Keep a single DFL Analytics block in <head>."""
    head_end = text.find("</head>")
    if head_end == -1:
        return text
    head, rest = text[:head_end], text[head_end:]
    marker = "<!-- DFL Analytics v1 -->"
    first = head.find(marker)
    if first == -1:
        return text
    second = head.find(marker, first + len(marker))
    if second == -1:
        return text
    # Remove second and subsequent analytics blocks up to next </script>
    while True:
        pos = head.find(marker, first + len(marker))
        if pos == -1:
            break
        end = head.find("</script>", pos)
        if end == -1:
            break
        head = head[:pos] + head[end + len("</script>") :]
    return head.lstrip("\n") if False else head + rest


def dedupe_head_scripts(text: str) -> str:
    """Remove duplicate gtag blocks and duplicate JSON-LD Article blocks in head."""
    head_end = text.find("</head>")
    if head_end == -1:
        return text
    head, rest = text[:head_end], text[head_end:]
    # Keep first gtag async loader only
    seen_gtag_async = False
    lines = head.split("\n")
    out: list[str] = []
    skip_until_close = False
    for line in lines:
        if 'googletagmanager.com/gtag/js' in line:
            if seen_gtag_async:
                continue
            seen_gtag_async = True
        if skip_until_close:
            if "</script>" in line:
                skip_until_close = False
            continue
        if line.strip() == "<script>" and out and "dataLayer" in "\n".join(out[-3:]):
            skip_until_close = True
            continue
        if "window.dataLayer=window.dataLayer||[]" in line and "<script>" not in line:
            continue
        out.append(line)
    return "\n".join(out) + rest


def fix_file(path: Path) -> bool:
    slug = slug_from_path(str(path.relative_to(ROOT)))
    original = path.read_text(encoding="utf-8")
    text = original

    text = THEME_BLOCK.sub("", text)
    text = RAW_ANALYTICS.sub("", text)

    # Fix inline gtag+meta pattern
    def _close_script(m: re.Match) -> str:
        return "gtag('config', 'G-3G1XPV4F0G');\n</script>\n  " + m.group(1)

    text = GTAG_META_INLINE.sub(_close_script, text)

    text = scrub_orphan_analytics(text)
    text = remove_fix3_markers(text)
    text = fix_dfl_sys_css(text)
    text = ensure_clean_analytics(text)
    text = dedupe_analytics_blocks(text)
    text = dedupe_dfltrack_scripts(text)
    text = ensure_og_meta(text, slug)
    text = dedupe_head_scripts(text)

    # Normalize duplicate blank lines in head
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = []
    for rel in GUIDES:
        p = ROOT / rel
        if not p.exists():
            print(f"SKIP missing: {rel}")
            continue
        if fix_file(p):
            changed.append(rel)
            print(f"FIXED: {rel}")
        else:
            print(f"OK (no change): {rel}")
    print(f"\n{len(changed)} file(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
