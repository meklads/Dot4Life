#!/usr/bin/env python3
"""Finish Batch 03: heroes + banner + close build/writing tickets."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "operating-system/batch-03.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"

B3_SLUGS = [
    "gulf-father-money-lessons",
    "government-vs-private-school-gulf",
    "digital-minimalism-families",
    "pregnancy-nutrition-first-trimester",
    "daily-islamic-habits-guide",
    "umrah-with-kids",
    "rent-vs-buy-gulf-family",
]


def close_tickets(data: dict, articles: list[dict]) -> dict[str, int]:
    ts = datetime.now().strftime("%Y-%m-%d")
    moved = {"N": 0, "C": 0, "A": 0}
    url_by_slug = {a["slug"]: a.get("url_path", "") for a in articles}

    for card in data.get("cards", []):
        cid = card.get("id", "")
        if not cid.startswith("B3-") or len(cid) < 6:
            continue
        suffix = cid[-1]
        slug = card.get("slug", "")

        if suffix == "N" and card.get("col") == "hema_writing":
            card["col"] = "member_done"
            card["stage"] = "member_complete"
            card["result"] = "Hema · كتابة — جاهز للبناء (Batch 03 close)"
            card["finished"] = ts
            card.pop("command", None)
            moved["N"] += 1

        elif suffix == "C" and card.get("col") == "cursor":
            card["col"] = "done"
            card["stage"] = "done"
            card["finished"] = ts
            up = url_by_slug.get(slug, card.get("url_path", ""))
            if up:
                card["url"] = "https://dotforlife.com" + up
                card["url_path"] = up
            card["result"] = "LIVE — Batch 03 · template + hero + sidebar"
            card.pop("command", None)
            moved["C"] += 1

    return moved


def main() -> int:
    import importlib.util

    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "apply_heroes", ROOT / "scripts/apply-approved-heroes.py"
    )
    heroes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(heroes)
    from image_manifest import is_approved, load_manifest, entries_by_slug

    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    articles = batch["articles"]
    by = entries_by_slug(load_manifest())

    patched = 0
    for a in articles:
        slug = a["slug"]
        entry = by.get(slug)
        if not entry or not is_approved(entry):
            print(f"  skip hero {slug}: not approved in manifest")
            continue
        folder = Path(a["url_path"].lstrip("/")).parent
        for name in (f"{slug}.html", f"{slug}-en.html"):
            fp = ROOT / folder / name
            if fp.exists() and heroes.apply_path(fp, entry):
                patched += 1
                print(f"  ✅ hero+banner {fp.relative_to(ROOT)}")

    data = json.loads(TICKETS.read_text(encoding="utf-8"))
    moved = close_tickets(data, articles)
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data["batch_active"] = "batch-03"
    data["batch_status"] = "complete"
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    batch["batch_status"] = "complete"
    batch["completed"] = datetime.now().strftime("%Y-%m-%d")
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/site_sections.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/team_board_refresh.py")],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/gsystem_notify.py")],
        check=True,
        env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "scripts")},
    )

    print(f"\nBatch 03 finish: {patched} pages patched · N→member_done:{moved['N']} · C→done:{moved['C']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
