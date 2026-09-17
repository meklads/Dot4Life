/**
 * Makkah Hotel Decision Tool UI — Tool 04
 */
(function () {
  'use strict';

  var S = window.DFLPlannerShared;
  var E = window.DFLHotelDecisionEngine;
  if (!S || !E) return;

  var STEPS = ['trip', 'group', 'walking', 'priorities', 'budget', 'result'];
  var state = {
    step: 0,
    started: false,
    inputs: E.normalize({}),
    plan: null,
    hotels: [],
    showCompare: false
  };

  var root, progressEl, resultEl;

  function $(sel, el) { return (el || document).querySelector(sel); }
  function $all(sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); }

  function track(name, extra) {
    S.track(name, Object.assign({
      tool: 'hotel_decision',
      step: STEPS[state.step]
    }, extra || {}));
  }

  function syncProgress() {
    var idx = Math.min(state.step, 4);
    var pct = Math.round((idx / 4) * 100);
    if (progressEl) {
      progressEl.setAttribute('aria-valuenow', String(idx + 1));
      progressEl.querySelector('.mtp-progress-bar').style.width = pct + '%';
      $all('[data-step-dot]', progressEl).forEach(function (dot, i) {
        dot.classList.toggle('is-done', i < idx);
        dot.classList.toggle('is-current', i === idx);
      });
    }
    $all('.mtp-panel', root).forEach(function (p, i) {
      var show = (state.step < 5 && i === state.step) || (state.step === 5 && p.getAttribute('data-panel') === 'result');
      p.hidden = !show;
    });
    var back = $('#hdt-back');
    var next = $('#hdt-next');
    if (back) back.hidden = state.step === 0 || state.step === 5;
    if (next) {
      next.hidden = state.step === 5;
      next.textContent = state.step === 4
        ? (S.lang() === 'ar' ? 'أنشئ ملف الفندق' : 'Create hotel profile')
        : (S.lang() === 'ar' ? 'التالي' : 'Next');
    }
  }

  function readForm() {
    state.inputs = E.normalize({
      duration: ($('input[name="hdt-duration"]:checked') || {}).value,
      adults: ($('#hdt-adults') || {}).value,
      children: ($('#hdt-children') || {}).value,
      elderly: ($('input[name="hdt-elderly"]:checked') || {}).value,
      walking: ($('input[name="hdt-walking"]:checked') || {}).value,
      pace: ($('input[name="hdt-pace"]:checked') || {}).value,
      priority: ($('input[name="hdt-priority"]:checked') || {}).value,
      budget: ($('input[name="hdt-budget"]:checked') || {}).value,
      roomNeed: ($('input[name="hdt-room"]:checked') || {}).value,
      locationPref: ($('input[name="hdt-location"]:checked') || {}).value
    });
  }

  function readHotels() {
    var hotels = [];
    for (var i = 1; i <= 3; i++) {
      var name = (($('#hdt-h' + i + '-name') || {}).value || '').trim();
      if (!name) continue;
      hotels.push({
        name: name,
        access: ($('#hdt-h' + i + '-access') || {}).value || 'unknown',
        family: ($('#hdt-h' + i + '-family') || {}).value || 'unknown',
        value: ($('#hdt-h' + i + '-value') || {}).value || 'unknown',
        comfort: ($('#hdt-h' + i + '-comfort') || {}).value || 'unknown'
      });
    }
    state.hotels = hotels;
    return hotels;
  }

  function validateStep() {
    readForm();
    clearError();
    if (state.step === 0 && !$('input[name="hdt-duration"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا مدة الإقامة.' : 'Please choose stay length.');
    }
    if (state.step === 1 && state.inputs.adults < 1) {
      return fail(S.lang() === 'ar' ? 'عدد البالغين يجب أن يكون 1 على الأقل.' : 'Adults must be at least 1.');
    }
    if (state.step === 2 && !$('input[name="hdt-walking"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا تفضيل المشي.' : 'Please choose walking preference.');
    }
    if (state.step === 3 && !$('input[name="hdt-priority"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا الأولوية.' : 'Please choose a priority.');
    }
    if (state.step === 4 && !$('input[name="hdt-budget"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا توجّه الميزانية.' : 'Please choose budget orientation.');
    }
    return true;
  }

  function fail(msg) {
    var err = $('#hdt-error');
    if (err) { err.hidden = false; err.textContent = msg; }
    return false;
  }
  function clearError() {
    var err = $('#hdt-error');
    if (err) { err.hidden = true; err.textContent = ''; }
  }

  function go(delta) {
    if (delta > 0 && !validateStep()) return;
    if (!state.started && state.step === 0 && delta > 0) {
      state.started = true;
      track('hotel_decision_start');
    }
    if (delta > 0 && state.step < 4) {
      track('hotel_decision_step_complete', { step_name: STEPS[state.step] });
    }
    if (delta > 0 && state.step === 4) {
      generatePlan();
      return;
    }
    state.step = Math.max(0, Math.min(5, state.step + delta));
    syncProgress();
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function generatePlan(adjustment) {
    readForm();
    var hotels = state.showCompare ? readHotels() : null;
    if (adjustment) {
      state.plan = E.applyAdjustment(Object.assign({}, state.plan, { _hotels: hotels }), adjustment);
      state.plan._hotels = hotels;
      track('hotel_decision_adjust', { adjustment: adjustment });
    } else {
      state.plan = E.generate(state.inputs, hotels);
      state.plan._hotels = hotels;
      track('hotel_decision_complete', {
        duration: state.inputs.duration,
        priority: state.inputs.priority,
        budget: state.inputs.budget,
        walking: state.inputs.walking,
        group: (state.inputs.children > 0 ? 'family' : 'adults') + (state.inputs.elderly === 'yes' ? '_elder' : ''),
        compare: hotels && hotels.length ? hotels.length : 0
      });
      if (hotels && hotels.length) track('hotel_decision_compare', { count: hotels.length });
    }
    renderPlan();
    state.step = 5;
    syncProgress();
    try {
      localStorage.setItem('dfl-hotel-decision', JSON.stringify({
        inputs: state.plan.inputs,
        generatedAt: state.plan.generatedAt
      }));
    } catch (e) { /* ignore */ }
  }

  function txt(pair) { return S.t(pair); }
  function esc(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function listHtml(items) {
    return '<ul>' + (items || []).map(function (it) {
      return '<li>' + esc(txt(it)) + '</li>';
    }).join('') + '</ul>';
  }
  function levelLabel(v) {
    if (v === 'high') return S.lang() === 'ar' ? 'مرتفع (حسب إدخالك)' : 'High (as you entered)';
    if (v === 'mid') return S.lang() === 'ar' ? 'متوسط (حسب إدخالك)' : 'Mid (as you entered)';
    if (v === 'low') return S.lang() === 'ar' ? 'منخفض (حسب إدخالك)' : 'Low (as you entered)';
    return S.lang() === 'ar' ? 'غير متاح' : 'Not available';
  }

  function renderPlan() {
    var plan = state.plan;
    if (!plan || !resultEl) return;
    var L = plan.labels;
    var html = '';
    html += '<div class="mtp-summary">';
    html += '<h3><span class="en">Your Makkah hotel profile</span><span class="ar">ملف فندق مكة لكم</span></h3>';
    html += '<ul class="mtp-summary-list">';
    html += '<li><strong><span class="en">Stay</span><span class="ar">الإقامة</span>:</strong> ' + esc(txt(L.duration)) + '</li>';
    html += '<li><strong><span class="en">Group</span><span class="ar">المجموعة</span>:</strong> ' + esc(txt(L.group)) + '</li>';
    html += '<li><strong><span class="en">Walking</span><span class="ar">المشي</span>:</strong> ' + esc(txt(L.walking)) + '</li>';
    html += '<li><strong><span class="en">Priority</span><span class="ar">الأولوية</span>:</strong> ' + esc(txt(L.priority)) + '</li>';
    html += '<li><strong><span class="en">Budget</span><span class="ar">الميزانية</span>:</strong> ' + esc(txt(L.budget)) + '</li>';
    html += '</ul></div>';

    html += '<article class="mtp-day">';
    html += '<h4><span class="en">Recommended stay type</span><span class="ar">نوع الإقامة الموصى به</span></h4>';
    html += '<p><strong>' + esc(txt(plan.category.title)) + '</strong></p>';
    html += '<p class="mtp-hint">' + esc(txt(plan.category.fit)) + '</p>';
    if (plan.alternativeCategory) {
      html += '<p class="mtp-hint"><span class="en">Also consider:</span><span class="ar">فكّروا أيضاً في:</span> ' + esc(txt(plan.alternativeCategory.title)) + '</p>';
    }
    html += '</article>';

    html += '<article class="mtp-day"><h4><span class="en">What to prioritize</span><span class="ar">ما الذي تولونه الأولوية</span></h4>' + listHtml(plan.prioritize) + '</article>';
    html += '<article class="mtp-day"><h4><span class="en">Why these factors matter for you</span><span class="ar">لماذا تهمكم هذه العوامل</span></h4>' + listHtml(plan.why) + '</article>';
    html += '<article class="mtp-day"><h4><span class="en">What to check before booking</span><span class="ar">ما الذي تتحققون منه قبل الحجز</span></h4>' + listHtml(plan.checklist) + '</article>';

    if (plan.compare && plan.compare.length) {
      html += '<article class="mtp-day"><h4><span class="en">Fit for your trip (from what you entered)</span><span class="ar">الملاءمة لرحلتكم (حسب ما أدخلتموه)</span></h4>';
      html += '<p class="mtp-hint"><span class="en">Not a quality ranking. Missing facts stay “Not available”.</span><span class="ar">ليس ترتيب جودة. الحقائق الناقصة تبقى «غير متاح».</span></p>';
      plan.compare.forEach(function (h) {
        html += '<div class="mtp-block" style="border:1px solid var(--mtp-line);border-radius:12px;padding:0.75rem;margin-bottom:0.65rem">';
        html += '<div class="mtp-slot">' + esc(h.name) + '</div>';
        html += '<ul><li><strong><span class="en">Fit</span><span class="ar">الملاءمة</span>:</strong> ' + esc(txt(h.fit)) + '</li>';
        html += '<li><span class="en">Access</span><span class="ar">الوصول</span>: ' + esc(levelLabel(h.access)) + '</li>';
        html += '<li><span class="en">Family practicality</span><span class="ar">العملية الأسرية</span>: ' + esc(levelLabel(h.family)) + '</li>';
        html += '<li><span class="en">Value</span><span class="ar">القيمة</span>: ' + esc(levelLabel(h.value)) + '</li>';
        html += '<li><span class="en">Comfort</span><span class="ar">الراحة</span>: ' + esc(levelLabel(h.comfort)) + '</li>';
        if (h.missing) html += '<li><em><span class="en">Some information not available — check before booking.</span><span class="ar">بعض المعلومات غير متاحة — تحققوا قبل الحجز.</span></em></li>';
        html += '</ul></div>';
      });
      html += '</article>';
    }

    html += '<p class="mtp-disclaimer">' + esc(txt(plan.disclaimer)) + '</p>';

    html += '<div class="mtp-adjust">';
    html += '<p class="mtp-adjust-label"><span class="en">Adjust</span><span class="ar">عدّل</span></p>';
    html += chip('convenience', 'More convenience', 'مزيد من الراحة العملية');
    html += chip('family', 'More family focus', 'تركيز أسري أكثر');
    html += chip('value', 'More value focus', 'تركيز قيمة أكثر');
    html += chip('comfort', 'More comfort', 'راحة أكثر');
    html += chip('balance', 'More balance', 'توازن أكثر');
    html += '</div>';

    html += '<div class="mtp-actions">';
    html += '<button type="button" class="mtp-btn mtp-btn-primary" data-act="copy"><span class="en">Copy checklist</span><span class="ar">نسخ القائمة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="share"><span class="en">Share profile</span><span class="ar">مشاركة الملف</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="compare"><span class="en">Compare hotels</span><span class="ar">قارن فنادق</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="print"><span class="en">Print / PDF</span><span class="ar">طباعة / PDF</span></button>';
    html += '<button type="button" class="mtp-btn mtp-btn-ghost" data-act="restart"><span class="en">Start over</span><span class="ar">البداية من جديد</span></button>';
    html += '</div>';

    html += '<div id="hdt-compare-panel" class="mtp-day" ' + (state.showCompare ? '' : 'hidden') + '>';
    html += '<h4><span class="en">Compare up to 3 hotels (manual traits only)</span><span class="ar">قارنوا حتى 3 فنادق (سمات يدوية فقط)</span></h4>';
    html += '<p class="mtp-hint"><span class="en">Enter what you already know. Leave unknown fields as “Not available”. We never invent hotel facts.</span><span class="ar">أدخلوا ما تعرفونه. اتركوا الحقول المجهولة «غير متاح». لا نخترع حقائق فندق.</span></p>';
    for (var i = 1; i <= 3; i++) {
      html += hotelFields(i);
    }
    html += '<button type="button" class="mtp-btn mtp-btn-primary" data-act="run-compare"><span class="en">Update comparison</span><span class="ar">حدّث المقارنة</span></button>';
    html += '</div>';

    html += '<div class="mtp-related">';
    html += '<a href="/makkah/tools/makkah-trip-planner/"><span class="en">Makkah Trip Planner</span><span class="ar">مخطط رحلة مكة</span></a>';
    html += '<a href="/makkah/tools/makkah-to-madinah-planner/"><span class="en">Makkah → Madinah Planner</span><span class="ar">مخطط مكة → المدينة</span></a>';
    html += '<a href="/tools/return-to-hotel"><span class="en">Return to Hotel</span><span class="ar">العودة للفندق</span></a>';
    html += '<a href="/blog/makkah-hotels-guide"><span class="en">Makkah hotels guide</span><span class="ar">دليل فنادق مكة</span></a>';
    html += '</div>';

    resultEl.innerHTML = html;
    // restore hotel field values if any
    if (state.hotels && state.hotels.length) {
      state.hotels.forEach(function (h, idx) {
        var n = idx + 1;
        var nameEl = $('#hdt-h' + n + '-name');
        if (nameEl) nameEl.value = h.name || '';
        ['access', 'family', 'value', 'comfort'].forEach(function (k) {
          var el = $('#hdt-h' + n + '-' + k);
          if (el) el.value = h[k] || 'unknown';
        });
      });
    }
  }

  function hotelFields(i) {
    var opts = function (id) {
      return '<select id="' + id + '" aria-label="Level">' +
        '<option value="unknown">' + (S.lang() === 'ar' ? 'غير متاح' : 'Not available') + '</option>' +
        '<option value="high">' + (S.lang() === 'ar' ? 'مرتفع' : 'High') + '</option>' +
        '<option value="mid">' + (S.lang() === 'ar' ? 'متوسط' : 'Mid') + '</option>' +
        '<option value="low">' + (S.lang() === 'ar' ? 'منخفض' : 'Low') + '</option>' +
        '</select>';
    };
    return '<div class="mtp-field" style="margin-bottom:0.85rem">' +
      '<label><span class="en">Hotel ' + i + ' name</span><span class="ar">اسم الفندق ' + i + '</span></label>' +
      '<input id="hdt-h' + i + '-name" type="text" maxlength="80" autocomplete="off"/>' +
      '<div class="mtp-row" style="margin-top:0.5rem">' +
      '<div><label class="mtp-hint"><span class="en">Access</span><span class="ar">الوصول</span></label>' + opts('hdt-h' + i + '-access') + '</div>' +
      '<div><label class="mtp-hint"><span class="en">Family</span><span class="ar">أسري</span></label>' + opts('hdt-h' + i + '-family') + '</div>' +
      '</div>' +
      '<div class="mtp-row" style="margin-top:0.5rem">' +
      '<div><label class="mtp-hint"><span class="en">Value</span><span class="ar">قيمة</span></label>' + opts('hdt-h' + i + '-value') + '</div>' +
      '<div><label class="mtp-hint"><span class="en">Comfort</span><span class="ar">راحة</span></label>' + opts('hdt-h' + i + '-comfort') + '</div>' +
      '</div></div>';
  }

  function chip(key, en, ar) {
    return '<button type="button" class="mtp-chip" data-adjust="' + key + '"><span class="en">' + en + '</span><span class="ar">' + ar + '</span></button>';
  }

  function planAsText() {
    var plan = state.plan;
    if (!plan) return '';
    var ar = S.lang() === 'ar';
    var lines = [ar ? 'ملف قرار فندق مكة' : 'Makkah Hotel Profile', txt(plan.category.title), ''];
    lines.push(ar ? 'الأولويات:' : 'Prioritize:');
    plan.prioritize.forEach(function (x) { lines.push('- ' + txt(x)); });
    lines.push('', ar ? 'تحققوا قبل الحجز:' : 'Checklist before booking:');
    plan.checklist.forEach(function (x) { lines.push('- ' + txt(x)); });
    lines.push('', txt(plan.disclaimer));
    lines.push('https://dotforlife.com/makkah/tools/hotel-decision/');
    return lines.join('\n');
  }

  function onResultClick(e) {
    var adj = e.target.closest('[data-adjust]');
    if (adj) {
      generatePlan(adj.getAttribute('data-adjust'));
      return;
    }
    var act = e.target.closest('[data-act]');
    if (!act) return;
    var a = act.getAttribute('data-act');
    if (a === 'copy') {
      S.copyText(planAsText()).then(function () {
        track('hotel_decision_copy');
        act.classList.add('is-ok');
      });
    }
    if (a === 'share') {
      var text = planAsText();
      if (navigator.share) {
        navigator.share({ title: 'Makkah Hotel Profile', text: text }).then(function () {
          track('hotel_decision_share');
        }).catch(function () {});
      } else {
        S.copyText(text).then(function () { track('hotel_decision_share'); });
      }
    }
    if (a === 'print') window.print();
    if (a === 'compare') {
      state.showCompare = true;
      renderPlan();
      var panel = $('#hdt-compare-panel');
      if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    if (a === 'run-compare') {
      state.showCompare = true;
      generatePlan();
    }
    if (a === 'restart') {
      track('hotel_decision_restart');
      state.step = 0;
      state.plan = null;
      state.started = false;
      state.showCompare = false;
      state.hotels = [];
      syncProgress();
    }
  }

  function init() {
    root = document.getElementById('hotel-decision');
    if (!root) return;
    progressEl = $('#hdt-progress', root);
    resultEl = $('#hdt-result', root);
    track('hotel_decision_view');
    $('#hdt-next', root).addEventListener('click', function () { go(1); });
    $('#hdt-back', root).addEventListener('click', function () { go(-1); });
    if (resultEl) resultEl.addEventListener('click', onResultClick);
    root.addEventListener('change', function () { readForm(); });
    readForm();
    syncProgress();
    if (S.onLangChange) {
      S.onLangChange(function () {
        if (state.plan) renderPlan();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
