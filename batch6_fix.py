#!/usr/bin/env python3
"""
Batch 6: BOOM compliance for remaining 22 blog articles.
- Articles with bilingual <span class="en">/<span class="ar"> pairs
- Extracts AR and EN content, wraps in BOOM template
- Creates redirect files (-ar.html)
"""

import re, os, json

BLOG = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life/blog"
ROOT = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life"

def extract_ar_from_body(body):
    body = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\2', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<span class="en">.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<h2>([a-zA-Z\s\:\-\'\,\.]+)([؀-ۿ].*?)</h2>', r'<h2>\2</h2>', body)
    return body

def extract_en_from_body(body):
    body = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\2', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="en">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<h2>([a-zA-Z\s\:\-\'\,\.]+)([؀-ۿ].*?)</h2>', r'<h2>\1</h2>', body)
    return body

def strip_old_sections(body):
    body = re.sub(r'<h2[^>]*>[^<]*Related[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<h2[^>]*>[^<]*مقالات[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<h2[^>]*>[^<]*Related[^<]*</h2>', '', body, flags=re.DOTALL)
    body = re.sub(r'<h2[^>]*>[^<]*مقالات[^<]*</h2>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="article-end">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="article-share">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<aside class="article-sidebar">.*?</aside>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="article-tool-cta">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="article-tools">.*?</div>\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<li>\s*</li>', '', body)
    body = re.sub(r'<span>\s*</span>', '', body)
    return body

def make_heading_id(text):
    h_id = text.replace(' ', '-')
    h_id = re.sub(r'[^؀-ۿ\w-]', '', h_id)
    h_id = re.sub(r'-+', '-', h_id).strip('-')
    if not h_id:
        h_id = f"section-{abs(hash(text)) % 1000}"
    return h_id

def balance_divs(html):
    opens = list(re.finditer(r'<div\b', html))
    closes = list(re.finditer(r'</div>', html))
    diff = len(opens) - len(closes)
    if diff > 0:
        html += '\n' + '</div>' * diff
    elif diff < 0:
        html = ('<div>' * abs(diff)) + '\n' + html
    return html

def fix_malformed_h2s(body):
    result = []
    i = 0
    while i < len(body):
        h2_start = body.find('<h2', i)
        if h2_start == -1:
            result.append(body[i:])
            break
        close_gt = body.find('>', h2_start)
        if close_gt == -1:
            result.append(body[i:])
            break
        h2_close = body.find('</h2>', close_gt)
        next_h2 = body.find('<h2', close_gt + 1, h2_close) if h2_close != -1 else -1
        if next_h2 != -1:
            result.append(body[i:h2_start])
            result.append(body[h2_start:close_gt+1])
            result.append(body[close_gt+1:next_h2])
            result.append('</h2>')
            i = next_h2
        else:
            if h2_close != -1:
                result.append(body[i:h2_close+6])
                i = h2_close + 6
            else:
                result.append(body[i:])
                break
    return ''.join(result)

