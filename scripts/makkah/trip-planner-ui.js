/**
 * Makkah Trip Planner UI — Tool 01
 */
(function () {
  'use strict';

  var S = window.DFLPlannerShared;
  var E = window.DFLMakkahTripEngine;
  if (!S || !E) return;

  var STEPS = ['trip', 'group', 'pace', 'stay', 'prefs', 'result'];
  var state = {
    step: 0,
    started: false,
    inputs: E.normalize({}),
    plan: null
  };

  var root, progressEl, panelsEl, navEl, resultEl;

  function $(sel, el) { return (el || document).querySelector(sel); }
  function $all(sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); }

  function track(name, extra) {
    S.track(name, Object.assign({
      tool: 'makkah_trip_planner',
      step: STEPS[state.step]
    }, extra || {}));
  }

  function syncProgress() {
    var total = STEPS.length - 1; // result not a form step in bar
    var idx = Math.min(state.step, 4);
    var pct = Math.round(((idx) / 4) * 100);
    if (progressEl) {
      progressEl.setAttribute('aria-valuenow', String(idx + 1));
      progressEl.querySelector('.mtp-progress-bar').style.width = pct + '%';
      $all('[data-step-dot]', progressEl).forEach(function (dot, i) {
        dot.classList.toggle('is-done', i < idx);
        dot.classList.toggle('is-current', i === idx);
      });
    }
    $all('.mtp-panel').forEach(function (p, i) {
      var show = (state.step < 5 && i === state.step) || (state.step === 5 && p.getAttribute('data-panel') === 'result');
      p.hidden = !show;
    });
    var back = $('#mtp-back');
    var next = $('#mtp-next');
    if (back) back.hidden = state.step === 0 || state.step === 5;
    if (next) {
      next.hidden = state.step === 5;
      next.textContent = state.step === 4
        ? (S.lang() === 'ar' ? 'أنشئ خطتي' : 'Create my plan')
        : (S.lang() === 'ar' ? 'التالي' : 'Next');
    }
  }

  function readForm() {
    var duration = ($('input[name="mtp-duration"]:checked') || {}).value || '3';
    var durationDays = ($('#mtp-duration-num') || {}).value;
    var interests = $all('input[name="mtp-interest"]:checked').map(function (el) { return el.value; });
    state.inputs = E.normalize({
      duration: duration,
      durationDays: durationDays,
      arrival: ($('input[name="mtp-arrival"]:checked') || {}).value,
      departure: ($('input[name="mtp-departure"]:checked') || {}).value,
      adults: ($('#mtp-adults') || {}).value,
      children: ($('#mtp-children') || {}).value,
      elderly: ($('input[name="mtp-elderly"]:checked') || {}).value,
      walking: ($('input[name="mtp-walking"]:checked') || {}).value,
      pace: ($('input[name="mtp-pace"]:checked') || {}).value,
      lodging: ($('input[name="mtp-lodging"]:checked') || {}).value,
      hotelName: ($('#mtp-hotel') || {}).value,
      startPref: ($('input[name="mtp-start"]:checked') || {}).value,
      interests: interests,
      seed: state.inputs.seed || 1
    });
    var hotelWrap = $('#mtp-hotel-wrap');
    if (hotelWrap) hotelWrap.hidden = state.inputs.lodging !== 'yes';
    var walkWrap = $('#mtp-walking-wrap');
    if (walkWrap) walkWrap.hidden = state.inputs.elderly !== 'yes';
  }

  function validateStep() {
    readForm();
    clearError();
    if (state.step === 0) {
      if (!$('input[name="mtp-duration"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا مدة الإقامة.' : 'Please choose trip length.');
      if (!$('input[name="mtp-arrival"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا سياق الوصول.' : 'Please choose how you arrive.');
      if (!$('input[name="mtp-departure"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا ما بعد مكة.' : 'Please choose what happens after Makkah.');
    }
    if (state.step === 1) {
      if (state.inputs.adults < 1) return fail(S.lang() === 'ar' ? 'عدد البالغين يجب أن يكون 1 على الأقل.' : 'Adults must be at least 1.');
    }
    if (state.step === 2) {
      if (!$('input[name="mtp-pace"]:checked')) return fail(S.lang() === 'ar' ? 'اختاروا وتيرة الرحلة.' : 'Please choose a pace.');
    }
    if (state.step === 3) {
      if (!$('input[name="mtp-lodging"]:checked')) return fail(S.lang() === 'ar' ? 'حدّدوا حالة الإقامة.' : 'Please set accommodation status.');
    }
    return true;
  }

  function fail(msg) {
    var err = $('#mtp-error');
    if (err) {
      err.hidden = false;
      err.textContent = msg;
    }
    return false;
  }

  function clearError() {
    var err = $('#mtp-error');
    if (err) { err.hidden = true; err.textContent = ''; }
  }

  function go(delta) {
    if (delta > 0 && !validateStep()) return;
    if (!state.started && state.step === 0 && delta > 0) {
      state.started = true;
      track('makkah_planner_start');
    }
    if (delta > 0 && state.step < 4) {
      track('makkah_planner_step_complete', { step_name: STEPS[state.step] });
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
      track('makkah_planner_regenerate', { adjustment: adjustment });
    } else {
      state.inputs.seed = (state.inputs.seed || 1) + 1;
      state.plan = E.generate(state.inputs);
      track('makkah_planner_complete', {
        duration: state.inputs.duration,
        pace: state.inputs.pace,
        group: (state.inputs.children > 0 ? 'family' : 'adults') + (state.inputs.elderly === 'yes' ? '_elder' : '')
      });
    }
    renderPlan();
    state.step = 5;
    syncProgress();
    try {
      localStorage.setItem('dfl-makkah-trip-plan', JSON.stringify({
        inputs: state.plan.inputs,
        generatedAt: state.plan.generatedAt
      }));
    } catch (e) { /* ignore */ }
  }

  function txt(pair) { return S.t(pair); }

  function renderPlan() {
    var plan = state.plan;
    if (!plan || !resultEl) return;
    var s = plan.summary;
    var html = '';
    html += '<div class="mtp-summary">';
    html += '<h3><span class="en">Your Makkah plan</span><span class="ar">خطتكم لمكة</span></h3>';
    html += '<ul class="mtp-summary-list">';
    html += '<li><strong><span class="en">Length</span><span class="ar">المدة</span>:</strong> ' + esc(txt(s.daysLabel)) + '</li>';
    html += '<li><strong><span class="en">Group</span><span class="ar">المجموعة</span>:</strong> ' + esc(txt(s.group)) + '</li>';
    html += '<li><strong><span class="en">Pace</span><span class="ar">الوتيرة</span>:</strong> ' + esc(txt(s.pace)) + '</li>';
    html += '<li><strong><span class="en">Stay</span><span class="ar">الإقامة</span>:</strong> ' + esc(txt(s.lodging)) + '</li>';
    html += '</ul></div>';

    plan.days.forEach(function (day) {
      html += '<article class="mtp-day">';
      html += '<h4>' + esc(txt(day.title)) + '</h4>';
      day.blocks.forEach(function (b) {
        html += '<div class="mtp-block">';
        html += '<div class="mtp-slot">' + esc(txt(b.slot)) + '</div><ul>';
        (b.items || []).forEach(function (it) {
          html += '<li>' + esc(txt(it)) + '</li>';
        });
        html += '</ul></div>';
      });
      html += '</article>';
    });

    html += '<p class="mtp-disclaimer">' + esc(txt(plan.disclaimer)) + '</p>';

    html += '<div class="mtp-adjust" role="group" aria-label="Adjust plan">';
    html += '<p class="mtp-adjust-label"><span class="en">Adjust</span><span class="ar">عدّل</span></p>';
    html += btnAdj('relaxed', 'Make it more relaxed', 'اجعلها أهدأ');
    html += btnAdj('active', 'Make it more active', 'اجعلها أنشط');
    html += btnAdj('family', 'Add more family time', 'زد وقت الأسرة');
    html += btnAdj('shopping', 'Add more shopping', 'زد التسوق');
    html += btnAdj('history', 'Add more historical visits', 'زد الزيارات التاريخية');
    html += '</div>';

    html += '<div class="mtp-actions">';
    html += '<button type="button" class="mtp-btn mtp-btn-primary" data-act="copy"><span class="en">Copy plan</span><span class="ar">نسخ الخطة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="share"><span class="en">Share</span><span class="ar">مشاركة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="print"><span class="en">Print / PDF</span><span class="ar">طباعة / PDF</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="regen"><span class="en">Regenerate</span><span class="ar">إعادة توليد</span></button>';
    html += '<button type="button" class="mtp-btn mtp-btn-ghost" data-act="restart"><span class="en">Start over</span><span class="ar">البداية من جديد</span></button>';
    html += '</div>';

    if (s.showHotelCta) {
      html += '<a class="mtp-hotel-cta" href="/tools/return-to-hotel"><span class="en">Need help finding your hotel again?</span><span class="ar">تحتاجون مساعدة للعودة للفندق؟</span> → <span class="en">Return to Hotel</span><span class="ar">العودة للفندق</span></a>';
    }

    resultEl.innerHTML = html;
    // re-apply lang visibility if global helper exists
    if (window.applyLanguage) {
      try { /* global.js uses internal */ } catch (e) {}
    }
  }

  function btnAdj(key, en, ar) {
    return '<button type="button" class="mtp-chip" data-adjust="' + key + '"><span class="en">' + en + '</span><span class="ar">' + ar + '</span></button>';
  }

  function esc(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  function planAsText() {
    var plan = state.plan;
    if (!plan) return '';
    var ar = S.lang() === 'ar';
    var lines = [ar ? 'خطة رحلة مكة' : 'Makkah Trip Plan', txt(plan.summary.daysLabel), txt(plan.summary.group), txt(plan.summary.pace), ''];
    plan.days.forEach(function (day) {
      lines.push(txt(day.title));
      day.blocks.forEach(function (b) {
        lines.push('  ' + txt(b.slot) + ':');
        (b.items || []).forEach(function (it) { lines.push('   - ' + txt(it)); });
      });
      lines.push('');
    });
    lines.push(txt(plan.disclaimer));
    lines.push('https://dotforlife.com/makkah/tools/makkah-trip-planner/');
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
        track('makkah_planner_copy');
        act.classList.add('is-ok');
      });
    }
    if (a === 'share') {
      var text = planAsText();
      if (navigator.share) {
        navigator.share({ title: 'Makkah Trip Plan', text: text }).then(function () {
          track('makkah_planner_share');
        }).catch(function () {});
      } else {
        S.copyText(text).then(function () { track('makkah_planner_share'); });
      }
    }
    if (a === 'print') {
      window.print();
    }
    if (a === 'regen') {
      state.inputs.seed = (state.inputs.seed || 1) + 3;
      generatePlan();
    }
    if (a === 'restart') {
      track('makkah_planner_restart');
      state.step = 0;
      state.plan = null;
      state.started = false;
      syncProgress();
    }
  }

  function bindOptionCards() {
    root.addEventListener('change', function () {
      readForm();
    });
  }

  function init() {
    root = document.getElementById('makkah-trip-planner');
    if (!root) return;
    progressEl = $('#mtp-progress', root);
    resultEl = $('#mtp-result', root);
    track('makkah_planner_view');

    $('#mtp-next', root).addEventListener('click', function () { go(1); });
    $('#mtp-back', root).addEventListener('click', function () { go(-1); });
    if (resultEl) resultEl.addEventListener('click', onResultClick);
    bindOptionCards();
    readForm();
    syncProgress();
    if (S.onLangChange) {
      S.onLangChange(function () {
        if (state.plan) renderPlan();
      });
    }

    // Ensure dflTrack exists
    if (!window.dflTrack && window.gtag) {
      window.dflTrack = function (event, params) {
        window.gtag('event', event, Object.assign({
          page_path: location.pathname,
          language: document.documentElement.getAttribute('data-lang') || 'en'
        }, params || {}));
      };
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
