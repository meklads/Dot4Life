#!/usr/bin/env python3
"""Seed data/capsules-published.json with 7 days of capsules (static-first mode)."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'capsules-published.json'

TEMPLATES = [
  {'category': 'wellness', 'emoji': '🌅', 'title_en': 'Wake Up Without Your Phone', 'title_ar': 'استيقظ بلا هاتف',
   'subtitle_en': 'The first 15 minutes set everything', 'subtitle_ar': 'أول 15 دقيقة تحدد كل شيء',
   'body_en': 'Keep the first 15 minutes screen-free — drink water, stretch, be still.',
   'body_ar': 'اجعل أول 15 دقيقة بلا شاشة — اشرب ماء، تمدد، كن هادئاً.',
   'tip_en': 'Put your phone on airplane mode before bed.', 'tip_ar': 'اجعل هاتفك على وضع الطيران قبل النوم.'},
  {'category': 'family', 'emoji': '👨‍👩‍👧', 'title_en': 'The Dinner Question', 'title_ar': 'سؤال العشاء',
   'subtitle_en': 'Better than "how was your day?"', 'subtitle_ar': 'أفضل من "كيف كان يومك؟"',
   'body_en': 'Ask: "What made you laugh today?" Specific questions get real answers.',
   'body_ar': 'اسأل: "ما الذي أضحكك اليوم؟" الأسئلة المحددة تجيب إجابات حقيقية.',
   'tip_en': 'Let each person answer before anyone comments.', 'tip_ar': 'دع كل شخص يجيب قبل أن يعلق أحد.'},
  {'category': 'faith', 'emoji': '🕌', 'title_en': 'The Fajr Gift', 'title_ar': 'هدية الفجر',
   'subtitle_en': 'Starting the day in peace', 'subtitle_ar': 'ابدأ اليوم بسلام',
   'body_en': 'That quiet walk to prayer sets a completely different tone for the day.',
   'body_ar': 'تلك المشية الهادئة للصلاة تضع نغمة مختلفة تماماً لليوم.',
   'tip_en': 'Sleep with the intention and ask your family to wake you.', 'tip_ar': 'نم بنية النية واطلب من عائلتك إيقاظك.'},
  {'category': 'money', 'emoji': '💰', 'title_en': 'The 24-Hour Rule', 'title_ar': 'قاعدة الـ24 ساعة',
   'subtitle_en': 'Stop impulse buying', 'subtitle_ar': 'أوقف الشراء الاندفاعي',
   'body_en': 'For any non-essential purchase over 200 SAR, wait 24 hours.',
   'body_ar': 'لأي شراء غير ضروري فوق 200 ريال، انتظر 24 ساعة.',
   'tip_en': 'Unsave your credit card from online stores.', 'tip_ar': 'احذف معلومات بطاقتك من المتاجر الإلكترونية.'},
  {'category': 'living', 'emoji': '🏠', 'title_en': 'The Clutter-Free Corner', 'title_ar': 'الزاوية الخالية من الفوضى',
   'subtitle_en': 'Start small — one corner at a time', 'subtitle_ar': 'ابدأ صغيراً — زاوية واحدة',
   'body_en': 'Spend 10 minutes clearing one visible corner.',
   'body_ar': 'اقضِ 10 دقائق في ترتيب زاوية واحدة مرئية.',
   'tip_en': 'Before and after photos are incredibly motivating.', 'tip_ar': 'صور قبل وبعد تحفّز بشكل لا يصدق.'},
  {'category': 'meals', 'emoji': '🍳', 'title_en': 'Eggs Three Ways', 'title_ar': 'البيض بثلاث طرق',
   'subtitle_en': 'Quick family dinner', 'subtitle_ar': 'عشاء عائلية سريع',
   'body_en': 'Scrambled, shakshuka, or egg curry — a family dinner solved with eggs is a win.',
   'body_ar': 'مخفوق، شكشوكة، أو كاري — عشاء عائلي بالبيض هو فوز.',
   'tip_en': 'Add vegetables to eggs.', 'tip_ar': 'أضف خضروات للبيض.'},
  {'category': 'wellness', 'emoji': '💧', 'title_en': 'Hydrate Before Everything', 'title_ar': 'الترطيب قبل كل شيء',
   'subtitle_en': 'Your brain works better with water', 'subtitle_ar': 'دماغك يعمل أفضل بالماء',
   'body_en': 'Keep a 1L bottle on your desk and finish it by lunch.',
   'body_ar': 'احتفظ بقنينة 1 لتر على مكتبك وأنهِها قبل الغداء.',
   'tip_en': 'Add mint or lemon.', 'tip_ar': 'أضف نعناعاً أو ليموناً.'},
]


def main():
    start = date.today()
    by_date = {}
    by_id = {}
    for i in range(7):
        d = start + timedelta(days=i)
        ds = d.isoformat()
        t = TEMPLATES[i % len(TEMPLATES)]
        cid = f'cap_{ds.replace("-", "")}_{i:02d}'
        entry = {'id': cid, **t}
        by_date[ds] = entry
        by_id[cid] = entry
    payload = {
        'updated': start.isoformat(),
        'mode': 'static',
        'byDate': by_date,
        'byId': by_id,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {OUT} — {len(by_date)} days from {start.isoformat()}')


if __name__ == '__main__':
    main()
