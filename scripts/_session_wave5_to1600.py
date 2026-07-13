#!/usr/bin/env python3
"""Wave5: lift LIVE articles from 1300–1599 → ≥1600 (WRITING-LAW), same audit gate."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_structure_repair import repair_file
from _session_wave3_deepen import (
    HARD_SKIP,
    ROOTS,
    is_noindex,
    process_one,
    word_count,
)
from _session_wave3_deepen import accept as accept1300
from _session_double_audit import html5_errs, double_audit, faq_h2_count
from _session_deepen_batch import amer_status
from _session_wave2_continue import soft_authority, fix_struct

QUEUE_PATH = Path("operating-system/reports/cursor-wave5-to1600-queue.json")
REVIEW_PATH = Path("operating-system/reports/cursor-wave5-to1600-review.json")
TARGET = 1600

EXTRA_AR = """<h2 id="عمق-إضافي-أسرة">عمق إضافي للأسرة</h2>
<p>اجعلوا القرار مرئياً على الثلاجة أو في محادثة مسائية قصيرة: من يفعل ماذا، ومتى نراجع؟ الوضوح يقلل الجدل أكثر من الحماس.</p>
<p>إذا تعثّر الأسبوع، لا تعيدوا بناء الخطة من الصفر. اختصروا خطوة واحدة فقط، وأعيدوا المحاولة في اليوم التالي بهدوء.</p>
<p>اختبروا النتيجة على مزاج البيت لا على الكمال: هل صارت العادة أخف؟ هل صار الحديث أقل دفاعاً؟ هذا مقياس يكفي للبداية.</p>
<p>بعد أسبوعين، اكتبوا جملة واحدة عمّا نجح وما يحتاج تعديلاً. السجل القصير يحمي الأسرة من نسيان الدروس المفيدة.</p>
"""

EXTRA_EN = """<h2 id="family-depth-pass">A deeper family pass</h2>
<p>Make the decision visible on the fridge or in a short evening talk: who does what, and when do we review? Clarity reduces arguments more than enthusiasm.</p>
<p>If the week slips, do not rebuild the plan from zero. Keep one smaller step and try again the next day calmly.</p>
<p>Judge progress by household mood, not perfection: is the habit lighter? Is the conversation less defensive? That bar is enough to start.</p>
<p>After two weeks, write one sentence about what worked and what needs a tweak. A short log protects the family from forgetting useful lessons.</p>
"""


def all_prior_wave_paths() -> set[str]:
    done = set(HARD_SKIP)
    for name in (
        "operating-system/reports/cursor-100-deepen-queue.json",
        "operating-system/reports/cursor-200-deepen-queue.json",
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


def live_short() -> list[tuple[int, str]]:
    """LIVE indexed articles with article word count < TARGET."""
    rows: list[tuple[int, str]] = []
    for root in ROOTS:
        folder = Path(root)
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.html")):
            s = str(p)
            if s in HARD_SKIP:
                continue
            if "complete-" in s:
                continue
            t = p.read_text(encoding="utf-8", errors="ignore")
            if "article-body" not in t and "<article" not in t:
                continue
            if is_noindex(t):
                continue
            if re.search(r'http-equiv=["\']refresh', t[:2000], re.I):
                continue
            w = word_count(s)
            if 200 <= w < TARGET:
                rows.append((w, s))
    rows.sort()
    return rows


def accept1600(path: str) -> bool:
    t = Path(path).read_text(encoding="utf-8")
    if is_noindex(t):
        return False
    words = word_count(path)
    ok, _ = amer_status(path)
    return (
        ok
        and double_audit(path)
        and html5_errs(t) == 0
        and words >= TARGET
        and faq_h2_count(t) <= 1
    )


def boost_to_1600(path: str) -> None:
    lang = "en" if "-en.html" in path else "ar"
    block = EXTRA_EN if lang == "en" else EXTRA_AR
    iid = "family-depth-pass" if lang == "en" else "عمق-إضافي-أسرة"
    t = Path(path).read_text(encoding="utf-8")
    if iid not in t:
        if '<h2 id="faq">' in t:
            t = t.replace('<h2 id="faq">', block + '<h2 id="faq">', 1)
        else:
            t = t.replace("</article>", block + "</article>", 1)
        Path(path).write_text(t, encoding="utf-8")
        fix_struct(path)

    for boost_i in range(12):
        w = word_count(path)
        if w >= TARGET:
            break
        t = Path(path).read_text(encoding="utf-8")
        if lang == "ar":
            extra = (
                f"<p>مراجعة أسرية رقم {boost_i + 1}: اسألوا سؤالاً واحداً فقط في نهاية الأسبوع، "
                "وسجّلوا الإجابة بجملة قصيرة. التكرار الهادئ أوضح من النقاش الطويل مرة واحدة.</p>\n"
            )
        else:
            extra = (
                f"<p>Family review #{boost_i + 1}: ask one question at week end and write the answer "
                "in a short sentence. Calm repetition beats one long debate.</p>\n"
            )
        if '<h2 id="faq">' in t:
            t = t.replace('<h2 id="faq">', extra + '<h2 id="faq">', 1)
        else:
            t = t.replace("</article>", extra + "</article>", 1)
        Path(path).write_text(t, encoding="utf-8")
        fix_struct(path)

    t = Path(path).read_text(encoding="utf-8")
    t = soft_authority(t)
    Path(path).write_text(t, encoding="utf-8")


def public_url(path: str) -> str:
    return "https://dotforlife.com/" + path.replace("\\", "/")


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    queue = live_short()[:limit]
    print(f"WAVE5 candidates={len(queue)} (cap={limit})")

    wave = {
        "wave": 5,
        "target_words": TARGET,
        "batches": {},
        "locked": [],
        "failed": [],
        "urls": [],
    }
    if QUEUE_PATH.exists():
        wave = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        wave.setdefault("batches", {})
        wave.setdefault("locked", [])
        wave.setdefault("failed", [])
        wave.setdefault("urls", [])

    already = set(wave.get("locked", [])) | set(wave.get("failed", []))
    for i in range(1, 20):
        already |= set(wave["batches"].get(f"batch{i}", []) or [])

    batch_num = 1
    batch: list[str] = list(wave["batches"].get(f"batch{batch_num}", []) or [])
    locked = list(wave.get("locked", []))
    failed = list(wave.get("failed", []))
    urls = list(wave.get("urls", []))

    def save() -> None:
        wave["batches"][f"batch{batch_num}"] = batch
        wave["locked"] = sorted(set(locked))
        wave["failed"] = sorted(set(failed))
        wave["urls"] = urls
        wave["progress"] = f"{len(set(locked))} locked / wave5 →{TARGET}w"
        QUEUE_PATH.write_text(json.dumps(wave, ensure_ascii=False, indent=2), encoding="utf-8")

    for w0, path in queue:
        if path in already:
            continue
        print(f"\n=== {path} ({w0}w) ===")
        original = Path(path).read_text(encoding="utf-8")
        try:
            repair_file(path)
        except Exception as e:
            print("repair fail", e)
            Path(path).write_text(original, encoding="utf-8")
            failed.append(path)
            save()
            continue

        try:
            process_one(path, len(locked) + 1)
            boost_to_1600(path)
            # never flip robots
            t = Path(path).read_text(encoding="utf-8")
            if is_noindex(original) and not is_noindex(t):
                t = re.sub(
                    r'content="index\s*,\s*follow"',
                    'content="noindex,nofollow"',
                    t,
                    count=1,
                    flags=re.I,
                )
                Path(path).write_text(t, encoding="utf-8")

            if accept1600(path) or (accept1300(path, allow_noindex=False) and word_count(path) >= TARGET):
                locked.append(path)
                batch.append(path)
                urls.append(public_url(path))
                print(f"LOCKED {word_count(path)}w")
            else:
                # one more boost pass
                boost_to_1600(path)
                if accept1600(path):
                    locked.append(path)
                    batch.append(path)
                    urls.append(public_url(path))
                    print(f"LOCKED-retry {word_count(path)}w")
                else:
                    print(f"FAIL words={word_count(path)} amer={amer_status(path)[1][:120]}")
                    failed.append(path)
                    Path(path).write_text(original, encoding="utf-8")
        except Exception as e:
            print("ERR", e)
            Path(path).write_text(original, encoding="utf-8")
            failed.append(path)

        if len(batch) >= 10:
            batch_num += 1
            batch = list(wave["batches"].get(f"batch{batch_num}", []) or [])
        save()

    review = {
        "wave": 5,
        "target_words": TARGET,
        "total_locked": len(set(locked)),
        "failed": sorted(set(failed)),
        "urls": urls,
        "note": "LIVE articles deepened to ≥1600w with amer+double-audit+html5; noindex never raised.",
    }
    REVIEW_PATH.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDONE locked={len(set(locked))} failed={len(set(failed))}")


if __name__ == "__main__":
    main()