HEADING_TRANS = {
    'the foundation: prayer on time': 'الأساس: الصلاة في وقتها',
    'morning and evening adhkar': 'أذكار الصباح والمساء',
    'daily quran reading': 'قراءة القرآن اليومية',
    'using the qibla direction': 'استخدام اتجاه القبلة',
    'tracking your hijri calendar': 'تتبع التقويم الهجري',
    'building a system that lasts': 'بناء نظام يدوم',
    'integrating technology for good': 'توظيف التكنولوجيا للخير',
    'tools that support your digital minimalism journey': 'أدوات تدعم رحلتك في البساطة الرقمية',
    'a calmer home starts today': 'بيت هادئ يبدأ اليوم',
    'the gulf family digital dilemma': 'المعضلة الرقمية للأسرة الخليجية',
    'why digital minimalism hits different in the gulf': 'لماذا البساطة الرقمية مختلفة في الخليج',
    'the hidden costs of screen overload': 'التكاليف الخفية لفرط الشاشات',
    'a practical framework for gulf families': 'إطار عملي للعائلات الخليجية',
    'managing whatsapp without losing family connection': 'إدارة واتساب دون فقدان التواصل العائلي',
    'children and screens, a developmental approach': 'الأطفال والشاشات: نهج تطوري',
    "the parent's mirror": 'الوالد: المرآة',
    'the 30-day digital minimalism challenge': 'تحدي 30 يوماً للبساطة الرقمية',
    'more than a bonus, it legal right': 'أكثر من مكافأة، إنه حق قانوني',
    "more than a bonus, it's a legal right": 'أكثر من مكافأة، إنه حق قانوني',
    'the core formula': 'المعادلة الأساسية',
    'resignation vs termination, a big difference': 'الاستقالة مقابل الفصل: فرق كبير',
    'three costly mistakes to avoid': 'ثلاثة أخطاء مكلفة تجنبها',
    'why the same salary requires different strategies': 'لماذا يحتاج نفس الراتب إلى استراتيجيات مختلفة',
    'the expat financial imperative: save 30%+ every month': 'الضرورة المالية للمقيم: ادّخر 30%+ شهرياً',
    'what saudi nationals often under-invest in': 'ما يُقلّل منه المواطنون السعوديون في الاستثمار',
    'the gulf family travel paradox': 'مفارقة السفر العائلي الخليجي',
    'why gulf families overspend on travel': 'لماذا تُفرط العائلات الخليجية في الإنفاق على السفر',
    'the 6-step budget travel system': 'نظام السفر ذي الميزانية المحدودة بـ 6 خطوات',
    'destination deep dives for gulf families': 'غوص في الوجهات للعائلات الخليجية',
    'the ultimate packing system for family travel': 'نظام التجهيز الأمثل للسفر العائلي',
    'travel insurance, why you need it': 'تأمين السفر: لماذا تحتاجه',
    'halal-friendly travel considerations': 'اعتبارات السفر الحلال',
    'tools to plan your next family trip': 'أدوات تخطيط رحلتك العائلية القادمة',
    'the proximity premium': 'علاوة القرب',
    'amenities and comfort: what you get for the price': 'وسائل الراحة: ما تحصل عليه مقابل السعر',
    'the mid-range compromise': 'حل الوسط',
    'family-specific considerations': 'اعتبارات خاصة بالعائلة',
    'making your decision': 'اتخاذ قرارك',
    'a duty most families postpone': 'واجب تؤجله معظم العائلات',
    'fixed shares come first': 'الأنصبة الثابتة أولاً',
    'common inheritance scenarios': 'سيناريوهات الميراث الشائعة',
    'when shares shift: complex situations': 'عندما تتغير الأنصبة: حالات معقدة',
    'why a calculator helps, but a scholar decides': 'لماذا تساعد الحاسبة لكن العالم يقرر',
    'act now, before it needed': 'تصرف الآن قبل الحاجة',
    "act now, before it's needed": 'تصرف الآن قبل الحاجة',
    'heat is not just physical, it rewires your brain': 'الحر ليس جسدياً فقط، إنه يعيد توصيل دماغك',
    'the gulf summer sleep problem': 'مشكلة النوم في صيف الخليج',
    'why the gulf knowledge worker has it harder': 'لماذا العامل المعرفي في الخليج يواجه صعوبة أكبر',
    'a sample deep-work day, gulf edition': 'نموذج ليوم عمل عميق في الخليج',
    'the nutritional showdown': 'المواجهة الغذائية',
    'protein content comparison': 'مقارنة محتوى البروتين',
    'vitamin and mineral content': 'محتوى الفيتامينات والمعادن',
    'satiety and weight management': 'الشبع وإدارة الوزن',
    'culinary uses and taste': 'الاستخدامات في الطهي والطعم',
    'the first 12 weeks shape everything': 'الأسابيع الـ12 الأولى تشكّل كل شيء',
    'the non-negotiable: folic acid': 'غير القابل للتفاوض: حمض الفوليك',
    'foods to approach with care': 'أطعمة تعاملي معها بحذر',
    'eating through nausea': 'الأكل رغم الغثيان',
    'the three trimesters at a glance': 'الأثلاث الثلاثة في لمحة',
    'first trimester (weeks 1-12)': 'الثلث الأول (الأسبوع 1-12)',
    'second trimester (weeks 13-27)': 'الثلث الثاني (الأسبوع 13-27)',
    'third trimester (weeks 28-40)': 'الثلث الثالث (الأسبوع 28-40)',
    'the paradox: a month of fasting where many gain weight': 'المفارقة: شهر صيام يزيد فيه الوزن',
    'suhoor: the meal that determines your entire day': 'السحور: الوجبة التي تحدد يومك كله',
    "iftar: break the fast, don't break your metabolism": 'الإفطار: أفطر ولا تكسر أيضك',
    'the ideal ramadan day: a simple template': 'يوم رمضاني مثالي: نموذج بسيط',
    'the question': 'السؤال',
    'the 10-year rule': 'قاعدة الـ 10 سنوات',
    'the renter alternative': 'بديل المستأجر',
    'hidden costs of each option': 'التكاليف الخفية لكل خيار',
    'market conditions in the gulf': 'ظروف السوق في الخليج',
    'the verdict': 'الحكم',
    'the question behind every family budget': 'السؤال وراء كل ميزانية عائلية',
    'compare the real numbers, not slogans': 'قارن الأرقام الحقيقية لا الشعارات',
    'when buying makes sense': 'متى يكون الشراء منطقياً',
    "the renting-isn't-wasting mindset": 'عقلية الإيجار ليس هدراً',
    'two paths to real estate exposure': 'طريقان للتعرض العقاري',
    'direct rental property': 'العقار التأجيري المباشر',
    'risk profiles compared': 'مقارنة ملفات المخاطر',
    'what khareef actually looks like': 'كيف يبدو الخريف فعلاً',
    'when to go, and what you actually need': 'متى تذهب وماذا تحتاج فعلاً',
    'the end of khareef, what happens next': 'نهاية الخريف: ماذا بعد',
    'the number that surprises every gulf parent': 'الرقم الذي يفاجئ كل والد في الخليج',
    'start early, let compounding do the heavy lifting': 'ابدأ مبكراً، دع المركّب يقوم بالعمل الشاق',
    'a simple three-account system': 'نظام بسيط من ثلاثة حسابات',
    'protect the plan from lifestyle creep': 'احم الخطة من زحف نمط الحياة',
    'the scale lies, it where your fat sits': 'الميزان يكذب، المهم أين توجد دهونك',
    "the scale lies, it's where your fat sits": 'الميزان يكذب، المهم أين توجد دهونك',
    'why gulf residents carry more of it': 'لماذا يحمل سكان الخليج دهوناً حشوية أكثر',
    'measure it yourself in one minute': 'قسها بنفسك في دقيقة',
    'five proven ways to shrink it': 'خمس طرق مثبتة لتقليلها',
    'the bottom line': 'الخلاصة',
    'step 1: determine your zakat date': 'الخطوة 1: تحديد تاريخ الزكاة',
    'cash and bank accounts': 'النقد والحسابات البنكية',
    'gold and silver': 'الذهب والفضة',
    'stocks and shares': 'الأسهم والحصص',
    'real estate': 'العقار',
    'retirement accounts and pensions': 'حسابات التقاعد والمعاشات',
    'cryptocurrency': 'العملات الرقمية',
    'business assets and inventory': 'الأصول التجارية والمخزون',
    'what is not zakatable': 'ما لا تجب فيه الزكاة',
    'putting it all together: a simple method': 'تجميع كل شيء: طريقة بسيطة',
    'asset class rulings': 'أحكام فئات الأصول',
    'a worked example': 'مثال تطبيقي',
    'practical steps for the modern muslim investor': 'خطوات عملية للمستثمر المسلم المعاصر',
    "what's wrong with bmi?": 'ما هي مشكلة BMI؟',
    'what did the ama say?': 'ماذا قالت الجمعية الطبية الأمريكية؟',
    'waist-to-height ratio, the superior metric': 'نسبة الخصر إلى الطول: المقياس الأفضل',
    'bmi vs whtr comparison': 'مقارنة BMI و WHtR',
    'what this means for you, practical guide': 'ماذا يعني هذا لك؟ دليل عملي',
    'practical tips for better health': 'نصائح عملية لتحسين صحتك',
    "introduction: the gulf family's digital dilemma": 'المقدمة: المعضلة الرقمية للأسرة الخليجية',
    'introduction: the gulf family travel paradox': 'المقدمة: مفارقة السفر العائلي الخليجي',
    'conclusion: a calmer home starts today': 'الخاتمة: بيت هادئ يبدأ اليوم',
    'related articles & tools': 'مقالات وأدوات ذات صلة',
}

def get_arabic_heading(heading_text):
    heading_text = heading_text.strip()
    en_lower = heading_text.lower().strip()
    
    if en_lower in HEADING_TRANS:
        return HEADING_TRANS[en_lower]
    
    if en_lower.startswith('introduction'):
        return 'مقدمة'
    if en_lower.startswith('conclusion'):
        return 'الخاتمة'
    if en_lower.startswith('frequently asked'):
        return 'أسئلة شائعة'
    
    m = re.match(r'.*?section\s+\d+:\s*(.+)$', en_lower)
    if m:
        topic = m.group(1).strip().rstrip('.')
        if topic in HEADING_TRANS:
            return HEADING_TRANS[topic]
    
    m = re.match(r'^(step\s+\d+):\s*(.+)$', en_lower)
    if m:
        step_num = m.group(1)
        topic = m.group(2).strip()
        if topic in HEADING_TRANS:
            return HEADING_TRANS[topic]
        step_map = {'step 1': 'الخطوة 1', 'step 2': 'الخطوة 2', 'step 3': 'الخطوة 3'}
        if step_num in step_map:
            return f'{step_map[step_num]}: {topic}'
    
    for key, val in HEADING_TRANS.items():
        if key in en_lower:
            return val
    
    return None

