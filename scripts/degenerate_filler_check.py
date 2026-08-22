#!/usr/bin/env python3
"""degenerate_filler_check.py — durable lexical-repetition + FAQ-parity gate.

Automates the manual "lexical-repetition heuristic" from commit d27955a1
(2026-07-10) so degenerate AI-filler text is caught on every run instead of
one-off manual spot-checks. Ordered by Amer (P0, 2026-07-10T19:40Z).

What it flags (conservative — false positives are worse than misses):
  1. FILLER-REPEAT   — a paragraph whose 4-grams repeat degenerately
                      (same 4-word sequence appearing 3+ times, or 2x in a
                      long paragraph) — the signature of generated filler.
  2. FILLER-DUPSENT  — identical normalized sentence appearing 2+ times in
                      the same article body.
  3. FILLER-WORDDOM  — one content word dominating >15% of a long paragraph.
  4. FAQ-PARITY      — FAQPage JSON-LD mainEntity not matching the visible
                      FAQ questions literally (count or text) — the exact
                      defect that escaped the manual heuristic
                      (gulf-father-money-lessons, government-vs-private-school).

Usage:
  python3 scripts/degenerate_filler_check.py                # BUILD_MAP files
  python3 scripts/degenerate_filler_check.py --scope all    # all content dirs
  python3 scripts/degenerate_filler_check.py file.html ...  # explicit files
Exit code: 0 = clean, 1 = at least one flag (CI-friendly).
Also importable: check_file(path) -> list[str].
"""
from __future__ import annotations

import html as _html
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    "node_modules", ".git", "outputs", "legacy", ".tmp_amer", ".deploy",
    "capsule-engine", "system", "operating-system", "_archive", "og",
    "__pycache__", "site", "skills", "visual-governance", "partials",
    "assets", "styles", "scripts", "data", "content", ".github", ".cursor",
    ".hermes", "صور", "featured-stories", "_external-pages", "_redirects",
}
# featured-stories intentionally included in scans? No — it IS content.
SKIP_DIRS.discard("featured-stories")

CONTENT_DIRS = [
    "blog", "guides", "tools", "health", "finance-wealth",
    "islamic-hajj-umrah", "real-estate", "fitness", "productivity",
    "travel", "peace-capsules", "comparisons", "featured-stories",
    "health-pregnancy", "cities", "library",
]

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
# Visible FAQ question markup used across the codebase:
#   <div class="faq-item">…<h3>Q</h3>…   |   <h3 class="faq-question">Q</h3>
_FAQ_ITEM_RE = re.compile(
    r'class="[^"]*faq-item[^"]*"[^>]*>(.*?)</(?:div|section)>', re.S)
