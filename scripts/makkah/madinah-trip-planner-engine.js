/**
 * Madinah Trip Planner — deterministic engine (Tool 02).
 * Madinah-specific rules. Shares schema conventions with Tool 01.
 * No network. No fatwas. No invented distances/hours/fees.
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
  function item(en, ar) { return bi(en, ar); }
  function block(slotEn, slotAr, items) {
    return { slot: bi(slotEn, slotAr), items: items };
  }

  function dayCount(inputs) {
    if (inputs.durationDays != null && inputs.durationDays !== '') {
      return Math.max(1, Math.min(10, parseInt(inputs.durationDays, 10) || 1));
    }
    return DURATION_DAYS[inputs.duration] || 3;
  }

  function hasInterest(inputs, key) {
    return (inputs.interests || []).indexOf(key) !== -1;
  }

  /** Madinah defaults to calmer baseline than Makkah (+1). */
  function restWeight(inputs) {
    var w = 1;
    if (inputs.pace === 'relaxed') w += 2;
    if (inputs.pace === 'active') w -= 1;
    if ((inputs.children || 0) > 0) w += 2;
    if (inputs.elderly === 'yes') w += 2;
    if (inputs.walking === 'low') w += 2;
    if (hasInterest(inputs, 'quiet') || hasInterest(inputs, 'rest')) w += 1;
    if (inputs.arrival === 'makkah') w += 1; // long transfer day
    return w;
  }

  function worshipItems(inputs, intensity) {
    var items = [];
    if (hasInterest(inputs, 'worship') || intensity !== 'light') {
      items.push(item(
        'Calm time at or near the Prophet’s Mosque — unhurried prayer and quiet presence.',
        'وقت هادئ عند المسجد النبوي أو بقربه — صلاة بلا استعجال وحضور هادئ.'
      ));
    }
    if (intensity === 'full' && (hasInterest(inputs, 'worship') || hasInterest(inputs, 'quiet'))) {
      items.push(item(
        'Leave space before and after for water, shade, and returning to your base without rushing.',
        'اتركوا هامشاً قبل وبعد للماء والظل والعودة لمقركم بلا عجلة.'
      ));
    }
    if (intensity === 'light' && restWeight(inputs) >= 4) {
      items.push(item(
        'Keep worship blocks short and repeatable — quality over stacking visits.',
        'اجعلوا فترات العبادة قصيرة وقابلة للتكرار — الجودة أهم من تكديس الزيارات.'
      ));
    }
    return items;
  }

  function mealItems(inputs) {
    if (hasInterest(inputs, 'food')) {
      return [item(
        'One unhurried Madinah meal near your base — confirm hours locally; avoid hopping distant restaurants.',
        'وجبة هادئة واحدة في المدينة قرب مقركم — أكّدوا المواعيد محلياً؛ تجنبوا التنقّل بين مطاعم متباعدة.'
      )];
    }
    return [item(
      'Simple meal break. Hydrate, especially with children or older travelers.',
      'استراحة وجبة بسيطة. اشربوا ماء خصوصاً مع الأطفال أو كبار السن.'
    )];
  }

  function historyItems(inputs, heavy) {
    if (!hasInterest(inputs, 'history') && !hasInterest(inputs, 'culture')) return [];
    if (heavy) {
      return [item(
        'One Madinah historical or cultural visit — check access and opening status before you leave.',
        'زيارة تاريخية أو ثقافية واحدة في المدينة — تحققوا من الدخول وحالة الفتح قبل المغادرة.'
      )];
    }
    return [item(
      'Optional short historical stop if energy allows. Skip it when the group needs quiet.',
      'محطة تاريخية قصيرة اختيارية إن سمحت الطاقة. تجاوزوها إن احتاجت المجموعة للهدوء.'
    )];
  }

  function shopItems(inputs, level) {
    if (!hasInterest(inputs, 'shopping') && level !== 'force') return [];
    if (level === 'light') {
      return [item(
        'Light shopping near your area — set a time box so it does not crowd worship or rest.',
        'تسوق خفيف قرب منطقتكم — حدّدوا وقتاً حتى لا يزاحم العبادة أو الراحة.'
      )];
    }
    return [item(
      'Dedicated shopping window. Cluster errands; return to base before evening worsens fatigue.',
      'نافذة تسوق مخصّصة. جمّعوا المشاوير؛ عودوا للمقر قبل أن يشتد إرهاق المساء.'
    )];
  }

  function familyItems(inputs) {
    if (!hasInterest(inputs, 'family') && !(inputs.children > 0)) return [];
    return [item(
      'Family reset in Madinah: quiet room time or gentle outdoor air. Let children recover before the next move.',
      'استراحة أسرية في المدينة: هدوء في الغرفة أو هواء لطيف. دعوا الأطفال يستعيدون طاقتهم قبل أي تنقّل.'
    )];
  }

  function quietItems(inputs) {
    if (!hasInterest(inputs, 'quiet') && !hasInterest(inputs, 'rest') && restWeight(inputs) < 3) return [];
    return [item(
      'Protected quiet hour — no errands. Madinah plans work better with empty space.',
      'ساعة هدوء محمية — بلا مشاوير. خطط المدينة تعمل أفضل مع فراغ متعمَّد.'
    )];
  }

  function restItems(inputs, strength) {
    var lines = [];
    if (strength === 'strong' || restWeight(inputs) >= 3) {
      lines.push(item(
        'Protected rest at your accommodation. Reduce walking; hydrate; do not fill every hour.',
        'راحة محمية في الإقامة. قلّلوا المشي؛ اشربوا ماء؛ لا تملأوا كل ساعة.'
      ));
    } else {
      lines.push(item(
        'Midday pause — even 45–60 minutes protects a calmer evening near Nabawi.',
        'وقفة منتصف النهار — حتى 45–60 دقيقة تحمي مساءً أهدأ قرب النبوي.'
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

  function flexibleItems() {
    return [item(
      'Flexible time — rest, short walk nearby, or quiet reading. Empty blocks are intentional.',
      'وقت مرن — راحة، مشي قصير بالقرب، أو قراءة هادئة. الفراغ مقصود.'
    )];
  }

  function arrivalBlocks(inputs) {
    var morning = [];
    morning.push(item(
      'Arrive and settle in Madinah: check-in, water, wash, short orientation around your base.',
      'الوصول والاستقرار في المدينة: تسجيل الدخول، ماء، اغتسال، تعرّف قصير حول المقر.'
    ));
    if (inputs.arrival === 'makkah') {
      morning.push(item(
        'You arrived from Makkah — treat this as a transfer-recovery day, not a packed visit day.',
        'وصلتم من مكة — اعتبروا هذا يوم استعادة بعد الانتقال، لا يوم زيارات مكتظ.'
      ));
    } else if (inputs.arrival === 'airport' || inputs.arrival === 'city') {
      morning.push(item(
        'Travel fatigue is real — keep the first Madinah hours light.',
        'إرهاق السفر حقيقي — اجعلوا الساعات الأولى في المدينة خفيفة.'
      ));
    }
    var midday = restItems(inputs, 'strong');
    var afternoon = [];
    if (inputs.pace === 'active' && restWeight(inputs) < 3) {
      afternoon = afternoon.concat(worshipItems(inputs, 'light'));
    } else {
      afternoon.push(item(
        'Optional short visit near your base only if everyone feels steady.',
        'زيارة قصيرة اختيارية قرب المقر فقط إن كان الجميع مرتاحاً.'
      ));
      afternoon = afternoon.concat(quietItems(inputs));
    }
    var evening = mealItems(inputs).concat([
      item(
        'Early night if possible. Save fuller Madinah days for when energy returns.',
        'نوم مبكر إن أمكن. ادّخروا أيام المدينة الأوفر طاقة لما تعود الطاقة.'
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
    } else if (inputs.startPref === 'early') {
      morning.push(item(
        'Early calm start: water, light breakfast, then unhurried time near Nabawi.',
        'بداية هادئة مبكرة: ماء وإفطار خفيف ثم وقت بلا استعجال قرب النبوي.'
      ));
    } else {
      morning.push(item(
        'Steady morning with water and a light breakfast — Madinah rewards an unhurried start.',
        'صباح ثابت مع ماء وإفطار خفيف — المدينة تكافئ البداية الهادئة.'
      ));
    }
    morning = morning.concat(worshipItems(inputs, relaxed ? 'light' : 'full'));

    var midday = restItems(inputs, relaxed ? 'strong' : 'normal').concat(mealItems(inputs));
    if (relaxed || hasInterest(inputs, 'quiet')) {
      midday = midday.concat(quietItems(inputs));
    }

    var afternoon = [];
    // Madinah rhythm: history/culture on alternate days; prefer quiet over stacking
    if ((hasInterest(inputs, 'history') || hasInterest(inputs, 'culture')) && (!relaxed || dayIndex % 2 === 0)) {
      afternoon = afternoon.concat(historyItems(inputs, active && dayIndex % 2 === 0));
    } else if (hasInterest(inputs, 'family') || (inputs.children || 0) > 0) {
      afternoon = afternoon.concat(familyItems(inputs));
    } else if (active && !hasInterest(inputs, 'quiet')) {
      afternoon.push(item(
        'One focused Madinah outing — then return to base. Avoid stacking distant stops.',
        'خرجة مركّزة واحدة في المدينة — ثم العودة للمقر. تجنبوا تكديس محطات متباعدة.'
      ));
    } else {
      afternoon = afternoon.concat(flexibleItems());
    }

    // Long stays: deliberately leave empty flexible afternoons
    if (total >= 6 && dayIndex % 3 === 0 && afternoon.length) {
      afternoon = flexibleItems().concat(quietItems(inputs));
    }

    var evening = [];
    if (hasInterest(inputs, 'shopping') && (active || dayIndex >= Math.ceil(total / 2))) {
      evening = evening.concat(shopItems(inputs, relaxed ? 'light' : 'normal'));
    }
    evening = evening.concat(mealItems(inputs));
    if (!relaxed && hasInterest(inputs, 'worship')) {
      evening = evening.concat(worshipItems(inputs, 'light'));
    } else if (relaxed || hasInterest(inputs, 'quiet')) {
      evening.push(item(
        'Quiet evening near your base — no new destinations.',
        'مساء هادئ قرب المقركم — بلا وجهات جديدة.'
      ));
    }
    evening.push(item(
      'Wind down in the room. Confirm tomorrow’s first Madinah step in one sentence.',
      'تهدئة في الغرفة. أكّدوا خطوة الغد الأولى في المدينة بجملة واحدة.'
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
    if (inputs.departure === 'makkah') {
      morning.push(item(
        'You noted Makkah next — protect transfer buffer; do not schedule a heavy visit this morning.',
        'أشرتم أن مكة هي التالية — احموا هامش الانتقال؛ لا تجدولوا زيارة ثقيلة هذا الصباح.'
      ));
    } else if (inputs.departure === 'airport' || inputs.departure === 'home') {
      morning.push(item(
        'Airport / travel day — leave generous buffer. Verify transport timing with your provider.',
        'يوم مطار/سفر — اتركوا هامشاً واسعاً. أكّدوا توقيت النقل مع مزوّدكم.'
      ));
    } else if (inputs.departure === 'saudi') {
      morning.push(item(
        'Continuing elsewhere in Saudi Arabia — keep this morning light and bags ready.',
        'المتابعة داخل السعودية — اجعلوا هذا الصباح خفيفاً والحقائب جاهزة.'
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

  function dayTitle(kind, index, total) {
    if (kind === 'arrival') {
      return bi('Day ' + index + ' — Arrival & settling in Madinah', 'اليوم ' + index + ' — الوصول والاستقرار في المدينة');
    }
    if (kind === 'departure') {
      return bi('Day ' + index + ' — Prepare to leave Madinah', 'اليوم ' + index + ' — الاستعداد لمغادرة المدينة');
    }
    if (total <= 2) {
      return bi('Day ' + index + ' — Main Madinah day', 'اليوم ' + index + ' — اليوم الأساسي في المدينة');
    }
    if (total >= 6 && index % 3 === 0) {
      return bi('Day ' + index + ' — Quiet & flexible', 'اليوم ' + index + ' — هدوء ومرونة');
    }
    if (index === Math.ceil(total / 2)) {
      return bi('Day ' + index + ' — Explore & flexible time', 'اليوم ' + index + ' — استكشاف ووقت مرن');
    }
    return bi('Day ' + index + ' — Steady Madinah day', 'اليوم ' + index + ' — يوم متوازن في المدينة');
  }

  function buildDays(inputs) {
    var n = dayCount(inputs);
    var days = [];
    var i;
    for (i = 1; i <= n; i++) {
      var kind = 'core';
      if (n === 1) {
        if (inputs.arrival === 'already' && inputs.departure !== 'airport' && inputs.departure !== 'home' && inputs.departure !== 'makkah') {
          kind = 'core';
        } else {
          days.push({
            index: i,
            kind: 'single',
            title: bi('Your day in Madinah — keep it light', 'يومكم في المدينة — اجعلوه خفيفاً'),
            blocks: (function () {
              var a = arrivalBlocks(inputs);
              var d = departureBlocks(inputs);
              return [
                a[0],
                block('Midday', 'الظهيرة', restItems(inputs, 'strong').concat(mealItems(inputs))),
                block('Afternoon', 'العصر', worshipItems(inputs, 'light').concat(familyItems(inputs)).concat(quietItems(inputs))),
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

      if (kind === 'core' && inputs.pace === 'active' && hasInterest(inputs, 'shopping') && i === Math.max(2, n - 2)) {
        blocks[3].items = shopItems(inputs, 'normal').concat(blocks[3].items);
      }
      if (kind === 'core' && hasInterest(inputs, 'history') && i === Math.max(2, Math.floor(n / 2))) {
        blocks[2].items = historyItems(inputs, true).concat(blocks[2].items);
      }

      days.push({
        index: i,
        kind: kind,
        title: dayTitle(kind, i, n),
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
    var days = buildDays(inputs);
    if (inputs.seed % 2 === 0 && days.length > 2) {
      var mid = days[Math.floor(days.length / 2)];
      if (mid && mid.kind === 'core' && mid.blocks[2]) {
        mid.blocks[2].items = mid.blocks[2].items.concat([
          item(
            'Alternate Madinah focus: protect one empty hour with no errands.',
            'تركيز بديل في المدينة: احموا ساعة فارغة بلا مشاوير.'
          )
        ]);
      }
    }
    return {
      version: 1,
      destination: 'madinah',
      generatedAt: new Date().toISOString().slice(0, 10),
      inputs: inputs,
      summary: summary(inputs),
      days: days,
      disclaimer: bi(
        'This is a practical Madinah planning assistant, not religious or official guidance. Verify live details locally. For religious questions, follow official Saudi guidance or consult a qualified scholar. Bookings remain on Nusuk and licensed providers.',
        'هذه أداة تخطيط عملية للمدينة، وليست توجيهاً دينياً أو رسمياً. تحققوا من التفاصيل الحية محلياً. للأسئلة الشرعية اتبعوا التوجيه الرسمي السعودي أو استشيروا عالماً مؤهلاً. الحجوزات عبر نسك والمزوّدين المرخّصين.'
      )
    };
  }

  function applyAdjustment(plan, adjustment) {
    var inputs = Object.assign({}, plan.inputs);
    if (adjustment === 'relaxed') {
      inputs.pace = 'relaxed';
      if (inputs.interests.indexOf('quiet') === -1) inputs.interests = inputs.interests.concat(['quiet']);
    }
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

  global.DFLMadinahTripEngine = {
    generate: generate,
    applyAdjustment: applyAdjustment,
    normalize: normalize,
    dayCount: dayCount
  };
})(window);
