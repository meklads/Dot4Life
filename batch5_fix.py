#!/usr/bin/env python3
"""
Batch 5 FIXED v2: Full BOOM compliance for 25 articles.
- Arabic-only content with proper Arabic headings
- EN version with sidebar/TOC
- Full BOOM structure (sidebar, TOC, article-end, inline grid)
- Section-number-agnostic heading matching
"""

import re, os

BLOG = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life/blog"

# ─── Section Topic Dictionary ─────────────────────────
# Key = the content AFTER "Section N: " (lowercase)
SECTION_TOPIC = {
    # building-personal-savings-system (1-8)
    'the psychology of saving': 'سيكولوجية الادخار',
    'the five-bucket savings system': 'نظام الادخار الخماسي',
    'automation is everything': 'الأتمتة هي الحل',
    'the emergency fund': 'صندوق الطوارئ',
    'saving for multiple goals': 'الادخار لأهداف متعددة',
    'gulf-specific savings challenges and solutions': 'تحديات الادخار في الخليج',
    'tracking progress without obsessing': 'تتبع التقدم بدون هوس',
    'what to do when you hit a setback': 'ماذا تفعل عند النكسة',
    
    # children-education-savings-guide (1-8)
    'understanding education costs in the gulf': 'فهم تكاليف التعليم في الخليج',
    'the earlier you start, the easier it is': 'البداية المبكرة تجعل الأمر أسهل',
    'education savings vehicles available in the gulf': 'أدوات ادخار التعليم في الخليج',
    'building your education savings strategy': 'بناء استراتيجية ادخار التعليم',
    'education savings for multiple children': 'الادخار لتعليم عدة أطفال',
    'tax-efficient education savings': 'الادخار الضريبي للتعليم',
    'what if you get a late start?': 'ماذا لو بدأت متأخراً',
    'what if you get a late start': 'ماذا لو بدأت متأخراً',
    'scholarships and financial aid': 'المنح الدراسية والمساعدات المالية',
    
    # complete-household-budget-system (1-7)
    'the four pillars of a household budget': 'أركان الميزانية المنزلية الأربعة',
    'the gulf family budget framework': 'إطار ميزانية الأسرة الخليجية',
    'building your emergency fund': 'بناء صندوق الطوارئ',
    'managing debt': 'إدارة الديون',
    'automation is the secret': 'الأتمتة هي السر',
    'budgeting for irregular expenses': 'ميزانية المصروفات غير المنتظمة',
    'teaching children about money': 'تعليم الأطفال المال',
    
    # end-of-service-benefits-expats (1-6)
    'end-of-service benefits in saudi arabia': 'مكافأة نهاية الخدمة في السعودية',
    'end-of-service benefits in the uae': 'مكافأة نهاية الخدمة في الإمارات',
    'key legal considerations': 'اعتبارات قانونية مهمة',
    'strategies to maximize your eos benefit': 'استراتيجيات تعظيم مكافأة نهاية الخدمة',
    'what to do with your eos payment': 'ماذا تفعل بمكافأة نهاية الخدمة',
    'why you should not rely only on eos': 'لماذا لا تعتمد فقط على مكافأة نهاية الخدمة',
    
    # life-insurance-gulf-families (1-8)
    'understanding life insurance basics': 'أساسيات التأمين على الحياة',
    'how much coverage do you need?': 'كم تحتاج من التغطية',
    'how much coverage do you need': 'كم تحتاج من التغطية',
    'life insurance options in saudi arabia': 'خيارات التأمين في السعودية',
    'life insurance options in the uae': 'خيارات التأمين في الإمارات',
    'family takaful: sharia-compliant protection': 'التكافل العائلي: حماية متوافقة مع الشريعة',
    'critical illness and disability insurance': 'تأمين الأمراض الخطيرة والعجز',
    'health insurance in the gulf': 'التأمين الصحي في الخليج',
    'common mistakes and how to avoid them': 'أخطاء شائعة وكيف تتجنبها',
    
    # starting-side-business-saudi-uae (1-6)
    'legal frameworks for side businesses': 'الأطر القانونية للأعمال الجانبية',
    'low-cost side business ideas': 'أفكار أعمال جانبية منخفضة التكلفة',
    'balancing a side business with full-time work': 'الموازنة بين العمل الجانبي والوظيفة',
    'financial management for side businesses': 'الإدارة المالية للأعمال الجانبية',
    'marketing your side business': 'تسويق عملك الجانبي',
    'scaling beyond a side business': 'التوسع بعد العمل الجانبي',
    
    # choosing-right-school-child-gulf (1-6)
    'understanding curriculum options': 'فهم خيارات المناهج الدراسية',
    'factors to consider beyond curriculum': 'عوامل إضافية إلى جانب المنهج',
    'the school visit checklist': 'قائمة تفقد المدرسة',
    'understanding school fees and hidden costs': 'فهم الرسوم المدرسية والتكاليف الخفية',
    'application timelines and procedures': 'مواعيد وإجراءات التقديم',
    'special educational needs': 'الاحتياجات التعليمية الخاصة',
    
    # complete-family-financial-planning (1-6)
    'the six domains of family financial health': 'المجالات الستة للصحة المالية العائلية',
    'building your family financial plan step by step': 'بناء خطتك المالية العائلية خطوة بخطوة',
    'gulf-specific financial considerations': 'اعتبارات مالية خاصة بالخليج',
    'investment basics for gulf families': 'أساسيات الاستثمار للعائلات الخليجية',
    "protecting your family's financial future": 'حماية مستقبل عائلتك المالي',
    'protecting your family financial future': 'حماية مستقبل عائلتك المالي',
    
    # complete-family-systems-productivity-hub (1-6)
    'understanding family productivity': 'فهم الإنتاجية العائلية',
    'digital minimalism for families': 'البساطة الرقمية للعائلات',
    'stress management for working parents': 'إدارة التوتر للآباء العاملين',
    'building daily systems that work': 'بناء أنظمة يومية فعالة',
    'time management for families': 'إدارة الوقت للعائلات',
    'managing household operations': 'إدارة العمليات المنزلية',
    
    # family-nutrition-on-budget (1-8)
    'the real cost of food in the gulf': 'التكلفة الحقيقية للطعام في الخليج',
    'meal planning: the foundation of food savings': 'تخطيط الوجبات: أساس توفير الطعام',
    'smart shopping strategies': 'استراتيجيات التسوق الذكية',
    'affordable nutritious foods available in the gulf': 'أطعمة مغذية بأسعار معقولة في الخليج',
    'cooking at home: the biggest money saver': 'الطبخ في المنزل: الأكبر توفيراً',
    'reducing food waste': 'تقليل هدر الطعام',
    'healthy eating on a busy schedule': 'الأكل الصحي مع جدول مزدحم',
    'teaching children about nutrition and budget': 'تعليم الأطفال التغذية والميزانية',
    
    # managing-screen-time-children (1-8)
    'understanding screen time recommendations': 'فهم توصيات وقت الشاشة',
    'quality over quantity': 'الجودة قبل الكمية',
    'age-by-age screen time strategies': 'استراتيجيات وقت الشاشة حسب العمر',
    'creating a family screen time plan': 'إنشاء خطة عائلية لوقت الشاشة',
    'screen-free alternatives for children': 'بدائل بدون شاشة للأطفال',
    'parental controls and tools': 'أدوات الرقابة الأبوية',
    'the parent as role model': 'الوالد كنموذج يحتذى',
    'handling resistance and relapses': 'التعامل مع المقاومة والانتكاسات',
    
    # organize-life-daily-systems (1-7)
    'the morning system': 'نظام الصباح',
    'the daily planning system': 'نظام التخطيط اليومي',
    'the home systems': 'الأنظمة المنزلية',
    'the financial systems': 'الأنظمة المالية',
    'the health systems': 'الأنظمة الصحية',
    'the digital systems': 'الأنظمة الرقمية',
    
    # stress-management-working-parents (1-7)
    'understanding working parent stress': 'فهم توتر الآباء العاملين',
    'time management strategies': 'استراتيجيات إدارة الوقت',
    'physical wellbeing': 'الصحة البدنية',
    'mental and emotional strategies': 'استراتيجيات الصحة النفسية والعاطفية',
    'building a support system': 'بناء نظام دعم',
    'quality time': 'الوقت النوعي',
    'quality time, not quantity': 'الوقت النوعي لا الكمي',
    
    # teaching-children-financial-literacy (1-6)
    'ages 3-5: foundations of money awareness': 'الأعمار 3-5: أساسيات الوعي المالي',
    'ages 6-10: the three-jar system': 'الأعمار 6-10: نظام الجرار الثلاثة',
    'ages 11-14: budgeting and earning': 'الأعمار 11-14: الميزانية والكسب',
    'ages 15-18: real-world money management': 'الأعمار 15-18: إدارة المال الواقعية',
    'islamic financial values for children': 'القيم المالية الإسلامية للأطفال',
    'the allowance decision': 'قرار العطاء',
    
    # complete-gulf-family-health-wellness (1-5)
    'the five pillars of family health': 'أركان الصحة العائلية الخمسة',
    'health through the family life cycle': 'الصحة عبر دورة حياة الأسرة',
    'gulf-specific health challenges': 'تحديات صحية خاصة بالخليج',
    'building your family health system': 'بناء نظام صحي عائلي',
    
    # managing-healthcare-costs-families (1-7)
    'understanding the gulf healthcare system': 'فهم نظام الرعاية الصحية في الخليج',
    'choosing the right health insurance plan': 'اختيار خطة التأمين الصحي المناسبة',
    'preventive care saves money': 'الرعاية الوقائية توفر المال',
    'smart pharmacy strategies': 'استراتيجيات الصيدلة الذكية',
    'hospital and clinic cost comparison': 'مقارنة تكاليف المستشفيات والعيادات',
    'emergency care vs urgent care': 'الرعاية الطارئة مقابل العاجلة',
    'emergency care vs. urgent care': 'الرعاية الطارئة مقابل العاجلة',
    
    # preparing-for-pregnancy-guide (1-6)
    'the 90-day pre-conception timeline': 'الجدول الزمني 90 يوماً قبل الحمل',
    'the pre-conception health checklist': 'قائمة الصحة قبل الحمل',
    'nutrition for fertility': 'التغذية للخصوبة',
    'financial planning before baby arrives': 'التخطيط المالي قبل وصول الطفل',
    'common pre-conception myths': 'خرافات شائعة عن الحمل',
    
    # complete-family-travel-activities-hub (1-5)
    'top family-friendly destinations in the gulf': 'أفضل وجهات العائلات في الخليج',
    'budget travel strategies for gulf families': 'استراتيجيات السفر بميزانية محدودة',
    'seasonal activities and events calendar': 'تقويم الأنشطة والفعاليات الموسمية',
    'family activities by age group': 'أنشطة عائلية حسب الفئة العمرية',
    'travel planning tools and resources': 'أدوات وموارد تخطيط السفر',
    
    # complete-islamic-lifestyle-guide (1-6)
    'the pillars of practice': 'أركان الممارسة الإسلامية',
    'islamic finance for families': 'المالية الإسلامية للعائلات',
    'islamic parenting and family life': 'التربية الإسلامية والحياة الأسرية',
    'health and wellness in islam': 'الصحة والعافية في الإسلام',
    'islamic travel and etiquette': 'السفر والآداب الإسلامية',
    'building daily islamic routines': 'بناء روتين إسلامي يومي',
    
    # family-friendly-activities-gulf-cities (1-5)
    'outdoor activities (october to april)': 'الأنشطة الخارجية (أكتوبر إلى أبريل)',
    'indoor activities (may to september)': 'الأنشطة الداخلية (مايو إلى سبتمبر)',
    'seasonal events and festivals': 'الفعاليات والمهرجانات الموسمية',
    'budget-friendly family activities': 'أنشطة عائلية مناسبة للميزانية',
    'planning family day trips': 'تخطيط رحلات اليوم الواحد',
    
    # complete-gulf-family-financial-life-hub (1-8)
    'the family budget — your financial foundation': 'ميزانية الأسرة: أساسك المالي',
    'building your savings system': 'بناء نظام الادخار',
    'financial planning for expatriate families': 'التخطيط المالي للعائلات الوافدة',
    'insurance and risk management': 'التأمين وإدارة المخاطر',
    'investing and building wealth': 'الاستثمار وبناء الثروة',
    'side businesses and additional income': 'الأعمال الجانبية والدخل الإضافي',
    'teaching children financial literacy': 'تعليم الأطفال الثقافة المالية',
    'real estate and housing decisions': 'العقار وقرارات السكن',
    # Malformed fragments from source HTML issues
    'section 3: a': 'استراتيجيات وقت الشاشة حسب العمر',
    'section 7: quality time, not q': 'الوقت النوعي لا الكمي',
    'section 7: emergency care vs. urge': 'الرعاية الطارئة مقابل العاجلة',
    'the 28/36 rule for s': 'قاعدة 28/36 للمشترين بدخل واحد',

    'section 3: a': 'استراتيجيات وقت الشاشة حسب العمر',
    'section 7: quality time, not q': 'الوقت النوعي لا الكمي',
    'section 7: emergency care vs. urge': 'الرعاية الطارئة مقابل العاجلة',

}

