/**
 * Makkah Trip Planner — deterministic planning engine (Tool 01).
 * Pure functions. No network. No religious rulings. No invented distances/hours.
 */
(function (global) {
  'use strict';

  var DURATION_DAYS = {
    'lt1': 1,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6-7': 7,
    'gt7': 8
  };

  function bi(en, ar) { return { en: en, ar: ar }; }

  function dayCount(inputs) {
    if (inputs.durationDays != null && inputs.durationDays !== '') {
      return Math.max(1, Math.min(10, parseInt(inputs.durationDays, 10) || 1));
    }
    return DURATION_DAYS[inputs.duration] || 3;
  }

  function restWeight(inputs) {
    var w = 0;
    if (inputs.pace === 'relaxed') w += 2;
    if (inputs.pace === 'active') w -= 1;
    if ((inputs.children || 0) > 0) w += 2;
    if (inputs.elderly === 'yes') w += 2;
    if (inputs.walking === 'low') w += 2;
    if (inputs.walking === 'flexible') w -= 0;
    return w;
  }

  function hasInterest(inputs, key) {
    return (inputs.interests || []).indexOf(key) !== -1;
  }

  function block(slotEn, slotAr, items) {
    return { slot: bi(slotEn, slotAr), items: items };
  }

  function item(en, ar) { return bi(en, ar); }

  function worshipItems(inputs, intensity) {
    var items = [];
    if (hasInterest(inputs, 'worship') || intensity !== 'light') {
      items.push(item(
        'Time near the Haram for prayer — keep it flexible and unhurried.',
        'وقت قرب الحرم للصلاة — اجعلوه مرناً بلا استعجال.'
      ));
    }
    if (intensity === 'full' && hasInterest(inputs, 'worship')) {
      items.push(item(
        'Leave buffer before and after worship for rest and water.',
        'اتركوا هامشاً قبل العبادة وبعدها للراحة والماء.'
      ));
    }
    return items;
  }

  function mealItems(inputs) {
    if (hasInterest(inputs, 'food')) {
      return [item(
        'Choose one calm meal near your base — verify hours locally; do not rush between distant spots.',
        'اختاروا وجبة هادئة قرب مقرّكم — تحققوا من المواعيد محلياً؛ لا تتعجلوا بين أماكن متباعدة.'
      )];
    }
    return [item(
      'Simple meal break. Keep water available, especially with children or elders.',
      'استراحة وجبة بسيطة. أبقوا الماء متاحاً خصوصاً مع الأطفال أو كبار السن.'
    )];
  }

  function historyItems(inputs, heavy) {
    if (!hasInterest(inputs, 'history') && !hasInterest(inputs, 'culture')) return [];
    if (heavy) {
      return [item(
        'One historical or cultural visit only — confirm opening status before you go.',
        'زيارة تاريخية أو ثقافية واحدة فقط — أكّدوا حالة الفتح قبل الذهاب.'
      )];
    }
    return [item(
      'Optional short cultural stop if energy allows. Skip if the group is tired.',
      'محطة ثقافية قصيرة اختيارية إن سمحت الطاقة. تجاوزوها إن تعبت المجموعة.'
    )];
  }

  function shopItems(inputs, level) {
    if (!hasInterest(inputs, 'shopping') && level !== 'force') return [];
    if (level === 'light') {
      return [item(
        'Light shopping window near your area — set a time limit so it does not eat the day.',
        'نافذة تسوق خفيفة قرب منطقتكم — حدّدوا وقتاً حتى لا يبتلع اليوم.'
      )];
    }
    return [item(
      'Dedicated shopping block. Cluster purchases; avoid multiple long trips across the city.',
      'فترة تسوق مخصّصة. جمّعوا المشتريات؛ تجنبوا رحلات طويلة متعددة عبر المدينة.'
    )];
  }

  function familyItems(inputs) {
    if (!hasInterest(inputs, 'family') && !(inputs.children > 0)) return [];
    return [item(
      'Family reset: short outdoor air or quiet room time. Let children recover before the next move.',
      'إعادة ضبط أسرية: هواء قصير أو هدوء في الغرفة. دعوا الأطفال يستعيدون طاقتهم قبل أي تنقّل.'
    )];
  }

  function restItems(inputs, strength) {
    var lines = [];
    if (strength === 'strong' || restWeight(inputs) >= 3) {
      lines.push(item(
        'Protected rest in the room. Reduce walking; hydrate; do not fill every hour.',
        'راحة محمية في الغرفة. قلّلوا المشي؛ اشربوا ماء؛ لا تملأوا كل ساعة.'
      ));
    } else {
      lines.push(item(
        'Midday pause — even 45–60 minutes protects the evening.',
        'وقفة منتصف النهار — حتى 45–60 دقيقة تحمي المساء.'
      ));
    }
    if (inputs.elderly === 'yes' || inputs.walking === 'low') {
      lines.push(item(
        'Prefer short walking segments. Agree a meeting point before leaving the room.',
        'فضّلوا مسافات مشي قصيرة. اتفقوا على نقطة لقاء قبل مغادرة الغرفة.'
      ));
    }
    return lines;
  }

  function arrivalBlocks(inputs) {
    var morning = [];
    morning.push(item(
      'Arrive and settle: check-in, water, wash, short orientation around your accommodation.',
      'الوصول والاستقرار: تسجيل الدخول، ماء، اغتسال، تعرّف قصير حول مقر الإقامة.'
    ));
    if (inputs.arrival === 'airport' || inputs.arrival === 'madinah' || inputs.arrival === 'city') {
      morning.push(item(
        'Travel day fatigue is real — keep the first hours light.',
        'إرهاق يوم السفر حقيقي — اجعلوا الساعات الأولى خفيفة.'
      ));
    }
    var midday = restItems(inputs, 'strong');
    var afternoon = [];
    if (inputs.pace === 'active' && restWeight(inputs) < 3) {
      afternoon = afternoon.concat(worshipItems(inputs, 'light'));
    } else {
      afternoon.push(item(
        'Optional short visit near your base only if everyone feels steady.',
        'زيارة قصيرة اختيارية قرب المقر فقط إن كان الجميع ثابتاً.'
      ));
    }
    var evening = mealItems(inputs).concat([
      item(
        'Early night if possible. Save demanding plans for a fuller day.',
        'نوم مبكر إن أمكن. ادّخروا الخطط الثقيلة ليوم أوفر طاقة.'
      )
    ]);
    return [
      block('Morning', 'الصباح', morning),
      block('Midday', 'الظهيرة', midday),
      block('Afternoon', 'العصر', afternoon),
      block('Evening', 'المساء', evening)
    ];
  }

  function coreBlocks(inputs, dayIndex, total) {
    var active = inputs.pace === 'active';
    var relaxed = inputs.pace === 'relaxed' || restWeight(inputs) >= 4;
    var morning = [];
    if (inputs.startPref === 'late') {
      morning.push(item(
        'Later start — no early pressure. Begin when the group is ready.',
        'بداية متأخرة — بلا ضغط صباحي. ابدأوا عندما تكون المجموعة جاهزة.'
      ));
    } else {
      morning.push(item(
        'Steady morning start with water and a light breakfast.',
        'بداية صباح ثابتة مع ماء وإفطار خفيف.'
      ));
    }
    morning = morning.concat(worshipItems(inputs, relaxed ? 'light' : 'full'));

    var midday = restItems(inputs, relaxed ? 'strong' : 'normal').concat(mealItems(inputs));

    var afternoon = [];
    if (hasInterest(inputs, 'history') || hasInterest(inputs, 'culture')) {
      afternoon = afternoon.concat(historyItems(inputs, active && dayIndex % 2 === 0));
    } else if (hasInterest(inputs, 'family') || (inputs.children || 0) > 0) {
      afternoon = afternoon.concat(familyItems(inputs));
    } else if (active) {
      afternoon.push(item(
        'One focused outing — then return to base. Avoid stacking distant stops.',
        'خرجة مركّزة واحدة — ثم العودة للمقر. تجنبوا تكديس محطات متباعدة.'
      ));
    } else {
      afternoon.push(item(
        'Flexible afternoon: rest, short walk nearby, or quiet time.',
        'عصر مرن: راحة، مشي قصير بالقرب، أو وقت هادئ.'
      ));
    }

    var evening = [];
    if (hasInterest(inputs, 'shopping') && (active || dayIndex >= Math.ceil(total / 2))) {
      evening = evening.concat(shopItems(inputs, relaxed ? 'light' : 'normal'));
    }
    evening = evening.concat(mealItems(inputs));
    if (!relaxed) {
      evening = evening.concat(worshipItems(inputs, 'light'));
    }
    evening.push(item(
      'End with a wind-down in the room. Confirm tomorrow’s first step in one sentence.',
      'اختموا بتهدئة في الغرفة. أكّدوا خطوة الغد الأولى بجملة واحدة.'
    ));

    return [
      block('Morning', 'الصباح', morning),
      block('Midday', 'الظهيرة', midday),
      block('Afternoon', 'العصر', afternoon),
      block('Evening', 'المساء', evening)
    ];
  }

  function departureBlocks(inputs) {
    var morning = [
      item(
        'Flexible morning only. Finish packing early; keep documents ready.',
        'صباح مرن فقط. أنهوا الحزم مبكراً؛ أبقوا الوثائق جاهزة.'
      )
    ];
    if (inputs.departure === 'madinah') {
      morning.push(item(
        'You noted Madinah next — protect transfer buffer; do not schedule a heavy visit this morning.',
        'أشرتم أن المدينة هي التالية — احموا هامش الانتقال؛ لا تجدولوا زيارة ثقيلة هذا الصباح.'
      ));
    } else if (inputs.departure === 'airport' || inputs.departure === 'home') {
      morning.push(item(
        'Airport / travel day — leave generous buffer. Verify transport timing with your provider.',
        'يوم مطار/سفر — اتركوا هامشاً واسعاً. أكّدوا توقيت النقل مع مزوّدكم.'
      ));
    }
    var midday = [
      item(
        'Final checks: bags, chargers, medications, hotel checkout timing.',
        'فحوصات أخيرة: حقائب، شواحن، أدوية، موعد المغادرة من الفندق.'
      )
    ];
    var afternoon = [
      item(
        'Departure window. Skip new attractions if time is tight.',
        'نافذة المغادرة. تجاوزوا معالم جديدة إن ضاق الوقت.'
      )
    ];
    var evening = [
      item(
        'If you remain overnight, keep the evening calm and local only.',
        'إن بقيتم للمبيت، اجعلوا المساء هادئاً ومحلياً فقط.'
      )
    ];
    return [
      block('Morning', 'الصباح', morning),
      block('Midday', 'الظهيرة', midday),
      block('Afternoon', 'العصر', afternoon),
      block('Evening', 'المساء', evening)
    ];
  }

  function dayTitle(kind, index, total, inputs) {
    if (kind === 'arrival') {
      return bi('Day ' + index + ' — Arrival & settling in', 'اليوم ' + index + ' — الوصول والاستقرار');
    }
    if (kind === 'departure') {
      return bi('Day ' + index + ' — Prepare to leave', 'اليوم ' + index + ' — الاستعداد للمغادرة');
    }
    if (total <= 2) {
      return bi('Day ' + index + ' — Main day', 'اليوم ' + index + ' — اليوم الأساسي');
    }
    if (index === Math.ceil(total / 2)) {
      return bi('Day ' + index + ' — Explore & flexible time', 'اليوم ' + index + ' — استكشاف ووقت مرن');
    }
    return bi('Day ' + index + ' — Steady day', 'اليوم ' + index + ' — يوم متوازن');
  }

  function buildDays(inputs) {
    var n = dayCount(inputs);
    var days = [];
    var i;
    for (i = 1; i <= n; i++) {
      var kind = 'core';
      if (n === 1) {
        kind = (inputs.arrival === 'already') ? 'core' : 'arrival';
        if (inputs.departure === 'airport' || inputs.departure === 'home' || inputs.departure === 'madinah') {
          // single day: merge arrival+departure lightness
          days.push({
            index: i,
            kind: 'single',
            title: bi('Your day in Makkah — keep it light', 'يومكم في مكة — أبقوه خفيفاً'),
            blocks: (function () {
              var a = arrivalBlocks(inputs);
              var d = departureBlocks(inputs);
              return [
                a[0],
                block('Midday', 'الظهيرة', restItems(inputs, 'strong').concat(mealItems(inputs))),
                block('Afternoon', 'العصر', worshipItems(inputs, 'light').concat(familyItems(inputs))),
                d[2]
              ];
            })()
          });
          return days;
        }
      } else {
        if (i === 1 && inputs.arrival !== 'already') kind = 'arrival';
        if (i === n) kind = 'departure';
      }
      var blocks;
      if (kind === 'arrival') blocks = arrivalBlocks(inputs);
      else if (kind === 'departure') blocks = departureBlocks(inputs);
      else blocks = coreBlocks(inputs, i, n);

      // Active + long stay: inject shopping/history on alternate core days
      if (kind === 'core' && inputs.pace === 'active' && hasInterest(inputs, 'shopping') && i === Math.max(2, n - 2)) {
        blocks[3].items = shopItems(inputs, 'normal').concat(blocks[3].items);
      }

      days.push({
        index: i,
        kind: kind,
        title: dayTitle(kind, i, n, inputs),
        blocks: blocks
      });
    }
    return days;
  }

  function summary(inputs) {
    var n = dayCount(inputs);
    return {
      days: n,
      daysLabel: bi(n + (n === 1 ? ' day' : ' days'), n + (n === 1 ? ' يوم' : ' أيام')),
      group: bi(
        (inputs.adults || 1) + ' adult(s)' + ((inputs.children || 0) > 0 ? ', ' + inputs.children + ' child(ren)' : '') + (inputs.elderly === 'yes' ? ', with older traveler(s)' : ''),
        (inputs.adults || 1) + ' بالغ' + ((inputs.children || 0) > 0 ? '، ' + inputs.children + ' طفل' : '') + (inputs.elderly === 'yes' ? '، مع كبار سن' : '')
      ),
      pace: bi(
        inputs.pace === 'relaxed' ? 'Relaxed' : inputs.pace === 'active' ? 'Active' : 'Balanced',
        inputs.pace === 'relaxed' ? 'هادئ' : inputs.pace === 'active' ? 'نشيط' : 'متوازن'
      ),
      lodging: bi(
        inputs.lodging === 'yes' ? 'Hotel booked' + (inputs.hotelName ? ' (' + inputs.hotelName + ')' : '') :
          inputs.lodging === 'family' ? 'Staying with family/friends' : 'Accommodation not set yet',
        inputs.lodging === 'yes' ? 'فندق محجوز' + (inputs.hotelName ? ' (' + inputs.hotelName + ')' : '') :
          inputs.lodging === 'family' ? 'إقامة مع أهل/أصدقاء' : 'الإقامة غير محددة بعد'
      ),
      interests: (inputs.interests || []).slice(),
      showHotelCta: true
    };
  }

  function normalize(raw) {
    var interests = Array.isArray(raw.interests) ? raw.interests.slice() : [];
    if (interests.indexOf('flexible') !== -1 && interests.length > 1) {
      interests = interests.filter(function (x) { return x !== 'flexible'; });
    }
    return {
      duration: raw.duration || '3',
      durationDays: raw.durationDays,
      arrival: raw.arrival || 'other',
      departure: raw.departure || 'undecided',
      adults: Math.max(1, parseInt(raw.adults, 10) || 1),
      children: Math.max(0, parseInt(raw.children, 10) || 0),
      elderly: raw.elderly === 'yes' ? 'yes' : 'no',
      walking: raw.walking || 'moderate',
      pace: raw.pace || 'balanced',
      interests: interests,
      lodging: raw.lodging || 'no',
      hotelName: (raw.hotelName || '').toString().trim().slice(0, 80),
      startPref: raw.startPref || 'flexible',
      seed: parseInt(raw.seed, 10) || 1
    };
  }

  function generate(raw) {
    var inputs = normalize(raw);
    // seed slightly varies optional wording order without inventing facts
    var days = buildDays(inputs);
    if (inputs.seed % 2 === 0 && days.length > 2) {
      // swap a soft tip on a middle core day for variety on regenerate
      var mid = days[Math.floor(days.length / 2)];
      if (mid && mid.kind === 'core' && mid.blocks[2]) {
        mid.blocks[2].items = mid.blocks[2].items.concat([
          item(
            'Alternate focus: protect one empty hour with no errands.',
            'تركيز بديل: احموا ساعة فارغة بلا مشاوير.'
          )
        ]);
      }
    }
    return {
      version: 1,
      generatedAt: new Date().toISOString().slice(0, 10),
      inputs: inputs,
      summary: summary(inputs),
      days: days,
      disclaimer: bi(
        'This is a practical planning assistant, not religious or official guidance. Verify live details locally. For religious questions, follow official Saudi guidance or consult a qualified scholar. Bookings remain on Nusuk and licensed providers.',
        'هذه أداة تخطيط عملية، وليست توجيهاً دينياً أو رسمياً. تحققوا من التفاصيل الحية محلياً. للأسئلة الشرعية اتبعوا التوجيه الرسمي السعودي أو استشيروا عالماً مؤهلاً. الحجوزات عبر نسك والمزوّدين المرخّصين.'
      )
    };
  }

  function applyAdjustment(plan, adjustment) {
    var inputs = Object.assign({}, plan.inputs);
    if (adjustment === 'relaxed') inputs.pace = 'relaxed';
    if (adjustment === 'active') inputs.pace = 'active';
    if (adjustment === 'family') {
      if (inputs.interests.indexOf('family') === -1) inputs.interests = inputs.interests.concat(['family']);
      if (inputs.children < 1) inputs.children = 1;
      inputs.pace = inputs.pace === 'active' ? 'balanced' : inputs.pace;
    }
    if (adjustment === 'shopping') {
      if (inputs.interests.indexOf('shopping') === -1) inputs.interests = inputs.interests.concat(['shopping']);
    }
    if (adjustment === 'history') {
      if (inputs.interests.indexOf('history') === -1) inputs.interests = inputs.interests.concat(['history']);
    }
    inputs.seed = (inputs.seed || 1) + 1;
    return generate(inputs);
  }

  global.DFLMakkahTripEngine = {
    generate: generate,
    applyAdjustment: applyAdjustment,
    normalize: normalize,
    dayCount: dayCount
  };
})(window);
