#!/usr/bin/env python3
"""Remove direct religious textual attributions from EN batch 1 (8 files)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "assets/queue/masjid-nabawi-complete-guide-en.html",
    "blog/masjid-nabawi-complete-guide-en.html",
    "blog/digital-minimalism-modern-families-en.html",
    "blog/life-insurance-gulf-families-en.html",
    "blog/islamic-inheritance-basics-en.html",
    "blog/zakat-guide-2025-en.html",
    "finance-wealth/teaching-children-savings-en.html",
    "islamic-hajj-umrah/hajj-first-timers-guide-en.html",
]

# Applied only outside <script type="application/ld+json"> blocks.
COMMON: list[tuple[str, str]] = [
    (
        'with the companions (Sahabah) actively participating alongside the Prophet ﷺ, reciting: "O Allah, there is no good except the good of the Hereafter, so forgive the Ansar and the Muhajirun."',
        "with the companions (Sahabah) actively participating alongside the Prophet ﷺ in building the mosque.",
    ),
    (
        'The Prophet ﷺ said: "What is between my house and my pulpit is a garden from the gardens of Paradise."',
        "Islamic tradition holds that the area between the pulpit and the Prophet's chamber (the Rawdah) carries special spiritual significance.",
    ),
    (
        '<p>The recommended greeting is: "Peace be upon you, O Messenger of Allah, and the mercy of Allah and His blessings," followed by greetings to Abu Bakr and Umar.</p>',
        "<p>Visitors offer respectful greetings of peace at the chamber; learn the traditional salutation from qualified guides or official apps before your visit.</p>",
    ),
    (
        'Allah mentions in Surah at-Tawbah (9:108): "Indeed, a mosque founded on righteousness from the first day is more worthy for you to stand in. Within it are men who love to purify themselves; and Allah loves those who purify themselves." Prayer in the Prophet\'s Mosque carries immense reward; the Prophet ﷺ said: "One prayer in this mosque of mine is better than a thousand prayers elsewhere, except in al-Masjid al-Haram."',
        "Islamic teaching holds that this mosque was founded on righteousness and that prayer here carries immense spiritual reward, second only to al-Masjid al-Haram.",
    ),
    (
        'as the Prophet ﷺ said: "Do not set out on a journey except to three mosques: al-Masjid al-Haram, this mosque of mine, and al-Masjid al-Aqsa."',
        "as Islamic teaching encourages purposeful travel to the three holy mosques: al-Masjid al-Haram, Masjid an-Nabawi, and al-Masjid al-Aqsa.",
    ),
    (
        "<p>According to hadith, a prayer in Masjid an-Nabawi is better than a thousand prayers elsewhere, except in al-Masjid al-Haram. Visitors therefore aim to perform as many prayers as possible during their stay.</p>",
        "<p>Islamic teaching holds that prayer in Masjid an-Nabawi carries exceptional reward, second only to al-Masjid al-Haram. Visitors therefore aim to perform as many prayers as possible during their stay.</p>",
    ),
    (
        'The Quran reminds us: "And do not pursue that of which you have no knowledge. Indeed, the hearing, the sight and the heart , about all those [one] will be questioned" (Al-Isra 17:36).',
        "Islamic teaching reminds us to use sight, hearing, and the heart responsibly, and that we are accountable for how we use them.",
    ),
    (
        'The Quran says: "Indeed, the wasteful are brothers of the devils" (Al-Isra 17:27). Hours lost to aimless scrolling are a form of waste that we will be questioned about on the Day of Judgment. The Prophet Muhammad (peace be upon him) said: "A person will not be able to move on the Day of Judgment until he is asked about four things , among them: how he spent his life" (Tirmidhi).',
        "Islamic teaching warns against wastefulness with time as well as resources. Hours lost to aimless scrolling are a form of waste, and believers are encouraged to reflect on how they spend their days.",
    ),
    (
        'Umar ibn Al-Khattab (may Allah be pleased with him) said: "Hold yourself accountable before you are held accountable."',
        "Islamic tradition encourages self-accountability before final accountability.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said: "It is better for you to leave your heirs wealthy than to leave them poor, begging from others."',
        "Islamic values encourage leaving your family financially protected rather than dependent on others.",
    ),
    (
        'Allah says in the Qur\'an: "And do not give the foolish your property, which Allah has made a means of support for you" (An-Nisa 4:5). This verse reminds us that managing wealth is a responsibility that must be learned. The Prophet Muhammad ﷺ said: "A strong believer is better and more beloved to Allah than a weak believer". and financial strength is part of that strength.',
        "Islamic teaching reminds us that wealth is a responsibility to be managed wisely, not handed carelessly to those unprepared to use it. Building financial strength and self-discipline supports both worldly stability and spiritual growth.",
    ),
    (
        'Allah says in the Quran: <strong>"Take from their wealth a charity to purify and sanctify them"</strong> (At-Tawbah 9:103).',
        "Zakat purifies wealth and supports those in need, a core purpose taught across Islamic finance guidance.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said, "Learn the laws of inheritance and teach them, for they are half of knowledge" (Ibn Majah).',
        "Islamic tradition places strong emphasis on learning and teaching inheritance rules.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said: "Whoever performs Hajj and does not commit any obscenity or wrongdoing will come back as pure as the day his mother gave birth to him." Think about that. You have a chance to wipe the slate completely clean.',
        "Hajj offers a profound opportunity for spiritual renewal and repentance when performed with sincerity and good conduct.",
    ),
    (
        'the Prophet said: "Hajj is Arafat."',
        "standing at Arafat is the essential heart of Hajj.",
    ),
]


def strip_ld_json(html: str) -> tuple[str, list[str]]:
    blocks: list[str] = []

    def keep(m: re.Match[str]) -> str:
        blocks.append(m.group(0))
        return f"__LDJSON_{len(blocks) - 1}__"

    stripped = re.sub(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        keep,
        html,
        flags=re.S | re.I,
    )
    return stripped, blocks


def restore_ld_json(html: str, blocks: list[str]) -> str:
    for i, block in enumerate(blocks):
        html = html.replace(f"__LDJSON_{i}__", block, 1)
    return html


def apply_replacements(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def fix_file(rel: str) -> int:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    robots_before = re.search(r'<meta name="robots" content="[^"]+"', html)
    stripped, blocks = strip_ld_json(html)
    changed = 0
    for old, new in COMMON:
        if old in stripped:
            stripped = stripped.replace(old, new)
            changed += 1
    out = restore_ld_json(stripped, blocks)
    robots_after = re.search(r'<meta name="robots" content="[^"]+"', html)
    if robots_before and robots_after and robots_before.group(0) != robots_after.group(0):
        raise SystemExit(f"robots changed in {rel}")
    if out != html:
        path.write_text(out, encoding="utf-8")
    print(f"{rel}: {changed} pattern(s) applied, written={out != html}")
    return changed


def main() -> None:
    for rel in FILES:
        fix_file(rel)


if __name__ == "__main__":
    main()
