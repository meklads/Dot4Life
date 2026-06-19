/**
 * DOTFORLIFE — Daily Capsule (homepage #morning-moment)
 * Priority: Railway API → data/capsules-published.json → weekly fallback
 */
(function () {
  'use strict';

  var API = 'https://dot4life-production.up.railway.app/api/capsule/today';

  var FALLBACK = [
    { id: 'quick-dinner', tagEn: 'Quick dinner · 15 min', tagAr: 'عشاء سريع · ١٥ دقيقة', titleEn: 'Pasta with Garlic & Olive Oil', titleAr: 'باستا بالثوم وزيت الزيتون', labelEn: 'Dinner in 15 minutes', labelAr: 'عشاء في ١٥ دقيقة', descEn: 'A simple, warming dinner the whole family will love, ready in 15 minutes with pantry staples.', descAr: 'عشاء دافئ وبسيط تحبه العائلة كلها، يتحضر في ١٥ دقيقة بمقادير أساسية.', ingredients: [{ en: 'Pasta, 200g', ar: 'باستا، ٢٠٠ جرام' }, { en: 'Garlic, 4 cloves', ar: 'ثوم، ٤ فصوص' }, { en: 'Olive oil, 4 tbsp', ar: 'زيت زيتون، ٤ ملاعق' }, { en: 'Parsley & chilli', ar: 'بقدونس وبهار حار' }], steps: [{ en: 'Boil pasta in salted water until al dente.', ar: 'اسلقي الباستا في ماء مملح حتى تنضج.' }, { en: 'Fry garlic in olive oil on low heat until golden.', ar: 'حمّري الثوم في زيت الزيتون على نار خفيفة.' }, { en: 'Toss pasta with garlic oil, parsley and chilli. Serve warm.', ar: 'اخلطي الباستا مع الثوم والبقدونس. قدميها دافئة.' }] },
    { id: 'one-pot', tagEn: 'Family meal · 30 min', tagAr: 'وجبة عائلية · ٣٠ دقيقة', titleEn: 'One-Pot Rice & Chicken', titleAr: 'أرز ودجاج في وعاء واحد', labelEn: 'One-pot family meal', labelAr: 'وجبة عائلية في وعاء واحد', descEn: 'Less washing up, more togetherness — a Gulf family classic in one pot.', descAr: 'أقل غسيل، أكثر تجمّعاً — كلاسيكية عائلية في وعاء واحد.', ingredients: [], steps: [{ en: 'Brown chicken, sauté onion and garlic, add rice and stock.', ar: 'حمّري الدجاج، قلّي البصل والثوم، أضيفي الأرز والمرق.' }] },
    { id: 'family-meals', tagEn: 'Family habit · daily', tagAr: 'عادة عائلية · يومية', titleEn: 'Family Meals Together', titleAr: 'الوجبات العائلية المشتركة', labelEn: 'Eat together tonight', labelAr: 'تناولوا معاً الليلة', descEn: 'The table is where your family connects — start with one shared meal today.', descAr: 'المائدة حيث تتصل عائلتك — ابدأوا بوجبة مشتركة واحدة اليوم.', ingredients: [], steps: [{ en: 'Set a consistent mealtime. No phones at the table.', ar: 'حدّدوا وقتاً ثابتاً. لا هواتف على الطاولة.' }] },
    { id: 'evening-routine', tagEn: 'Evening calm · 20 min', tagAr: 'هدوء مسائي · ٢٠ دقيقة', titleEn: 'Calm Evening Routine', titleAr: 'روتين مسائي هادئ', labelEn: 'Wind down as a family', labelAr: 'هدّئوا المساء معاً', descEn: 'A gentle sequence that signals the day is ending and home is safe.', descAr: 'تسلسل لطيف يُعلِن أن اليوم انتهى والبيت آمِن.', ingredients: [], steps: [{ en: 'Dim lights, herbal tea together, one minute of quiet breathing.', ar: 'خفّفوا الإضاءة، شاي أعشاب، دقيقة تنفس.' }] },
    { id: 'morning-routine', tagEn: 'Morning · 15 min', tagAr: 'صباح · ١٥ دقيقة', titleEn: 'Calm Morning Start', titleAr: 'بداية صباحية هادئة', labelEn: 'Start slow tomorrow', labelAr: 'ابدأوا ببطء غداً', descEn: 'Fifteen intentional minutes change the tone of the whole day.', descAr: 'خمس عشرة دقيقة بنية تغيّر نغمة اليوم كله.', ingredients: [], steps: [{ en: 'Prepare the night before. Wake 10 minutes earlier — no phone first.', ar: 'جهّزوا من الليلة. استيقظوا أبكر بلا هاتف.' }] },
    { id: 'gratitude', tagEn: 'Faith · 5 min', tagAr: 'إيمان · ٥ دقائق', titleEn: 'Daily Gratitude', titleAr: 'امتنان يومي', labelEn: 'Three thanks today', labelAr: 'ثلاث شكرات اليوم', descEn: 'A simple practice that shifts perspective for the whole household.', descAr: 'ممارسة بسيطة تغيّر منظور البيت كله.', ingredients: [], steps: [{ en: 'Each person names one good thing from today.', ar: 'كل فرد يذكر شيئاً جميلاً من اليوم.' }] },
    { id: 'home-reset', tagEn: 'Home · 20 min', tagAr: 'المنزل · ٢٠ دقيقة', titleEn: 'Quick Home Reset', titleAr: 'ترتيب سريع للبيت', labelEn: 'Reset one room', labelAr: 'رتّبوا غرفة واحدة', descEn: 'One tidy corner creates calm for everyone — start small.', descAr: 'زاوية مرتبة واحدة تخلق هدوءاً للجميع.', ingredients: [], steps: [{ en: 'Pick one room, 20-minute timer, clear surfaces first.', ar: 'اختاروا غرفة، ٢٠ دقيقة، صفّوا الأسطح أولاً.' }] }
  ];

  function lang() { return document.documentElement.getAttribute('data-lang') === 'ar' ? 'ar' : 'en'; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function todayStr() { return new Date().toISOString().slice(0, 10); }

  function setBilingual(root, sel, en, ar) {
    if (!root) return;
    var enEl = root.querySelector(sel + ' .en');
    var arEl = root.querySelector(sel + ' .ar');
    if (enEl) enEl.textContent = en;
    if (arEl) arEl.textContent = ar;
  }

  function fromApiCapsule(raw) {
    if (!raw) return null;
    var cat = raw.category || 'wellness';
    var tagEn = (raw.subtitle_en || raw.title_en || '').slice(0, 40);
    var tagAr = (raw.subtitle_ar || raw.title_ar || '').slice(0, 40);
    return {
      id: raw.id || cat,
      capsuleId: /^cap_/.test(raw.id || '') ? raw.id : null,
      tagEn: tagEn, tagAr: tagAr,
      titleEn: raw.title_en || '', titleAr: raw.title_ar || '',
      labelEn: raw.subtitle_en || raw.title_en || "Today's idea",
      labelAr: raw.subtitle_ar || raw.title_ar || 'فكرة اليوم',
      descEn: raw.body_en || '', descAr: raw.body_ar || '',
      ingredients: [],
      steps: raw.tip_en ? [{ en: raw.tip_en, ar: raw.tip_ar || raw.tip_en }] : []
    };
  }

  function fromPublishedEntry(raw, date) {
    return fromApiCapsule(Object.assign({ id: raw.id || date }, raw));
  }

  function applyCapsule(c) {
    if (!c) return;
    var trigger = document.getElementById('mm-capsule-trigger');
    if (trigger) setBilingual(trigger, '.mm-capsule-title', c.labelEn, c.labelAr);
    var overlay = document.getElementById('capsule-overlay');
    if (!overlay) return;
    setBilingual(overlay, '.capsule-tag', c.tagEn, c.tagAr);
    setBilingual(overlay, '.capsule-title', c.titleEn, c.titleAr);
    setBilingual(overlay, '.capsule-desc', c.descEn, c.descAr);
    var ingWrap = overlay.querySelector('.capsule-ingredients');
    if (ingWrap) {
      if (c.ingredients && c.ingredients.length) {
        ingWrap.innerHTML = c.ingredients.map(function (ing) {
          return '<div class="capsule-ing"><span class="en">' + esc(ing.en) + '</span><span class="ar">' + esc(ing.ar) + '</span></div>';
        }).join('');
        var ingSection = ingWrap.closest('.capsule-section');
        if (ingSection) ingSection.hidden = false;
      } else {
        ingWrap.innerHTML = '';
        var ingSec = ingWrap.closest('.capsule-section');
        if (ingSec) ingSec.hidden = true;
      }
    }
    var stepsWrap = overlay.querySelector('.capsule-steps');
    if (stepsWrap && c.steps && c.steps.length) {
      stepsWrap.innerHTML = c.steps.map(function (step, i) {
        return '<div class="capsule-step"><span class="capsule-step-num">' + (i + 1) + '</span><span class="en">' + esc(step.en) + '</span><span class="ar">' + esc(step.ar) + '</span></div>';
      }).join('');
    }
    var fullLink = overlay.querySelector('.capsule-btn-full');
    if (fullLink) {
      var langQ = lang() === 'ar' ? '&lang=ar' : '&lang=en';
      if (c.capsuleId) {
        fullLink.href = '/life-guide.html?c=' + encodeURIComponent(c.capsuleId) + langQ;
      } else if (c.id) {
        fullLink.href = '/life-guide.html?g=' + encodeURIComponent(c.id) + langQ;
      }
    }
  }

  function applyFallback() {
    var day = new Date().getDay();
    applyCapsule(FALLBACK[day % FALLBACK.length]);
  }

  function fetchJson(url) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      var ct = r.headers.get('content-type') || '';
      if (!ct.includes('application/json')) throw new Error('not json');
      return r.json();
    });
  }

  function init() {
    var date = todayStr();
    fetchJson(API + '?date=' + date)
      .then(function (data) {
        if (data && data.found && data.capsule) {
          applyCapsule(fromApiCapsule(data.capsule));
          return;
        }
        throw new Error('no capsule');
      })
      .catch(function () {
        return fetchJson('/data/capsules-published.json?v=20260619e')
          .then(function (file) {
            var entry = file.byDate && (file.byDate[date] || file.byDate[Object.keys(file.byDate).sort().pop()]);
            if (entry) applyCapsule(fromPublishedEntry(entry, date));
            else applyFallback();
          })
          .catch(applyFallback);
      });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  document.addEventListener('dfl:langchange', init);
})();