# Emergency fund guide (no sections, special headings)
EMERGENCY_HEADINGS = {
    'what counts as an emergency': 'ما الذي يعتبر طارئاً',
    'where to keep your emergency fund': 'أين تحتفظ بصندوق الطوارئ',
    'when to use your emergency fund': 'متى تستخدم صندوق الطوارئ',
    'step 1: calculate your essential monthly expenses': 'الخطوة 1: احسب مصروفاتك الشهرية الأساسية',
    'step 2: determine your risk factor': 'الخطوة 2: حدد عامل المخاطرة',
    'step 3: build your fund with a savings plan': 'الخطوة 3: ابنِ صندوق الطوارئ',
}

# House affordability special headings
HOUSE_HEADINGS = {
    'the 28/36 rule for single-income buyers': 'قاعدة 28/36 للمشترين بدخل واحد',
    'calculating your affordable home price': 'حساب سعر المنزل المناسب',
    'hidden costs single-income buyers often miss': 'التكاليف الخفية التي يغفل عنها المشترون',
    'down payment strategies for single-income buyers': 'استراتيجيات الدفعة الأولى',
}

# Umrah special headings
UMRAH_HEADINGS = {
    'ihram and prayer essentials': 'أساسيات الإحرام والصلاة',
    'clothing for the family': 'ملابس العائلة',
    'footwear': 'الأحذية',
    'toiletries and health items': 'مستلزمات النظافة والصحة',
    'medications and first aid': 'الأدوية والإسعافات الأولية',
    'documents and money': 'المستندات والنقود',
    'items for children': 'أغراض الأطفال',
    'what not to pack': 'ما لا يجب أن تأخذه',
}

