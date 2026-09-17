/**
 * Makkah Hotel Decision Tool — deterministic engine (Tool 04).
 * Decision framework only. No invented prices, distances, or hotel facts.
 * Mode B compare uses user-declared characteristics only.
 */
(function (global) {
  'use strict';

  function bi(en, ar) { return { en: en, ar: ar }; }
  function item(en, ar) { return bi(en, ar); }

  var DURATION = {
    'lt1': 1, '1-2': 2, '3': 3, '4-5': 5, '6-7': 7, 'gt7': 8
  };

  function normalize(raw) {
    return {
      duration: raw.duration || '3',
      adults: Math.max(1, parseInt(raw.adults, 10) || 1),
      children: Math.max(0, parseInt(raw.children, 10) || 0),
      elderly: raw.elderly === 'yes' ? 'yes' : 'no',
      walking: raw.walking || 'moderate',
      pace: raw.pace || 'balanced',
      priority: raw.priority || 'convenience',
      budget: raw.budget || 'mid',
      roomNeed: raw.roomNeed || 'basic',
      locationPref: raw.locationPref || 'convenient'
    };
  }

  function dayCount(inputs) {
    return DURATION[inputs.duration] || 3;
  }

  function scores(inputs) {
    var s = {
      convenience: 3,
      family: 2,
      value: 3,
      comfort: 3,
      proximity: 2,
      balance: 3
    };
    var days = dayCount(inputs);

    if (inputs.priority === 'convenience' || inputs.priority === 'movement') s.convenience += 4;
    if (inputs.priority === 'cost') s.value += 4;
    if (inputs.priority === 'family') s.family += 4;
    if (inputs.priority === 'comfort') s.comfort += 4;
    if (inputs.priority === 'proximity') s.proximity += 4;
    if (inputs.priority === 'room') { s.family += 2; s.comfort += 2; }
    if (inputs.priority === 'balanced') s.balance += 4;

    if (inputs.walking === 'low') { s.convenience += 3; s.proximity += 2; s.value -= 1; }
    if (inputs.walking === 'flexible') { s.value += 1; s.balance += 1; }

    if ((inputs.children || 0) > 0) { s.family += 3; s.convenience += 1; }
    if ((inputs.children || 0) >= 2) s.family += 1;
    if (inputs.elderly === 'yes') { s.convenience += 3; s.proximity += 1; s.comfort += 1; }

    if (inputs.pace === 'relaxed') { s.convenience += 2; s.comfort += 1; }
    if (inputs.pace === 'active') { s.value += 1; s.balance += 1; }

    if (days <= 2) { s.convenience += 2; s.proximity += 1; }
    if (days >= 6) { s.comfort += 2; s.value += 1; s.balance += 1; }

    if (inputs.budget === 'value') s.value += 3;
    if (inputs.budget === 'comfort') s.comfort += 3;
    if (inputs.budget === 'mid') s.balance += 2;

    if (inputs.roomNeed === 'family') { s.family += 2; s.comfort += 1; }
    if (inputs.roomNeed === 'critical') { s.family += 3; s.comfort += 2; }

    if (inputs.locationPref === 'convenient') s.convenience += 2;
    if (inputs.locationPref === 'farther') { s.value += 2; s.proximity -= 1; }
    if (inputs.locationPref === 'balanced') s.balance += 2;

    // Distance must not dominate: cap proximity relative to convenience/value
    if (s.proximity > s.convenience + 2 && inputs.priority !== 'proximity') {
      s.proximity = s.convenience + 1;
    }
    return s;
  }

  function pickCategory(inputs) {
    var sc = scores(inputs);
    var map = {
      convenience: {
        id: 'convenience',
        title: bi('Convenience-focused stay', 'إقامة تركّز على الراحة العملية'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      },
      family: {
        id: 'family',
        title: bi('Family-oriented stay', 'إقامة موجّهة للأسرة'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      },
      value: {
        id: 'value',
        title: bi('Value-oriented stay', 'إقامة موجّهة للقيمة'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      },
      comfort: {
        id: 'comfort',
        title: bi('Comfort-oriented stay', 'إقامة موجّهة للراحة'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      },
      proximity: {
        id: 'proximity',
        title: bi('Access-priority stay', 'إقامة بأولوية سهولة الوصول'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      },
      balance: {
        id: 'balance',
        title: bi('Balanced stay', 'إقامة متوازنة'),
        fit: bi('Strong fit for your stated priorities', 'ملاءمة قوية لأولوياتكم المعلنة')
      }
    };
    var ranked = Object.keys(sc).sort(function (a, b) {
      return sc[b] - sc[a] || a.localeCompare(b);
    });
    return { primary: map[ranked[0]], secondary: map[ranked[1]], scores: sc };
  }

  function prioritizeList(inputs, categoryId) {
    var list = [];
    if (categoryId === 'convenience' || inputs.walking === 'low' || inputs.elderly === 'yes') {
      list.push(item('Easy daily access and a simple return route to your room', 'وصول يومي سهل ومسار عودة بسيط لغرفتكم'));
      list.push(item('Lower movement complexity between room, meals, and prayer times', 'تعقيد أقل في التنقّل بين الغرفة والوجبات وأوقات الصلاة'));
    }
    if (categoryId === 'family' || (inputs.children || 0) > 0 || inputs.roomNeed !== 'basic') {
      list.push(item('Suitable room arrangement for your group size', 'ترتيب غرف يناسب حجم مجموعتكم'));
      list.push(item('Practical family movement — fewer tight transfers each day', 'تنقّل أسري عملي — وصلات ضيقة أقل كل يوم'));
    }
    if (categoryId === 'value' || inputs.budget === 'value') {
      list.push(item('Balance stay value against daily transport friction', 'وازنوا قيمة الإقامة مع احتكاك التنقّل اليومي'));
    }
    if (categoryId === 'comfort' || dayCount(inputs) >= 6 || inputs.pace === 'relaxed') {
      list.push(item('Comfort for a longer or calmer stay — room rest matters', 'راحة لإقامة أطول أو أهدأ — راحة الغرفة مهمة'));
    }
    if (categoryId === 'proximity' || inputs.priority === 'proximity') {
      list.push(item('Practical access to key areas — verify current routes before booking', 'وصول عملي للمناطق الرئيسية — تحققوا من المسارات الحالية قبل الحجز'));
    }
    if (categoryId === 'balance' || !list.length) {
      list.push(item('A balanced location/value tradeoff that fits your pace', 'مقايضة متوازنة بين الموقع والقيمة تناسب وتيرتكم'));
    }
    // Always keep at least two actionable priorities
    list.push(item('Verify current rates, occupancy, and access with the property before you pay', 'تحققوا من الأسعار والإشغال والوصول الحالية مع المنشأة قبل الدفع'));
    list.push(item('Treat distance as one factor — not the only hotel decision', 'عاملوا المسافة كعامل واحد — لا كقرار الفندق الوحيد'));
    // Deduplicate by English text
    var seen = {};
    return list.filter(function (x) {
      if (seen[x.en]) return false;
      seen[x.en] = true;
      return true;
    }).slice(0, 4);
  }

  function why(inputs, categoryId) {
    var reasons = [];
    var days = dayCount(inputs);
    if (days <= 2) {
      reasons.push(item(
        'A short stay usually raises the cost of inconvenient daily movement — convenience often outweighs maximizing savings.',
        'الإقامة القصيرة ترفع عادة تكلفة التنقّل اليومي غير المريح — الراحة العملية غالباً أهم من تعظيم التوفير.'
      ));
    }
    if (days >= 6) {
      reasons.push(item(
        'A longer stay makes room comfort and cancellation flexibility more important to verify before you book.',
        'الإقامة الأطول تجعل راحة الغرفة ومرونة الإلغاء أهم للتحقق قبل الحجز.'
      ));
    }
    if ((inputs.children || 0) > 0) {
      reasons.push(item(
        'With children, room occupancy and simple daily movement often matter more than a single distance claim.',
        'مع الأطفال، إشغال الغرفة والتنقّل اليومي البسيط غالباً أهم من رقم مسافة واحد.'
      ));
    }
    if (inputs.elderly === 'yes' || inputs.walking === 'low') {
      reasons.push(item(
        'Lower walking preference points toward easier access and fewer complicated returns to the room.',
        'تفضيل المشي الأقل يدفع نحو وصول أسهل وعودات أقل تعقيداً للغرفة.'
      ));
    }
    if (inputs.priority === 'cost' || inputs.budget === 'value') {
      reasons.push(item(
        'Value orientation is valid — still check transport friction so a cheaper room does not create costly daily hassle.',
        'التوجّه للقيمة مشروع — تحققوا مع ذلك من احتكاك النقل حتى لا تخلق غرفة أرخص إزعاجاً يومياً مكلفاً.'
      ));
    }
    if (inputs.priority === 'proximity') {
      reasons.push(item(
        'You prioritized access — still verify current hotel access and routes; closer is not automatically better for every group.',
        'أولويتم الوصول — تحققوا مع ذلك من مسارات الوصول الحالية؛ الأقرب ليس أفضل تلقائياً لكل مجموعة.'
      ));
    }
    if (inputs.roomNeed === 'critical' || inputs.roomNeed === 'family') {
      reasons.push(item(
        'Room arrangement is important for you — confirm occupancy and configuration with the property before paying.',
        'ترتيب الغرف مهم لكم — أكّدوا الإشغال والتكوين مع المنشأة قبل الدفع.'
      ));
    }
    var fillers = [
      item(
        'This profile is a decision framework for your situation — not a universal hotel ranking or live inventory.',
        'هذا الملف إطار قرار لوضعكم — وليس ترتيباً عاماً للفنادق أو مخزوناً حياً.'
      ),
      item(
        'Always recheck rates, availability, and policies on the booking platform you trust before you commit.',
        'أعيدوا دائماً التحقق من الأسعار والتوفر والسياسات على منصة الحجز التي تثقون بها قبل الالتزام.'
      ),
      item(
        'Closer is not automatically better — weigh daily movement, room fit, and your group’s energy.',
        'الأقرب ليس أفضل تلقائياً — وازنوا التنقّل اليومي وملاءمة الغرفة وطاقة مجموعتكم.'
      )
    ];
    var fi = 0;
    while (reasons.length < 3 && fi < fillers.length) {
      reasons.push(fillers[fi++]);
    }
    return reasons.slice(0, 4);
  }

  function checklist(inputs) {
    var list = [
      item('Current rate and total stay cost (not a screenshot from another date)', 'السعر الحالي وإجمالي تكلفة الإقامة (لا لقطة من تاريخ آخر)'),
      item('Current availability for your exact dates', 'التوفر الحالي لتواريخكم الدقيقة'),
      item('Cancellation and change rules', 'قواعد الإلغاء والتعديل'),
      item('Exact room occupancy vs your group size', 'إشغال الغرفة الدقيق مقابل حجم مجموعتكم')
    ];
    if ((inputs.children || 0) > 0 || inputs.roomNeed !== 'basic') {
      list.push(item('Family / connecting room options — ask the property, do not assume', 'خيارات غرف أسرية/متصلة — اسألوا المنشأة ولا تفترضوا'));
    }
    if (inputs.elderly === 'yes' || inputs.walking === 'low') {
      list.push(item('Practical access notes for your group (verify with property; do not invent distances)', 'ملاحظات وصول عملية لمجموعتكم (تحققوا من المنشأة؛ لا تخترعوا مسافات)'));
    }
    if (dayCount(inputs) >= 6) {
      list.push(item('Comfort for a longer stay and flexible cancellation if plans shift', 'الراحة لإقامة أطول ومرونة الإلغاء إن تغيّرت الخطط'));
    }
    if (inputs.locationPref === 'farther' || inputs.budget === 'value') {
      list.push(item('Daily transport plan if you trade distance for other advantages', 'خطة تنقّل يومية إن قايضتم المسافة بمزايا أخرى'));
    }
    list.push(item('Check-in / check-out timing and any current property policies', 'توقيت الدخول/الخروج وأي سياسات حالية للمنشأة'));
    return list;
  }

  function profileLabels(inputs) {
    return {
      duration: bi(
        ({ lt1: 'Less than 1 day', '1-2': '1–2 days', '3': '3 days', '4-5': '4–5 days', '6-7': '6–7 days', gt7: 'More than 7 days' })[inputs.duration] || '3 days',
        ({ lt1: 'أقل من يوم', '1-2': '١–٢ يوم', '3': '٣ أيام', '4-5': '٤–٥ أيام', '6-7': '٦–٧ أيام', gt7: 'أكثر من ٧ أيام' })[inputs.duration] || '٣ أيام'
      ),
      group: bi(
        (inputs.adults || 1) + ' adult(s)' + ((inputs.children || 0) > 0 ? ', ' + inputs.children + ' child(ren)' : '') + (inputs.elderly === 'yes' ? ', older traveler(s)' : ''),
        (inputs.adults || 1) + ' بالغ' + ((inputs.children || 0) > 0 ? '، ' + inputs.children + ' طفل' : '') + (inputs.elderly === 'yes' ? '، كبار سن' : '')
      ),
      walking: bi(
        inputs.walking === 'low' ? 'Prefer less walking' : inputs.walking === 'flexible' ? 'Walking not a major concern' : 'Moderate walking is fine',
        inputs.walking === 'low' ? 'يفضّلون مشياً أقل' : inputs.walking === 'flexible' ? 'المشي ليس هماً كبيراً' : 'مشي متوسط مناسب'
      ),
      priority: bi(
        ({
          convenience: 'Easy access / convenience', cost: 'Lower overall cost', family: 'Family practicality',
          comfort: 'Comfort', proximity: 'Staying close to key areas', room: 'Room for the group',
          movement: 'Less complicated daily movement', balanced: 'Flexible / balanced'
        })[inputs.priority] || 'Convenience',
        ({
          convenience: 'سهولة الوصول / الراحة العملية', cost: 'تكلفة إجمالية أقل', family: 'عملية أسرية',
          comfort: 'الراحة', proximity: 'القرب من المناطق الرئيسية', room: 'غرفة للمجموعة',
          movement: 'تنقّل يومي أقل تعقيداً', balanced: 'مرن / متوازن'
        })[inputs.priority] || 'الراحة العملية'
      ),
      budget: bi(
        ({ value: 'Value-oriented', mid: 'Mid-range balance', comfort: 'Comfort-oriented', flexible: 'Flexible' })[inputs.budget] || 'Mid-range',
        ({ value: 'موجّه للقيمة', mid: 'توازن متوسط', comfort: 'موجّه للراحة', flexible: 'مرن' })[inputs.budget] || 'متوسط'
      )
    };
  }

  /**
   * Manual compare: hotels = [{ name, access: 'high'|'mid'|'low'|'unknown', family: ..., value: ..., notes }]
   * Fit labels only — no fabricated quality scores.
   */
  function compareHotels(inputs, hotels) {
    var cat = pickCategory(inputs);
    var primaryId = cat.primary.id;
    var weightKeys = {
      convenience: 'access',
      proximity: 'access',
      family: 'family',
      comfort: 'comfort',
      value: 'value',
      balance: 'access'
    };
    var key = weightKeys[primaryId] || 'access';
    var rankVal = { high: 3, mid: 2, low: 1, unknown: 0 };

    return (hotels || []).filter(function (h) { return h && (h.name || '').trim(); }).slice(0, 3).map(function (h) {
      var access = h.access || 'unknown';
      var family = h.family || 'unknown';
      var value = h.value || 'unknown';
      var comfort = h.comfort || 'unknown';
      var focus = h[key] || 'unknown';
      var fitLabel;
      if (focus === 'unknown') {
        fitLabel = bi('Information not available — check before booking', 'المعلومة غير متاحة — تحققوا قبل الحجز');
      } else if (rankVal[focus] >= 3) {
        fitLabel = bi('Better fit for your priorities (based on what you entered)', 'ملاءمة أفضل لأولوياتكم (حسب ما أدخلتموه)');
      } else if (rankVal[focus] === 2) {
        fitLabel = bi('Partial fit for your priorities (based on what you entered)', 'ملاءمة جزئية لأولوياتكم (حسب ما أدخلتموه)');
      } else {
        fitLabel = bi('Weaker fit for your priorities (based on what you entered)', 'ملاءمة أضعف لأولوياتكم (حسب ما أدخلتموه)');
      }
      return {
        name: String(h.name || '').trim().slice(0, 80),
        access: access,
        family: family,
        value: value,
        comfort: comfort,
        fit: fitLabel,
        missing: [access, family, value, comfort].indexOf('unknown') !== -1
      };
    }).sort(function (a, b) {
      // Sort by declared focus fit, unknown last — not a quality ranking
      var av = rankVal[(a[key])] || 0;
      var bv = rankVal[(b[key])] || 0;
      return bv - av;
    });
  }

  function generate(raw, hotels) {
    var inputs = normalize(raw);
    var cat = pickCategory(inputs);
    var out = {
      version: 1,
      tool: 'hotel-decision',
      generatedAt: new Date().toISOString().slice(0, 10),
      inputs: inputs,
      labels: profileLabels(inputs),
      category: cat.primary,
      alternativeCategory: cat.secondary,
      prioritize: prioritizeList(inputs, cat.primary.id),
      why: why(inputs, cat.primary.id),
      checklist: checklist(inputs),
      compare: null,
      disclaimer: bi(
        'This is a hotel decision assistant, not a booking engine or universal ranking. We do not invent prices, distances, availability, or hotel features. Verify all details with the property and your booking platform before you pay.',
        'هذه أداة قرار فندقي، وليست محرك حجز أو ترتيباً عاماً. لا نخترع أسعاراً أو مسافات أو توفراً أو ميزات فندق. تحققوا من كل التفاصيل مع المنشأة ومنصة الحجز قبل الدفع.'
      )
    };
    if (hotels && hotels.length) {
      out.compare = compareHotels(inputs, hotels);
    }
    return out;
  }

  function applyAdjustment(plan, adjustment) {
    var inputs = Object.assign({}, plan.inputs);
    if (adjustment === 'convenience') { inputs.priority = 'convenience'; inputs.walking = 'low'; }
    if (adjustment === 'family') { inputs.priority = 'family'; if (inputs.children < 1) inputs.children = 1; inputs.roomNeed = 'family'; }
    if (adjustment === 'value') { inputs.priority = 'cost'; inputs.budget = 'value'; }
    if (adjustment === 'comfort') { inputs.priority = 'comfort'; inputs.budget = 'comfort'; inputs.pace = 'relaxed'; }
    if (adjustment === 'balance') { inputs.priority = 'balanced'; inputs.budget = 'mid'; inputs.locationPref = 'balanced'; }
    return generate(inputs, plan._hotels || null);
  }

  global.DFLHotelDecisionEngine = {
    generate: generate,
    applyAdjustment: applyAdjustment,
    normalize: normalize,
    compareHotels: compareHotels,
    scores: scores
  };
})(window);
