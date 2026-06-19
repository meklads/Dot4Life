#!/usr/bin/env python3
"""Legacy entry — delegates to auto_capsules_weekly.py (--force for fresh 7-day seed)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
script = ROOT / 'scripts' / 'auto_capsules_weekly.py'
force = '--force' in sys.argv
args = [sys.executable, str(script)] + (['--force'] if force else [])
raise SystemExit(subprocess.call(args))
