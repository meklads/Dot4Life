/**
 * Dot4Life — site-wide static config (no backend required)
 * Email list: wire Brevo/Sibforms IDs here when ready (Phase 1+)
 */
(function (global) {
  'use strict';

  var DFL = global.DFL || {};

  DFL.staticMode = true;
  DFL.capsulesJson = '/data/capsules-published.json';
  DFL.capsulesJsonVersion = '20260619f';

  /** @type {'brevo'|'mailto'|'none'} */
  DFL.emailListProvider = 'brevo';

  DFL.emailList = {
    /** Friday Letter / general newsletter (Sibforms — already on homepage) */
    fridayLetterUrl: 'https://fe27e801.sibforms.com/serve/MUIFAMkd5JF8otYrMcB78hsqyZpw5wTN_7YySpRiweUlDxrkVYKYCrrPbD7kVPKDWPtR1Y2FuJm7DX7fLUYM9lS2Xl5e3DHTOOXRA9Q8TTew25sU4ZeRTgjfcJozA-eFIUVjCLZBe8t7DxqSAqOCSlwjdt4XsxxtSQ9MVfxbhd5cWsvg3rPEeezNhOqv4Dkk4BM4cyB7bqUPzy7VAQ==',
    /** Pregnancy weekly list — set when Brevo list is created */
    pregnancyListUrl: null,
    /** Contact form opt-in list — set when Brevo list is created */
    contactListUrl: null,
    contactEmail: 'hello@dotforlife.com',
  };

  /**
   * Subscribe email to a Sibforms/Brevo endpoint (no-cors — fire-and-forget).
   * @param {string} url
   * @param {string} email
   * @param {Record<string,string>} [extra]
   */
  DFL.subscribeEmail = function (url, email, extra) {
    if (!url || !email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return Promise.resolve(false);
    var body = new URLSearchParams(Object.assign({ EMAIL: email }, extra || {}));
    return fetch(url, { method: 'POST', mode: 'no-cors', body: body }).then(function () { return true; }).catch(function () { return false; });
  };

  DFL.capsulesJsonUrl = function () {
    return DFL.capsulesJson + '?v=' + DFL.capsulesJsonVersion;
  };

  global.DFL = DFL;
})(typeof window !== 'undefined' ? window : globalThis);
