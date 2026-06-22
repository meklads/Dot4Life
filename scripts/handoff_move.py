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
    "عمر": "omar",
    "omar": "omar",
    "عامر": "amer",
    "amer": "amer",
    "كلود": "amer",
    "hema": "hema",
    "cursor": "cursor",
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
