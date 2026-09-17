#!/usr/bin/env python3
"""Generate serve.json + _redirects so extensionless URLs map to .html files.

Also appends legacy 301 aliases from operating-system/legacy-404-redirects.json
so GSC 404 debt stays closed after regenerating routes.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "operating-system" / "legacy-404-redirects.json"
SKIP_DIRS = {
    "node_modules", ".git", "outputs", "legacy", ".tmp_amer",
    "capsule-engine", "system", "operating-system", "assets/queue",
}

# Extra WP / junk redirects kept at end of _redirects
JUNK_301 = [
    ("/wp-login.php", "/"),
    ("/wp-admin", "/"),
    ("/wp-admin/:path*", "/"),
    ("/wp-content/:path*", "/"),
    ("/wp-includes/:path*", "/"),
    ("/category/:path*", "/blog"),
    ("/tag/:path*", "/blog"),
    ("/feed", "/blog"),
    ("/comments/feed", "/blog"),
    ("/2016/:path*", "/blog"),
    ("/2017/:path*", "/blog"),
    ("/2018/:path*", "/blog"),
    ("/2019/:path*", "/blog"),
    ("/2020/:path*", "/blog"),
    ("/2021/:path*", "/blog"),
    ("/2022/:path*", "/blog"),
    ("/2023/:path*", "/blog"),
    ("/2024/:path*", "/blog"),
    ("/2025/:path*", "/blog"),
]


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("assets/queue/"):
        return True
    return any(part in SKIP_DIRS for part in path.parts)


def collect_html_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("."):
            continue
        files.append(path)
    return files


def extensionless_route(rel_posix: str) -> str:
    if rel_posix == "index.html":
        return "/"
    return "/" + rel_posix[:-5]  # drop .html


def load_legacy() -> dict[str, str]:
    if not LEGACY.exists():
        return {}
    data = json.loads(LEGACY.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


def main() -> None:
    legacy = load_legacy()
    legacy_sources = set(legacy.keys()) | {f"{k}.html" for k in legacy.keys()}

    rewrites: list[dict[str, str]] = []
    redirects: list[dict[str, str]] = []
    rewrite_lines: list[str] = []
    redirect_lines: list[str] = []

    # Legacy 301s FIRST (first-match wins on Netlify/CF Pages _redirects)
    for src, dest in sorted(legacy.items()):
        redirects.append({"source": src, "destination": dest})
        redirect_lines.append(f"{src} {dest} 301")
        html_src = f"{src}.html"
        if html_src not in legacy_sources:
            redirects.append({"source": html_src, "destination": dest})
            redirect_lines.append(f"{html_src} {dest} 301")

    redirects.append(
        {
            "source": "/blog/saudi-mortgage-guide",
            "destination": "/blog/saudi-mortgage-guide-2025-en.html",
        }
    )
    redirect_lines.append(
        "/blog/saudi-mortgage-guide /blog/saudi-mortgage-guide-2025-en.html 301"
    )
    redirect_lines.append(
        "/blog/saudi-mortgage-guide.html /blog/saudi-mortgage-guide-2025-en.html 301"
    )

    for src, dest in JUNK_301:
        redirects.append({"source": src, "destination": dest})
        redirect_lines.append(f"{src} {dest} 301")

    for path in collect_html_files():
        rel = path.relative_to(ROOT).as_posix()
        route = extensionless_route(rel)
        dest = "/" + rel
        if route == dest:
            continue
        # Prefer explicit 301 over 200 rewrite for legacy aliases
        if route in legacy or route in legacy_sources:
            continue
        rewrites.append({"source": route, "destination": dest})
        rewrite_lines.append(f"{route} {dest} 200")

    redirect_lines.extend(rewrite_lines)

    serve_cfg = {
        "trailingSlash": False,
        "redirects": redirects,
        "rewrites": rewrites,
        "headers": [
            {
                "source": "/styles/**",
                "headers": [
                    {
                        "key": "Cache-Control",
                        "value": "public, max-age=31536000, immutable",
                    }
                ],
            },
            {
                "source": "/scripts/**",
                "headers": [
                    {
                        "key": "Cache-Control",
                        "value": "public, max-age=31536000, immutable",
                    }
                ],
            },
            {
                "source": "/assets/**",
                "headers": [
                    {
                        "key": "Cache-Control",
                        "value": "public, max-age=31536000, immutable",
                    }
                ],
            },
            {
                "source": "/og/**",
                "headers": [
                    {
                        "key": "Cache-Control",
                        "value": "public, max-age=31536000, immutable",
                    }
                ],
            },
            {
                "source": "/**",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {
                        "key": "Referrer-Policy",
                        "value": "strict-origin-when-cross-origin",
                    },
                ],
            },
        ],
    }
    (ROOT / "serve.json").write_text(
        json.dumps(serve_cfg, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "_redirects").write_text(
        "\n".join(redirect_lines) + "\n", encoding="utf-8"
    )
    print(
        f"static routes: {len(rewrites)} rewrites · {len(redirects)} redirects "
        f"→ serve.json + _redirects"
    )


if __name__ == "__main__":
    main()
