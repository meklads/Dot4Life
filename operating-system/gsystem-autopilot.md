# GSystem Autopilot — بناء تلقائي + تنبيهات الفريق

> **المالك:** Cursor · **التاريخ:** 2026-06-22

## هل 100% أوتوماتيك؟ — صراحة

| ما يُؤتمت بالكامل | ما يبقى بشرياً |
|-------------------|----------------|
| `approved` + WebP في `approved/` → **بناء HTML + push** | عمر يكتب برومبت ويعتمد |
| تنبيهات صندوق الوارد لكل عضو | كلود يولّد في Higgsfield |
| GitHub Action كل 30 دقيقة + cron محلي 15 دقيقة | Hema تكتب DEEPEN |
| | عامر BUILD VERIFY للنصوص |

**لا يوجد نظام بلا بشر للكتابة والإجازة البصرية.** الأوتوبايلوت يغلق **فجوة Cursor** (لم نعد ننتظر «ابنِ»).

## القاعدة الذهبية

```
image-manifest.json → visual_director: approved
+ ملف في assets/images/approved/
= gsystem_autopilot يبني فوراً (بدون سؤال جوست)
```

## التشغيل

```bash
# بناء ما ينقص + تحديث inbox
PYTHONPATH=scripts python3 scripts/gsystem_autopilot.py

# بناء + git push
PYTHONPATH=scripts python3 scripts/gsystem_autopilot.py --push

# تنبيهات فقط
PYTHONPATH=scripts python3 scripts/gsystem_autopilot.py --notify

# تنبيهات macOS (جهازك)
PYTHONPATH=scripts python3 scripts/gsystem_autopilot.py --push --desktop-notify
```

### cron على Mac (كل 15 دقيقة)

```bash
bash scripts/install-gsystem-autopilot-cron.sh
```

### GitHub (كل push على الفهرس/approved + كل 30 دقيقة)

`.github/workflows/gsystem-autopilot.yml`

## صناديق التنبيه

| عضو | الملف |
|-----|--------|
| عمر | `operating-system/inbox/omar.md` |
| كلود | `operating-system/inbox/claude.md` |
| Hema | `operating-system/inbox/hema.md` |
| عامر | `operating-system/inbox/amer.md` |
| Cursor | `operating-system/inbox/cursor.md` |
| جوست | `operating-system/inbox/ghost.md` |

## السجلات

- `outputs/logs/gsystem-autopilot.log`
- `operating-system/.gsystem-state.json`
