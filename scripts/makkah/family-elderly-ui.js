/**
 * Family & Elderly Journey Planner UI — Tool 05
 */
(function () {
  'use strict';

  var S = window.DFLPlannerShared;
  var E = window.DFLFamilyElderlyEngine;
  if (!S || !E) return;

  var STEPS = ['group', 'trip', 'pace', 'needs', 'result'];
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
      tool: 'family_elders_planner',
      step: STEPS[state.step]
    }, extra || {}));
  }

  function syncProgress() {
    var idx = Math.min(state.step, 3);
    var pct = Math.round((idx / 3) * 100);
    if (progressEl) {
      progressEl.setAttribute('aria-valuenow', String(idx + 1));
      var bar = progressEl.querySelector('.mtp-progress-bar');
      if (bar) bar.style.width = pct + '%';
      $all('[data-step-dot]', progressEl).forEach(function (dot, i) {
        dot.classList.toggle('is-done', i < idx);
        dot.classList.toggle('is-current', i === idx);
      });
    }
    $all('.mtp-panel', root).forEach(function (p) {
      var name = p.getAttribute('data-panel');
      var show = (state.step < 4 && name === STEPS[state.step]) ||
        (state.step === 4 && name === 'result');
      p.hidden = !show;
    });
    var back = $('#fep-back');
    var next = $('#fep-next');
    if (back) back.hidden = state.step === 0 || state.step === 4;
    if (next) {
      next.hidden = state.step === 4;
      next.textContent = state.step === 3
        ? (S.lang() === 'ar' ? 'أنشئ خطة العائلة' : 'Create family plan')
        : (S.lang() === 'ar' ? 'التالي' : 'Next');
    }
    syncConditional();
  }

  function syncConditional() {
    var composition = ($('input[name="fep-composition"]:checked') || {}).value || 'adults';
    var dest = ($('input[name="fep-destination"]:checked') || {}).value || 'makkah';
    var childBlock = $('#fep-children-block');
    var ageBlock = $('#fep-age-block');
    var bothBlock = $('#fep-both-days');
    var showKids = composition === 'children' || composition === 'both';
    if (childBlock) childBlock.hidden = !showKids;
    if (ageBlock) ageBlock.hidden = !showKids;
    if (bothBlock) bothBlock.hidden = dest !== 'both';
  }

  function readForm() {
    var interests = $all('input[name="fep-interest"]:checked').map(function (el) { return el.value; });
    state.inputs = E.normalize({
      composition: ($('input[name="fep-composition"]:checked') || {}).value,
      adults: ($('#fep-adults') || {}).value,
      children: ($('#fep-children') || {}).value,
      childAge: ($('input[name="fep-child-age"]:checked') || {}).value,
      destination: ($('input[name="fep-destination"]:checked') || {}).value,
      duration: ($('input[name="fep-duration"]:checked') || {}).value,
      daysMakkah: ($('#fep-days-makkah') || {}).value,
      daysMadinah: ($('#fep-days-madinah') || {}).value,
      walking: ($('input[name="fep-walking"]:checked') || {}).value,
      pace: ($('input[name="fep-pace"]:checked') || {}).value,
      interests: interests,
      meals: ($('input[name="fep-meals"]:checked') || {}).value,
      rest: ($('input[name="fep-rest"]:checked') || {}).value,
      keepTogether: ($('input[name="fep-together"]:checked') || {}).value
    });
  }

  function validateStep() {
    readForm();
    clearError();
    if (state.step === 0 && !$('input[name="fep-composition"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا من يسافر معكم.' : 'Please choose who is traveling.');
    }
    if (state.step === 1) {
      if (!$('input[name="fep-destination"]:checked')) {
        return fail(S.lang() === 'ar' ? 'اختاروا الوجهة.' : 'Please choose a destination.');
      }
      if (state.inputs.destination !== 'both' && !$('input[name="fep-duration"]:checked')) {
        return fail(S.lang() === 'ar' ? 'اختاروا مدة الرحلة.' : 'Please choose trip length.');
      }
      if (state.inputs.destination === 'both') {
        var m = parseInt(($('#fep-days-makkah') || {}).value, 10) || 0;
        var d = parseInt(($('#fep-days-madinah') || {}).value, 10) || 0;
        if (m < 1 || d < 1) {
          return fail(S.lang() === 'ar' ? 'حددوا يوماً واحداً على الأقل في كل مدينة.' : 'Enter at least 1 day in each city.');
        }
      }
      if (state.inputs.adults < 1) {
        return fail(S.lang() === 'ar' ? 'عدد البالغين يجب أن يكون 1 على الأقل.' : 'Adults must be at least 1.');
      }
    }
    if (state.step === 2) {
      if (!$('input[name="fep-pace"]:checked')) {
        return fail(S.lang() === 'ar' ? 'اختاروا وتيرة مناسبة.' : 'Please choose a pace.');
      }
      if (!$('input[name="fep-walking"]:checked')) {
        return fail(S.lang() === 'ar' ? 'اختاروا تفضيل المشي.' : 'Please choose walking preference.');
      }
    }
    if (state.step === 3 && !$('input[name="fep-rest"]:checked')) {
      return fail(S.lang() === 'ar' ? 'اختاروا أهمية الراحة.' : 'Please choose rest importance.');
    }
    return true;
  }

  function fail(msg) {
    var err = $('#fep-error');
    if (err) { err.hidden = false; err.textContent = msg; }
    return false;
  }
  function clearError() {
    var err = $('#fep-error');
    if (err) { err.hidden = true; err.textContent = ''; }
  }

  function go(delta) {
    if (delta > 0 && !validateStep()) return;
    if (!state.started && state.step === 0 && delta > 0) {
      state.started = true;
      track('family_elders_planner_start');
    }
    if (delta > 0 && state.step < 3) {
      track('family_elders_planner_step_complete', { step_name: STEPS[state.step] });
    }
    if (delta > 0 && state.step === 3) {
      generatePlan();
      return;
    }
    state.step = Math.max(0, Math.min(4, state.step + delta));
    syncProgress();
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function generatePlan(adjustment) {
    readForm();
    if (adjustment) {
      state.plan = E.applyAdjustment(state.plan, adjustment);
      track('family_elders_planner_adjust', { adjustment: adjustment });
    } else {
      state.plan = E.generate(state.inputs);
      var inp = state.plan.inputs;
      track('family_elders_planner_complete', {
        destination: inp.destination,
        family_type: inp.composition,
        children_bucket: inp.children > 0 ? (inp.children >= 3 ? '3plus' : String(inp.children)) : '0',
        elderly_present: inp.elderly === 'yes' ? 'yes' : 'no',
        walking_preference: inp.walking,
        pace: inp.pace,
        priority: (inp.interests || []).slice(0, 3).join(',') || 'none'
      });
    }
    renderPlan();
    state.step = 4;
    syncProgress();
    try {
      localStorage.setItem('dfl-family-elderly', JSON.stringify({
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

  function kindLabel(kind) {
    var map = {
      priority: { en: 'Priority', ar: 'أولوية' },
      optional: { en: 'Optional', ar: 'اختياري' },
      rest: { en: 'Rest', ar: 'راحة' },
      flexible: { en: 'Flexible', ar: 'مرن' }
    };
    var m = map[kind];
    if (!m) return '';
    return '<span class="mtp-kind mtp-kind-' + kind + '"><span class="en">' + m.en + '</span><span class="ar">' + m.ar + '</span></span>';
  }

  function listHtml(items) {
    return '<ul>' + (items || []).map(function (it) {
      var kind = it.kind ? kindLabel(it.kind) + ' ' : '';
      return '<li>' + kind + esc(txt(it)) + '</li>';
    }).join('') + '</ul>';
  }

  function renderPlan() {
    var plan = state.plan;
    if (!plan || !resultEl) return;
    var p = plan.profile;
    var html = '';
    html += '<div class="mtp-summary">';
    html += '<h3><span class="en">Your Family Journey Plan</span><span class="ar">خطة رحلة عائلتكم</span></h3>';
    html += '<h4 style="margin:0.5rem 0 0.35rem;font-size:0.95rem"><span class="en">Your Family Profile</span><span class="ar">ملف عائلتكم</span></h4>';
    html += '<ul class="mtp-summary-list">';
    html += '<li><strong><span class="en">Destination</span><span class="ar">الوجهة</span>:</strong> ' + esc(txt(p.destination)) + '</li>';
    html += '<li><strong><span class="en">Duration</span><span class="ar">المدة</span>:</strong> ' + esc(txt(p.duration)) + '</li>';
    html += '<li><strong><span class="en">Family</span><span class="ar">العائلة</span>:</strong> ' + esc(txt(p.family)) + '</li>';
    html += '<li><strong><span class="en">Group</span><span class="ar">المجموعة</span>:</strong> ' + esc(txt(p.group)) + '</li>';
    html += '<li><strong><span class="en">Walking</span><span class="ar">المشي</span>:</strong> ' + esc(txt(p.walking)) + '</li>';
    html += '<li><strong><span class="en">Pace</span><span class="ar">الوتيرة</span>:</strong> ' + esc(txt(p.pace)) + '</li>';
    html += '</ul></div>';

    html += '<article class="mtp-day">';
    html += '<h4><span class="en">Your Planning Principles</span><span class="ar">مبادئ تخطيطكم</span></h4>';
    html += listHtml(plan.principles);
    html += '</article>';

    html += '<h3 style="margin:1.25rem 0 0.65rem;font-size:1.1rem"><span class="en">Your Suggested Plan</span><span class="ar">خطتكم المقترحة</span></h3>';

    plan.days.forEach(function (day) {
      html += '<article class="mtp-day">';
      html += '<h4>' + esc(txt(day.title)) + '</h4>';
      if (day.linkTool03) {
        html += '<p class="mtp-hint"><span class="en">Need help planning the move?</span><span class="ar">تحتاجون مساعدة لتخطيط الانتقال؟</span></p>';
        html += '<a class="mtp-hotel-cta" href="/makkah/tools/makkah-to-madinah-planner/"><span class="en">Open Makkah → Madinah Planner</span><span class="ar">افتحوا مخطط مكة → المدينة</span></a>';
      }
      day.blocks.forEach(function (b) {
        html += '<div class="mtp-block">';
        html += '<div class="mtp-slot">' + esc(txt(b.slot)) + '</div>';
        html += listHtml(b.items);
        html += '</div>';
      });
      html += '</article>';
    });

    html += '<article class="mtp-day">';
    html += '<h4><span class="en">Family checklist</span><span class="ar">قائمة العائلة</span></h4>';
    html += listHtml(plan.checklist);
    html += '</article>';

    html += '<p class="mtp-disclaimer">' + esc(txt(plan.disclaimer)) + '</p>';

    html += '<div class="mtp-adjust" role="group" aria-label="Adjust plan">';
    html += '<p class="mtp-adjust-label"><span class="en">Adjust</span><span class="ar">عدّل</span></p>';
    html += chip('relaxed', 'Make it more relaxed', 'اجعلها أهدأ');
    html += chip('walking', 'Reduce walking', 'قلّل المشي');
    html += chip('family', 'Add more family time', 'زد وقت الأسرة');
    html += chip('rest', 'Add more rest', 'زد الراحة');
    html += chip('history', 'Add more history', 'زد التاريخ');
    html += chip('shopping', 'Add more shopping', 'زد التسوق');
    html += '</div>';

    html += '<div class="mtp-actions">';
    html += '<button type="button" class="mtp-btn mtp-btn-primary" data-act="copy"><span class="en">Copy plan</span><span class="ar">نسخ الخطة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="share"><span class="en">Share plan</span><span class="ar">مشاركة الخطة</span></button>';
    html += '<button type="button" class="mtp-btn" data-act="print"><span class="en">Print / PDF</span><span class="ar">طباعة / PDF</span></button>';
    html += '<button type="button" class="mtp-btn mtp-btn-ghost" data-act="restart"><span class="en">Start over</span><span class="ar">البداية من جديد</span></button>';
    html += '</div>';

    html += '<div class="mtp-related">';
    html += '<a href="/makkah/tools/makkah-trip-planner/"><span class="en">Makkah Trip Planner</span><span class="ar">مخطط رحلة مكة</span></a>';
    html += '<a href="/makkah/tools/madinah-trip-planner/"><span class="en">Madinah Trip Planner</span><span class="ar">مخطط رحلة المدينة</span></a>';
    html += '<a href="/makkah/tools/makkah-to-madinah-planner/"><span class="en">Makkah → Madinah</span><span class="ar">مكة → المدينة</span></a>';
    html += '<a href="/makkah/tools/hotel-decision/"><span class="en">Hotel Decision</span><span class="ar">قرار الفندق</span></a>';
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
    var kindLabel = {
      priority: ar ? 'أساسي' : 'priority',
      optional: ar ? 'اختياري' : 'optional',
      rest: ar ? 'راحة' : 'rest',
      flexible: ar ? 'مرن' : 'flexible'
    };
    var lines = [ar ? 'خطة رحلة العائلة' : 'Family Journey Plan', txt(plan.profile.family), txt(plan.profile.destination), txt(plan.profile.pace), ''];
    lines.push(ar ? 'المبادئ:' : 'Principles:');
    plan.principles.forEach(function (x) { lines.push('- ' + txt(x)); });
    lines.push('');
    plan.days.forEach(function (day) {
      lines.push(txt(day.title));
      day.blocks.forEach(function (b) {
        lines.push('  ' + txt(b.slot) + ':');
        (b.items || []).forEach(function (it) {
          var k = it.kind ? '[' + (kindLabel[it.kind] || it.kind) + '] ' : '';
          lines.push('   - ' + k + txt(it));
        });
      });
      lines.push('');
    });
    lines.push(ar ? 'القائمة:' : 'Checklist:');
    plan.checklist.forEach(function (x) { lines.push('- ' + txt(x)); });
    lines.push('', txt(plan.disclaimer));
    lines.push('https://dotforlife.com/makkah/tools/family-elderly-planner/');
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
        track('family_elders_planner_copy');
        act.classList.add('is-ok');
      });
    }
    if (a === 'share') {
      var text = planAsText();
      if (navigator.share) {
        navigator.share({ title: 'Family Journey Plan', text: text }).then(function () {
          track('family_elders_planner_share');
        }).catch(function () {});
      } else {
        S.copyText(text).then(function () { track('family_elders_planner_share'); });
      }
    }
    if (a === 'print') window.print();
    if (a === 'restart') {
      track('family_elders_planner_restart');
      state.step = 0;
      state.plan = null;
      state.started = false;
      syncProgress();
    }
  }

  function init() {
    root = document.getElementById('family-elderly-planner');
    if (!root) return;
    progressEl = $('#fep-progress', root);
    resultEl = $('#fep-result', root);
    track('family_elders_planner_view');
    $('#fep-next', root).addEventListener('click', function () { go(1); });
    $('#fep-back', root).addEventListener('click', function () { go(-1); });
    if (resultEl) resultEl.addEventListener('click', onResultClick);
    root.addEventListener('change', function () {
      readForm();
      syncConditional();
    });
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
