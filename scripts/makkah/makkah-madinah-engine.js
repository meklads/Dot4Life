/**
 * Makkah → Madinah Planner — transfer decision engine (Tool 03).
 * Door-to-door journey planning. No schedules, fares, or invented distances.
 */
(function (global) {
  'use strict';

  function bi(en, ar) { return { en: en, ar: ar }; }
  function item(en, ar) { return bi(en, ar); }

  function normalize(raw) {
    return {
      departureContext: raw.departureContext || 'hotel',
      arrivalContext: raw.arrivalContext || 'hotel',
      makkahHotel: (raw.makkahHotel || '').toString().trim().slice(0, 80),
      madinahHotel: (raw.madinahHotel || '').toString().trim().slice(0, 80),
      adults: Math.max(1, parseInt(raw.adults, 10) || 1),
      children: Math.max(0, parseInt(raw.children, 10) || 0),
      elderly: raw.elderly === 'yes' ? 'yes' : 'no',
      walking: raw.walking || 'moderate',
      luggage: raw.luggage || 'moderate',
      stroller: raw.stroller === 'yes' ? 'yes' : 'no',
      pace: raw.pace || 'balanced',
      priority: raw.priority || 'simplicity',
      transportPreference: raw.transportPreference || 'none',
      departureFlexibility: raw.departureFlexibility || 'flexible',
      hotelReady: raw.hotelReady === 'yes' ? 'yes' : raw.hotelReady === 'no' ? 'no' : 'partial'
    };
  }

  function complexityScore(inputs) {
    var s = 0;
    if ((inputs.children || 0) > 0) s += 2;
    if ((inputs.children || 0) >= 2) s += 1;
    if (inputs.elderly === 'yes') s += 2;
    if (inputs.walking === 'low') s += 2;
    if (inputs.luggage === 'heavy') s += 3;
    if (inputs.luggage === 'moderate') s += 1;
    if (inputs.stroller === 'yes') s += 1;
    if (inputs.pace === 'relaxed') s += 1;
    if (inputs.departureFlexibility === 'tight') s += 1;
    return s;
  }

  function scoreModes(inputs) {
    var scores = { train: 4, car: 4, bus: 3 };
    var c = complexityScore(inputs);

    if (inputs.luggage === 'heavy' || inputs.stroller === 'yes') {
      scores.car += 3;
      scores.train += 1;
      scores.bus -= 1;
    }
    if ((inputs.children || 0) > 0) {
      scores.car += 2;
      scores.train += 1;
    }
    if (inputs.elderly === 'yes' || inputs.walking === 'low') {
      scores.car += 2;
      scores.train += 1;
      scores.bus -= 1;
    }
    if (inputs.priority === 'simplicity' || inputs.priority === 'comfort' || inputs.priority === 'luggage') {
      scores.car += 2;
      scores.train += 1;
    }
    if (inputs.priority === 'speed') {
      scores.train += 2;
      scores.car += 1;
    }
    if (inputs.priority === 'flexibility') {
      scores.car += 3;
    }
    if (inputs.priority === 'family') {
      scores.car += 2;
      scores.train += 1;
    }
    if (inputs.pace === 'active' && c < 3 && inputs.luggage === 'light') {
      scores.train += 2;
      scores.bus += 1;
    }
    if (inputs.pace === 'relaxed') {
      scores.car += 1;
      scores.train += 1;
      scores.bus -= 1;
    }
    if (inputs.departureFlexibility === 'tight') {
      scores.train += 1;
      scores.car += 1;
      scores.bus -= 1;
    }
    if (inputs.luggage === 'light' && (inputs.children || 0) === 0 && inputs.elderly !== 'yes') {
      scores.train += 2;
      scores.bus += 1;
    }

    // Honor preference without pretending it's objectively best
    if (inputs.transportPreference === 'train') scores.train += 5;
    if (inputs.transportPreference === 'car') scores.car += 5;
    if (inputs.transportPreference === 'bus') scores.bus += 5;

    return scores;
  }

  function modeMeta(key) {
    var map = {
      train: {
        id: 'train',
        title: bi('Train-oriented journey', 'رحلة تعتمد على القطار'),
        short: bi('Train', 'القطار'),
        blurb: bi(
          'Organize around a scheduled rail link, then plan first- and last-mile connections separately.',
          'رتّبوا اليوم حول رحلة قطار مجدولة، ثم خطّطوا الوصول من وإلى المحطة على حدة.'
        )
      },
      car: {
        id: 'car',
        title: bi('Private-car-oriented journey', 'رحلة تعتمد على سيارة خاصة'),
        short: bi('Private car', 'سيارة خاصة'),
        blurb: bi(
          'Fewer mid-journey transfers and more control over stops, luggage, and timing.',
          'انتقالات أقل في الطريق، وتحكم أوضح في التوقفات والحقائب والتوقيت.'
        )
      },
      bus: {
        id: 'bus',
        title: bi('Bus / shared-transport journey', 'رحلة حافلة أو نقل مشترك'),
        short: bi('Bus / shared', 'حافلة أو مشترك'),
        blurb: bi(
          'Plan carefully around departure points, luggage access, and group coordination.',
          'خطّطوا بعناية حول نقطة الانطلاق والحقائب وتنسيق المجموعة.'
        )
      }
    };
    return map[key];
  }

  function pickModes(inputs) {
    var scores = scoreModes(inputs);
    var ranked = Object.keys(scores).sort(function (a, b) {
      return scores[b] - scores[a] || a.localeCompare(b);
    });
    var primary = ranked[0];
    var secondary = ranked[1];
    // Only show alternative if meaningfully close or different
    var showAlt = scores[secondary] >= scores[primary] - 2;
    return {
      primary: modeMeta(primary),
      alternative: showAlt ? modeMeta(secondary) : null,
      scores: scores
    };
  }

  function whyReasons(inputs, primaryId) {
    var reasons = [];
    var c = complexityScore(inputs);

    if (inputs.transportPreference !== 'none' && inputs.transportPreference === primaryId) {
      reasons.push(item(
        'You already preferred this approach — the plan organizes the transition around it rather than overriding you.',
        'فضّلتم هذا النهج مسبقاً — الخطة تنظّم الانتقال حوله بدل تجاوز اختياركم.'
      ));
    }
    if (inputs.luggage === 'heavy') {
      reasons.push(item(
        'Several large bags raise the cost of complicated transfers, so the plan reduces handoffs where possible.',
        'الحقائب الكبيرة ترفع تكلفة الانتقالات المعقّدة، لذلك تقلّل الخطة المناولات قدر الإمكان.'
      ));
    }
    if ((inputs.children || 0) > 0) {
      reasons.push(item(
        'Traveling with children benefits from accessible essentials, snacks, and fewer tight connection points.',
        'السفر مع الأطفال يستفيد من أساسيات في متناول اليد ومرونة أكبر ووصلات أقل إحكاماً.'
      ));
    }
    if (inputs.elderly === 'yes' || inputs.walking === 'low') {
      reasons.push(item(
        'With older travelers or lower walking comfort, larger buffers and fewer walking segments usually matter more than squeezing the clock.',
        'مع كبار السن أو مشي أقل راحة، الهوامش الأكبر ومقاطع المشي الأقل أهم عادة من ضغط الوقت.'
      ));
    }
    if (inputs.priority === 'flexibility') {
      reasons.push(item(
        'Flexibility is your stated priority — the plan leaves room to adjust without inventing exact schedules.',
        'المرونة أولويتكم المعلنة — الخطة تترك مجالاً للتعديل دون اختراع جداول دقيقة.'
      ));
    }
    if (inputs.priority === 'speed' && primaryId === 'train') {
      reasons.push(item(
        'You prioritized speed — a train-oriented structure can work when first- and last-mile pieces are planned early.',
        'أولويّتكم السرعة — هيكل القطار قد يناسبكم إن خُطّطت قطع الوصول الأولى والأخيرة مبكراً.'
      ));
    }
    if (inputs.priority === 'simplicity' || inputs.priority === 'comfort') {
      reasons.push(item(
        'Simplicity and comfort point toward fewer stressful changes of mode on transfer day.',
        'البساطة والراحة تدفعان نحو تغييرات أقل إرهاقاً في يوم الانتقال.'
      ));
    }
    if (inputs.priority === 'family') {
      reasons.push(item(
        'Family travel is your stated priority — the plan favors coordination, accessible essentials, and calmer sequencing.',
        'سفر الأسرة أولويتكم المعلنة — الخطة تفضّل التنسيق والأساسيات في المتناول وتسلسلاً أهدأ.'
      ));
    }
    if (inputs.departureContext === 'undecided' || inputs.arrivalContext === 'undecided') {
      reasons.push(item(
        'Because lodging context is still open, the plan emphasizes confirming bases before stacking travel steps.',
        'لأن سياق الإقامة ما زال مفتوحاً، تؤكّد الخطة المقرّين قبل تكديس خطوات السفر.'
      ));
    }
    if (c < 3 && inputs.luggage === 'light' && primaryId === 'train') {
      reasons.push(item(
        'Light luggage and a simpler group make a scheduled rail-oriented plan more practical to organize.',
        'الحقائب الخفيفة والمجموعة الأبسط تجعل خطة القطار أيسر تنظيماً.'
      ));
    }
    var fillers = [
      item(
        'This is a planning framework for the transition day — verify live times, tickets, and policies with official providers before you leave.',
        'هذا إطار تخطيط ليوم الانتقال — تحققوا من الأوقات والتذاكر والسياسات الحية من مزوّدين رسميين قبل المغادرة.'
      ),
      item(
        'Door-to-door thinking matters more than picking a vehicle name: prepare, leave, travel, arrive, settle.',
        'التفكير من الباب للباب أهم من اسم الوسيلة: حضّروا، غادروا، سافروا، صلوا، استقروا.'
      ),
      item(
        'Keep one adult focused on people and one on bags whenever the group moves between spaces.',
        'اجعلوا بالغاً يركّز على الأشخاص وآخر على الحقائب كلما تحركت المجموعة بين الأماكن.'
      )
    ];
    var fi = 0;
    while (reasons.length < 3 && fi < fillers.length) {
      reasons.push(fillers[fi++]);
    }
    return reasons.slice(0, 4);
  }

  function checklistBefore(inputs, modeId) {
    var list = [
      item('Finish packing the night before when possible; keep one small bag with documents, phones, chargers, and medicines.', 'أنهوا الحزم مساء اليوم السابق إن أمكن؛ أبقوا حقيبة صغيرة للوثائق والجوالات والشواحن والأدوية.'),
      item('Confirm Madinah accommodation details and how you will reach it after arrival.', 'أكّدوا تفاصيل إقامة المدينة وكيف ستصلون إليها بعد الوصول.'),
      item('Confirm your chosen transport booking or arrangement with the official provider — do not rely on remembered schedules.', 'أكّدوا حجز النقل أو الترتيب المختار مع المزوّد الرسمي — لا تعتمدوا على جداول محفوظة في الذاكرة.'),
      item('Keep water and light snacks accessible, especially with children or older travelers.', 'أبقوا الماء ووجبات خفيفة في متناول اليد خصوصاً مع الأطفال أو كبار السن.')
    ];
    if (inputs.luggage === 'heavy') {
      list.push(item('Label bags clearly and decide who carries which piece before leaving the room.', 'ضعوا ملصقات واضحة واتفقوا من يحمل أي حقيبة قبل مغادرة الغرفة.'));
    }
    if (inputs.stroller === 'yes') {
      list.push(item('Decide when the stroller is folded vs used, and keep a hand free for children at doorways.', 'اتفقوا متى تُطوى العربة ومتى تُستخدم، واتركوا يداً حرة للأطفال عند المداخل.'));
    }
    if (inputs.departureFlexibility === 'tight') {
      list.push(item('Build a generous early buffer — verify current departure requirements with your provider; do not invent minutes.', 'ابنوا هامشاً مبكراً واسعاً — تحققوا من متطلبات المغادرة الحالية من مزوّدكم؛ لا تخترعوا دقائق.'));
    } else {
      list.push(item('Leave earlier than you think you need — transfer day rarely goes exactly as imagined.', 'غادروا أبكر مما تظنون — يوم الانتقال نادراً يسير كما تتخيلون تماماً.'));
    }
    if (modeId === 'train') {
      list.push(item('Plan how you will reach the departure station from your Makkah base without assuming walking times.', 'خطّطوا كيف تصلون للمحطة من مقر مكة دون افتراض أوقات مشي.'));
    }
    if (modeId === 'car') {
      list.push(item('Confirm pickup point, luggage space, and meeting time with your driver or provider.', 'أكّدوا نقطة الالتقاط ومساحة الحقائب وموعد اللقاء مع السائق أو المزوّد.'));
    }
    if (modeId === 'bus') {
      list.push(item('Confirm the exact departure point and luggage rules with the operator before checkout.', 'أكّدوا نقطة الانطلاق الدقيقة وقواعد الحقائب مع المشغّل قبل تسجيل المغادرة.'));
    }
    return list;
  }

  function departureItems(inputs, modeId) {
    var list = [
      item('Checkout / farewell sequence: bags first, then room check, then leave together as one group.', 'تسلسل المغادرة: الحقائب أولاً، ثم فحص الغرفة، ثم الخروج معاً كمجموعة واحدة.'),
      item('Keep documents and booking confirmations in one pocket or phone folder — not buried in a large suitcase.', 'أبقوا الوثائق وتأكيدات الحجز في جيب أو مجلد واحد — لا تدفنوها في حقيبة كبيرة.')
    ];
    if (modeId === 'train' || modeId === 'bus') {
      list.push(item('Reach the departure point with buffer. Recheck gate/platform information on site — do not trust screenshots alone.', 'صلوا لنقطة المغادرة بهامش. أعيدوا التحقق من البوابة/الرصيف في الموقع — لا تثقوا باللقطات وحدها.'));
    }
    if (modeId === 'car') {
      list.push(item('Load luggage once, seat children and elders next, then start. Avoid reopening every bag at the curb.', 'حمّلوا الحقائب مرة واحدة، أجسلوا الأطفال وكبار السن بعد ذلك، ثم انطلقوا. تجنبوا فتح كل الحقائب على الرصيف.'));
    }
    if ((inputs.children || 0) > 0) {
      list.push(item('Assign one adult to children and one to luggage during the exit — splitting both roles often causes delays.', 'كلّفوا بالغاً بالأطفال وآخر بالحقائب عند الخروج — جمع الدورين غالباً يسبب تأخيراً.'));
    }
    return list;
  }

  function duringItems(inputs, modeId) {
    var list = [
      item('Keep essential items within reach: water, tissues, phone power, booking details.', 'أبقوا الأساسيات في المتناول: ماء، مناديل، شحن الجوال، تفاصيل الحجز.'),
      item('Do not treat journey duration as fixed — traffic, boarding, and waits vary. Use the time to rest when you can.', 'لا تعتبروا مدة الرحلة ثابتة — الزحام والصعود والانتظار يتغيّران. استخدموا الوقت للراحة إن أمكن.')
    ];
    if ((inputs.children || 0) > 0) {
      list.push(item('Plan one calm activity or rest stretch for children instead of filling every minute.', 'خطّطوا نشاطاً هادئاً أو فترة راحة للأطفال بدل ملء كل دقيقة.'));
    }
    if (inputs.elderly === 'yes') {
      list.push(item('Protect seated rest and avoid unnecessary standing moves when the group can wait together.', 'احموا الراحة جلوساً وتجنبوا حركات الوقوف غير الضرورية إن أمكن انتظار المجموعة معاً.'));
    }
    if (modeId === 'train') {
      list.push(item('Keep luggage visible and grouped. Confirm the arrival station name before you stand to exit.', 'أبقوا الحقائب مرئية ومجمّعة. أكّدوا اسم محطة الوصول قبل الوقوف للخروج.'));
    }
    if (modeId === 'car') {
      list.push(item('Agree one short rest stop rule in advance so the group does not renegotiate every thirty minutes.', 'اتفقوا مسبقاً على قاعدة توقف راحة قصيرة حتى لا تعيد المجموعة التفاوض كل نصف ساعة.'));
    }
    return list;
  }

  function arrivalItems(inputs) {
    var list = [
      item('Collect all bags and people first — do not start looking for the next ride until the group is complete.', 'اجمعوا الحقائب والأشخاص أولاً — لا تبدأوا البحث عن التنقّل التالي قبل اكتمال المجموعة.'),
      item('Confirm the last-mile step to your Madinah base. If accommodation is not ready, keep expectations flexible.', 'أكّدوا خطوة الميل الأخير إلى مقر المدينة. إن لم تكن الإقامة جاهزة، أبقوا التوقعات مرنة.'),
      item('Allow settling time: water, wash, short rest before any optional visit.', 'اتركوا وقت استقرار: ماء، اغتسال، راحة قصيرة قبل أي زيارة اختيارية.')
    ];
    if (inputs.arrivalContext === 'undecided') {
      list.push(item('Since Madinah lodging is not set, prioritize confirming a base before adding activities.', 'بما أن إقامة المدينة غير محددة، أولوا تأكيد المقر قبل إضافة أنشطة.'));
    }
    if (inputs.pace === 'relaxed' || inputs.elderly === 'yes' || (inputs.children || 0) > 0) {
      list.push(item('Keep the rest of arrival day light — the transition already used energy.', 'أبقوا بقية يوم الوصول خفيفة — الانتقال استهلك طاقة أصلاً.'));
    }
    return list;
  }

  function dayBlocks(inputs, modeId) {
    return [
      {
        slot: bi('Morning', 'الصباح'),
        items: [
          item('Prepare, checkout, and leave with buffer — no last-minute packing marathon.', 'التحضير وتسجيل المغادرة والخروج بهامش — بلا سباق حزم في آخر لحظة.'),
          item('Confirm the day’s transport arrangement once more with your provider.', 'أكّدوا ترتيب نقل اليوم مرة أخرى مع مزوّدكم.')
        ]
      },
      {
        slot: bi('Travel block', 'كتلة السفر'),
        items: [
          item(
            modeId === 'car'
              ? 'Door-to-door travel period. Keep one calm stop rule and essentials accessible.'
              : 'Travel period via your chosen mode. Recheck live boarding details on site.',
            modeId === 'car'
              ? 'فترة سفر من الباب للباب. حافظوا على قاعدة توقف هادئة وأساسيات في المتناول.'
              : 'فترة السفر عبر الوسيلة المختارة. أعيدوا التحقق من تفاصيل الصعود الحية في الموقع.'
          )
        ]
      },
      {
        slot: bi('Arrival', 'الوصول'),
        items: [
          item('Last-mile to Madinah accommodation, then settle. Skip stacking visits immediately.', 'الميل الأخير لإقامة المدينة ثم الاستقرار. تجنبوا تكديس الزيارات فوراً.')
        ]
      },
      {
        slot: bi('Evening', 'المساء'),
        items: [
          item(
            inputs.pace === 'active' && complexityScore(inputs) < 3
              ? 'Optional light evening only if energy remains — otherwise rest.'
              : 'Flexible / rest. Protect sleep after a transfer day.',
            inputs.pace === 'active' && complexityScore(inputs) < 3
              ? 'مساء خفيف اختياري فقط إن بقيت طاقة — وإلا الراحة.'
              : 'مرن / راحة. احموا النوم بعد يوم انتقال.'
          )
        ]
      }
    ];
  }

  function comparison(inputs, primaryId) {
    // Qualitative only — situation-weighted notes, not absolute rankings
    function note(mode) {
      if (mode === 'train') {
        return bi(
          inputs.luggage === 'heavy'
            ? 'Useful when first/last mile are planned; heavy luggage needs careful station handling.'
            : 'Often predictable once booked; still needs station connections planned separately.',
          inputs.luggage === 'heavy'
            ? 'مفيد إن خطّطتم الوصول من وإلى المحطة؛ الحقائب الثقيلة تحتاج تعاملاً حذراً هناك.'
            : 'غالباً أوضح بعد الحجز؛ ما زال يحتاج تخطيط وصلات المحطة على حدة.'
        );
      }
      if (mode === 'car') {
        return bi(
          'Strong on door-to-door simplicity and luggage control; confirm provider details in advance.',
          'أقوى في البساطة من الباب إلى الباب والتحكم بالحقائب؛ أكّدوا تفاصيل المزوّد مسبقاً.'
        );
      }
      return bi(
        'Can work for lighter setups; confirm departure point and luggage rules carefully.',
        'قد يناسب الترتيبات الأخف؛ أكّدوا نقطة الانطلاق وقواعد الحقائب بعناية.'
      );
    }
    return [
      { mode: modeMeta('train').short, note: note('train'), highlight: primaryId === 'train' },
      { mode: modeMeta('car').short, note: note('car'), highlight: primaryId === 'car' },
      { mode: modeMeta('bus').short, note: note('bus'), highlight: primaryId === 'bus' }
    ];
  }

  function profile(inputs) {
    return {
      group: bi(
        (inputs.adults || 1) + ' adult(s)' + ((inputs.children || 0) > 0 ? ', ' + inputs.children + ' child(ren)' : '') + (inputs.elderly === 'yes' ? ', older traveler(s)' : ''),
        (inputs.adults || 1) + ' بالغ' + ((inputs.children || 0) > 0 ? '، ' + inputs.children + ' طفل' : '') + (inputs.elderly === 'yes' ? '، كبار سن' : '')
      ),
      luggage: bi(
        inputs.luggage === 'light' ? 'Light' : inputs.luggage === 'heavy' ? 'Several large bags' : 'Moderate',
        inputs.luggage === 'light' ? 'خفيف' : inputs.luggage === 'heavy' ? 'حقائب كبيرة متعددة' : 'متوسط'
      ),
      pace: bi(
        inputs.pace === 'relaxed' ? 'Relaxed' : inputs.pace === 'active' ? 'Active' : 'Balanced',
        inputs.pace === 'relaxed' ? 'هادئ' : inputs.pace === 'active' ? 'نشيط' : 'متوازن'
      ),
      priority: bi(
        ({
          simplicity: 'Simplicity', flexibility: 'Flexibility', comfort: 'Comfort',
          speed: 'Speed', luggage: 'Managing luggage', family: 'Traveling with family'
        })[inputs.priority] || 'Simplicity',
        ({
          simplicity: 'البساطة', flexibility: 'المرونة', comfort: 'الراحة',
          speed: 'السرعة', luggage: 'إدارة الحقائب', family: 'السفر مع الأسرة'
        })[inputs.priority] || 'البساطة'
      ),
      walking: inputs.elderly === 'yes' ? bi(
        inputs.walking === 'low' ? 'Low walking comfort' : inputs.walking === 'flexible' ? 'Flexible walking' : 'Moderate walking',
        inputs.walking === 'low' ? 'مشي منخفض الراحة' : inputs.walking === 'flexible' ? 'مشي مرن' : 'مشي متوسط'
      ) : null
    };
  }

  function generate(raw) {
    var inputs = normalize(raw);
    var modes = pickModes(inputs);
    var primaryId = modes.primary.id;
    return {
      version: 1,
      destination: 'makkah-to-madinah',
      generatedAt: new Date().toISOString().slice(0, 10),
      inputs: inputs,
      profile: profile(inputs),
      primary: modes.primary,
      alternative: modes.alternative,
      why: whyReasons(inputs, primaryId),
      comparison: comparison(inputs, primaryId),
      before: checklistBefore(inputs, primaryId),
      departure: departureItems(inputs, primaryId),
      during: duringItems(inputs, primaryId),
      arrival: arrivalItems(inputs),
      day: dayBlocks(inputs, primaryId),
      disclaimer: bi(
        'This is a practical transition planner, not a booking or live schedule service. Verify current times, fares, baggage rules, and availability with official transport providers before you travel.',
        'هذه أداة تخطيط انتقال عملية، وليست خدمة حجز أو جداول حية. تحققوا من الأوقات والأسعار وقواعد الحقائب والتوفر الحالية من مزوّدي النقل الرسميين قبل السفر.'
      ),
      officialNote: bi(
        'Check current official transport information before departure.',
        'تحققوا من معلومات النقل الرسمية الحالية قبل المغادرة.'
      )
    };
  }

  function applyAdjustment(plan, adjustment) {
    var inputs = Object.assign({}, plan.inputs);
    if (adjustment === 'simpler') {
      inputs.priority = 'simplicity';
      inputs.pace = 'relaxed';
    }
    if (adjustment === 'comfort') {
      inputs.priority = 'comfort';
      inputs.pace = 'relaxed';
      if (inputs.transportPreference === 'none') inputs.transportPreference = 'car';
    }
    if (adjustment === 'flexibility') {
      inputs.priority = 'flexibility';
      inputs.departureFlexibility = 'flexible';
      if (inputs.transportPreference === 'none') inputs.transportPreference = 'car';
    }
    if (adjustment === 'family') {
      inputs.priority = 'family';
      if (inputs.children < 1) inputs.children = 1;
      inputs.pace = inputs.pace === 'active' ? 'balanced' : inputs.pace;
    }
    if (adjustment === 'luggage') {
      inputs.priority = 'luggage';
      if (inputs.luggage === 'light') inputs.luggage = 'moderate';
      else inputs.luggage = 'heavy';
      if (inputs.transportPreference === 'none') inputs.transportPreference = 'car';
    }
    return generate(inputs);
  }

  global.DFLMakkahMadinahEngine = {
    generate: generate,
    applyAdjustment: applyAdjustment,
    normalize: normalize,
    complexityScore: complexityScore
  };
})(window);
