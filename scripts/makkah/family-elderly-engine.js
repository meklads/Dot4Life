/**
 * Family & Elderly Journey Planner — Tool 05.
 * Practical family travel planning only. No medical advice. No fabricated distances/hours.
 */
(function (global) {
  'use strict';

  function bi(en, ar) { return { en: en, ar: ar }; }
  function item(en, ar, kind) {
    var o = bi(en, ar);
    if (kind) o.kind = kind; // priority | optional | rest | flexible
    return o;
  }
  function block(slotEn, slotAr, items) {
    return { slot: bi(slotEn, slotAr), items: items };
  }

  var DURATION = { '1': 1, '2': 2, '3': 3, '4-5': 5, '6-7': 7, 'gt7': 8 };

  function normalize(raw) {
    var composition = raw.composition || 'adults';
    var hasChildren = false;
    var hasElderly = false;
    if (composition === 'children') { hasChildren = true; hasElderly = false; }
    else if (composition === 'elderly') { hasChildren = false; hasElderly = true; }
    else if (composition === 'both') { hasChildren = true; hasElderly = true; }
    else { hasChildren = false; hasElderly = false; }

    var children = hasChildren ? Math.max(1, Math.min(8, parseInt(raw.children, 10) || 1)) : 0;

    return {
      composition: composition,
      destination: raw.destination || 'makkah',
      duration: raw.duration || '3',
      daysMakkah: Math.max(0, parseInt(raw.daysMakkah, 10) || 0),
      daysMadinah: Math.max(0, parseInt(raw.daysMadinah, 10) || 0),
      adults: Math.max(1, parseInt(raw.adults, 10) || 2),
      children: children,
      elderly: hasElderly ? 'yes' : 'no',
      childAge: raw.childAge || '7-12',
      walking: raw.walking || 'moderate',
      pace: raw.pace || 'balanced',
      interests: Array.isArray(raw.interests) ? raw.interests.slice() : [],
      meals: raw.meals || 'somewhat',
      rest: raw.rest || 'important',
      keepTogether: raw.keepTogether === 'yes' ? 'yes' : 'no'
    };
  }

  function dayCount(inputs) {
    if (inputs.destination === 'both') {
      var m = inputs.daysMakkah || 0;
      var d = inputs.daysMadinah || 0;
      if (m + d >= 1) return Math.min(10, m + d);
    }
    return DURATION[inputs.duration] || 3;
  }

  function friction(inputs) {
    var f = 0;
    if (inputs.children > 0) f += 2;
    if (inputs.children >= 2) f += 1;
    if (inputs.childAge === 'u3' || inputs.childAge === '3-6') f += 1;
    if (inputs.elderly === 'yes') f += 2;
    if (inputs.walking === 'low') f += 3;
    if (inputs.pace === 'very-relaxed') f += 3;
    if (inputs.pace === 'relaxed') f += 2;
    if (inputs.pace === 'active') f -= 1;
    if (inputs.rest === 'very') f += 2;
    if (inputs.rest === 'important') f += 1;
    if (inputs.children > 0 && inputs.elderly === 'yes') f += 2;
    return f;
  }

  function hasInterest(inputs, key) {
    return (inputs.interests || []).indexOf(key) !== -1;
  }

  function placeName(dest) {
    if (dest === 'madinah') return bi('Madinah', 'المدينة');
    if (dest === 'both') return bi('Makkah & Madinah', 'مكة والمدينة');
    return bi('Makkah', 'مكة');
  }

  function worshipBlock(inputs, intensity) {
    var place = inputs._city === 'madinah'
      ? bi('Calm time near the Prophet’s Mosque — unhurried and flexible.', 'وقت هادئ قرب المسجد النبوي — بلا استعجال وبمرونة.')
      : bi('Calm time near the Haram — unhurried and flexible.', 'وقت هادئ قرب الحرم — بلا استعجال وبمرونة.');
    var items = [item(place.en, place.ar, intensity === 'light' ? 'optional' : 'priority')];
    if (friction(inputs) >= 4) {
      items.push(item(
        'Keep this block short enough that the group can return to base without pressure.',
        'أبقوا هذه الفترة قصيرة بما يكفي لعودة المجموعة للمقر بلا ضغط.',
        'flexible'
      ));
    }
    return items;
  }

  function restBlock(inputs, strength) {
    var items = [];
    if (strength === 'strong' || friction(inputs) >= 5 || inputs.rest === 'very') {
      items.push(item(
        'Protected rest in the room. Do not fill this hour.',
        'راحة محمية في الغرفة. لا تملأوا هذه الساعة.',
        'rest'
      ));
    } else {
      items.push(item(
        'Midday pause — even a shorter rest protects the evening.',
        'وقفة منتصف النهار — حتى راحة أقصر تحمي المساء.',
        'rest'
      ));
    }
    if (inputs.meals !== 'not') {
      items.push(item(
        'Simple meal break near your base. Verify hours locally; do not invent restaurant plans.',
        'استراحة وجبة بسيطة قرب المقر. تحققوا من المواعيد محلياً؛ لا تخترعوا خطط مطاعم.',
        'priority'
      ));
    }
    return items;
  }

  function familyBlock(inputs) {
    if (inputs.children <= 0 && !hasInterest(inputs, 'family')) return [];
    return [item(
      'Family reset: quiet room time or gentle outdoor air. Let children recover before the next move.',
      'استراحة أسرية: هدوء في الغرفة أو هواء لطيف. دعوا الأطفال يستعيدون طاقتهم قبل أي تنقّل.',
      'flexible'
    )];
  }

  function historyBlock(inputs) {
    if (!hasInterest(inputs, 'history') && !hasInterest(inputs, 'culture')) return [];
    if (friction(inputs) >= 6) {
      return [item(
        'Optional short historical/cultural stop only if energy remains. Skip freely.',
        'محطة تاريخية/ثقافية قصيرة اختيارية فقط إن بقيت طاقة. تجاوزوها بحرية.',
        'optional'
      )];
    }
    return [item(
      'One historical or cultural visit — confirm opening status before leaving.',
      'زيارة تاريخية أو ثقافية واحدة — أكّدوا حالة الفتح قبل المغادرة.',
      'optional'
    )];
  }

  function shopBlock(inputs) {
    if (!hasInterest(inputs, 'shopping')) return [];
    return [item(
      'Light shopping window with a time limit — do not let it crowd rest.',
      'وقت تسوق خفيف بحد زمني — لا تدعوه يزاحم الراحة.',
      'optional'
    )];
  }

  function movementNote(inputs) {
    if (inputs.walking === 'low' || hasInterest(inputs, 'simple')) {
      return [item(
        'Keep movement simple: fewer transfers, shorter segments, agree a meeting point before leaving the room.',
        'أبقوا التنقّل بسيطاً: انتقالات أقل ومقاطع أقصر واتفاق على نقطة لقاء قبل مغادرة الغرفة.',
        'priority'
      )];
    }
    return [];
  }

  function arrivalDay(inputs) {
    return [
      block('Morning', 'الصباح', [
        item('Arrive and settle: check-in, water, wash, short orientation around your base.', 'الوصول والاستقرار: تسجيل الدخول، ماء، اغتسال، تعرّف قصير حول المقر.', 'priority'),
        item('Keep the first hours light — travel day already used energy.', 'اجعلوا الساعات الأولى خفيفة — يوم السفر استهلك طاقة أصلاً.', 'flexible')
      ].concat(movementNote(inputs))),
      block('Midday', 'الظهيرة', restBlock(inputs, 'strong')),
      block('Afternoon', 'العصر', friction(inputs) >= 4
        ? [item('Optional short priority near your base only if everyone feels steady.', 'أولوية قصيرة اختيارية قرب المقر فقط إن كان الجميع مرتاحاً.', 'optional')]
        : worshipBlock(inputs, 'light')),
      block('Evening', 'المساء', [
        item('Flexible family evening. Early night if possible.', 'مساء أسري مرن. نوم مبكر إن أمكن.', 'flexible')
      ].concat(familyBlock(inputs)))
    ];
  }

  function departureDay(inputs) {
    return [
      block('Morning', 'الصباح', [
        item('Flexible morning only. Pack early; keep documents and essentials accessible.', 'صباح مرن فقط. احزموا مبكراً؛ أبقوا الوثائق والأساسيات في المتناول.', 'priority'),
        item('Leave buffer before onward travel — verify timing with your provider.', 'اتركوا هامشاً قبل السفر التالي — أكّدوا التوقيت مع مزوّدكم.', 'priority')
      ]),
      block('Midday', 'الظهيرة', [
        item('Final checks: bags, chargers, children’s essentials, hotel checkout timing.', 'فحوصات أخيرة: حقائب، شواحن، أساسيات الأطفال، موعد المغادرة من الفندق.', 'priority')
      ].concat(restBlock(inputs, 'normal').slice(0, 1))),
      block('Afternoon', 'العصر', [
        item('Departure window. Skip new attractions if time is tight.', 'نافذة المغادرة. تجاوزوا معالم جديدة إن ضاق الوقت.', 'flexible')
      ]),
      block('Evening', 'المساء', [
        item('If you remain overnight, keep the evening calm and local only.', 'إن بقيتم للمبيت، اجعلوا المساء هادئاً ومحلياً فقط.', 'rest')
      ])
    ];
  }

  function coreDay(inputs, dayIndex, total) {
    var f = friction(inputs);
    var relaxed = f >= 5 || inputs.pace === 'very-relaxed' || inputs.pace === 'relaxed';
    var morning = [];
    morning.push(item(
      'Steady start with water and a light breakfast — no early pressure on the group.',
      'بداية ثابتة مع ماء وإفطار خفيف — بلا ضغط صباحي على المجموعة.',
      'priority'
    ));
    morning = morning.concat(worshipBlock(inputs, relaxed ? 'light' : 'full'));
    morning = morning.concat(movementNote(inputs));

    var midday = restBlock(inputs, relaxed ? 'strong' : 'normal');

    var afternoon = [];
    if (hasInterest(inputs, 'history') || hasInterest(inputs, 'culture')) {
      afternoon = afternoon.concat(historyBlock(inputs));
    } else if (inputs.children > 0 || hasInterest(inputs, 'family')) {
      afternoon = afternoon.concat(familyBlock(inputs));
    } else if (!relaxed && inputs.pace === 'active') {
      afternoon.push(item(
        'One focused outing — then return to base. Avoid stacking distant stops.',
        'خرجة مركّزة واحدة — ثم العودة للمقر. تجنبوا تكديس محطات متباعدة.',
        'optional'
      ));
    } else {
      afternoon.push(item(
        'Flexible afternoon: rest, short walk nearby, or quiet time. Empty blocks are intentional.',
        'عصر مرن: راحة، مشي قصير بالقرب، أو وقت هادئ. الفراغ مقصود.',
        'flexible'
      ));
    }
    if (f >= 6 && afternoon.length > 1) {
      afternoon = [afternoon[0], item('Protect one empty hour with no errands.', 'احموا ساعة فارغة بلا مشاوير.', 'flexible')];
    }

    var evening = [];
    if (hasInterest(inputs, 'shopping') && dayIndex >= Math.ceil(total / 2) && f < 7) {
      evening = evening.concat(shopBlock(inputs));
    }
    if (inputs.meals !== 'not') {
      evening.push(item(
        'Unhurried evening meal. Keep water available.',
        'وجبة مساء بلا استعجال. أبقوا الماء متاحاً.',
        'priority'
      ));
    }
    evening.push(item(
      'Wind down in the room. Confirm tomorrow’s first step in one sentence.',
      'تهدئة في الغرفة. أكّدوا خطوة الغد الأولى بجملة واحدة.',
      'flexible'
    ));
    if (inputs.keepTogether === 'yes') {
      evening.push(item(
        'Agree tomorrow’s meeting point before sleep so the group starts aligned.',
        'اتفقوا على نقطة لقاء الغد قبل النوم حتى تبدأ المجموعة على وفاق.',
        'priority'
      ));
    }

    return [
      block('Morning', 'الصباح', morning),
      block('Midday', 'الظهيرة', midday),
      block('Afternoon', 'العصر', afternoon),
      block('Evening', 'المساء', evening)
    ];
  }

  function buildCityDays(inputs, city, n, offset) {
    inputs._city = city;
    var days = [];
    var i;
    for (i = 1; i <= n; i++) {
      var kind = 'core';
      if (n === 1) kind = 'single';
      else if (i === 1) kind = 'arrival';
      else if (i === n) kind = 'departure';

      var blocks;
      if (kind === 'single') {
        blocks = [
          arrivalDay(inputs)[0],
          block('Midday', 'الظهيرة', restBlock(inputs, 'strong')),
          block('Afternoon', 'العصر', worshipBlock(inputs, 'light').concat(familyBlock(inputs))),
          departureDay(inputs)[2]
        ];
      } else if (kind === 'arrival') blocks = arrivalDay(inputs);
      else if (kind === 'departure') blocks = departureDay(inputs);
      else blocks = coreDay(inputs, i, n);

      var cityLabel = city === 'madinah' ? bi('Madinah', 'المدينة') : bi('Makkah', 'مكة');
      var title;
      if (kind === 'arrival') title = bi('Day ' + (offset + i) + ' — ' + cityLabel.en + ' arrival & settling', 'اليوم ' + (offset + i) + ' — وصول واستقرار في ' + cityLabel.ar);
      else if (kind === 'departure') title = bi('Day ' + (offset + i) + ' — ' + cityLabel.en + ' prepare to leave', 'اليوم ' + (offset + i) + ' — استعداد لمغادرة ' + cityLabel.ar);
      else if (kind === 'single') title = bi('Your day in ' + cityLabel.en + ' — keep it light', 'يومكم في ' + cityLabel.ar + ' — اجعلوه خفيفاً');
      else title = bi('Day ' + (offset + i) + ' — ' + cityLabel.en + ' steady family day', 'اليوم ' + (offset + i) + ' — يوم أسري متوازن في ' + cityLabel.ar);

      days.push({ index: offset + i, kind: kind, city: city, title: title, blocks: blocks });
    }
    return days;
  }

  function buildDays(inputs) {
    if (inputs.destination === 'both') {
      var m = inputs.daysMakkah || Math.max(1, Math.floor(dayCount(inputs) / 2));
      var d = inputs.daysMadinah || Math.max(1, dayCount(inputs) - m);
      var days = buildCityDays(inputs, 'makkah', m, 0);
      // Transition reminder day marker (not a full Tool 03 clone)
      days.push({
        index: m + 0.5,
        kind: 'transition',
        city: 'transfer',
        title: bi('Transition — Makkah → Madinah', 'الانتقال — مكة → المدينة'),
        blocks: [
          block('Plan the move', 'خطّطوا الانتقال', [
            item('Keep this transfer day lighter for the family. Use the dedicated planner for door-to-door structure.', 'اجعلوا يوم الانتقال أخف للأسرة. استخدموا المخطط المخصّص لترتيب الرحلة من الباب إلى الباب.', 'priority'),
            item('Open Makkah → Madinah Planner for luggage, buffers, and journey organization.', 'افتحوا مخطط مكة → المدينة للحقائب والهوامش وتنظيم الرحلة.', 'priority')
          ])
        ],
        linkTool03: true
      });
      return days.concat(buildCityDays(inputs, 'madinah', d, m));
    }
    var city = inputs.destination === 'madinah' ? 'madinah' : 'makkah';
    return buildCityDays(inputs, city, dayCount(inputs), 0);
  }

  function principles(inputs) {
    var list = [
      item('Keep movement simple', 'أبقوا التنقّل بسيطاً'),
      item('Protect rest periods', 'احموا فترات الراحة'),
      item('Leave flexible time — empty blocks are intentional', 'اتركوا وقتاً مرناً — الفراغ مقصود'),
      item('Keep essentials accessible', 'أبقوا الأساسيات في المتناول')
    ];
    if (inputs.children > 0) list.push(item('Allow meal and break flexibility for children', 'اسمحوا بمرونة الوجبات والاستراحات للأطفال'));
    if (inputs.elderly === 'yes' || inputs.walking === 'low') list.push(item('Reduce unnecessary transfers', 'قلّلوا الانتقالات غير الضرورية'));
    if (inputs.keepTogether === 'yes') list.push(item('Agree meeting points before each exit', 'اتفقوا على نقاط لقاء قبل كل خروج'));
    if (inputs.children > 0 && inputs.elderly === 'yes') list.push(item('Use the strongest flexibility setting for this multi-generation group', 'استخدموا أعلى مرونة لهذه المجموعة متعددة الأجيال'));
    return list.slice(0, 6);
  }

  function checklist(inputs) {
    var list = [
      item('Keep essential items accessible (documents, phones, chargers, water)', 'أبقوا الأساسيات في المتناول (وثائق، جوالات، شواحن، ماء)'),
      item('Keep hotel information accessible for the group', 'أبقوا معلومات الفندق في متناول المجموعة'),
      item('Allow buffer before scheduled movement', 'اتركوا هامشاً قبل أي تنقّل مجدول')
    ];
    if (inputs.children > 0) {
      list.push(item('Keep children’s essentials together (snacks, water, spare clothes as needed)', 'اجمعوا أساسيات الأطفال معاً (وجبات خفيفة، ماء، ملابس إضافية حسب الحاجة)'));
    }
    if (inputs.keepTogether === 'yes' || inputs.children > 0 || inputs.elderly === 'yes') {
      list.push(item('Plan a family meeting point before leaving the room', 'خطّطوا نقطة لقاء أسرية قبل مغادرة الغرفة'));
    }
    if (inputs.walking === 'low' || inputs.rest !== 'standard') {
      list.push(item('Identify rest opportunities during the day — do not invent facility claims', 'حدّدوا فرص راحة خلال اليوم — لا تخترعوا ميزات منشآت'));
    }
    list.push(item('For religious guidance, follow official Saudi guidance or consult a qualified scholar', 'للتوجيه الشرعي اتبعوا التوجيه الرسمي السعودي أو استشيروا عالماً مؤهلاً'));
    list.push(item('This planner is not medical advice — consult a healthcare professional for health-related travel decisions', 'هذه الأداة ليست نصيحة طبية — استشيروا مختص رعاية صحية لقرارات السفر الصحية'));
    return list;
  }

  function profile(inputs) {
    var familyType = bi('Adults only', 'بالغون فقط');
    if (inputs.children > 0 && inputs.elderly === 'yes') familyType = bi('Children + older family member(s)', 'أطفال + كبار سن');
    else if (inputs.children > 0) familyType = bi('With children', 'مع أطفال');
    else if (inputs.elderly === 'yes') familyType = bi('With older family member(s)', 'مع كبار سن');

    return {
      destination: placeName(inputs.destination),
      duration: bi(dayCount(inputs) + ' day(s)', dayCount(inputs) + ' يوم/أيام'),
      family: familyType,
      group: bi(
        inputs.adults + ' adult(s)' + (inputs.children ? ', ' + inputs.children + ' child(ren)' : '') + (inputs.elderly === 'yes' ? ', older traveler(s)' : ''),
        inputs.adults + ' بالغ' + (inputs.children ? '، ' + inputs.children + ' طفل' : '') + (inputs.elderly === 'yes' ? '، كبار سن' : '')
      ),
      walking: bi(
        inputs.walking === 'low' ? 'Keep walking to a minimum' : inputs.walking === 'flexible' ? 'Flexible' : 'Moderate',
        inputs.walking === 'low' ? 'أقل مشي ممكن' : inputs.walking === 'flexible' ? 'مرن' : 'متوسط'
      ),
      pace: bi(
        ({ 'very-relaxed': 'Very relaxed', relaxed: 'Relaxed', balanced: 'Balanced', active: 'Active' })[inputs.pace] || 'Balanced',
        ({ 'very-relaxed': 'هادئ جداً', relaxed: 'هادئ', balanced: 'متوازن', active: 'نشيط' })[inputs.pace] || 'متوازن'
      )
    };
  }

  function generate(raw) {
    var inputs = normalize(raw);
    return {
      version: 1,
      tool: 'family-elderly',
      generatedAt: new Date().toISOString().slice(0, 10),
      inputs: inputs,
      profile: profile(inputs),
      principles: principles(inputs),
      days: buildDays(inputs),
      checklist: checklist(inputs),
      disclaimer: bi(
        'This is a practical family travel planner, not medical advice and not a religious authority. It does not invent distances, accessibility, or facility claims. Verify current details locally. For health-related decisions, consult an appropriate healthcare professional. For religious guidance, follow official Saudi guidance or consult a qualified scholar.',
        'هذه أداة تخطيط سفر أسرية عملية، وليست نصيحة طبية وليست جهة دينية. لا تخترع مسافات أو إمكانية وصول أو ميزات منشآت. تحققوا من التفاصيل الحية محلياً. للقرارات الصحية استشيروا مختص رعاية صحية مناسباً. للتوجيه الشرعي اتبعوا التوجيه الرسمي السعودي أو استشيروا عالماً مؤهلاً.'
      )
    };
  }

  function applyAdjustment(plan, adjustment) {
    var inputs = Object.assign({}, plan.inputs);
    if (adjustment === 'relaxed') {
      inputs.pace = 'very-relaxed';
      inputs.rest = 'very';
    }
    if (adjustment === 'walking') {
      inputs.walking = 'low';
      if (inputs.interests.indexOf('simple') === -1) inputs.interests = inputs.interests.concat(['simple']);
    }
    if (adjustment === 'family') {
      if (inputs.interests.indexOf('family') === -1) inputs.interests = inputs.interests.concat(['family']);
      if (inputs.children < 1) { inputs.children = 1; inputs.composition = inputs.elderly === 'yes' ? 'both' : 'children'; }
      inputs.pace = inputs.pace === 'active' ? 'balanced' : inputs.pace;
    }
    if (adjustment === 'rest') {
      inputs.rest = 'very';
      inputs.pace = inputs.pace === 'active' ? 'relaxed' : inputs.pace;
    }
    if (adjustment === 'history') {
      if (inputs.interests.indexOf('history') === -1) inputs.interests = inputs.interests.concat(['history']);
    }
    if (adjustment === 'shopping') {
      if (inputs.interests.indexOf('shopping') === -1) inputs.interests = inputs.interests.concat(['shopping']);
    }
    return generate(inputs);
  }

  global.DFLFamilyElderlyEngine = {
    generate: generate,
    applyAdjustment: applyAdjustment,
    normalize: normalize,
    friction: friction,
    dayCount: dayCount
  };
})(window);