# Introduction/Conclusion patterns
INTRO_PREFIXES = [
    'introduction: why saving feels impossible and how to fix it',
    'introduction: the rising cost of education in the gulf',
    'introduction: why most budgets fail and how yours will succeed',
    'introduction: your largest single payout',
    'introduction: why financial protection matters more in the gulf',
    'introduction: the rise of the side hustle in the gulf',
    'introduction: one of the most important decisions you will make',
    'introduction: why your family needs a financial plan, not just a budget',
    'introduction: designing a family life that works',
    'introduction: you can eat well without spending more',
    'introduction: the digital parenting challenge',
    'introduction: systems over goals',
    'introduction: the working parent paradox',
    'introduction: the gift of financial wisdom',
    'introduction: health as a family system, not an individual pursuit',
    'introduction: the growing challenge of healthcare costs',
    'introduction: the most important preparation you will ever make',
    'introduction: making family memories across the gulf',
    'introduction: islam as a complete way of life',
    'introduction: endless opportunities for family fun',
    'introduction: building generational financial wellness',
]


def extract_ar_from_body(body):
    body = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\2', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<span class="en">.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    return body

def extract_en_from_body(body):
    body = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\2', body, flags=re.DOTALL)
    body = re.sub(r'<span class="ar">.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="en">(.*?)</span>', r'\1', body, flags=re.DOTALL)
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
    body = re.sub(r'<\s*<h2', '<h2', body)  # Fix double <<h2
    return body

def make_heading_id(text):
    h_id = text.replace(' ', '-')
    h_id = re.sub(r'[^؀-ۿ\w-]', '', h_id)
    h_id = re.sub(r'-+', '-', h_id).strip('-')
    if not h_id:
        h_id = f"section-{abs(hash(text)) % 1000}"
    return h_id

