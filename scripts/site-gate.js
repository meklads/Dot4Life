/*!
 * Dot4Life — pre-launch site gate (GitHub Pages static)
 * Set SITE_GATE_ENABLED to false when ready to launch publicly.
 * Password is verified client-side via SHA-256 hash (not stored in repo).
 */
(function () {
  'use strict';

  var SITE_GATE_ENABLED = true;
  var GATE_STORAGE_KEY = 'dfl-site-gate-v1';
  /* SHA-256 of site password — rotate hash if password changes */
  var GATE_PASSWORD_HASH = '8248c7ae40e0134d712024986fb17eefb0d7eed11a779554158e5bbd12c391eb';

  if (!SITE_GATE_ENABLED) return;
  if (sessionStorage.getItem(GATE_STORAGE_KEY) === GATE_PASSWORD_HASH) return;

  document.documentElement.classList.add('dfl-gate-pending');

  function sha256(text) {
    if (!window.crypto || !crypto.subtle) {
      return Promise.reject(new Error('Secure context required'));
    }
    var enc = new TextEncoder().encode(text);
    return crypto.subtle.digest('SHA-256', enc).then(function (buf) {
      return Array.from(new Uint8Array(buf)).map(function (b) {
        return b.toString(16).padStart(2, '0');
      }).join('');
    });
  }

  function unlock() {
    sessionStorage.setItem(GATE_STORAGE_KEY, GATE_PASSWORD_HASH);
    document.documentElement.classList.remove('dfl-gate-pending');
    document.documentElement.classList.add('dfl-gate-ok');
    var overlay = document.getElementById('dfl-site-gate');
    if (overlay) overlay.remove();
  }

  function buildOverlay() {
    if (document.getElementById('dfl-site-gate')) return;

    var lang = (document.documentElement.getAttribute('data-lang') || 'ar');
    var isAr = lang === 'ar';

    var overlay = document.createElement('div');
    overlay.id = 'dfl-site-gate';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', isAr ? 'دخول الموقع' : 'Site access');
    overlay.innerHTML =
      '<div class="dfl-gate-card">' +
        '<div class="dfl-gate-logo">Dot4Life</div>' +
        '<p class="dfl-gate-eyebrow">' + (isAr ? 'معاينة خاصة' : 'Private preview') + '</p>' +
        '<h1 class="dfl-gate-title">' + (isAr ? 'الموقع قيد الإعداد' : 'Site under preparation') + '</h1>' +
        '<p class="dfl-gate-desc">' + (isAr
          ? 'أدخل كلمة المرور للمعاينة. سنطلق الموقع رسمياً قريباً.'
          : 'Enter the preview password. Public launch coming soon.') + '</p>' +
        '<form class="dfl-gate-form" autocomplete="off">' +
          '<label class="dfl-gate-label" for="dfl-gate-password">' + (isAr ? 'كلمة المرور' : 'Password') + '</label>' +
          '<input id="dfl-gate-password" class="dfl-gate-input" type="password" name="password" required autofocus />' +
          '<p class="dfl-gate-error" hidden></p>' +
          '<button type="submit" class="dfl-gate-btn">' + (isAr ? 'دخول' : 'Enter') + '</button>' +
        '</form>' +
      '</div>';

    document.body.appendChild(overlay);

    var form = overlay.querySelector('.dfl-gate-form');
    var input = overlay.querySelector('#dfl-gate-password');
    var err = overlay.querySelector('.dfl-gate-error');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      err.hidden = true;
      sha256(input.value).then(function (hash) {
        if (hash === GATE_PASSWORD_HASH) {
          unlock();
        } else {
          err.textContent = isAr ? 'كلمة المرور غير صحيحة.' : 'Incorrect password.';
          err.hidden = false;
          input.focus();
          input.select();
        }
      }).catch(function () {
        err.textContent = isAr ? 'تعذّر التحقق. افتح الموقع عبر HTTPS.' : 'Could not verify. Use HTTPS.';
        err.hidden = false;
      });
    });
  }

  if (document.body) {
    buildOverlay();
  } else {
    document.addEventListener('DOMContentLoaded', buildOverlay);
  }
})();
