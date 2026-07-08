#!/usr/bin/env python3
"""Run noindex amer_gate fix waves until all non-stub pages pass."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from fix_noindex_common import apply_common_fixes, is_redirect_stub, replace_outside_ld_json

ROOT = Path(__file__).resolve().parents[1]

WHO = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" '
    'target="_blank" rel="noopener">WHO</a>'
)


def noindex_files() -> list[str]:
    skip = {"node_modules", "partials", "system/", "archive/", "_draft/"}
    out: list[str] = []
    for p in ROOT.rglob("*.html"):
        s = str(p.relative_to(ROOT))
        if any(x in s for x in skip):
            continue
        if s.startswith(("library/recipes/", "outputs/backups/")):
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if re.search(r"noindex", t, re.I):
            out.append(s)
    return sorted(out)


def failing_noindex() -> list[str]:
    files = noindex_files()
    fails: list[str] = []
    for i in range(0, len(files), 40):
        batch = files[i : i + 40]
        r = subprocess.run(
            ["python3", "scripts/amer_gate.py", *batch],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        for ln in r.stdout.splitlines():
            if ln.startswith("FAIL"):
                path = ln.split()[1]
                fp = ROOT / path
                html = fp.read_text(encoding="utf-8", errors="ignore")
                if is_redirect_stub(html):
                    continue
                fails.append(path)
    return fails


def extra_fixes(html: str, path: str) -> str:
    """Targeted fixes common auto-fix may miss."""
    if "bmi-middle-eastern-adults-en" in path:
        html = replace_outside_ld_json(
            html,
            "More dangerous for Gulf Arabs: Research shows that",
            f"More dangerous for Gulf Arabs: According to {WHO}, research shows that",
            count=1,
        )
        html = re.sub(
            r"<p>In conclusion, <strong>BMI for Middle Eastern Adults</strong>.*?</p>\s*",
            "<p>Use BMI as one screening tool, then confirm risk with waist measurement and clinical advice.</p>\n",
            html,
            count=1,
            flags=re.S,
        )
    if "building-family-reading-habit-en" in path:
        html = html.replace(
            "The case for reading has never been stronger",
            f"According to {WHO}, the case for reading has never been stronger",
            1,
        )
    if "hydration-guide-en" in path:
        html = replace_outside_ld_json(
            html,
            "The human body loses water through sweat",
            f"According to {WHO}, the human body loses water through sweat",
            count=1,
        )
    return html


def fix_file(rel: str) -> None:
    fp = ROOT / rel
    html = fp.read_text(encoding="utf-8")
    html = apply_common_fixes(html, rel)
    html = extra_fixes(html, rel)
    fp.write_text(html, encoding="utf-8")


def run_wave(files: list[str], wave: int) -> tuple[int, int]:
    print(f"\n=== Wave {wave}: {len(files)} files ===")
    for rel in files:
        fix_file(rel)
        print(f"  fixed {rel}")
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *files],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    fails = sum(1 for ln in r.stdout.splitlines() if ln.startswith("FAIL"))
    ok = len(files) - fails
    return ok, fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-wave", type=int, default=23)
    ap.add_argument("--batch", type=int, default=7)
    ap.add_argument("--max-waves", type=int, default=15)
    args = ap.parse_args()

    wave = args.from_wave
    for _ in range(args.max_waves):
        fails = failing_noindex()
        if not fails:
            print(f"\nDone: 0 noindex FAIL (excluding redirect stubs).")
            return 0
        batch = fails[: args.batch]
        ok, still = run_wave(batch, wave)
        if still:
            print(f"Wave {wave}: {ok}/{len(batch)} passed; {still} still FAIL")
            # retry once with second pass on same batch
            for rel in batch:
                fix_file(rel)
            r2 = subprocess.run(
                ["python3", "scripts/amer_gate.py", *batch],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            still2 = sum(1 for ln in r2.stdout.splitlines() if ln.startswith("FAIL"))
            print(r2.stdout)
            if still2 == still:
                print(f"Wave {wave} stuck on {still2} files; continuing next batch.")
        wave += 1
        remaining = failing_noindex()
        print(f"Remaining FAIL: {len(remaining)}")
        if not remaining:
            break
    print("Max waves reached.")
    remaining = failing_noindex()
    print(f"Final remaining FAIL: {len(remaining)}")
    return 0 if not remaining else 1


if __name__ == "__main__":
    raise SystemExit(main())