def balance_divs(html):
    """Auto-fix div imbalance by counting opens/closes."""
    opens = list(re.finditer(r'<div\b', html))
    closes = list(re.finditer(r'</div>', html))
    diff = len(opens) - len(closes)
    if diff > 0:
        html += '\n' + '</div>' * diff
    elif diff < 0:
        html = ('<div>' * abs(diff)) + '\n' + html
    return html


def get_arabic_heading(heading_text):
    """Convert English heading to Arabic heading using dictionary matching."""
    heading_text = heading_text.strip()
    en_lower = heading_text.lower().strip()
    
    # 1. Exact match on full heading
    if en_lower in SECTION_TOPIC:
        return SECTION_TOPIC[en_lower]
    if en_lower in EMERGENCY_HEADINGS:
        return EMERGENCY_HEADINGS[en_lower]
    if en_lower in HOUSE_HEADINGS:
        return HOUSE_HEADINGS[en_lower]
    if en_lower in UMRAH_HEADINGS:
        return UMRAH_HEADINGS[en_lower]
    
    # 2. Introduction patterns - always return just 'مقدمة'
    if en_lower.startswith('introduction'):
        return 'مقدمة'
    
    # 3. Conclusion / FAQ
    if en_lower.startswith('conclusion'):
        return 'الخاتمة'
    if en_lower.startswith('frequently asked'):
        return 'أسئلة شائعة'
    
    # 4. Section pattern: strip "section N: " prefix and match topic
    m = re.match(r'.*?section\s+\d+:\s*(.+)$', en_lower)
    if not m:
        # Try with possible prepended text (case where malformed page has text before section)
        m = re.match(r'.*?section\s+\d+:\s*(.+)$', en_lower)
    if m:
        topic = m.group(1).strip().rstrip('.')
        # Try exact topic match
        if topic in SECTION_TOPIC:
            return SECTION_TOPIC[topic]
        # Try removing trailing question mark
        if topic.endswith('?'):
            topic2 = topic[:-1].strip()
            if topic2 in SECTION_TOPIC:
                return SECTION_TOPIC[topic2]
        # Try with trailing '?' added
        if not topic.endswith('?'):
            topic3 = topic + '?'
            if topic3 in SECTION_TOPIC:
                return SECTION_TOPIC[topic3]
        # Try matching without possessive 's
        topic4 = topic.replace("'s", "")
        if topic4 in SECTION_TOPIC:
            return SECTION_TOPIC[topic4]
        print(f"    ⚠️ Section topic not found: {topic}")
    
    # 5. Step pattern
    m = re.match(r'^(step\s+\d+):\s*(.+)$', en_lower)
    if m:
        step_num = m.group(1)
        topic = m.group(2).strip()
        if topic in SECTION_TOPIC:
            return SECTION_TOPIC[topic]
        # Map common step formats
        step_map = {
            'step 1': 'الخطوة 1',
            'step 2': 'الخطوة 2',
            'step 3': 'الخطوة 3',
        }
        if step_num in step_map:
            return f'{step_map[step_num]}: {topic}'
    
    # 6. Try house headings (full match)
    for h_name, h_ar in HOUSE_HEADINGS.items():
        if h_name in en_lower:
            return h_ar
    for h_name, h_ar in UMRAH_HEADINGS.items():
        if h_name in en_lower:
            return h_ar
    for h_name, h_ar in EMERGENCY_HEADINGS.items():
        if h_name in en_lower:
            return h_ar
    
    # 7. Keyword-based fallback
    if heading_text == 'Introduction':
        return 'مقدمة'
    
    return None


def fix_malformed_h2s(body):
    """Fix cases where h2 tags contain other h2 tags (malformed HTML)."""
    # Pattern: <h2>...<h2>...</h2>... (h2 without closing before next h2)
    # Fix by splitting: first h2 gets closed just before second h2 starts
    result = []
    i = 0
    while i < len(body):
        # Find next <h2
        h2_start = body.find('<h2', i)
        if h2_start == -1:
            result.append(body[i:])
            break
        
        # Find the closing > of this h2 tag
        close_gt = body.find('>', h2_start)
        if close_gt == -1:
            result.append(body[i:])
            break
        
        # Find the next </h2> from here
        h2_close = body.find('</h2>', close_gt)
        
        # Check if there's another <h2 before the </h2> (nested)
        next_h2 = body.find('<h2', close_gt + 1, h2_close)
        if next_h2 != -1:
            # Malformed: close this h2 before the next one
            result.append(body[i:h2_start])  # text before
            result.append(body[h2_start:close_gt+1])  # opening h2 tag
            result.append(body[close_gt+1:next_h2])  # content up to next h2
            result.append('</h2>')  # close early
            i = next_h2  # Continue from the nested h2
        else:
            # Properly formed - include everything up to </h2>
            if h2_close != -1:
                result.append(body[i:h2_close+6])
                i = h2_close + 6
            else:
                result.append(body[i:])
                break
    return ''.join(result)

def arabize_headings(body):
    """Replace English h2 headings with Arabic ones."""
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', body, flags=re.DOTALL)
    result = []
    
    for part in parts:
        h2_match = re.match(r'<h2[^>]*>(.*?)</h2>', part, re.DOTALL)
        if h2_match:
            heading_text = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
            
            # Skip old structural headings
            if any(x in heading_text for x in ['Related', 'مقالات', 'Tools', 'أدوات']):
                continue
            
            # If already has Arabic, keep as-is
            if re.search(r'[؀-ۿ]', heading_text):
                result.append(part)
            else:
                ar = get_arabic_heading(heading_text)
                if ar:
                    result.append(f'<h2>{ar}</h2>')
                else:
                    # Keep as-is if we can't translate
                    result.append(part)
        else:
            result.append(part)
    
    return ''.join(result)


