#!/usr/bin/env python3
"""Export operating-system markdown → system/gsystem-data/*.json for board.html (server blocks .md)."""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OS = ROOT / "operating-system"
OUT = ROOT / "system/gsystem-data"

# id → path under operating-system/
GS_DOCS: dict[str, str] = {
    "team-board": "team-board.md",
    "handoff-board": "handoff-board.md",
    "track-board": "reports/track-board.md",
    "ready-to-build": "reports/ready-to-build.md",
    "yellow-mode-active": "reports/yellow-mode-active.md",
    "gsystem-charter": "gsystem-charter.md",
    "manager-charter-adsense": "manager-charter-adsense.md",
    "track-c": "reports/track-C-adsense-technical.md",
    "claude-chef-execution-plan": "reports/claude-chef-execution-plan.md",
    "track-b-thin": "reports/track-B-thin-live-top20.md",
    "kanban-frozen": "reports/kanban-frozen.md",
}

GHOST_SKIP = re.compile(r"^_|STANDING-ORDERS|amer-to-cursor-notify|TEAM-NOTICE")
MARKED = ROOT / "system/vendor/marked.min.js"


def md_to_html(markdown: str) -> str:
    """Pre-render markdown → HTML (board does not depend on marked.js at runtime)."""
    import subprocess

    clean = re.sub(r"<!--[\s\S]*?-->", "", markdown)
    if not MARKED.is_file():
        return f"<pre>{clean}</pre>"
    script = r"""
const fs=require('fs');
const vm=require('vm');
const code=fs.readFileSync(process.argv[1],'utf8');
const ctx={console,globalThis:{}};
vm.createContext(ctx);
vm.runInContext(code,ctx);
const marked=ctx.globalThis.marked||ctx.marked;
if(!marked||typeof marked.parse!=='function')process.exit(2);
const md=fs.readFileSync(0,'utf8');
process.stdout.write(marked.parse(md));
"""
    try:
        r = subprocess.run(
            ["node", "-e", script, str(MARKED)],
            input=clean,
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=30,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return f"<pre style='white-space:pre-wrap'>{clean}</pre>"


def pack(source: Path, markdown: str) -> dict:
    return {
        "source": str(source.relative_to(ROOT)),
        "synced_at": datetime.now().isoformat(timespec="seconds"),
        "markdown": markdown,
        "html": md_to_html(markdown),
    }


def sync_doc(doc_id: str, rel: str) -> bool:
    src = OS / rel
    if not src.is_file():
        return False
    text = src.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{doc_id}.json").write_text(
        json.dumps(pack(src, text), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return True


def sync_ghost() -> int:
    ghost_dir = OS / "reports/ghost"
    reports: list[dict] = []
    for fp in sorted(ghost_dir.glob("*.md"), reverse=True):
        if GHOST_SKIP.search(fp.name):
            continue
        kind = "images" if fp.name.startswith("images") else "daily"
        label = fp.stem.replace("-", " / ", 1) if fp.stem.count("-") >= 2 else fp.stem
        if fp.name.startswith("images-"):
            label = "🖼️ " + fp.stem.replace("images-", "", 1)
        elif re.match(r"\d{4}-\d{2}-\d{2}", fp.name):
            label = "📅 " + fp.name.replace(".md", "")
        text = fp.read_text(encoding="utf-8")
        reports.append(
            {
                "date": fp.stem[:10] if re.match(r"\d{4}-\d{2}-\d{2}", fp.name) else fp.stem,
                "kind": kind,
                "label": label,
                "source": str(fp.relative_to(ROOT)),
                "markdown": text,
                "html": md_to_html(text),
            }
        )
    bundle = {
        "synced_at": datetime.now().isoformat(timespec="seconds"),
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "reports": reports,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ghost.json").write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return len(reports)


def sync_all() -> dict:
    synced: list[str] = []
    missing: list[str] = []
    for doc_id, rel in GS_DOCS.items():
        if sync_doc(doc_id, rel):
            synced.append(doc_id)
        else:
            missing.append(rel)
    n_ghost = sync_ghost()
    handoff = False
    ht = ROOT / "operating-system/handoff-tickets.json"
    if ht.is_file():
        OUT.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ht, OUT / "handoff-tickets.json")
        handoff = True
    ss = ROOT / "operating-system/site-sections.json"
    if ss.is_file():
        OUT.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ss, OUT / "site-sections.json")
    return {"synced": synced, "missing": missing, "ghost_reports": n_ghost, "handoff_tickets": handoff}


def main() -> None:
    result = sync_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
