/**
 * Dot4Life — unified email list helpers (static / Brevo Sibforms)
 * Requires scripts/dfl-config.js loaded first.
 */
(function (global) {
  'use strict';

  var DFL = global.DFL || {};

  DFL.subscribeFridayLetter = function (email) {
    return DFL.subscribeEmail(DFL.emailList.fridayLetterUrl, email);
  };

  DFL.subscribePregnancyList = function (email, name) {
    var url = DFL.emailList.pregnancyListUrl;
    if (!url) return Promise.resolve(false);
    return DFL.subscribeEmail(url, email, { FIRSTNAME: name || '' });
  };

  DFL.subscribeContactList = function (email, name) {
    var url = DFL.emailList.contactListUrl || DFL.emailList.fridayLetterUrl;
    return DFL.subscribeEmail(url, email, { FIRSTNAME: name || '' });
  };

  global.DFL = DFL;
})(typeof window !== 'undefined' ? window : globalThis);