def arabize_headings(body):
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', body, flags=re.DOTALL)
    result = []
    for part in parts:
        h2_match = re.match(r'<h2[^>]*>(.*?)</h2>', part, re.DOTALL)
        if h2_match:
            heading_text = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
            if any(x in heading_text for x in ['Related', 'مقالات', 'Tools', 'أدوات']):
                continue
            if re.search(r'[؀-ۿ]', heading_text):
                result.append(part)
            else:
                ar = get_arabic_heading(heading_text)
                if ar:
                    result.append(f'<h2>{ar}</h2>')
                else:
                    print(f"    ⚠️ No translation for: {heading_text[:60]}")
                    result.append(part)
        else:
            result.append(part)
    return ''.join(result)

CAT_CFG = {
    'finance': {'cta': 'استخدم أدوات التخطيط المالي لإدارة أموالك.', 'tools': [('حاسبة الميزانية','/tools/budget-calculator.html'),('حاسبة الزكاة','/tools/zakat-calculator.html'),('محول التاريخ','/tools/hijri-converter.html')]},
    'savings': {'cta': 'استخدم حاسبة الادخار لتحقيق أهدافك المالية.', 'tools': [('حاسبة الادخار','/tools/budget-calculator.html'),('حاسبة الزكاة','/tools/zakat-calculator.html'),('محول التاريخ','/tools/hijri-converter.html')]},
    'family': {'cta': 'اكتشف أدوات تنظيم الأسرة والتربية.', 'tools': [('حاسبة السعرات','/tools/calorie-calculator.html'),('حاسبة الماء','/tools/water-calculator.html'),('حاسبة BMI','/tools/bmi-calculator.html')]},
    'health': {'cta': 'استخدم أدوات الصحة لتتبع لياقتك.', 'tools': [('حاسبة BMI','/tools/bmi-calculator.html'),('حاسبة الماء','/tools/water-calculator.html'),('حاسبة السعرات','/tools/calorie-calculator.html')]},
    'travel': {'cta': 'احسب ميزانية سفرك واستكشف الوجهات.', 'tools': [('حاسبة السفر','/tools/travel-budget.html'),('محول التاريخ','/tools/hijri-converter.html'),('اتجاه القبلة','/tools/qibla.html')]},
    'islamic': {'cta': 'احسب زكاتك بدقة وفق الأحكام الشرعية.', 'tools': [('حاسبة الزكاة','/tools/zakat-calculator.html'),('محول التاريخ','/tools/hijri-converter.html'),('اتجاه القبلة','/tools/qibla.html')]},
    'realestate': {'cta': 'قارن بين خيارات التمويل واحسب أقساطك.', 'tools': [('حاسبة التمويل','/tools/mortgage-calculator.html'),('حاسبة الزكاة','/tools/zakat-calculator.html'),('محول التاريخ','/tools/hijri-converter.html')]},
    'holistic': {'cta': 'استكشف الأدوات الشاملة لتحسين حياتك.', 'tools': [('حاسبة السعرات','/tools/calorie-calculator.html'),('حاسبة الماء','/tools/water-calculator.html'),('حاسبة BMI','/tools/bmi-calculator.html')]},
}

