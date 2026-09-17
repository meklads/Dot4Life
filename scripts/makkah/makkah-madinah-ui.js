/**
 * Makkah → Madinah Planner UI — Tool 03
 */
(function () {
  'use strict';

  var S = window.DFLPlannerShared;
  var E = window.DFLMakkahMadinahEngine;
  if (!S || !E) return;

  var STEPS = ['journey', 'group', 'luggage', 'timing', 'prefs', 'result'];
  var state = {
    step: 0,
    started: false,
    inputs: E.normalize({}),
    plan: null
  };

  var root, progressEl, resultEl;

  function $(sel, el) { return (el || document).querySelector(sel); }
  function $all(sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); }

  function track(name, extra) {
    S.track(name, Object.assign({
      tool: 'makkah_to_madinah_planner',
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
    var back = $('#mmp-back');
    var next = $('#mmp-next');
    if (back) back.hidden = state.step === 0 || state.step === 5;
    if (next) {
      next.hidden = state.step === 5;
      next.textContent = state.step === 4
        ? (S.lang() === 'ar' ? 'أنشئ خطة الانتقال' : 'Create transition plan')
        : (S.lang() === 'ar' ? 'التالي' : 'Next');
    }
  }

  function readForm() {
    state.inputs = E.normalize({
      departureContext: ($('input[name="mmp-dep-ctx"]:checked') || {}).value,
      arrivalContext: ($('input[name="mmp-arr-ctx"]:checked') || {}).value,
      makkahHotel: ($('#mmp-makkah-hotel') || {}).value,
      madinahHotel: ($('#mmp-madinah-hotel') || {}).value,
      adults: ($('#mmp-adults') || {}).value,
      children: ($('#mmp-children') || {}).value,
      elderly: ($('input[name="mmp-elderly"]:checked') || {}).value,
      walking: ($('input[name="mmp-walking"]:checked') || {}).value,
      luggage: ($('input[name="mmp-luggage"]:checked') || {}).value,
      stroller: ($('input[name="mmp-stroller"]:checked') || {}).value,
      pace: ($('input[name="mmp-pace"]:checked') || {}).value,
      priority: ($('input[name="mmp-priority"]:checked') || {}).value,
      transportPreference: ($('input[name="mmp-transport"]:checked') || {}).value,
      departureFlexibility: ($('input[name="mmp-flex"]:checked') || {}).value,
      hotelReady: ($('input[name="mmp-hotel-ready"]:checked') || {}).value
    });
    var walkWrap = $('#mmp-walking-wrap');
    if (walkWrap) walkWrap.hidden = state.inputs.elderly !== 'yes';
    var mkHotel = $('#mmp-makkah-hotel-wrap');
    if (mkHotel) mkHotel.hidden = state.inputs.departureContext !== 'hotel';
    var mdHotel = $('#mmp-madinah-hotel-wrap');
    if (mdHotel) mdHotel.hidden = state.inputs.arrivalContext !== 'hotel';
  }

  function validateStep() {
    readForm();
    clearError();
    if (state.step === 0) {
      if (!$('input[name="mmp-dep-ctx"]:checked')) return fail(S.lang() === 'ar' ? 'حدّدوا سياق المغادرة من مكة.' : 'Please set Makkah departure context.');
      if (!$('input[name="mmp-arr-ctx"]:checked')) return fail(S.lang() === 'ar' ? 'حدّدوا سياق الوصول للمدينة.' : 'Please set Madinah arrival context.');
    }
    if (state.step === 1) {
      if (state.inputs.adults < 1) return fail(S.lang() === 'ar' ? 'عدد البالغين يجب أن يكون 1 على الأقل.' : 'Adults must be at least 1.');
    }
    if (state.step === 2) {
      if (!$('input[name="mmp-luggage"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا مستوى الحقائب.' : 'Please choose luggage level.');
    }
    if (state.step === 3) {
      if (!$('input[name="mmp-pace"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا وتيرة الانتقال.' : 'Please choose a pace.');
      if (!$('input[name="mmp-flex"]:checked')) return fail(S.lang() === 'ar' ? 'حدّدوا مرونة المغادرة.' : 'Please set departure flexibility.');
    }
    if (state.step === 4) {
      if (!$('input[name="mmp-priority"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا الأولوية.' : 'Please choose a priority.');
    }
    return true;
  }

  function fail(msg) {
    var err = $('#mmp-error');
    if (err) { err.hidden = false; err.textContent = msg; }
    return false;
  }
  function clearError() {
    var err = $('#mmp-error');
    if (err) { err.hidden = true; err.textContent = ''; }
  }

  function go(delta) {
    if (delta > 0 && !validateStep()) return;
    if (!state.started && state.step === 0 && delta > 0) {
      state.started = true;
      track('makkah_madinah_planner_start');
    }
    if (delta > 0 && state.step < 4) {
      track('makkah_madinah_planner_step_complete', { step_name: STEPS[state.step] });
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
    if (adjustment) {
      state.plan = E.applyAdjustment(state.plan || { inputs: state.inputs }, adjustment);
      track('makkah_madinah_planner_adjust', { adjustment: adjustment });
    } else {
      state.plan = E.generate(state.inputs);
      track('makkah_madinah_planner_complete', {
        luggage: state.inputs.luggage,
        pace: state.inputs.pace,
        priority: state.inputs.priority,
        transport: state.inputs.transportPreference,
        group: (state.inputs.children > 0 ? 'family' : 'adults') + (state.inputs.elderly === 'yes' ? '_elder' : '')
      });
    }
    renderPlan();
    state.step = 5;
    syncProgress();
    try {
      localStorage.setItem('dfl-makkah-madinah-plan', JSON.stringify({
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

  function renderPlan() {
    var plan = state.plan;
    if (!plan || !resultEl) return;
    var p = plan.profile;
    var html = '';
    html += '<div class="mtp-summary">';
    html += '<h3><span class="en">Your Makkah → Madinah plan</span><span class="ar">خطتكم مكة → المدينة</span></h3>';
    html += '<p class="mtp-hint" style="margin:0 0 0.5rem"><span class="en">Your journey profile</span><span class="ar">ملف رحلتكم</span></p>';
    html += '<ul class="mtp-summary-list">';
    html += '<li><strong><span class="en">Group</span><span class="ar">المجموعة</span>:</strong> ' + esc(txt(p.group)) + '</li>';
    html += '<li><strong><span class="en">Luggage</span><span class="ar">الحقائب</span>:</strong> ' + esc(txt(p.luggage)) + '</li>';
    html += '<li><strong><span class="en">Pace</span><span class="ar">الوتيرة</span>:</strong> ' + esc(txt(p.pace)) + '</li>';
    html += '<li><strong><span class="en">Priority</span><span class="ar">الأولوية</span>:</strong> ' + esc(txt(p.priority)) + '</li>';
    if (p.walking) html += '<li><strong><span class="en">Walking</span><span class="ar">المشي</span>:</strong> ' + esc(txt(p.walking)) + '</li>';
    html += '</ul></div>';

    html += '<article class="mtp-day">';
    html += '<h4><span class="en">Recommended approach</span><span class="ar">النهج الموصى به</span></h4>';
    html += '<p><strong>' + esc(txt(plan.primary.title)) + '</strong></p>';
    html += '<p class="mtp-hint">' + esc(txt(plan.primary.blurb)) + '</p>';
    html += '<p class="mtp-adjust-label"><span class="en">Why this fits</span><span class="ar">لماذا يناسبكم</span></p>';
    html += listHtml(plan.why);
    html += '</article>';

    if (plan.alternative) {
      html += '<article class="mtp-day">';
      html += '<h4><span class="en">Alternative</span><span class="ar">بديل</span></h4>';
      html += '<p><strong>' + esc(txt(plan.alternative.title)) + '</strong></p>';
      html += '<p class="mtp-hint">' + esc(txt(plan.alternative.blurb)) + '</p>';
      html += '</article>';
    }

    html += '<article class="mtp-day">';
    html += '<h4><span class="en">Journey considerations</span><span class="ar">اعتبارات الرحلة</span></h4>';
    html += '<ul class="mtp-summary-list">';
    plan.comparison.forEach(function (row) {
      html += '<li' + (row.highlight ? ' style="font-weight:700"' : '') + '><strong>' + esc(txt(row.mode)) + ':</strong> ' + esc(txt(row.note)) + '</li>';
    });
    html += '</ul></article>';

    html += '<article class="mtp-day"><h4><span class="en">Before leaving Makkah</span><span class="ar">قبل مغادرة مكة</span></h4>' + listHtml(plan.before) + '</article>';
    html += '<article class="mtp-day"><h4><span class="en">Departure</span><span class="ar">المغادرة</span></h4>' + listHtml(plan.departure) + '</article>';
    html += '<article class="mtp-day"><h4><span class="en">During the journey</span><span class="ar">أثناء الرحلة</span></h4>' + listHtml(plan.during) + '</article>';
    html += '<article class="mtp-day"><h4><span class="en">Arrival in Madinah</span><span class="ar">الوصول إلى المدينة</span></h4>' + listHtml(plan.arrival) + '</article>';

    html += '<article class="mtp-day"><h4><span class="en">Transition-day outline</span><span class="ar">هيكل يوم الانتقال</span></h4>';
    plan.day.forEach(function (b) {
      html += '<div class="mtp-block"><div class="mtp-slot">' + esc(txt(b.slot)) + '</div>' + listHtml(b.items) + '</div>';
    });
    html += '</article>';

    html += '<p class="mtp-disclaimer">' + esc(txt(plan.disclaimer)) + '</p>';
    html += '<p class="mtp-hint"><a href="https://www.sar.com.sa/" rel="noopener noreferrer" target="_blank">' + esc(txt(plan.officialNote)) + '</a> · <span class="en">via SAR and official providers</span><span class="ar">عبر سار والمزودين الرسميين</span></p>';

    html += '<div class="mtp-adjust" role="group" aria-label="Adjust plan">';
    html += '<p class="mtp-adjust-label"><span class="en">Adjust</span><span class="ar">عدّل</span></p>';
    html += chip('simpler', 'Make it simpler', 'اجعلها أبسط');
    html += chip('comfort', 'Optimize for comfort', 'حسّن للراحة');
    html += chip('flexibility', 'Optimize for flexibility', 'حسّن للمرونة');
    html += chip('family', 'Optimize for family', 'حسّن للأسرة');
    html += chip('luggage', 'Optimize for luggage', 'حسّن للحقائب');
    html += '</div>';

    html += '<div class="mtp-actions">';
    html += '<button type="button" class="mtp-btn mtp-btn-primary" data-act="copy"><span class="en">Copy plan</span><span class="ar">نسخ الخطة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="share"><span class="en">Share</span><span class="ar">مشاركة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="print"><span class="en">Print / PDF</span><span class="ar">طباعة / PDF</span></button>';
    html += '<button type="button" class="mtp-btn mtp-btn-ghost" data-act="restart"><span class="en">Start over</span><span class="ar">البداية من جديد</span></button>';
    html += '</div>';

    html += '<div class="mtp-related">';
    html += '<a href="/makkah/tools/makkah-trip-planner/"><span class="en">Before: Makkah Trip Planner</span><span class="ar">قبل: مخطط رحلة مكة</span></a>';
    html += '<a href="/makkah/tools/madinah-trip-planner/"><span class="en">After: Madinah Trip Planner</span><span class="ar">بعد: مخطط رحلة المدينة</span></a>';
    html += '<a href="/tools/return-to-hotel"><span class="en">Return to Hotel</span><span class="ar">العودة للفندق</span></a>';
    html += '</div>';

    resultEl.innerHTML = html;
  }

  function chip(key, en, ar) {
    return '<button type="button" class="mtp-chip" data-adjust="' + key + '"><span class="en">' + en + '</span><span class="ar">' + ar + '</span></button>';
  }

  function planAsText() {
    var plan = state.plan;
    if (!plan) return '';
    var ar = S.lang() === 'ar';
    var lines = [ar ? 'خطة مكة → المدينة' : 'Makkah → Madinah Plan', txt(plan.primary.title), ''];
    lines.push(ar ? 'لماذا يناسبكم:' : 'Why this fits:');
    plan.why.forEach(function (w) { lines.push('- ' + txt(w)); });
    lines.push('', ar ? 'قبل المغادرة:' : 'Before leaving:');
    plan.before.forEach(function (w) { lines.push('- ' + txt(w)); });
    lines.push('', ar ? 'الوصول:' : 'Arrival:');
    plan.arrival.forEach(function (w) { lines.push('- ' + txt(w)); });
    lines.push('', txt(plan.disclaimer));
    lines.push('https://dotforlife.com/makkah/tools/makkah-to-madinah-planner/');
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
        track('makkah_madinah_planner_copy');
        act.classList.add('is-ok');
      });
    }
    if (a === 'share') {
      var text = planAsText();
      if (navigator.share) {
        navigator.share({ title: 'Makkah → Madinah Plan', text: text }).then(function () {
          track('makkah_madinah_planner_share');
        }).catch(function () {});
      } else {
        S.copyText(text).then(function () { track('makkah_madinah_planner_share'); });
      }
    }
    if (a === 'print') window.print();
    if (a === 'restart') {
      track('makkah_madinah_planner_restart');
      state.step = 0;
      state.plan = null;
      state.started = false;
      syncProgress();
    }
  }

  function init() {
    root = document.getElementById('makkah-madinah-planner');
    if (!root) return;
    progressEl = $('#mmp-progress', root);
    resultEl = $('#mmp-result', root);
    track('makkah_madinah_planner_view');
    $('#mmp-next', root).addEventListener('click', function () { go(1); });
    $('#mmp-back', root).addEventListener('click', function () { go(-1); });
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
