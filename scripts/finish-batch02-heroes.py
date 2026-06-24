#!/usr/bin/env python3
"""Close Batch 02 cursor2 tickets — heroes approved, wire HTML done."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TICKETS = ROOT / "operating-system/handoff-tickets.json"

B2_SLUGS = [
    "arab-mother-startup",
    "saving-vs-investing-gulf-family",
    "evening-rituals",
    "family-nutrition-on-budget",
    "umrah-visa-gulf-residents-guide",
    "medina-hotels-near-masjid-nabawi",
    "gold-vs-real-estate-gulf-family",
]


def main() -> int:
    import importlib.util

    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "apply_heroes", ROOT / "scripts/apply-approved-heroes.py"
    )
    heroes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(heroes)
    from image_manifest import entries_by_slug, is_approved, load_manifest

    by = entries_by_slug(load_manifest())
    patched = 0
    for slug in B2_SLUGS:
        entry = by.get(slug)
        if not entry or not is_approved(entry):
            print(f"  skip {slug}: not approved")
            continue
        for fp in ROOT.rglob(f"{slug}*.html"):
            if "outputs" in fp.parts or ".bak" in fp.name:
                continue
            if fp.name.startswith(slug) and fp.suffix == ".html":
                if heroes.apply_path(fp, entry):
                    patched += 1
                    print(f"  ✅ {fp.relative_to(ROOT)}")

    data = json.loads(TICKETS.read_text(encoding="utf-8"))
    ts = datetime.now().strftime("%Y-%m-%d")
    closed = 0
    for card in data.get("cards", []):
        cid = card.get("id", "")
        if not (cid.startswith("B2-") and cid.endswith("C")):
            continue
        if card.get("col") != "cursor2":
            continue
        slug = card.get("slug", "")
        up = card.get("url_path", "")
        card["col"] = "done"
        card["stage"] = "done"
        card["finished"] = ts
        card["task"] = "✅ hero معتمد + بانر + figure — LIVE"
        card["result"] = "Cursor — ربط hero من manifest (عامر approved)"
        if up:
            card["url"] = "https://dotforlife.com" + up
        card.pop("command", None)
        closed += 1

    # Column label — no longer "waiting for images"
    for col in data.get("columns", []):
        if col.get("id") == "cursor2":
            col["title"] = "📥 كورسر ٢ · ربط hero (احتياطي)"

    data["updated"] = ts
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(ROOT / "scripts/handoff_sync.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/sync_gsystem_web.py")], check=True)

    print(f"\nBatch 02 heroes: {patched} pages patched · {closed} tickets → done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