ARTICLES = [
    {"name": "bmi-article", "cat": "health",
     "title_ar": "مؤشر كتلة الجسم: مشكلة BMI والبديل الأكثر دقة", "title_en": "BMI Article: The Problem with BMI and a Better Alternative",
     "desc_ar": "دليل شامل لفهم مؤشر كتلة الجسم وبدائله.", "desc_en": "Complete guide to understanding BMI and its alternatives.",
     "tags_ar": ["#BMI", "#صحة", "#وزن", "#قياسات"], "tags_en": ["#BMI", "#health", "#weight", "#measurement"]},
    {"name": "daily-islamic-habits-guide", "cat": "islamic",
     "title_ar": "دليل العادات الإسلامية اليومية", "title_en": "Daily Islamic Habits Guide",
     "desc_ar": "دليل لبناء عادات إسلامية يومية للعائلة.", "desc_en": "Guide to building daily Islamic habits for the family.",
     "tags_ar": ["#إسلام", "#عبادة", "#عادات", "#عائلة"], "tags_en": ["#islamic", "#worship", "#habits", "#family"]},
    {"name": "digital-minimalism-families", "cat": "family",
     "title_ar": "البساطة الرقمية للعائلات", "title_en": "Digital Minimalism for Families",
     "desc_ar": "دليل للبساطة الرقمية وتقليل وقت الشاشة للعائلة.", "desc_en": "Guide to digital minimalism and reducing screen time for families.",
     "tags_ar": ["#رقمي", "#بساطة", "#شاشة", "#عائلة"], "tags_en": ["#digital", "#minimalism", "#screentime", "#family"]},
    {"name": "end-of-service-saudi", "cat": "finance",
     "title_ar": "مكافأة نهاية الخدمة في السعودية", "title_en": "End of Service Benefits in Saudi Arabia",
     "desc_ar": "دليل شامل لحساب مكافأة نهاية الخدمة في السعودية.", "desc_en": "Complete guide to end-of-service benefits in Saudi Arabia.",
     "tags_ar": ["#نهاية-خدمة", "#سعودية", "#مالية", "#وافدين"], "tags_en": ["#end-of-service", "#saudi", "#finance", "#expat"]},
    {"name": "expat-vs-national-finance", "cat": "finance",
     "title_ar": "التخطيط المالي: مقيم vs مواطن", "title_en": "Expat vs National Financial Planning",
     "desc_ar": "مقارنة بين التخطيط المالي للمقيمين والمواطنين في الخليج.", "desc_en": "Comparison between expat and national financial planning in the Gulf.",
     "tags_ar": ["#مالية", "#مقيم", "#مواطن", "#خليج"], "tags_en": ["#finance", "#expat", "#national", "#gulf"]},
    {"name": "family-travel-planning-without-overspending", "cat": "travel",
     "title_ar": "تخطيط السفر العائلي بدون إسراف", "title_en": "Family Travel Planning Without Overspending",
     "desc_ar": "دليل لتخطيط السفر العائلي بميزانية ذكية.", "desc_en": "Guide to family travel planning on a smart budget.",
     "tags_ar": ["#سفر", "#عائلة", "#ميزانية", "#تخطيط"], "tags_en": ["#travel", "#family", "#budget", "#planning"]},
    {"name": "hotel-near-haram-vs-budget-umrah", "cat": "travel",
     "title_ar": "فندق قرب الحرم vs عمرة اقتصادية", "title_en": "Hotel Near Haram vs Budget Umrah",
     "desc_ar": "مقارنة بين الإقامة قرب الحرم وخيارات العمرة الاقتصادية.", "desc_en": "Comparison between staying near Haram and budget Umrah options.",
     "tags_ar": ["#عمرة", "#فندق", "#حرم", "#سفر"], "tags_en": ["#umrah", "#hotel", "#haram", "#travel"]},
    {"name": "islamic-inheritance-basics", "cat": "islamic",
     "title_ar": "أساسيات الميراث في الإسلام", "title_en": "Islamic Inheritance Basics",
     "desc_ar": "دليل أساسي لفهم أحكام الميراث في الإسلام.", "desc_en": "Basic guide to understanding Islamic inheritance rules.",
     "tags_ar": ["#ميراث", "#إسلام", "#مواريث", "#فقه"], "tags_en": ["#inheritance", "#islamic", "#estate", "#fiqh"]},
    {"name": "mindful-living-gulf-heat", "cat": "health",
     "title_ar": "الحياة الواعية في حر الخليج", "title_en": "Mindful Living in Gulf Heat",
     "desc_ar": "دليل للحياة الواعية والتعامل مع حرارة الخليج.", "desc_en": "Guide to mindful living and dealing with Gulf heat.",
     "tags_ar": ["#وعي", "#حرارة", "#صحة", "#خليج"], "tags_en": ["#mindful", "#heat", "#health", "#gulf"]},
    {"name": "notification-cost-productivity", "cat": "family",
     "title_ar": "تكلفة الإشعارات على الإنتاجية", "title_en": "The Cost of Notifications on Productivity",
     "desc_ar": "كيف تؤثر الإشعارات على إنتاجيتك وحلول عملية.", "desc_en": "How notifications affect your productivity and practical solutions.",
     "tags_ar": ["#إشعارات", "#إنتاجية", "#تركيز", "#رقمي"], "tags_en": ["#notifications", "#productivity", "#focus", "#digital"]},
    {"name": "pistachios-vs-almonds-comparison", "cat": "health",
     "title_ar": "الفستق vs اللوز: مقارنة صحية", "title_en": "Pistachios vs Almonds: A Health Comparison",
     "desc_ar": "مقارنة شاملة بين الفستق واللوز من حيث القيمة الغذائية.", "desc_en": "Complete comparison between pistachios and almonds nutritionally.",
     "tags_ar": ["#فستق", "#لوز", "#صحة", "#تغذية"], "tags_en": ["#pistachios", "#almonds", "#health", "#nutrition"]},
    {"name": "pregnancy-nutrition-first-trimester", "cat": "health",
     "title_ar": "التغذية في الحمل: الثلث الأول", "title_en": "Pregnancy Nutrition: First Trimester",
     "desc_ar": "دليل التغذية الأساسي للحامل في الأشهر الثلاثة الأولى.", "desc_en": "Essential nutrition guide for the first trimester of pregnancy.",
     "tags_ar": ["#حمل", "#تغذية", "#صحة", "#أمومة"], "tags_en": ["#pregnancy", "#nutrition", "#health", "#motherhood"]},
    {"name": "pregnancy-weeks-guide", "cat": "health",
     "title_ar": "دليل أسابيع الحمل", "title_en": "Pregnancy Weeks Guide",
     "desc_ar": "دليل أسبوع بأسبوع لمراحل الحمل.", "desc_en": "Week-by-week guide to pregnancy stages.",
     "tags_ar": ["#حمل", "#أسابيع", "#صحة", "#أمومة"], "tags_en": ["#pregnancy", "#weeks", "#health", "#motherhood"]},
    {"name": "ramadan-meal-planning", "cat": "family",
     "title_ar": "تخطيط وجبات رمضان", "title_en": "Ramadan Meal Planning",
     "desc_ar": "دليل لتخطيط وجبات رمضان بشكل صحي وموفر.", "desc_en": "Guide to healthy and budget-friendly Ramadan meal planning.",
     "tags_ar": ["#رمضان", "#وجبات", "#تخطيط", "#تغذية"], "tags_en": ["#ramadan", "#meals", "#planning", "#nutrition"]},
    {"name": "rent-vs-buy-comparison-guide", "cat": "realestate",
     "title_ar": "الإيجار vs التملك: دليل المقارنة", "title_en": "Rent vs Buy: Comparison Guide",
     "desc_ar": "مقارنة شاملة بين الإيجار والتملك في الخليج.", "desc_en": "Complete comparison between renting and buying in the Gulf.",
     "tags_ar": ["#إيجار", "#تملك", "#عقار", "#مقارنة"], "tags_en": ["#rent", "#buy", "#realestate", "#comparison"]},
    {"name": "rent-vs-buy-saudi", "cat": "realestate",
     "title_ar": "الإيجار vs التملك في السعودية", "title_en": "Rent vs Buy in Saudi Arabia",
     "desc_ar": "مقارنة بين الإيجار والتملك في السوق السعودي.", "desc_en": "Comparison between renting and buying in the Saudi market.",
     "tags_ar": ["#إيجار", "#تملك", "#سعودية", "#عقار"], "tags_en": ["#rent", "#buy", "#saudi", "#realestate"]},
    {"name": "rental-property-vs-reits-comparison", "cat": "realestate",
     "title_ar": "العقار التأجيري vs صناديق REITs", "title_en": "Rental Property vs REITs Comparison",
     "desc_ar": "مقارنة بين الاستثمار في العقار التأجيري وصناديق REITs.", "desc_en": "Comparison between rental property and REITs investment.",
     "tags_ar": ["#عقار", "#REITs", "#استثمار", "#تأجير"], "tags_en": ["#realestate", "#REITs", "#investment", "#rental"]},
    {"name": "salalah-khareef", "cat": "travel",
     "title_ar": "دليل صلالة والخريف", "title_en": "Salalah Khareef Guide",
     "desc_ar": "دليل شامل لزيارة صلالة في موسم الخريف.", "desc_en": "Complete guide to visiting Salalah during Khareef season.",
     "tags_ar": ["#صلالة", "#خريف", "#سفر", "#عمان"], "tags_en": ["#salalah", "#khareef", "#travel", "#oman"]},
    {"name": "saving-for-education-gulf", "cat": "savings",
     "title_ar": "الادخار لتعليم الأبناء في الخليج", "title_en": "Saving for Education in the Gulf",
     "desc_ar": "دليل للادخار لتعليم الأبناء في دول الخليج.", "desc_en": "Guide to saving for children's education in Gulf countries.",
     "tags_ar": ["#تعليم", "#ادخار", "#أبناء", "#خليج"], "tags_en": ["#education", "#savings", "#children", "#gulf"]},
    {"name": "visceral-fat-gulf", "cat": "health",
     "title_ar": "الدهون الحشوية: دليل شامل", "title_en": "Visceral Fat: Complete Guide",
     "desc_ar": "دليل شامل لفهم والتخلص من الدهون الحشوية.", "desc_en": "Complete guide to understanding and reducing visceral fat.",
     "tags_ar": ["#دهون", "#حشوية", "#صحة", "#وزن"], "tags_en": ["#visceral-fat", "#health", "#weight", "#fitness"]},
    {"name": "zakat-calculator-modern-investments-guide", "cat": "islamic",
     "title_ar": "زكاة الاستثمارات الحديثة", "title_en": "Zakat on Modern Investments Guide",
     "desc_ar": "دليل حساب زكاة الاستثمارات والأصول المالية الحديثة.", "desc_en": "Guide to calculating Zakat on modern investments and financial assets.",
     "tags_ar": ["#زكاة", "#استثمار", "#إسلام", "#تمويل"], "tags_en": ["#zakat", "#investment", "#islamic", "#finance"]},
    {"name": "zakat-investment-portfolios", "cat": "islamic",
     "title_ar": "زكاة المحافظ الاستثمارية", "title_en": "Zakat on Investment Portfolios",
     "desc_ar": "دليل حساب زكاة المحافظ الاستثمارية المتنوعة.", "desc_en": "Guide to calculating Zakat on diversified investment portfolios.",
     "tags_ar": ["#زكاة", "#محافظ", "#استثمار", "#إسلام"], "tags_en": ["#zakat", "#portfolio", "#investment", "#islamic"]},
]

