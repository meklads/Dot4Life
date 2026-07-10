#!/usr/bin/env python3
"""Generate serve.json + _redirects so extensionless URLs map to .html files."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    "node_modules", ".git", "outputs", "legacy", ".tmp_amer",
    "capsule-engine", "system", "operating-system", "assets/queue",
}


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
    route = "/" + rel_posix[:-5]  # drop .html
    return route


def main() -> None:
    rewrites: list[dict[str, str]] = []
    redirect_lines: list[str] = []

    for path in collect_html_files():
        rel = path.relative_to(ROOT).as_posix()
        route = extensionless_route(rel)
        dest = "/" + rel
        if route == dest:
            continue
        rewrites.append({"source": route, "destination": dest})
        redirect_lines.append(f"{route} {dest} 200")

    serve_cfg = {
        "trailingSlash": False,
        "rewrites": rewrites,
    }
    (ROOT / "serve.json").write_text(
        json.dumps(serve_cfg, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "_redirects").write_text("\n".join(redirect_lines) + "\n", encoding="utf-8")
    print(f"static routes: {len(rewrites)} rewrites → serve.json + _redirects")


if __name__ == "__main__":
    main()