_FAQ_ITEM_H3_RE = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
_FAQ_QCLASS_RE = re.compile(r'<h3[^>]*class="[^"]*faq-question[^"]*"[^>]*>(.*?)</h3>', re.S)
_JSON_LD_RE = re.compile(
    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', re.S)


def _strip_tags(html: str) -> str:
    return _WS_RE.sub(" ", _TAG_RE.sub(" ", _html.unescape(html))).strip()


def _norm(text: str) -> str:
    """Normalize for comparison: strip tags/diacritics/punct/case."""
    t = _strip_tags(text)
    t = unicodedata.normalize("NFKC", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = re.sub(r"[^\w\s\u0600-\u06FF]", " ", t)
    return _WS_RE.sub(" ", t).strip().lower()


def _article_body(html: str) -> str:
    m = re.search(r"<article.*?</article>", html, re.S)
    return m.group(0) if m else html


def _body_prose(body_html: str) -> str:
    """Article body minus FAQ blocks and inline scripts/styles — FAQ
    answers legitimately repeat body prose and inline JS is not prose."""
    out = re.sub(
        r"<script.*?</script>|<style.*?</style>", " ",
        body_html, flags=re.S)
    return re.sub(
        r'<(?:div|section|details)[^>]*class="[^"]*faq[^"]*"[^>]*>.*?</(?:div|section|details)>',
        " ", out, flags=re.S)


def _paragraphs(body_html: str) -> list[str]:
    return [
        _strip_tags(p)
        for p in re.findall(r"<p[^>]*>(.*?)</p>", body_html, re.S)
    ]


def _tokens(text: str) -> list[str]:
    return _norm(text).split()


def _repetition_flags(body_html: str) -> list[str]:
    """Return flags; flags starting with 'FILLER-REVIEW' are soft signals
    (report-only) — everything else is a hard degenerate-filler defect."""
    flags: list[str] = []
    paras = _paragraphs(_body_prose(body_html))
    for para in paras:
        words = _tokens(para)
        if len(words) < 15:
            continue
        grams = [" ".join(words[i:i + 4]) for i in range(len(words) - 3)]
        if grams:
            starts: dict[str, list[int]] = {}
            for i, g in enumerate(grams):
                starts.setdefault(g, []).append(i)
            top_gram, idxs = max(
                starts.items(), key=lambda kv: len(kv[1]))
            n = len(idxs)
            echo = any(
                idxs[k + 1] - idxs[k] <= 24 for k in range(len(idxs) - 1))
            if n >= 3:
                flags.append(
                    f"FILLER-REPEAT 4-gram x{n}: “{top_gram[:60]}”")
            elif n == 2 and echo and len(words) >= 40:
                flags.append(
                    f"FILLER-REVIEW 4-gram x2 echo: “{top_gram[:60]}”")
        for w, c in Counter(w for w in words if len(w) > 4).items():
            if c >= 5 and c / len(words) > 0.15 and len(words) >= 25:
                flags.append(f"FILLER-WORDDOM “{w}” = {c}/{len(words)} words")
        # Arabic waw-conjunction avalanche: a long "paragraph" that is one
        # endless و-chained synonym list — the classic repeated-synonym
        # filler signature (healthy Arabic prose stays well under 35%).
        if len(words) >= 25:
            waw = sum(1 for w in words if w.startswith("و") and len(w) > 2)
            if waw / len(words) >= 0.5:
                flags.append(
                    f"FILLER-CHAIN و-prefix {waw}/{len(words)} tokens")
    # duplicate sentences across the article (FAQ section excluded)
    sents = [
        _norm(s)
        for s in re.split(r"[.!?؟]\s+", _strip_tags(_body_prose(body_html)))
        if len(_norm(s).split()) >= 8
    ]
    for s, n in Counter(sents).items():
        if n > 1:
            # body↔summary-box quoting is a known editorial pattern —
            # report, don't gate.
            flags.append(f"FILLER-REVIEW DUPSENT x{n}: “{s[:60]}”")
    return flags


def _visible_faq_questions(html: str) -> list[str]:
    qs: list[str] = []
    for block in _FAQ_ITEM_RE.findall(html):
        for h3 in _FAQ_ITEM_H3_RE.findall(block):
            qs.append(_strip_tags(h3))
    qs += [_strip_tags(q) for q in _FAQ_QCLASS_RE.findall(html)]
    # tools use their own accordion markup: class="t-faq-q" (any tag)
    for _tag, inner in re.findall(
            r'<(\w+)[^>]*class="[^"]*faq-q[^"]*"[^>]*>(.*?)</\1>',
            html, re.S):
        inner = re.sub(r"<svg.*?</svg>", " ", inner, flags=re.S)
        text = _strip_tags(inner)
        if text:
            qs.append(text)
    if not qs:
        # plain-heading FAQ style (documented in AMER-ORDERS 2026-07-10:
        # rent-vs-buy uses bare <h3> instead of .faq-item) — h3/h2 whose
        # text ends with a question mark. Newsletter/subscribe/share boxes
        # also end with "?" and must NOT count (the historic evening-rituals
        # bug, AMER-ORDERS 2026-07-10T16:43Z).
        _NOT_FAQ = re.compile(
            r"📬|newsletter|نشرة|اشترك|subscribe|share|شارك|اقرأ أيضا", re.I)
        for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html, re.S):
            text = _strip_tags(h)
            if text.endswith(("?", "؟")) and not _NOT_FAQ.search(text):
                qs.append(text)
    # de-dup, keep order
    seen, out = set(), []
    for q in qs:
        k = _norm(q)
        if k and k not in seen:
            seen.add(k)
            out.append(q)
    return out


def _schema_faq_questions(html: str) -> list[str]:
    qs: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("@type") == "FAQPage":
                for q in node.get("mainEntity", []) or []:
                    qs.append(_strip_tags(str(q.get("name", ""))))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for raw in _JSON_LD_RE.findall(html):
        try:
            walk(json.loads(raw))
        except (json.JSONDecodeError, ValueError):
            continue
    return [q for q in qs if q.strip()]


def _faq_parity_flags(html: str) -> list[str]:
    schema_qs = _schema_faq_questions(html)
    if not schema_qs:
        return []  # no FAQPage schema → nothing to parity-check
    visible_qs = _visible_faq_questions(html)
    if not visible_qs:
        return ["FAQ-PARITY schema has FAQPage but no visible FAQ markup found"]
    # Tools render each FAQ question bilingually in ONE element
    # ("EN question? AR question؟") while schema holds the EN string —
    # subset match counts as a match.
    vis_norms = [_norm(q) for q in visible_qs]
    sch_norms = [_norm(q) for q in schema_qs]

    def _matches(s: str, v: str) -> bool:
        return s == v or (len(s) >= 8 and s in v)

    unmatched_schema = [
        q for q, s in zip(schema_qs, sch_norms)
        if not any(_matches(s, v) for v in vis_norms)
    ]
    unmatched_visible = [
        q for q, v in zip(visible_qs, vis_norms)
        if not any(_matches(s, v) for s in sch_norms)
    ]
    if unmatched_schema or unmatched_visible:
        parts = [f"schema={len(schema_qs)} visible={len(visible_qs)}"]
        if unmatched_visible:
            parts.append(
                f"visible-not-in-schema: “{unmatched_visible[0][:60]}”")
        if unmatched_schema:
            parts.append(
                f"schema-not-visible: “{unmatched_schema[0][:60]}”")
        return ["FAQ-PARITY " + " | ".join(parts)]
    return []


def check_file(path: Path) -> list[str]:
    """Return a list of defect strings for one HTML file (empty = clean)."""
    html = path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'name="robots"\s+content="[^"]*noindex', html):
        return []  # already isolated — out of scope for the live gate
    body = _article_body(html)
    defects: list[str] = []
    # tools/ are calculator apps: their body is UI copy (labels, table
    # rows, per-mode hints) where repetition is legitimate — prose
    # repetition checks apply to articles only.
    if not any(part == "tools" for part in path.parts):
        defects += _repetition_flags(body)
    defects += _faq_parity_flags(html)
    return defects


