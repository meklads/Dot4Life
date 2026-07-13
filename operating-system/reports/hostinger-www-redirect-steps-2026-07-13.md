# توحيد www على Hostinger — خطوات جوست (2026-07-13)

> **القرار:** النسخة الرسمية = `https://dotforlife.com` (**بدون** www)  
> لأن كل روابط canonical في الموقع هكذا.  
> الملف الجاهز في جذر المشروع: `.htaccess`

## أ) إن كان الاستضافة Shared / hPanel (الأشهر)

1. ادخل [hPanel Hostinger](https://hpanel.hostinger.com)
2. اختر موقع **dotforlife.com**
3. **ملفات** → **مدير الملفات** (File Manager)
4. افتح مجلد الموقع الجذر — غالباً `public_html`
5. ارفع / أنشئ ملف اسمه بالضبط: `.htaccess`  
   (انسخ محتوى ملف `.htaccess` من الريبو)
6. إن وُجد `.htaccess` قديم: ادمجه أو استبدله بعد نسخة احتياطية
7. اختبر من المتصفح (نافذة خاصة):
   - `http://www.dotforlife.com/tools/qibla.html`
   - يجب أن تصبح: `https://dotforlife.com/tools/qibla.html`

### بديل من اللوحة بدون ملف
**النطاقات** → **إعادة التوجيه** (Redirects):
- من: `www.dotforlife.com`
- إلى: `https://dotforlife.com`
- نوع: **301 Permanent**
- طبّق على كل المسارات إن وُجد الخيار

## ب) إن كان VPS / سيرفر خاص (Nginx)

ملف Apache `.htaccess` **لن يعمل** على Nginx. أضف في إعداد الموقع:

```nginx
server {
  server_name www.dotforlife.com;
  return 301 https://dotforlife.com$request_uri;
}
server {
  server_name dotforlife.com;
  listen 443 ssl;
  # ... باقي إعداد الموقع
}
```

ثم: `nginx -t` و `systemctl reload nginx`

## ج) بعد التحويل (Search Console)

1. تأكد أن لديك property لـ `https://dotforlife.com` (بدون www) — هذا الأساسي
2. إن وُجدت property لـ `https://www.dotforlife.com`: اتركها، وجوجل سيتبع 301 تدريجياً
3. لا تستخدم «تغيير العنوان» بين www وغير www كبديل وحيد — الـ301 يكفي

## د) تحقق سريع بعد ساعة

```bash
curl -I https://www.dotforlife.com/tools/qibla.html
```

ابحث عن: `HTTP/1.1 301` و `Location: https://dotforlife.com/...`

---

بعد ما تطبّق: أرسل نتيجة `curl` أو لقطة من شريط العنوان بعد فتح رابط www، وأكّد أن التحويل يعمل.
