#!/usr/bin/env python3
"""Move a handoff ticket to a team member column."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from handoff_sync import load, move_card, save, sync_all  # noqa: E402

ALIASES = {
    "جوست": "ghost",
    "ghost": "ghost",
    "عمر": "hema_omar",
    "omar": "hema_omar",
    "عامر": "amer",
    "amer": "amer",
    "كلود": "amer",
    "moni": "hema_moni",
    "hema_moni": "hema_moni",
    "ruwaq": "hema_ruwaq",
    "hema_ruwaq": "hema_ruwaq",
    "hema_omar": "hema_omar",
    "hema": "hema_moni",
    "رواق": "hema_ruwaq",
    "cursor": "cursor",
    "cursor2": "cursor2",
    "كورسر2": "cursor2",
    "كورسر ٢": "cursor2",
    "wait": "cursor2",
    "منتهي": "done",
    "done": "done",
    "تم": "done",
    "member_done": "member_done",
    "انتهى": "member_done",
    "انتهيت": "member_done",
    "منتهى": "member_done",
}


def norm_id(raw: str) -> str:
    raw = raw.strip()
    m = re.match(r"^H-?(\d+)$", raw, re.I)
    if m:
        return f"H-{int(m.group(1)):02d}"
    m = re.match(r"^C-?(\d+)$", raw, re.I)
    if m:
        return f"C-{int(m.group(1)):02d}"
    m = re.match(r"^T-?(\d+)$", raw, re.I)
    if m:
        return f"T-{int(m.group(1)):02d}"
    m = re.match(r"^A-?(\d+)$", raw, re.I)
    if m:
        return f"A-{int(m.group(1)):02d}"
    m = re.match(r"^R-?(\d+)$", raw, re.I)
    if m:
        return f"R-{int(m.group(1)):02d}"
    m = re.match(r"^W-?(\d+)$", raw, re.I)
    if m:
        return f"W-{int(m.group(1)):02d}"
    return raw


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/handoff_move.py H-07 omar", file=sys.stderr)
        return 1
    card_id = norm_id(sys.argv[1])
    col = ALIASES.get(sys.argv[2].lower(), sys.argv[2].lower())
    data = load()
    card = move_card(data, card_id, col)
    if not card:
        print(json.dumps({"error": f"card not found: {card_id}"}, ensure_ascii=False))
        return 1
    save(data)
    result = sync_all()
    subprocess.run(["python3", str(ROOT / "scripts/sync_gsystem_web.py")], cwd=ROOT, check=False)
    print(
        json.dumps(
            {"moved": card_id, "col": col, "command": card.get("command", ""), **result},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
