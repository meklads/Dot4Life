#!/usr/bin/env python3
"""Wave4 close-out: deepen remaining live inventory (43) after structural repair."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_structure_repair import repair_file
from _session_wave3_deepen import (
    HARD_SKIP,
    ROOTS,
    accept,
    is_noindex,
    prior_done as prior_w12,
    process_one,
    word_count,
)
from _session_double_audit import html5_errs

QUEUE_PATH = Path("operating-system/reports/cursor-343-deepen-queue.json")
REVIEW_PATH = Path("operating-system/reports/cursor-343-full-batch-review.json")


def all_prior_done() -> set[str]:
    done = prior_w12()
    for name in (
        "operating-system/reports/cursor-300-deepen-queue.json",
        "operating-system/reports/cursor-343-deepen-queue.json",
    ):
        p = Path(name)
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for i in range(1, 12):
            done |= set(data.get(f"batch{i}", []) or [])
            done |= set(data.get("batches", {}).get(f"batch{i}", []) or [])
        done |= set(data.get("live", []) or [])
        done |= set(data.get("noindex", []) or [])
    return done


def inventory(include_noindex: bool = False) -> list[str]:
    done = all_prior_done()
    rows: list[tuple[int, str, bool]] = []
    for root in ROOTS:
        folder = Path(root)
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.html")):
            s = str(p)
            if s in done or s in HARD_SKIP:
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            if "article-body" not in t:
                continue
            ni = is_noindex(t)
            if ni and not include_noindex:
                continue
            if (not ni) and include_noindex:
                continue
            rows.append((0 if not ni else 1, s, ni))
    rows.sort()
    return [s for _, s, _ in rows]


def public_url(path: str) -> str:
    return "https://dotforlife.com/" + path.replace("\\", "/")


def main() -> None:
    if QUEUE_PATH.exists():
        wave = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    else:
        wave = {"wave": 4, "batches": {}, "live": [], "noindex": [], "failed": []}

    targets = inventory(False)
    # Also try recoverable noindex leftovers after live
    targets += inventory(True)
    print(f"WAVE4 targets={len(targets)}")

    locked: list[str] = []
    failed: list[str] = list(wave.get("failed", []))
    live_meta: list[str] = list(wave.get("live", []))
    noindex_meta: list[str] = list(wave.get("noindex", []))

    already = set()
    for i in range(1, 12):
        already |= set(wave.get("batches", {}).get(f"batch{i}", []) or [])

    batch_num = 1
    batch: list[str] = list(wave.get("batches", {}).get(f"batch{batch_num}", []) or [])

    def save() -> None:
        wave["batches"][f"batch{batch_num}"] = batch
        wave["live"] = sorted(set(live_meta))
        wave["noindex"] = sorted(set(noindex_meta))
        wave["failed"] = sorted(set(failed))
        total = sum(len(wave["batches"].get(f"batch{i}", [])) for i in range(1, 12))
        wave["progress"] = f"{total} locked / wave4 close-out"
        wave["wave"] = 4
        for i in range(1, 12):
            wave[f"batch{i}"] = wave["batches"].get(f"batch{i}", [])
        QUEUE_PATH.write_text(json.dumps(wave, ensure_ascii=False, indent=2), encoding="utf-8")

    for path in targets:
        if path in already or path in failed:
            continue
        if path in HARD_SKIP:
            continue
        print(f"\n=== try {path} ===")
        original = Path(path).read_text(encoding="utf-8")
        was_ni = is_noindex(original)
        # 1) structure repair
        try:
            errs = repair_file(path)
        except Exception as e:
            print("repair EXC", e)
            Path(path).write_text(original, encoding="utf-8")
            failed.append(path)
            save()
            continue
        if errs > 0:
            print("repair still html5=", errs)
            Path(path).write_text(original, encoding="utf-8")
            failed.append(path)
            save()
            continue
        # 2) deepen + audit
        ok = False
        try:
            ok = process_one(path, len(locked) + 1) and accept(path, allow_noindex=was_ni)
        except Exception as e:
            print("process EXC", e)
            ok = False
        if ok:
            # re-assert robots
            t = Path(path).read_text(encoding="utf-8")
            if was_ni and not is_noindex(t):
                t = re.sub(
                    r'(<meta\s+name="robots"\s+content=")[^"]*(")',
                    r"\1noindex,nofollow\2",
                    t,
                    count=1,
                    flags=re.I,
                )
                Path(path).write_text(t, encoding="utf-8")
            # final structure sanity
            if html5_errs(Path(path).read_text(encoding="utf-8")) > 0:
                repair_file(path)
            if not accept(path, allow_noindex=was_ni):
                print("DROP after final accept", path)
                Path(path).write_text(original, encoding="utf-8")
                failed.append(path)
            else:
                locked.append(path)
                already.add(path)
                batch.append(path)
                (noindex_meta if was_ni else live_meta).append(path)
                print("KEEP", path, "words", word_count(path))
                if len(batch) >= 10:
                    save()
                    batch_num += 1
                    batch = list(wave.get("batches", {}).get(f"batch{batch_num}", []) or [])
        else:
            print("DROP", path)
            Path(path).write_text(original, encoding="utf-8")
            failed.append(path)
        save()

    # flush last batch
    if batch:
        wave["batches"][f"batch{batch_num}"] = batch
        save()

    # Full review
    review = {
        "wave": 4,
        "total": len(locked),
        "pass": [],
        "fails": [],
        "live_count": len(set(live_meta)),
        "noindex_count": len(set(noindex_meta)),
        "failed_paths": sorted(set(failed)),
        "urls": [],
        "note": "Close-out deepen of remaining inventory after Waves 1–3; structure repair + amer_gate + double-audit×2.",
    }
    for p in locked:
        ni = is_noindex(Path(p).read_text(encoding="utf-8"))
        ok = accept(p, allow_noindex=ni)
        entry = {
            "path": p,
            "url": public_url(p),
            "words": word_count(p),
            "noindex": ni,
            "ok": ok,
        }
        if ok:
            review["pass"].append(entry)
            review["urls"].append(entry["url"])
        else:
            review["fails"].append(entry)
    REVIEW_PATH.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "WAVE4 DONE",
        "locked",
        len(locked),
        "pass",
        len(review["pass"]),
        "fails",
        len(review["fails"]),
        "dropped",
        len(set(failed)),
    )


if __name__ == "__main__":
    main()
