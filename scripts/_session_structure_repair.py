#!/usr/bin/env python3
"""Structural repair for leftover deepen inventory (html5lib=0 target)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import html5lib
from html5lib import serialize

from _session_wave2_continue import balance_article_divs, fix_list_mismatches

GOOD_SHELL = Path("blog/teaching-children-financial-literacy.html")
_SHELL = GOOD_SHELL.read_text(encoding="utf-8")

GOOD_TAIL = """
<link rel="stylesheet" href="/styles/global.css?v=20260624n">
<link rel="stylesheet" href="/styles/home.css?v=20260608u">
<link rel="stylesheet" href="/styles/pages/articles.css?v=20260608u">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');</script>
"""


def _extract_body_chrome(html: str) -> tuple[str, str] | tuple[None, None]:
    m_aw = re.search(r'<div class="article-wrap">', html)
    m_ft = re.search(r"<footer\b", html)
    m_body = re.search(r"<body[^>]*>", html)
    m_body_end = re.search(r"</body>", html)
    if not (m_aw and m_ft and m_body and m_body_end):
        return None, None
    pre = html[m_body.end() : m_aw.end()]
    post = html[m_ft.start() : m_body_end.start()]
    return pre, post


_GOOD_PRE, _GOOD_POST = _extract_body_chrome(_SHELL)

_ARTICLE_END = ""
_m_end = re.search(
    r'(<div class="article-end">[\s\S]*?</div>)\s*</main>',
    _SHELL,
)
if _m_end:
    # depth-aware: find article-end opening and match closes
    start = _SHELL.find('<div class="article-end">')
    if start >= 0:
        i = start
        depth = 0
        while i < len(_SHELL):
            if _SHELL.startswith("<div", i):
                depth += 1
                i = _SHELL.find(">", i) + 1
                continue
            if _SHELL.startswith("</div>", i):
                depth -= 1
                i += len("</div>")
                if depth == 0:
                    _ARTICLE_END = _SHELL[start:i]
                    break
                continue
            i += 1

_SHELL_ASIDE = ""
_m_aside = re.search(r'<aside class="article-sidebar"[\s\S]*?</aside>', _SHELL, re.I)
if _m_aside:
    _SHELL_ASIDE = _m_aside.group(0)


def _rebuild_head(html: str) -> str:
    hm = re.search(r"<head\b[^>]*>([\s\S]*?)</head>", html, re.I)
    h = hm.group(1) if hm else ""
    # Fix known broken og:title / og:description glue (salalah-oman)
    h = re.sub(
        r'(<meta property="og:title" content="[^"]*)"\s*\n\s*<meta property="og:description" content="([^"]*)"\s*/>\s*/>',
        r'\1"/>\n<meta property="og:description" content="\2"/>',
        h,
    )
    h = re.sub(r'"\s*/>\s*/>', '"/>', h)
    metas: list[str] = []
    for pat in [
        r'<meta charset="[^"]*">',
        r'<meta name="viewport"[^>]*>',
        r"<title>[\s\S]*?</title>",
        r'<meta name="description"[^>]*>',
        r'<link rel="canonical"[^>]*>',
        r'<link rel="alternate"[^>]*>',
        r'<meta property="og:[^>]*>',
        r'<meta name="twitter:[^>]*>',
        r'<meta name="robots"[^>]*>',
        r'<meta name="author"[^>]*>',
        r'<link rel="icon"[^>]*>',
        r'<link rel="apple-touch-icon"[^>]*>',
    ]:
        for m in re.finditer(pat, h, re.I):
            tag = re.sub(r'"\s*/>\s*/>', '"/>', m.group(0))
            tag = re.sub(r'"\s*/\s*>\s*/>', '"/>', tag)
            if tag.count('"') % 2:
                continue
            if "<meta" in tag[1:] or "<link" in tag[1:] or "<title" in tag[1:]:
                continue  # glued tags
            metas.append(tag)
    seen: set[str] = set()
    out: list[str] = []
    for t in metas:
        k = t[:90]
        if k in seen:
            continue
        seen.add(k)
        out.append(t)
    if not any("charset" in t.lower() for t in out):
        out.insert(0, '<meta charset="UTF-8">')
    if not any("viewport" in t.lower() for t in out):
        out.insert(1, '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    # Fix salalah-oman broken og:description with trailing />/>
    out = [re.sub(r'"\s*/>\s*/>', '"/>', t) for t in out]

    ld: list[dict] = []
    for m in re.finditer(
        r'<script type="application/ld\+json">([\s\S]*?)</script>', html, re.I
    ):
        try:
            ld.append(json.loads(m.group(1).strip()))
        except Exception:
            continue
    by: dict[str, dict] = {}
    for d in ld:
        by["graph" if d.get("@graph") else str(d.get("@type"))] = d
    scripts = "".join(
        '<script type="application/ld+json">'
        + json.dumps(d, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n"
        for d in by.values()
    )
    new = "<head>\n" + "\n".join(out) + "\n" + scripts + GOOD_TAIL + "\n</head>"
    return re.sub(r"<head\b[^>]*>[\s\S]*?</head>", new, html, count=1, flags=re.I)


def _reserialize_fragment(inner: str) -> str:
    frag = f'<div id="dfl-fix">{inner}</div>'
    try:
        doc = html5lib.parse(frag, treebuilder="dom")
        out = serialize(
            doc,
            tree="dom",
            omit_optional_tags=False,
            alphabetical_attributes=False,
            quote_attr_values="always",
            use_trailing_solidus=False,
        )
    except Exception:
        return inner
    mm = re.search(r'<div id="dfl-fix">([\s\S]*?)</div>\s*</body>', out, re.I)
    if not mm:
        mm = re.search(r'<div id="dfl-fix">([\s\S]*?)</div>', out, re.I)
    if not mm:
        return inner
    new_inner = mm.group(1)
    if abs(len(new_inner) - len(inner)) > max(12000, len(inner) // 2):
        return inner
    return new_inner


def _extract_guide_prose(inner: str) -> str:
    """Guides/tools sometimes embed custom chrome inside <article> — keep prose only."""
    chrome = (
        '<div class="logo">' in inner
        or '<nav class="nav">' in inner
        or 'class="guide-hero"' in inner
        or 'class="hero-stats"' in inner
        or "hero-badge" in inner
        or "<!-- JUMP NAV -->" in inner
        or "<!-- TRUST BAR -->" in inner
        or 'class="tool-embed"' in inner
        or "hero-stat" in inner
    )
    if not chrome:
        return inner
    # Drop jump/trust chrome sections
    inner = re.sub(
        r"<!--\s*JUMP NAV\s*-->[\s\S]*?(?=<!--|<h[12])",
        "",
        inner,
        flags=re.I,
    )
    inner = re.sub(
        r"<!--\s*TRUST BAR\s*-->[\s\S]*?(?=<!--|<h[12])",
        "",
        inner,
        flags=re.I,
    )
    inner = re.sub(r'(?:<div class="hero-stats"[\s\S]*?</div>\s*)+', "", inner)
    while True:
        n = re.sub(r"^\s*</div>\s*", "", inner)
        if n == inner:
            break
        inner = n
    fig = re.search(r"<figure[\s\S]*?</figure>", inner, re.I)
    fig_html = fig.group(0) if fig else ""
    m = re.search(r"<h[12]\b[^>]*>[\s\S]*$", inner, re.I)
    if not m:
        return inner
    rest = m.group(0)
    rest = re.split(
        r'<footer\b|<nav class="nav">|<!--\s*═══\s*UNIFIED FOOTER',
        rest,
        maxsplit=1,
    )[0]
    return fig_html + "\n" + rest


def _flatten_to_safe_blocks(inner: str) -> str:
    """Last-resort: keep only heading/paragraph/faq blocks that serialize cleanly."""
    parts: list[str] = []
    for m in re.finditer(r"<(h[1-3]|p)(\b[^>]*)>([\s\S]*?)</\1>", inner, re.I):
        tag = m.group(1).lower()
        body = re.sub(r"<script[\s\S]*?</script>", "", m.group(3), flags=re.I)
        text = re.sub(r"<[^>]+>", "", body).strip()
        if len(text) < 8:
            continue
        parts.append(f"<{tag}>{body}</{tag}>")
    for m in re.finditer(r'<div class="faq-item">[\s\S]*?</div>', inner, re.I):
        parts.append(m.group(0))
    return "\n".join(parts) if parts else inner


def _clean_article_inner(inner: str) -> str:
    from _session_double_audit import html5_errs

    inner = _extract_guide_prose(inner)
    inner = re.sub(
        r'<div class="callout-label"><svg[\s\S]*?(?:</svg>)?</div>',
        '<div class="callout-label"></div>',
        inner,
        flags=re.I,
    )
    inner = re.sub(r"</(?:html|body|head)>", "", inner, flags=re.I)
    inner = re.sub(
        r"<!--\s*═══\s*UNIFIED HEADER[\s\S]*?END HEADER[\s\S]*?-->",
        "",
        inner,
        flags=re.I,
    )
    inner = re.sub(
        r"<!--\s*NAV\s*-->[\s\S]*?(?=<h1|<h2|<p|<section|<div class=\"|$)",
        "",
        inner,
        flags=re.I,
    )
    inner = fix_list_mismatches(inner)
    inner = re.sub(
        r"(<a\b[^>]*>)([^<]*?)(?=<a\b)",
        lambda m: m.group(0)
        if "</a>" in m.group(0)
        else m.group(1) + m.group(2) + "</a>",
        inner,
    )
    inner = _reserialize_fragment(inner)
    probe = (
        "<!doctype html><html><body><article class=\"article-body\">"
        + inner
        + "</article></body></html>"
    )
    if html5_errs(probe) > 0:
        inner = _reserialize_fragment(_flatten_to_safe_blocks(inner))
    return inner


def _balance_divs(fragment: str) -> str:
    opens = len(re.findall(r"<div\b", fragment, re.I))
    closes = len(re.findall(r"</div>", fragment, re.I))
    if opens > closes:
        fragment += "</div>\n" * (opens - closes)
    elif closes > opens:
        for _ in range(closes - opens):
            fragment = re.sub(r"</div>\s*$", "", fragment)
    return fragment


def rebuild_page(html: str) -> str:
    """Rebuild page around extracted article using known-good chrome."""
    was_noindex = bool(re.search(r'name="robots"[^>]*noindex', html[:2500], re.I))
    html = _rebuild_head(html)

    am = re.search(r"(<article\b[^>]*>)([\s\S]*?)(</article>)", html, re.I)
    if not am or not _GOOD_PRE or not _GOOD_POST:
        return repair_html_light(html)

    banner = ""
    bm = re.search(r'<section class="article-banner"[\s\S]*?</section>', html, re.I)
    if bm:
        banner = bm.group(0) + "\n"

    inner = _clean_article_inner(am.group(2))
    article = _balance_divs(am.group(1) + inner) + "</article>"

    aside_m = re.search(r'<aside class="article-sidebar"[\s\S]*?</aside>', html, re.I)
    aside = aside_m.group(0) if aside_m else _SHELL_ASIDE

    lang = re.search(r"<html[^>]*>", html, re.I)
    html_open = lang.group(0) if lang else '<html lang="ar" dir="rtl">'
    head_m = re.search(r"<head\b[^>]*>[\s\S]*?</head>", html, re.I)
    head = head_m.group(0) if head_m else "<head></head>"

    layout = (
        '<div class="article-layout">\n'
        '<main class="article-main">\n'
        f"{banner}{article}\n"
        f"{_ARTICLE_END}\n"
        "</main>\n"
        f"{aside}\n"
        "</div>\n"
        "</div>\n"  # close article-wrap opened in PRE
    )

    out = (
        "<!DOCTYPE html>\n"
        f"{html_open}\n"
        f"{head}\n"
        '<body data-template="article">\n'
        f"{_GOOD_PRE}\n"
        f"{layout}"
        f"{_GOOD_POST}\n"
        "</body>\n</html>\n"
    )
    if was_noindex and not re.search(r'name="robots"[^>]*noindex', out[:2500], re.I):
        out = re.sub(
            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
            r"\1noindex,nofollow\2",
            out,
            count=1,
            flags=re.I,
        )
    return out


def repair_html_light(html: str) -> str:
    """Chrome transplant + local fixes (no full rebuild)."""
    was_noindex = bool(re.search(r'name="robots"[^>]*noindex', html[:2500], re.I))
    html = re.sub(r'"\s*/>\s*/>', '"/>', html)
    html = html.replace("</head></head>", "</head>")
    html = re.sub(r"</head>\s*</head>", "</head>", html)
    html = re.sub(r"</article>\s*</article>", "</article>", html)
    html = _rebuild_head(html)

    m_body = re.search(r"<body([^>]*)>", html)
    m_aw = re.search(r'<div class="article-wrap">', html)
    m_ft = re.search(r"<footer\b", html)
    m_body_end = re.search(r"</body>", html)
    if m_body and m_aw and m_ft and m_body_end and _GOOD_PRE and _GOOD_POST:
        body_attrs = m_body.group(1) or ""
        if "data-template" not in body_attrs:
            body_attrs += ' data-template="article"'
        mid = html[m_aw.end() : m_ft.start()]
        # drop nested chrome in mid
        mid = re.sub(
            r"<!--\s*═══\s*UNIFIED HEADER[\s\S]*?END HEADER[\s\S]*?-->",
            "",
            mid,
            flags=re.I,
        )
        html = (
            html[: m_body.start()]
            + f"<body{body_attrs}>"
            + _GOOD_PRE
            + mid
            + _GOOD_POST
            + "</body>"
            + html[m_body_end.end() :]
        )

    html = re.sub(
        r'(<div class="article-end">[\s\S]*?</div>)\s*</article>',
        lambda m: "</article>\n" + m.group(1),
        html,
        count=1,
    )
    html = re.sub(r"(</footer>[\s\S]*?)</article>\s*(?=</body>)", r"\1", html, count=1)

    if html.count("<article") > html.count("</article>"):
        if '<div class="article-end">' in html:
            html = html.replace(
                '<div class="article-end">',
                '</article>\n<div class="article-end">',
                1,
            )
        elif "</main>" in html:
            html = html.replace("</main>", "</article>\n</main>", 1)

    while html.count("</article>") > html.count("<article"):
        idx = html.rfind("</article>")
        html = html[:idx] + html[idx + len("</article>") :]

    html = html.replace(
        '<span class="ar">الحياة، براحة.</p>',
        '<span class="ar">الحياة، براحة.</span></p>',
    )
    html = html.replace(
        '<span class="en">Life, at ease.</p>',
        '<span class="en">Life, at ease.</span></p>',
    )
    html = fix_list_mismatches(html)
    html = balance_article_divs(html)

    aw = html.find('<div class="article-wrap">')
    ft = html.find("<footer")
    if aw >= 0 and ft > aw:
        frag = html[aw:ft]
        opens = len(re.findall(r"<div\b", frag, re.I))
        closes = len(re.findall(r"</div>", frag, re.I))
        if opens > closes:
            html = html[:ft] + ("</div>\n" * (opens - closes)) + html[ft:]
        elif closes > opens:
            chunk = html[:ft]
            for _ in range(closes - opens):
                chunk = re.sub(r"</div>\s*$", "", chunk)
            html = chunk + html[ft:]

    # Clean article inners if still broken
    from _session_double_audit import html5_errs

    if html5_errs(html) > 0:
        am = re.search(r"(<article\b[^>]*>)([\s\S]*?)(</article>)", html, re.I)
        if am:
            new_inner = _clean_article_inner(am.group(2))
            html = html[: am.start(2)] + new_inner + html[am.end(2) :]
            html = balance_article_divs(html)

    if was_noindex and not re.search(r'name="robots"[^>]*noindex', html[:2500], re.I):
        html = re.sub(
            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
            r"\1noindex,nofollow\2",
            html,
            count=1,
            flags=re.I,
        )
    return html


def repair_html(html: str) -> str:
    """Prefer full rebuild when light repair cannot reach html5=0."""
    from _session_double_audit import html5_errs

    light = repair_html_light(html)
    if html5_errs(light) == 0:
        return light
    try:
        rebuilt = rebuild_page(html)
    except Exception:
        return light
    if html5_errs(rebuilt) == 0:
        return rebuilt
    if html5_errs(rebuilt) < html5_errs(light):
        return rebuilt
    return light


def repair_file(path: str) -> int:
    from _session_double_audit import html5_errs

    p = Path(path)
    after = repair_html(p.read_text(encoding="utf-8"))
    p.write_text(after, encoding="utf-8")
    return html5_errs(after)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(arg, "html5=", repair_file(arg))