# ─── Article configs ──────────────────────────────────────
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

BATCH6_ARTICLES = [
    # Articles needing full BOOM compliance (22 articles)
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

ARTICLES = [
    {"name": "building-personal-savings-system", "cat": "savings",
     "title_ar": "بناء نظام ادخار شخصي: دليل عملي للعائلات", "title_en": "Building a Personal Savings System: Practical Guide",
     "desc_ar": "دليل عملي لبناء نظام ادخار شخصي ناجح للعائلات في الخليج.", "desc_en": "Practical guide to building a successful personal savings system for Gulf families.",
     "tags_ar": ["#ادخار", "#مالية", "#توفير", "#عائلة"], "tags_en": ["#savings", "#finance", "#family", "#budget"]},
    {"name": "children-education-savings-guide", "cat": "savings",
     "title_ar": "دليل ادخار تعليم الأطفال", "title_en": "Children Education Savings Guide",
     "desc_ar": "دليل شامل للادخار لتعليم الأطفال في الخليج.", "desc_en": "Complete guide to saving for children's education in the Gulf.",
     "tags_ar": ["#تعليم", "#ادخار", "#أطفال", "#مالية"], "tags_en": ["#education", "#savings", "#children", "#finance"]},
    {"name": "complete-household-budget-system", "cat": "finance",
     "title_ar": "نظام الميزانية المنزلية الشامل", "title_en": "Complete Household Budget System",
     "desc_ar": "نظام متكامل لإدارة ميزانية المنزل في الخليج.", "desc_en": "Integrated household budget management system for the Gulf.",
     "tags_ar": ["#ميزانية", "#منزل", "#مالية", "#تخطيط"], "tags_en": ["#budget", "#household", "#finance", "#planning"]},
    {"name": "end-of-service-benefits-expats", "cat": "finance",
     "title_ar": "دليل مكافأة نهاية الخدمة للوافدين", "title_en": "End of Service Benefits Guide for Expats",
     "desc_ar": "دليل شامل لحساب مكافأة نهاية الخدمة للوافدين في دول الخليج.", "desc_en": "Complete guide to calculating end-of-service benefits for expats.",
     "tags_ar": ["#نهاية-خدمة", "#وافدين", "#مالية", "#خليج"], "tags_en": ["#end-of-service", "#expat", "#finance", "#gulf"]},
    {"name": "life-insurance-gulf-families", "cat": "finance",
     "title_ar": "دليل التأمين على الحياة للعائلات", "title_en": "Life Insurance Guide for Gulf Families",
     "desc_ar": "دليل شامل للتأمين على الحياة في الخليج.", "desc_en": "Complete guide to life insurance in the Gulf.",
     "tags_ar": ["#تأمين", "#حياة", "#عائلة", "#مالية"], "tags_en": ["#insurance", "#life", "#family", "#finance"]},
    {"name": "starting-side-business-saudi-uae", "cat": "finance",
     "title_ar": "دليل بدء مشروع جانبي في السعودية والإمارات", "title_en": "Starting a Side Business in Saudi and UAE",
     "desc_ar": "دليل شامل لبدء مشروع جانبي في السعودية والإمارات.", "desc_en": "Complete guide to starting a side business.",
     "tags_ar": ["#مشروع", "#جانبي", "#ريادة", "#أعمال"], "tags_en": ["#business", "#side-hustle", "#entrepreneurship", "#startup"]},
    {"name": "choosing-right-school-child-gulf", "cat": "family",
     "title_ar": "دليل اختيار المدرسة المناسبة", "title_en": "Guide to Choosing the Right School",
     "desc_ar": "دليل شامل لاختيار المدرسة المناسبة لأطفالك في الخليج.", "desc_en": "Complete guide to choosing the right school in the Gulf.",
     "tags_ar": ["#مدارس", "#تعليم", "#أطفال", "#تربية"], "tags_en": ["#schools", "#education", "#children", "#parenting"]},
    {"name": "complete-family-financial-planning", "cat": "finance",
     "title_ar": "التخطيط المالي العائلي الشامل", "title_en": "Complete Family Financial Planning",
     "desc_ar": "دليل شامل للتخطيط المالي للعائلة في الخليج.", "desc_en": "Complete family financial planning guide for the Gulf.",
     "tags_ar": ["#تخطيط", "#مالي", "#عائلة", "#مستقبل"], "tags_en": ["#planning", "#financial", "#family", "#future"]},
    {"name": "complete-family-systems-productivity-hub", "cat": "family",
     "title_ar": "منظومة الإنتاجية العائلية", "title_en": "Complete Family Systems & Productivity Hub",
     "desc_ar": "منظومة متكاملة لتنظيم وإدارة شؤون الأسرة.", "desc_en": "Integrated system for organizing family affairs.",
     "tags_ar": ["#إنتاجية", "#تنظيم", "#عائلة", "#نظام"], "tags_en": ["#productivity", "#organization", "#family", "#system"]},
    {"name": "family-nutrition-on-budget", "cat": "family",
     "title_ar": "التغذية العائلية بميزانية محدودة", "title_en": "Family Nutrition on a Budget",
     "desc_ar": "دليل للتغذية الصحية للعائلة بدون إرهاق الميزانية.", "desc_en": "Guide to healthy family nutrition on a budget.",
     "tags_ar": ["#تغذية", "#صحة", "#ميزانية", "#عائلة"], "tags_en": ["#nutrition", "#health", "#budget", "#family"]},
    {"name": "managing-screen-time-children", "cat": "family",
     "title_ar": "إدارة وقت الشاشة للأطفال", "title_en": "Managing Screen Time for Children",
     "desc_ar": "دليل عملي لإدارة وقت الشاشة للأطفال.", "desc_en": "Practical guide to managing children's screen time.",
     "tags_ar": ["#شاشة", "#أطفال", "#تربية", "#رقمي"], "tags_en": ["#screentime", "#children", "#parenting", "#digital"]},
    {"name": "organize-life-daily-systems", "cat": "family",
     "title_ar": "نظم حياتك: أنظمة يومية للعائلات", "title_en": "Organize Your Life: Daily Systems for Families",
     "desc_ar": "أنظمة يومية عملية لتنظيم حياة العائلة.", "desc_en": "Practical daily systems for organizing family life.",
     "tags_ar": ["#تنظيم", "#حياة", "#عائلة", "#نظام"], "tags_en": ["#organization", "#life", "#family", "#system"]},
    {"name": "stress-management-working-parents", "cat": "family",
     "title_ar": "إدارة التوتر للآباء العاملين", "title_en": "Stress Management for Working Parents",
     "desc_ar": "دليل عملي لإدارة التوتر للآباء والأمهات العاملين.", "desc_en": "Practical stress management guide for working parents.",
     "tags_ar": ["#توتر", "#آباء", "#عمل", "#صحة-نفسية"], "tags_en": ["#stress", "#parents", "#work", "#mentalhealth"]},
    {"name": "teaching-children-financial-literacy", "cat": "family",
     "title_ar": "تعليم الأطفال الثقافة المالية", "title_en": "Teaching Children Financial Literacy",
     "desc_ar": "دليل لتعليم الأطفال أساسيات الثقافة المالية.", "desc_en": "Guide to teaching children financial literacy.",
     "tags_ar": ["#ثقافة-مالية", "#أطفال", "#تعليم", "#تربية"], "tags_en": ["#financial-literacy", "#children", "#education", "#parenting"]},
    {"name": "complete-gulf-family-health-wellness", "cat": "health",
     "title_ar": "الصحة والعافية الشاملة للعائلة الخليجية", "title_en": "Complete Gulf Family Health & Wellness",
     "desc_ar": "دليل شامل للصحة والعافية للعائلة في الخليج.", "desc_en": "Complete health and wellness guide for Gulf families.",
     "tags_ar": ["#صحة", "#عافية", "#عائلة", "#خليج"], "tags_en": ["#health", "#wellness", "#family", "#gulf"]},
    {"name": "managing-healthcare-costs-families", "cat": "health",
     "title_ar": "إدارة تكاليف الرعاية الصحية", "title_en": "Managing Healthcare Costs for Families",
     "desc_ar": "دليل لإدارة تكاليف الرعاية الصحية للعائلات.", "desc_en": "Guide to managing healthcare costs for families.",
     "tags_ar": ["#صحة", "#تكاليف", "#عائلة", "#تأمين"], "tags_en": ["#healthcare", "#costs", "#family", "#insurance"]},
    {"name": "preparing-for-pregnancy-guide", "cat": "health",
     "title_ar": "دليل الاستعداد للحمل", "title_en": "Preparing for Pregnancy Guide",
     "desc_ar": "دليل شامل للاستعداد للحمل.", "desc_en": "Complete guide to preparing for pregnancy.",
     "tags_ar": ["#حمل", "#صحة", "#أمومة", "#عائلة"], "tags_en": ["#pregnancy", "#health", "#motherhood", "#family"]},
    {"name": "complete-family-travel-activities-hub", "cat": "travel",
     "title_ar": "دليل السفر والأنشطة العائلية", "title_en": "Complete Family Travel & Activities Hub",
     "desc_ar": "دليل شامل للسفر والأنشطة العائلية في الخليج.", "desc_en": "Complete guide to family travel and activities.",
     "tags_ar": ["#سفر", "#عائلة", "#أنشطة", "#خليج"], "tags_en": ["#travel", "#family", "#activities", "#gulf"]},
    {"name": "complete-islamic-lifestyle-guide", "cat": "islamic",
     "title_ar": "الدليل الإسلامي الشامل للحياة اليومية", "title_en": "Complete Islamic Lifestyle Guide",
     "desc_ar": "دليل شامل للحياة الإسلامية اليومية.", "desc_en": "Complete guide to daily Islamic lifestyle.",
     "tags_ar": ["#إسلام", "#عبادة", "#حياة", "#عائلة"], "tags_en": ["#islamic", "#worship", "#lifestyle", "#family"]},
    {"name": "family-friendly-activities-gulf-cities", "cat": "travel",
     "title_ar": "أنشطة عائلية في مدن الخليج", "title_en": "Family-Friendly Activities in Gulf Cities",
     "desc_ar": "دليل لأفضل الأنشطة العائلية في الخليج.", "desc_en": "Guide to the best family-friendly activities in Gulf cities.",
     "tags_ar": ["#أنشطة", "#عائلة", "#خليج", "#ترفيه"], "tags_en": ["#activities", "#family", "#gulf", "#fun"]},
    {"name": "complete-gulf-family-financial-life-hub", "cat": "holistic",
     "title_ar": "محور الحياة المالية للعائلة الخليجية", "title_en": "Complete Gulf Family Financial Life Hub",
     "desc_ar": "مركز شامل للحياة المالية للعائلة في الخليج.", "desc_en": "Comprehensive hub for Gulf family financial life.",
     "tags_ar": ["#مالية", "#عائلة", "#خليج", "#شامل"], "tags_en": ["#finance", "#family", "#gulf", "#comprehensive"]},
    {"name": "emergency-fund-calculator-guide", "cat": "finance",
     "title_ar": "دليل صندوق الطوارئ المالي", "title_en": "Emergency Fund Calculator Guide",
     "desc_ar": "دليل شامل لحساب صندوق الطوارئ المالي.", "desc_en": "Complete guide to calculating the right emergency fund.",
     "tags_ar": ["#طوارئ", "#مالية", "#ادخار", "#عائلة"], "tags_en": ["#emergency", "#finance", "#savings", "#family"]},
    {"name": "family-budget-planning-guide", "cat": "finance",
     "title_ar": "دليل تخطيط الميزانية العائلية", "title_en": "Family Budget Planning Guide",
     "desc_ar": "دليل شامل لتخطيط وإدارة ميزانية الأسرة.", "desc_en": "Complete guide to planning and managing family budget.",
     "tags_ar": ["#ميزانية", "#عائلة", "#تخطيط", "#مالية"], "tags_en": ["#budget", "#family", "#planning", "#finance"]},
    {"name": "house-affordability-single-income-guide", "cat": "realestate",
     "title_ar": "دليل شراء منزل بدخل واحد", "title_en": "House Affordability on a Single Income",
     "desc_ar": "دليل لشراء منزل بدخل واحد في السعودية والخليج.", "desc_en": "Guide to buying a home on a single income.",
     "tags_ar": ["#عقار", "#منزل", "#دخل-واحد", "#تمويل"], "tags_en": ["#realestate", "#home", "#single-income", "#mortgage"]},
    {"name": "umrah-packing-checklist-guide", "cat": "travel",
     "title_ar": "دليل حقيبة العمرة: قائمة التجهيزات", "title_en": "Umrah Packing Checklist Guide",
     "desc_ar": "قائمة شاملة لتجهيزات حقيبة العمرة.", "desc_en": "Complete Umrah packing checklist for families.",
     "tags_ar": ["#عمرة", "#سفر", "#تجهيزات", "#عائلة"], "tags_en": ["#umrah", "#travel", "#packing", "#family"]},
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
  <link rel="stylesheet" href="/styles/global.css?v=20260617c"><link rel="stylesheet" href="/styles/home.css?v=20260617b"><link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
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
<footer class="site-footer"><div class="footer-inner"><div class="footer-top"><div class="footer-brand"><a href="/"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE"></a><p>مساحة هادئة لاحتياجات عائلتك اليومية.</p></div><div class="footer-cols"><div class="footer-col"><h4>الأقسام</h4><ul><li><a href="/health.html">الصحة</a></li><li><a href="/finance.html">المالية</a></li><li><a href="/real-estate.html">العقار</a></li><li><a href="/travel.html">السفر</a></li><li><a href="/islamic.html">الإسلامية</a></li></ul></div><div class="footer-col"><h4>الأدوات</h4><ul><li><a href="/tools/water-calculator.html">حاسبة الماء</a></li><li><a href="/tools/bmi-calculator.html">حاسبة BMI</a></li><li><a href="/tools/calorie-calculator.html">حاسبة السعرات</a></li><li><a href="/tools/hijri-converter.html">محوّل التاريخ</a></li></ul></div><div class="footer-col"><h4>الشركة</h4><ul><li><a href="/about.html">عنّا</a></li><li><a href="/blog.html">المدونة</a></li><li><a href="/contact.html">اتصل بنا</a></li><li><a href="/privacy.html">الخصوصية</a></li></ul></div></div></div><hr><div class="footer-bottom"><span>© 2026 DOTFORLIFE</span></div></div></footer>
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
    
    # Read from git (use HEAD~1 for source content, HEAD now has batch5 output)
    src_ref = 'HEAD~1'
    ar_html = os.popen(f'git show {src_ref}:blog/{name}-ar.html 2>/dev/null').read()
    main_html = os.popen(f'git show {src_ref}:blog/{name}.html 2>/dev/null').read()
    # Fallback: try HEAD if HEAD~1 doesn't have the file
    if not ar_html or len(ar_html) < 500:
        ar_html = os.popen(f'git show HEAD:blog/{name}.html 2>/dev/null').read()
    if not main_html or len(main_html) < 500:
        main_html = os.popen(f'git show HEAD:blog/{name}.html 2>/dev/null').read()
    if not ar_html or not main_html:
        print(f"  ❌ Cannot read from git")
        return False
    
    # ─── AR extraction ───
    m = re.search(r'<article class="article-body">(.*?)</article>', ar_html, re.DOTALL)
    if not m:
        print(f"  ❌ No article-body in -ar.html")
        return False
    ar_body = extract_ar_from_body(m.group(1))
    ar_body = strip_old_sections(ar_body)
    
    # Keep all content from -ar.html as-is (it's the designated Arabic version)
    
    ar_body = fix_malformed_h2s(ar_body)
    ar_body = arabize_headings(ar_body)
    ar_body = re.sub(r'<p>\s*</p>', '', ar_body)
    ar_body = re.sub(r'<li>\s*</li>', '', ar_body)
    ar_body = balance_divs(ar_body)
    
    ar_text = re.sub(r'<[^>]+>', ' ', ar_body)
    ar_ar = len(re.findall(r'[؀-ۿ]', ar_text))
    ar_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', ar_text))
    print(f"  AR: {ar_ar} chars, {ar_en} EN words")
    
    # ─── EN extraction ───
    m = re.search(r'<article class="article-body">(.*?)</article>', main_html, re.DOTALL)
    if m:
        en_body = m.group(1)
        if '<span class="en">' in en_body and '<span class="ar">' in en_body:
            en_body = extract_en_from_body(en_body)
        en_body = strip_old_sections(en_body)
    else:
        en_body = extract_en_from_body(ar_html)
        en_body = strip_old_sections(en_body)
    
    en_text = re.sub(r'<[^>]+>', ' ', en_body)
    en_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', en_text))
    print(f"  EN: {en_en} words")
    en_body = balance_divs(en_body)
    
    # ─── TOC ───
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
        # Replace h2 with id
        ar_body = re.sub(
            rf'<h2[^>]*>\s*{re.escape(htext)}\s*</h2>',
            f'<h2 id="{hid}">{htext}</h2>',
            ar_body
        )
    
    # ─── Write ───
    ar_final = build_ar_html(ar_body, config, toc_items)
    with open(ar_path, 'w', encoding='utf-8') as f:
        f.write(ar_final)
    
    # Build EN sidebar components
    en_toc_links = ""
    if toc_items:
        en_toc_links = '\n'.join(f'  <a href="#{hid}" class="toc-item">{h}</a>' for h, hid in toc_items)

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
  <link rel="stylesheet" href="/styles/global.css?v=20260617c"><link rel="stylesheet" href="/styles/home.css?v=20260617b"><link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
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
<div class="article-tool-cta"><h3>Get Started Today</h3><p>Use our tools to improve your financial planning.</p><a href="/tools/budget-calculator.html" class="tool-cta-btn">Use the Tool →</a></div>
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
<footer class="site-footer"><div class="footer-inner"><div class="footer-top"><div class="footer-brand"><a href="/"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE"></a><p>A calm space for your family's daily needs.</p></div><div class="footer-cols"><div class="footer-col"><h4>Categories</h4><ul><li><a href="/health.html">Health</a></li><li><a href="/finance.html">Finance</a></li><li><a href="/real-estate.html">Real Estate</a></li><li><a href="/travel.html">Travel</a></li><li><a href="/islamic.html">Islamic</a></li></ul></div><div class="footer-col"><h4>Tools</h4><ul><li><a href="/tools/water-calculator.html">Water Calculator</a></li><li><a href="/tools/bmi-calculator.html">BMI Calculator</a></li><li><a href="/tools/calorie-calculator.html">Calorie Calculator</a></li><li><a href="/tools/hijri-converter.html">Hijri Converter</a></li></ul></div><div class="footer-col"><h4>Company</h4><ul><li><a href="/about.html">About</a></li><li><a href="/blog.html">Blog</a></li><li><a href="/contact.html">Contact</a></li><li><a href="/privacy.html">Privacy</a></li></ul></div></div></div><hr><div class="footer-bottom"><span>© 2026 DOTFORLIFE</span></div></div></footer>
<script src="/scripts/global.js?v=20260617a" defer></script>
<script>(function(){{var bar=document.getElementById('reading-progress');if(bar)window.addEventListener('scroll',function(){{var h=document.documentElement,pct=(h.scrollTop||document.body.scrollTop)/(h.scrollHeight-h.clientHeight||1)*100;bar.style.width=pct+'%'}},{{passive:true}});var tocLinks=document.querySelectorAll('.toc-item');if(tocLinks.length){{var headings=[];tocLinks.forEach(function(l){{var el=document.getElementById(l.getAttribute('href').replace('#',''));if(el)headings.push({{el:el,link:l}})}});window.addEventListener('scroll',function(){{var sy=window.scrollY+130,cur=null;headings.forEach(function(h){{if(h.el.offsetTop<=sy)cur=h}});tocLinks.forEach(function(l){{l.classList.remove('is-active')}});if(cur)cur.link.classList.add('is-active')}},{{passive:true}})}})()</script>
</body>
</html>''')
    
    # Redirect
    with open(redir_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="0;url=/blog/{name}.html"><meta name="robots" content="noindex"><title>تم النقل</title></head><body><p>تم نقل الصفحة إلى <a href="/blog/{name}.html">{name}</a>.</p></body></html>''')
    
    print(f"  ✅ {name}.html + -en.html + -ar.html")
    
    # ─── Verify ───
    with open(ar_path, 'r') as f:
        v = f.read()
    issues = []
    if 'article-layout' not in v: issues.append("no layout")
    if 'article-sidebar' not in v: issues.append("no sidebar")
    if 'toc-item' not in v: issues.append("no TOC")
    if 'display:grid' not in v: issues.append("no grid")
    if 'hreflang' not in v: issues.append("no hreflang")
    
    en_h2s = re.findall(r'<h2[^>]*>[^<]*[a-zA-Z]{4,}[^<]*</h2>', v)
    if en_h2s: issues.append(f"{len(en_h2s)} EN headings: {[re.sub(r'<[^>]+>','',h).strip() for h in en_h2s[:3]]}")
    
    do = len(re.findall(r'<div\b', v))
    dc = len(re.findall(r'</div>', v))
    if do != dc: issues.append(f"div {do}/{dc}")
    
    if issues:
        print(f"  ❌ {'; '.join(issues)}")
        return False
    print(f"  ✅ Verified (div {do}/{dc})")
    return True


if __name__ == "__main__":
    s, f = 0, 0
    for c in ARTICLES:
        ok = process_article(c)
        if ok: s += 1
        else: f += 1
    print(f"\n{'='*60}\n✅ Batch 5 Fix: {s} succeeded, {f} failed\n{'='*60}")