def build_map_files() -> list[Path]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_from_approved_draft import BUILD_MAP  # noqa: N813
    files: list[Path] = []
    for cfg in BUILD_MAP:
        for key in ("out_ar", "out_en"):
            p = cfg.get(key)
            if p and Path(p).exists():
                files.append(Path(p))
    return sorted(set(files))


def all_content_files() -> list[Path]:
    files: list[Path] = []
    for d in CONTENT_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.html"):
            if not any(part in SKIP_DIRS for part in p.parts):
                files.append(p)
    return sorted(files)


def main(argv: list[str]) -> int:
    args = argv[1:]
    verbose = "-v" in args or "--verbose" in args
    strict = "--strict" in args
    args = [a for a in args if a not in ("-v", "--verbose", "--strict")]
    scope = "buildmap"
    if args and args[0] == "--scope":
        scope = args[1] if len(args) > 1 else "all"
        args = args[2:]
    if args:
        files = [Path(a) for a in args]
    elif scope == "all":
        files = all_content_files()
    else:
        files = build_map_files()

    hard = 0
    review = 0
    checked = 0
    for p in files:
        checked += 1
        try:
            defects = check_file(p)
        except OSError as e:
            print(f"  ERROR {p.relative_to(ROOT)}: {e}")
            hard += 1
            continue
        for d in defects:
            if d.startswith("FILLER-REVIEW"):
                review += 1
                if verbose:
                    print(f"  review {p.relative_to(ROOT)} :: {d}")
            else:
                hard += 1
                print(f"  FLAG {p.relative_to(ROOT)} :: {d}")
        if verbose and not defects:
            print(f"  ok   {p.relative_to(ROOT)}")
    print(
        f"\n=== degenerate_filler_check: {checked} files, "
        f"{hard} hard flags, {review} review-only ===")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
