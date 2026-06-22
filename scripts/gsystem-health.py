#!/usr/bin/env python3
"""GSystem daily health — audits, quality, LIVE gates."""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], title: str) -> int:
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode


def main() -> None:
    py = sys.executable
    codes = [
        run([py, "scripts/build-from-approved-draft.py", "--audit"], "LIVE audit (29)"),
        run([py, "scripts/quality-audit.py"], "Archive quality"),
        run([py, "scripts/list-image-pending.py"], "Image pending (Omar)"),
    ]
    print(f"\n--- GSystem health {date.today().isoformat()} ---")
    print(f"LIVE audit: {'PASS' if codes[0]==0 else 'FAIL'}")
    print(f"Quality + image queue: exit {codes[1:]}")


if __name__ == "__main__":
    main()
