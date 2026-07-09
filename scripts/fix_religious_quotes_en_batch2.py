#!/usr/bin/env python3
"""EN religious quotes batch 2 + masjid FAQPage schema text (explicit permission)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MASJID_ONLY = ["blog/masjid-nabawi-complete-guide-en.html"]

BATCH2 = [
    "islamic-hajj-umrah/umrah-with-elderly-parents-en.html",
    "islamic-hajj-umrah/spiritual-benefits-umrah-families-en.html",
    "islamic-hajj-umrah/spiritual-preparation-umrah-family-en.html",
    "islamic-hajj-umrah/umrah-off-peak-seasons-guide-en.html",
    "peace-capsules/art-of-sincere-apology-marriage-en.html",
    "peace-capsules/power-of-i-love-you-arab-families-en.html",
    "peace-capsules/power-of-patience-marriage-en.html",
    "real-estate/three-generation-table-family-meals-en.html",
]

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "According to hadith, a prayer in Masjid an-Nabawi is better than a thousand prayers elsewhere, except in al-Masjid al-Haram. Visitors therefore aim to perform as many prayers as possible during their stay.",
        "Prayer in Masjid an-Nabawi carries immense spiritual reward according to Islamic tradition, and visitors aim to pray as many times as possible during their stay.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said, <em>"He is not one of us who does not show mercy to our young and respect to our elders."</em>',
        "Islamic teaching emphasizes showing mercy to children and respect to elders",
    ),
    (
        'Allah says in the Qur\'an: <em>"And your Lord has decreed that you not worship except Him, and to parents, good treatment. Whether one or both of them reach old age [while] with you, say not to them [so much as] \'uff,\' and do not repel them but speak to them a noble word."</em> (Al-Isra 17:23).',
        "Islamic teaching places honoring parents among the highest duties, including caring for them in old age with patience and a noble word.",
    ),
    (
        'The Prophet (peace be upon him) said, <em>"This religion is ease, and no one will ever make the religion hard except that it will overcome him."</em>',
        "Islamic teaching emphasizes ease in worship; avoid making rituals harder than your parent can bear",
    ),
    (
        'the Prophet (peace be upon him) said "This religion is ease."',
        "Islamic teaching reminds us that worship should remain within your parent's capacity",
    ),
    (
        "The Prophet Muhammad (peace be upon him) said that prayer in congregation is twenty-seven times more rewarding than prayer alone.",
        "Islamic teaching holds that congregational prayer carries greater reward than prayer alone.",
    ),
    (
        "The Prophet (peace be upon him) said that the believer who mixes with people and endures their harm is better than the one who avoids people and does not endure their harm.",
        "Islamic teaching values the believer who engages patiently with people despite difficulties.",
    ),
    (
        "The Prophet (peace be upon him) said that Umrah expiates sins between one Umrah and the next, and doing it as a family multiplies the barakah.",
        "Islamic tradition holds that Umrah brings spiritual renewal, and doing it as a family multiplies the barakah.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said: "Umrah is an expiation for the sins committed between it and the previous Umrah" (Bukhari and Muslim).',
        "Islamic tradition holds that Umrah brings spiritual renewal between one journey and the next.",
    ),
    (
        "The Prophet (peace be upon him) said that the greatest jihad is a word of truth in the presence of a tyrant.",
        "Islamic teaching values speaking truth with courage, even when it is difficult.",
    ),
    (
        'The Prophet Muhammad (peace be upon him) said: "The one who initiates the greeting of peace is free from pride" (al-Mundhiri).',
        "Islamic teaching encourages humility, including being the first to greet others with peace.",
    ),
    (
        'Allah says in the Quran: "Let them pardon and forgive. Do you not wish that Allah should forgive you?" (Quran 24:22).',
        "Islamic teaching links forgiving others with seeking Allah's mercy.",
    ),
    (
        'The Prophet (peace be upon him) said: "The best of you are those who are best to their families, and I am the best among you to my family" (Tirmidhi).',
        "Islamic teaching ranks excellence in family treatment among the highest virtues.",
    ),
    (
        'The Prophet (peace be upon him) said: "The best of you are the best to their wives" (Ibn Majah).',
        "Islamic teaching encourages spouses to treat each other with consistent kindness and repair.",
    ),
    (
        'The Prophet (peace be upon him) said: "Eat together, for there is barakah in togetherness."',
        "Islamic tradition encourages eating together as a source of barakah in the home.",
    ),
    (
        '<p>There is a hadith that every person reading this should know. A companion came to the Prophet ﷺ and said, "O Messenger of Allah, I love this man for the sake of Allah." The Prophet ﷺ asked, "Did you tell him?" The companion said no. So the Prophet ﷺ told him: <strong>"Go and inform him that you love him for the sake of Allah."</strong> (Abu Dawood, authentic).</p>\n\n<p>Think about that. The Prophet ﷺ did not simply approve of expressing love ,  he commanded it. He instructed a grown man to actively go and say, "I love you." This was not a recommendation for romantic partners or close friends only. This was for a brother in faith. How much more important is it, then, within your own family?</p>\n\n<p>In another hadith, the Prophet ﷺ said: <strong>"When a man loves his brother, let him tell him that he loves him."</strong> (Abu Dawood, Tirmidhi). The word used here is <em>yuhibbuhu</em> ,  the same root as <em>hubb</em>, love. The Prophet ﷺ did not say "show him through actions." He said: tell him. Say it.</p>\n\n<p>And the Quran itself describes love between spouses as one of the great signs of Allah: <strong>"And among His signs is that He created for you from yourselves mates that you may find tranquility in them, and He placed between you affection and mercy."</strong> (Quran 30:21). The word <em>mawaddah</em> (affection) implies not just feeling love but expressing it warmly.</p>',
        "<p>Islamic teaching encourages expressing love openly, not only feeling it privately. Telling family members that you love them removes doubt and strengthens bonds. Marriage is also described in Islamic teaching as a relationship rooted in affection and mercy, where warm words matter as much as acts of service.</p>",
    ),
    (
        'Absolutely. The Prophet Muhammad ﷺ not only expressed love verbally but taught his companions to do the same. He told a companion, "I love you for the sake of Allah" and instructed him to inform others of that love. In another hadith, the Prophet said, "When a man loves his brother, let him tell him that he loves him." The Quran also describes love and mercy between spouses as signs of Allah.',
        "Absolutely. Islamic tradition strongly encourages expressing love openly within the family. Teaching companions to share affection verbally reflects a values-based approach that complements acts of service. Marriage is also described in Islamic teaching as a relationship rooted in love and mercy.",
    ),
    (
        "The Prophet (peace be upon him) said: 'There should be neither harm nor reciprocating harm' (Ibn Majah).",
        "Islamic teaching prohibits causing harm or accepting ongoing harm without seeking reform.",
    ),
    (
        'The Prophet (peace be upon him) said: "There should be neither harm nor reciprocating harm" (Ibn Majah).',
        "Islamic teaching prohibits causing harm or accepting ongoing harm without seeking reform.",
    ),
    (
        'The Prophet (peace be upon him) said: "Richness is not the abundance of worldly goods, but richness is the richness of the soul" (Bukhari and Muslim).',
        "Islamic teaching defines true richness as contentment of the soul, not abundance of possessions.",
    ),
    (
        'Allah says: "And if a woman fears from her husband contempt or evasion, there is no sin upon them if they make terms of settlement between them ,  and settlement is best" (An-Nisa 4:128).',
        "Islamic teaching permits settlement, mediation, and lawful separation when contempt or harm persists in marriage.",
    ),
    (
        'The Prophet (peace be upon him) did not ask women who suffered abuse to simply "be patient"',
        "Islamic teaching does not require anyone to endure abuse silently without seeking help",
    ),
    (
        'The Prophet (peace be upon him) said: "No one is given a better and more abundant gift than patience" (Bukhari and Muslim).',
        "Islamic tradition ranks patience among the greatest spiritual gifts.",
    ),
    (
        "The Prophet (peace be upon him) said: 'No one is given a better and more abundant gift than patience' (Bukhari and Muslim).",
        "Islamic tradition ranks patience among the greatest spiritual gifts.",
    ),
    (
        "Allah promises: 'Indeed, the patient will be given their reward without account' (Az-Zumar 39:10) ,  meaning the reward is limitless. Patience is a means of receiving Allah's companionship: 'Indeed, Allah is with the patient' (Al-Baqarah 2:153). It is a path to paradise: 'Peace be upon you for what you patiently endured' (Ar-Rad 13:24).",
        "Islamic teaching promises immense reward for patience, divine support in difficulty, and peace for those who endure with faith.",
    ),
    (
        "Key verses include: 'Indeed, Allah is with the patient' (Al-Baqarah 2:153), 'And seek help through patience and prayer' (Al-Baqarah 2:45), and 'Only those who are patient shall receive their reward in full, without reckoning' (Az-Zumar 39:10).",
        "Islamic teaching repeatedly links patience with divine support, prayer, and limitless reward.",
    ),
    (
        "The Prophet (peace be upon him) advised patience during times of trial but never instructed anyone to remain in a situation that harms their faith or well-being.",
        "Islamic teaching advises patience during trial but not remaining in situations that harm faith or well-being.",
    ),
    (
        "remember the Prophet's example: he never retaliated against personal slights and was the most patient of husbands.",
        "Islamic tradition models patience and restraint in marriage, even under personal slights.",
    ),
    (
        'Absolutely. The Prophet Muhammad ﷺ not only expressed love verbally but taught his companions to do the same. He told a companion, \'I love you for the sake of Allah\' and instructed him to inform others of that love. In another hadith, the Prophet said, \'When a man loves his brother, let him tell him that he loves him.\' The Quran also describes love and mercy between spouses as signs of Allah.',
        "Absolutely. Islamic tradition strongly encourages expressing love openly within the family. Teaching companions to share affection verbally reflects a values-based approach that complements acts of service. Marriage is also described in Islamic teaching as a relationship rooted in love and mercy.",
    ),
    (
        "<p>The word sabr and its derivatives appear more than 140 times in the Quran. Allah commands patience in times of fear, hunger, and loss (Al-Baqarah 2:155). He promises that \"Indeed, Allah is with the patient\" (Al-Baqarah 2:153). He pairs patience with prayer as the two essential supports: \"And seek help through patience and prayer\" (Al-Baqarah 2:45). And He reserves an extraordinary reward for those who practise it: \"Only those who are patient shall receive their reward in full, without reckoning\" (Az-Zumar 39:10) ,  meaning the reward is so immense that it bypasses the usual scales of accounting.</p>",
        "<p>The word sabr and its derivatives appear more than 140 times in the Quran. Islamic teaching repeatedly links patience with divine support, prayer, and limitless reward for those who endure hardship with faith.</p>",
    ),
    (
        '<p>The Quran offers a direct instruction: "Let the wealthy spend from his wealth, and he whose provision is restricted ,  let him spend from what Allah has given him. Allah does not charge a soul except [according to] what He has given it" (At-Talaq 65:7). This verse is a reminder that provision comes from Allah alone, and that financial hardship is a test for both spouses.',
        "<p>Islamic teaching reminds couples to spend according to their means and that provision is a trust from Allah. Financial hardship is a test for both spouses",
    ),
    (
        '<p>In marriage, patience and forgiveness are inseparable. Patience is the vessel that carries you through the difficult moment. Forgiveness is what you do when you arrive on the other side. The Quran pairs them beautifully: "And if you pardon and overlook and forgive ,  then indeed, Allah is Forgiving and Merciful" (At-Taghabun 64:14). This verse is addressed directly to spouses and family members.</p>',
        "<p>In marriage, patience and forgiveness are inseparable. Patience carries you through the difficult moment; forgiveness is what you offer when you arrive on the other side. Islamic teaching encourages pardon and mercy between spouses and family members.</p>",
    ),
    (
        "<p>Aisha (may Allah be pleased with her) narrated that the Prophet (peace be upon him) never struck anyone with his hand ,  not a woman, not a servant ,  and he never retaliated against personal wrongs. But he did take action when the boundaries of Allah were violated. This is the model: patience for personal slights, firmness for principles. Forgiveness is not weakness; it is the strongest form of patience, because it means releasing your right to retaliate for the sake of Allah.</p>",
        "<p>Islamic tradition models restraint in personal conflicts, firmness on principles, and forgiveness as a form of strength rather than weakness in marriage.</p>",
    ),
    (
        "The rewards of sabr are immense. Allah promises: 'Indeed, the patient will be given their reward without account' (Az-Zumar 39:10) ,  meaning the reward is limitless. Patience is a means of receiving Allah's companionship: 'Indeed, Allah is with the patient' (Al-Baqarah 2:153). It is a path to paradise: 'Peace be upon you for what you patiently endured. And excellent is the final home' (Ar-Rad 13:24). The Prophet (peace be upon him) said: 'Whoever remains patient, Allah will make him patient. No one is given a better and more abundant gift than patience' (Bukhari and Muslim).",
        "The rewards of sabr are immense. Islamic teaching promises immense reward for patience, divine support in difficulty, and peace for those who endure with faith. Islamic tradition ranks patience among the greatest spiritual gifts.",
    ),
    # Single-quote schema variants + remaining batch2 misses
    (
        "the Prophet (peace be upon him) said 'This religion is ease.'",
        "Islamic teaching reminds us that worship should remain within your parent's capacity.",
    ),
    (
        "The Prophet (peace be upon him) never responded to a mistake with harshness.",
        "Islamic teaching encourages responding gently to mistakes, not with harshness.",
    ),
    (
        "The Prophet advised the one who wronged to stay patient and keep showing good conduct.",
        "Islamic teaching advises the one who wronged to stay patient and keep showing good conduct.",
    ),
    (
        "The Prophet's sunnah shows that action completes words.",
        "Islamic tradition shows that action completes words.",
    ),
    (
        "The Prophet was always the first to initiate reconciliation.",
        "Islamic tradition encourages being the first to initiate reconciliation.",
    ),
    (
        "The Prophet said that whoever humbles themselves before Allah for His sake, Allah raises their rank.",
        "Islamic teaching holds that humbling oneself before Allah leads to being raised in rank.",
    ),
    (
        "a sunnah of the Prophet (peace be upon him),",
        "a practice rooted in Islamic tradition,",
    ),
    (
        'The sunnah of the Prophet is even more direct. <a href="https://sunnah.com/bukhari/78/113" target="_blank" rel="noopener">Aisha (may Allah be pleased with her) reported that the Prophet never struck a servant or a woman with his hand</a>. When he was wronged, he did not retaliate. He forgave.',
        "Islamic tradition is even more direct: restraint in conflict, refusal to retaliate, and readiness to forgive.",
    ),
    (
        "The Prophet was patient even when people wronged him repeatedly.",
        "Islamic tradition models patience even when people wrong us repeatedly.",
    ),
    (
        '<a href="https://sunnah.com/tirmidhi/27/77" target="_blank" rel="noopener">The Prophet\'s sunnah shows that action completes words</a>.',
        "Islamic tradition shows that action completes words.",
    ),
    (
        "drawing from the Quran, the Sunnah, the example of the Prophet Muhammad (peace be upon him) and Khadija (may Allah be pleased with her), and modern relationship science.",
        "drawing from the Quran, Islamic tradition, the example of Khadija (may Allah be pleased with her), and modern relationship science.",
    ),
    (
        "Consider the example of the Prophet Muhammad (peace be upon him). When his wife Aisha (may Allah be pleased with her) was slandered by hypocrites, he did not react impulsively. He waited, he prayed, he consulted. And then, when the revelation came clearing her name, he acted with justice and compassion. His patience was not weakness ,  it was strategic trust in Allah.",
        "Islamic tradition offers examples of couples facing public slander and hardship with prayer, consultation, and restraint until the right moment to act with justice and compassion. Such patience is not weakness ,  it is strategic trust in Allah.",
    ),
    (
        "The Prophet (peace be upon him) demonstrated extraordinary patience as a father. He carried his grandchildren on his back during prayer. He let them climb on him while he was speaking. He waited while his grandson Hasan climbed onto his shoulders.",
        "Islamic tradition models extraordinary patience as parents and grandparents ,  making room for children's needs even during prayer or conversation.",
    ),
    (
        "The Prophet (peace be upon him) set the example. He never asked any of his wives to tolerate injustice from his family. When relatives spoke harshly, he addressed it. When his daughter Fatima faced difficulty, he supported her.",
        "Islamic teaching sets a clear example: spouses should not be asked to tolerate injustice from in-laws. When relatives speak harshly, address it; when a daughter or son faces difficulty, offer support.",
    ),
    (
        "The Prophet (peace be upon him) taught this as the first line of defence against anger.",
        "Islamic teaching recommends this as a first line of defence against anger.",
    ),
    (
        "The Prophet (peace be upon him) advised patience during trials but never instructed anyone to remain in a situation that harms their faith or well-being.",
        "Islamic teaching advises patience during trials but not remaining in situations that harm faith or well-being.",
    ),
    (
        "Islamic teaching does not require anyone to endure abuse silently without seeking help ,  he took action, supported them, and in some cases approved separation.",
        "Islamic teaching does not require anyone to endure abuse silently without seeking help; settlement, mediation, and lawful separation are permitted when harm persists.",
    ),
    (
        "<p>The Prophet Muhammad ﷺ was the most loving of fathers and husbands. He did not simply feel love; he spoke it freely. He told his daughter Fatimah (may Allah be pleased with her) that he loved her, and he told his wife Aishah (may Allah be pleased with her) plainly that he loved her. His love was not hidden behind formality or shyness.</p>",
        "<p>Islamic tradition models expressing love openly within the family ,  not only through acts of service but through warm words between parents, spouses, and children. Love that is spoken removes doubt and strengthens bonds that actions alone cannot fully reach.</p>",
    ),
]


def validate_ld_json(html: str, rel: str) -> None:
    for i, m in enumerate(
        re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html,
            re.S | re.I,
        )
    ):
        raw = m.group(1).strip()
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            raise SystemExit(f"{rel}: JSON-LD block {i + 1} invalid: {e}") from e


def robots_unchanged(before: str, after: str, rel: str) -> None:
    rb = re.search(r'<meta name="robots" content="([^"]+)"', before)
    ra = re.search(r'<meta name="robots" content="([^"]+)"', after)
    if (rb.group(1) if rb else None) != (ra.group(1) if ra else None):
        raise SystemExit(f"robots changed in {rel}")


def fix_file(rel: str) -> bool:
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    html = before
    n = 0
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            n += 1
    validate_ld_json(html, rel)
    robots_unchanged(before, html, rel)
    if html != before:
        path.write_text(html, encoding="utf-8")
    print(f"{rel}: {n} patterns, written={html != before}")
    return html != before


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    files = MASJID_ONLY if mode == "masjid" else (MASJID_ONLY + BATCH2 if mode == "all" else BATCH2)
    changed = sum(fix_file(rel) for rel in files)
    print(f"done: {changed}/{len(files)} files changed")


if __name__ == "__main__":
    main()