def build_ar_html(body, config, toc_items):
    c = config
    name, title, desc = c['name'], c['title_ar'], c['desc_ar']
    cat = c.get('cat', 'finance')
    cfg = CAT_CFG.get(cat, CAT_CFG['finance'])
    tags = c.get('tags_ar', [])
    
    same = [a for a in ARTICLES if a['cat'] == cat and a['name'] != name]
    read_items = [(a['title_ar'], f"/blog/{a['name']}.html") for a in same[:3]]
    
    toc_links = '\n'.join(f'  <a href="#{hid}" class="toc-item">{htext}</a>' for htext, hid in toc_items)
    tools_html = '\n'.join(f'  <a href="{link}" class="tool-btn">{t}</a>' for t, link in cfg['tools'])
    tag_items = '\n  '.join(f'<span class="tag">{t}</span>' for t in tags)
    
    imgs = ["https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=64&h=48&q=80"]
    
    related_html = ""
    for i, (rtitle, rlink) in enumerate(read_items[:3]):
        related_html += f"""  <div class="sidebar-related-item"><img src="{imgs[i%3]}" alt="" width="64" height="48" loading="lazy"><div><div class="related-title"><a href="{rlink}">{rtitle}</a></div></div></div>\n"""
    
    read_cards = "".join(f'    <a href="{rlink}" class="read-also-card"><span class="read-also-title">{rtitle}</span></a>\n' for rtitle, rlink in read_items)
    
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl" data-lang="ar" data-theme="light">
<head><script>(function(){{var h=document.documentElement,t=localStorage.getItem("dfl-theme")||"light";h.setAttribute("data-lang","ar");h.setAttribute("lang","ar");h.setAttribute("dir","rtl");h.setAttribute("data-theme",t);}})()</script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title}</title><meta name="description" content="{desc}" />
  <link rel="canonical" href="https://dotforlife.com/blog/{name}.html" />
  <meta property="og:title" content="{title}" /><meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://dotforlife.com/blog/{name}.html" /><meta property="og:type" content="article" />
  <link rel="alternate" hreflang="ar" href="https://dotforlife.com/blog/{name}.html" />
  <link rel="alternate" hreflang="en" href="https://dotforlife.com/blog/{name}-en.html" />
  <meta property="og:image" content="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" />
  <style>:root{{--green:#054241;--teal:#6abfb8;--orange:#fd781c;--cream:#FAF8F4;--text:#1a1d23;--text2:#6C757D;--radius:16px;--max-w:1100px}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Almarai','Segoe UI',sans-serif;background:var(--cream);color:var(--text);line-height:1.9}}img{{max-width:100%;height:auto}}</style>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?v=20260626c"><link rel="stylesheet" href="/styles/home.css?v=20260617b"><link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');window.addEventListener('DOMContentLoaded',function(){{var lt=document.getElementById('lang-toggle');if(lt)lt.addEventListener('click',function(){{var u=location.pathname.replace('.html','-en.html');if(u.endsWith('-en-en.html'))u=u.replace('-en-en.html','.html');location.href=u;}});}});</script>
</head>
<body data-template="article">
<div id="reading-progress" role="progressbar"></div>
<nav id="navbar"><div class="nav-inner"><a href="/" class="nav-logo"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="100" height="100" style="height:100px;width:auto;object-fit:contain;" loading="lazy"></a><ul class="nav-links"><li><a href="/health.html">الصحة</a></li><li><a href="/finance.html">المالية</a></li><li><a href="/real-estate.html">العقار</a></li><li><a href="/travel.html">السفر</a></li><li><a href="/islamic.html">الإسلامية</a></li><li><a href="/about.html">عنّا</a></li><li><a href="/archive.html">الأرشيف</a></li><li><a href="/blog.html">المدونة</a></li><li><a href="/library.html">المكتبة</a></li></ul><div class="nav-controls"><button class="nav-btn" id="lang-toggle">English</button><button class="nav-btn" id="theme-toggle"><svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button></div></div></nav>
<div class="article-wrap">
<section class="article-banner"><div class="article-banner-img-wrap"><img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" alt="" class="article-banner-img" width="1200" height="420" loading="eager"><div class="article-banner-overlay"><h1 class="article-banner-title">{title}</h1><div class="article-banner-meta"><span>2026-06-08</span><span>٨ دقائق</span></div></div></div></section>
<div class="article-layout" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.5rem">
<main class="article-main">
<article class="article-body">
{body}
</article>
<div class="article-end">
<div class="article-share"><a href="#" target="_blank" rel="noopener" class="share-btn wa"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a><a href="#" target="_blank" rel="noopener" class="share-btn tw"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="#" target="_blank" rel="noopener" class="share-btn fb"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a><button class="share-btn cp" onclick="navigator.clipboard.writeText(location.href)"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></button></div>
<div class="article-tool-cta"><h3>ابدأ اليوم</h3><p>{cfg['cta']}</p><a href="{cfg['tools'][0][1]}" class="tool-cta-btn">استخدم الأداة ←</a></div>
<div class="article-read-also"><h3>📖 اقرأ أيضاً</h3><div class="read-also-grid">{read_cards}</div></div>
<div class="article-friday-cta"><h3>📬 نصائح الجمعة العائلية</h3><p>احصل على إلهام أسبوعي في بريدك.</p><div class="friday-input-wrap"><input type="email" placeholder="your@email.com"><button onclick="alert(\'قريباً — تكامل التسجيل.\')">اشترك</button></div></div>
<div class="article-tags">{tag_items}</div>
</div>
</main>
<aside class="article-sidebar">
<div class="sidebar-module sidebar-team-card"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="56" height="56"><div class="team-name">فريق دوت فور لايف</div><div class="team-trust">محتوى موثوق للعائلات الخليجية.</div><a href="/editorial-standards.html" class="team-link">معاييرنا التحريرية ←</a></div>
<div class="sidebar-module sidebar-toc"><h4>📑 المحتويات</h4>{toc_links}</div>
<div class="sidebar-module sidebar-related"><h4>ذات صلة</h4>{related_html}</div>
<div class="sidebar-module sidebar-tools"><h4>🛠 أدوات</h4>{tools_html}</div>
</aside>
</div></div>
<footer class="site-footer" role="contentinfo">
  <div class="footer-accent" aria-hidden="true"></div>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label="DOTFORLIFE">
          <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="auto" loading="lazy">
        </a>
        <p class="footer-tagline"><span class="en">One calm place for your family's everyday decisions. Free, always.</span><span class="ar">مكان هادئ واحد لقرارات عائلتك اليومية. مجاني دائماً.</span></p>
        <p class="footer-motto"><span class="en">Life, at ease.</span><span class="ar">الحياة، براحة.</span></p>
      </div>
      <div class="footer-links-grid">
        <div class="footer-col">
          <h4><span class="en">Life</span><span class="ar">الحياة</span></h4>
          <ul>
            <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
            <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
            <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
            <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
            <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Tools</span><span class="ar">الأدوات</span></h4>
          <ul>
            <li><a href="/tools/bmi-calculator.html"><span class="en">BMI Calculator</span><span class="ar">حاسبة BMI</span></a></li>
            <li><a href="/tools/mortgage-calculator.html"><span class="en">Mortgage</span><span class="ar">التمويل</span></a></li>
            <li><a href="/tools/zakat-calculator.html"><span class="en">Zakat</span><span class="ar">الزكاة</span></a></li>
            <li><a href="/tools/water-calculator.html"><span class="en">Hydration</span><span class="ar">الترطيب</span></a></li>
            <li><a href="/library.html"><span class="en">All Tools</span><span class="ar">كل الأدوات</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Discover</span><span class="ar">اكتشف</span></h4>
          <ul>
            <li><a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a></li>
            <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
            <li><a href="/our-vision.html"><span class="en">Our Vision</span><span class="ar">رؤيتنا</span></a></li>
            <li><a href="/pregnancy-journey.html"><span class="en">Pregnancy Journey</span><span class="ar">رحلة الحمل</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Support</span><span class="ar">الدعم</span></h4>
          <ul>
            <li><a href="/contact.html"><span class="en">Contact</span><span class="ar">اتصل بنا</span></a></li>
            <li><a href="/privacy.html"><span class="en">Privacy</span><span class="ar">الخصوصية</span></a></li>
            <li><a href="/about.html"><span class="en">About</span><span class="ar">عنا</span></a></li>
            <li><a href="/editorial-standards.html"><span class="en">Standards</span><span class="ar">المعايير</span></a></li>
          </ul>
        </div>
      </div>
    </div>
    <hr>
    <div class="footer-bottom">
      <span>© 2026 DOTFORLIFE</span>
    </div>
  </div>
</footer>
<script src="/scripts/global.js?v=20260617a" defer></script>
<script>(function(){{var bar=document.getElementById('reading-progress');if(bar)window.addEventListener('scroll',function(){{var h=document.documentElement,pct=(h.scrollTop||document.body.scrollTop)/(h.scrollHeight-h.clientHeight||1)*100;bar.style.width=pct+'%'}},{{passive:true}});var tocLinks=document.querySelectorAll('.toc-item');if(tocLinks.length){{var headings=[];tocLinks.forEach(function(l){{var el=document.getElementById(l.getAttribute('href').replace('#',''));if(el)headings.push({{el:el,link:l}})}});window.addEventListener('scroll',function(){{var sy=window.scrollY+130,cur=null;headings.forEach(function(h){{if(h.el.offsetTop<=sy)cur=h}});tocLinks.forEach(function(l){{l.classList.remove('is-active')}});if(cur)cur.link.classList.add('is-active')}},{{passive:true}})}})()</script>
</body>
</html>'''


def process_article(config):
    name = config['name']
    ar_path = f"{BLOG}/{name}.html"
    en_path = f"{BLOG}/{name}-en.html"
    redir_path = f"{BLOG}/{name}-ar.html"
    
    print(f"\n{'='*60}")
    print(f"📄 {name}")
    print(f"{'='*60}")
    
    with open(ar_path, 'r', encoding='utf-8') as f:
        source_html = f.read()
    
    m = re.search(r'<article[^>]*class="article-body"[^>]*>(.*?)</article>', source_html, re.DOTALL)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', source_html, re.DOTALL)
    if not m:
        print(f"  ❌ No article body found")
        return False
    
    source_body = m.group(1)
    is_bmi = (name == 'bmi-article')
    has_bilingual = '<span class="en">' in source_body and '<span class="ar">' in source_body
    
    if is_bmi:
        with open(en_path, 'r', encoding='utf-8') as f:
            en_html = f.read()
        m_en = re.search(r'<article[^>]*class="article-body"[^>]*>(.*?)</article>', en_html, re.DOTALL)
        en_body = m_en.group(1) if m_en else source_body
        ar_body = source_body
    elif has_bilingual:
        ar_body = extract_ar_from_body(source_body)
        en_body = extract_en_from_body(source_body)
    else:
        ar_body = source_body
        en_body = re.sub(r'[؀-ۿ\s]+', ' ', source_body)
        en_body = re.sub(r'<p>\s*<[^>]+>\s*</p>', '', en_body)
    
    ar_body = strip_old_sections(ar_body)
    en_body = strip_old_sections(en_body)
    ar_body = fix_malformed_h2s(ar_body)
    en_body = fix_malformed_h2s(en_body)
    ar_body = arabize_headings(ar_body)
    ar_body = re.sub(r'<p>\s*</p>', '', ar_body)
    ar_body = re.sub(r'<li>\s*</li>', '', ar_body)
    en_body = re.sub(r'<p>\s*</p>', '', en_body)
    en_body = re.sub(r'<li>\s*</li>', '', en_body)
    ar_body = balance_divs(ar_body)
    en_body = balance_divs(en_body)
    
    ar_text = re.sub(r'<[^>]+>', ' ', ar_body)
    ar_ar = len(re.findall(r'[؀-ۿ]', ar_text))
    ar_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', ar_text))
    print(f"  AR: {ar_ar} AR chars, {ar_en} EN words")
    
    en_text = re.sub(r'<[^>]+>', ' ', en_body)
    en_ar = len(re.findall(r'[؀-ۿ]', en_text))
    en_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', en_text))
    print(f"  EN: {en_ar} AR chars, {en_en} EN words")
    
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', ar_body, re.DOTALL)
    seen_h2s = set()
    toc_items = []
    for h in h2s:
        h_clean = re.sub(r'<[^>]+>', '', h).strip()
        if h_clean and h_clean not in seen_h2s:
            seen_h2s.add(h_clean)
            h_id = make_heading_id(h_clean)
            toc_items.append((h_clean, h_id))
    
    for htext, hid in toc_items:
        ar_body = re.sub(
            rf'<h2[^>]*>\s*{re.escape(htext)}\s*</h2>',
            f'<h2 id="{hid}">{htext}</h2>',
            ar_body
        )
    
    ar_final = build_ar_html(ar_body, config, toc_items)
    with open(ar_path, 'w', encoding='utf-8') as f:
        f.write(ar_final)
    
    cat = config.get('cat', 'finance')
    same = [a for a in ARTICLES if a['cat'] == cat and a['name'] != name]
    en_read_items = [(a['title_en'], f"/blog/{a['name']}-en.html") for a in same[:3]]
    en_read_cards = "".join(f'    <a href="{rlink}" class="read-also-card"><span class="read-also-title">{rtitle}</span></a>\n' for rtitle, rlink in en_read_items)
    
    imgs = ["https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=64&h=48&q=80"]
    
    en_related_html = ""
    for i, (rtitle, rlink) in enumerate(en_read_items[:3]):
        en_related_html += f"""  <div class="sidebar-related-item"><img src="{imgs[i%3]}" alt="" width="64" height="48" loading="lazy"><div><div class="related-title"><a href="{rlink}">{rtitle}</a></div></div></div>\n"""
    
    en_tag_items = '\n  '.join(f'<span class="tag">{t}</span>' for t in config.get('tags_en', []))
    en_title = config['title_en']
    
    en_h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', en_body, re.DOTALL)
    en_toc_links = ""
    for h in en_h2s:
        h_clean = re.sub(r'<[^>]+>', '', h).strip()
        if h_clean and not any(x in h_clean for x in ['Related', 'Tools', 'مقالات', 'أدوات']):
            h_id = make_heading_id(h_clean)
            en_toc_links += f'  <a href="#{h_id}" class="toc-item">{h_clean}</a>\n'
            en_body = re.sub(
                rf'<h2[^>]*>\s*{re.escape(h_clean)}\s*</h2>',
                f'<h2 id="{h_id}">{h_clean}</h2>',
                en_body
            )
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="en" dir="ltr" data-lang="en" data-theme="light">
<head><script>(function(){{var h=document.documentElement,t=localStorage.getItem("dfl-theme")||"light";h.setAttribute("data-lang","en");h.setAttribute("lang","en");h.setAttribute("dir","ltr");h.setAttribute("data-theme",t);}})()</script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{en_title}</title><meta name="description" content="{config["desc_en"]}" />
  <link rel="canonical" href="https://dotforlife.com/blog/{name}-en.html" />
  <meta property="og:title" content="{en_title}" /><meta property="og:description" content="{config["desc_en"]}" />
  <meta property="og:url" content="https://dotforlife.com/blog/{name}-en.html" /><meta property="og:type" content="article" />
  <link rel="alternate" hreflang="en" href="https://dotforlife.com/blog/{name}-en.html" />
  <link rel="alternate" hreflang="ar" href="https://dotforlife.com/blog/{name}.html" />
  <meta property="og:image" content="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" />
  <style>:root{{--green:#054241;--teal:#6abfb8;--orange:#fd781c;--cream:#FAF8F4;--text:#1a1d23;--text2:#6C757D;--radius:16px;--max-w:1100px}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Inter','Segoe UI',sans-serif;background:var(--cream);color:var(--text);line-height:1.9}}img{{max-width:100%;height:auto}}</style>
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?v=20260626c"><link rel="stylesheet" href="/styles/home.css?v=20260617b"><link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');window.addEventListener('DOMContentLoaded',function(){{var lt=document.getElementById('lang-toggle');if(lt)lt.addEventListener('click',function(){{var u=location.pathname.replace('-en.html','.html');if(!u.includes('-en-'))u=location.pathname.replace('.html','-en.html');if(u.endsWith('-en-en.html'))u=u.replace('-en-en.html','.html');location.href=u;}});}});</script>
</head>
<body data-template="article">
<div id="reading-progress" role="progressbar"></div>
<nav id="navbar"><div class="nav-inner"><a href="/" class="nav-logo"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="100" height="100" style="height:100px;width:auto;object-fit:contain;" loading="lazy"></a><ul class="nav-links"><li><a href="/health.html">Health</a></li><li><a href="/finance.html">Finance</a></li><li><a href="/real-estate.html">Real Estate</a></li><li><a href="/travel.html">Travel</a></li><li><a href="/islamic.html">Islamic</a></li><li><a href="/about.html">About</a></li><li><a href="/archive.html">Archive</a></li><li><a href="/blog.html">Blog</a></li></ul><div class="nav-controls"><button class="nav-btn" id="lang-toggle">العربية</button><button class="nav-btn" id="theme-toggle"><svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button></div></div></nav>
<div class="article-wrap">
<section class="article-banner"><div class="article-banner-img-wrap"><img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" alt="" class="article-banner-img" width="1200" height="420" loading="eager"><div class="article-banner-overlay"><h1 class="article-banner-title">{en_title}</h1><div class="article-banner-meta"><span>2026-06-08</span><span>8 min read</span></div></div></div></section>
<div class="article-layout" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.5rem">
<main class="article-main">
<article class="article-body">
{en_body}
</article>
<div class="article-end">
<div class="article-share"><a href="#" target="_blank" rel="noopener" class="share-btn wa"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a><a href="#" target="_blank" rel="noopener" class="share-btn tw"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="#" target="_blank" rel="noopener" class="share-btn fb"><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a><button class="share-btn cp" onclick="navigator.clipboard.writeText(location.href)"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></button></div>
<div class="article-tool-cta"><h3>Get Started Today</h3><p>Use our tools to improve your planning.</p><a href="/tools/budget-calculator.html" class="tool-cta-btn">Use the Tool →</a></div>
<div class="article-read-also"><h3>📖 Read Also</h3><div class="read-also-grid">{en_read_cards}</div></div>
<div class="article-friday-cta"><h3>📬 Friday Family Tips</h3><p>Get weekly inspiration in your inbox.</p><div class="friday-input-wrap"><input type="email" placeholder="your@email.com"><button onclick="alert(\'Coming soon — signup integration.\')">Subscribe</button></div></div>
<div class="article-tags">{en_tag_items}</div>
</div>
</main>
<aside class="article-sidebar">
<div class="sidebar-module sidebar-team-card"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="56" height="56"><div class="team-name">DOTFORLIFE Team</div><div class="team-trust">Trusted content for Gulf families.</div><a href="/editorial-standards.html" class="team-link">Our Editorial Standards →</a></div>
<div class="sidebar-module sidebar-toc"><h4>📑 Contents</h4>{en_toc_links}</div>
<div class="sidebar-module sidebar-related"><h4>Related</h4>{en_related_html}</div>
<div class="sidebar-module sidebar-tools"><h4>🛠 Tools</h4><a href="/tools/budget-calculator.html" class="tool-btn">Budget Calculator</a><a href="/tools/savings-goal.html" class="tool-btn">Savings Goal Calculator</a><a href="/tools/hijri-converter.html" class="tool-btn">Hijri Converter</a></div>
</aside>
</div></div>
<footer class="site-footer" role="contentinfo">
  <div class="footer-accent" aria-hidden="true"></div>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label="DOTFORLIFE">
          <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="auto" loading="lazy">
        </a>
        <p class="footer-tagline"><span class="en">One calm place for your family's everyday decisions. Free, always.</span><span class="ar">مكان هادئ واحد لقرارات عائلتك اليومية. مجاني دائماً.</span></p>
        <p class="footer-motto"><span class="en">Life, at ease.</span><span class="ar">الحياة، براحة.</span></p>
      </div>
      <div class="footer-links-grid">
        <div class="footer-col">
          <h4><span class="en">Life</span><span class="ar">الحياة</span></h4>
          <ul>
            <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
            <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
            <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
            <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
            <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Tools</span><span class="ar">الأدوات</span></h4>
          <ul>
            <li><a href="/tools/bmi-calculator.html"><span class="en">BMI Calculator</span><span class="ar">حاسبة BMI</span></a></li>
            <li><a href="/tools/mortgage-calculator.html"><span class="en">Mortgage</span><span class="ar">التمويل</span></a></li>
            <li><a href="/tools/zakat-calculator.html"><span class="en">Zakat</span><span class="ar">الزكاة</span></a></li>
            <li><a href="/tools/water-calculator.html"><span class="en">Hydration</span><span class="ar">الترطيب</span></a></li>
            <li><a href="/library.html"><span class="en">All Tools</span><span class="ar">كل الأدوات</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Discover</span><span class="ar">اكتشف</span></h4>
          <ul>
            <li><a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a></li>
            <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
            <li><a href="/our-vision.html"><span class="en">Our Vision</span><span class="ar">رؤيتنا</span></a></li>
            <li><a href="/pregnancy-journey.html"><span class="en">Pregnancy Journey</span><span class="ar">رحلة الحمل</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Support</span><span class="ar">الدعم</span></h4>
          <ul>
            <li><a href="/contact.html"><span class="en">Contact</span><span class="ar">اتصل بنا</span></a></li>
            <li><a href="/privacy.html"><span class="en">Privacy</span><span class="ar">الخصوصية</span></a></li>
            <li><a href="/about.html"><span class="en">About</span><span class="ar">عنا</span></a></li>
            <li><a href="/editorial-standards.html"><span class="en">Standards</span><span class="ar">المعايير</span></a></li>
          </ul>
        </div>
      </div>
    </div>
    <hr>
    <div class="footer-bottom">
      <span>© 2026 DOTFORLIFE</span>
    </div>
  </div>
</footer>
<script src="/scripts/global.js?v=20260617a" defer></script>
<script>(function(){{var bar=document.getElementById('reading-progress');if(bar)window.addEventListener('scroll',function(){{var h=document.documentElement,pct=(h.scrollTop||document.body.scrollTop)/(h.scrollHeight-h.clientHeight||1)*100;bar.style.width=pct+'%'}},{{passive:true}});var tocLinks=document.querySelectorAll('.toc-item');if(tocLinks.length){{var headings=[];tocLinks.forEach(function(l){{var el=document.getElementById(l.getAttribute('href').replace('#',''));if(el)headings.push({{el:el,link:l}})}});window.addEventListener('scroll',function(){{var sy=window.scrollY+130,cur=null;headings.forEach(function(h){{if(h.el.offsetTop<=sy)cur=h}});tocLinks.forEach(function(l){{l.classList.remove('is-active')}});if(cur)cur.link.classList.add('is-active')}},{{passive:true}})}})()</script>
</body>
</html>''')
    
    with open(redir_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="0;url=/blog/{name}.html"><meta name="robots" content="noindex"><title>تم النقل</title></head><body><p>تم نقل الصفحة إلى <a href="/blog/{name}.html">{name}</a>.</p></body></html>''')
    
    print(f"  ✅ {name}.html + -en.html + -ar.html")
    
    with open(ar_path, 'r') as f:
        v = f.read()
    issues = []
    if 'article-layout' not in v: issues.append("no layout")
    if 'article-sidebar' not in v: issues.append("no sidebar")
    if 'toc-item' not in v: issues.append("no TOC")
    if 'display:grid' not in v: issues.append("no grid")
    if 'hreflang' not in v: issues.append("no hreflang")
    if 'article-end' not in v: issues.append("no article-end")
    if 'article-banner' not in v: issues.append("no banner")
    
    ar_h2s = re.findall(r'<h2[^>]*>[^<]*[a-zA-Z]{4,}[^<]*</h2>', v)
    if ar_h2s: issues.append(f"{len(ar_h2s)} EN headings in AR")
    
    do = len(re.findall(r'<div\b', v))
    dc = len(re.findall(r'</div>', v))
    if do != dc: issues.append(f"div {do}/{dc}")
    
    with open(en_path, 'r') as f:
        en_v = f.read()
    en_issues = []
    if 'article-layout' not in en_v: en_issues.append("no layout")
    if 'article-sidebar' not in en_v: en_issues.append("no sidebar")
    if 'display:grid' not in en_v: en_issues.append("no grid")
    if 'article-banner' not in en_v: en_issues.append("no banner")
    if 'article-end' not in en_v: en_issues.append("no article-end")
    
    en_do = len(re.findall(r'<div\b', en_v))
    en_dc = len(re.findall(r'</div>', en_v))
    if en_do != en_dc: en_issues.append(f"div {en_do}/{en_dc}")
    
    if issues:
        print(f"  ❌ AR: {'; '.join(issues)}")
    else:
        print(f"  ✅ AR verified (div {do}/{dc})")
    
    if en_issues:
        print(f"  ❌ EN: {'; '.join(en_issues)}")
    else:
        print(f"  ✅ EN verified (div {en_do}/{en_dc})")
    
    return len(issues) == 0 and len(en_issues) == 0


if __name__ == "__main__":
    s, f = 0, 0
    for c in ARTICLES:
        ok = process_article(c)
        if ok: s += 1
        else: f += 1
    print(f"\n{'='*60}")
    print(f"✅ Batch 6: {s} succeeded, {f} failed")
    print(f"{'='*60}")
