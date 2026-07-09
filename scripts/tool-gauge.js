/**
 * DOTFORLIFE — shared range gauge for flagship tools.
 * Sets marker position (%) and optional label text.
 */
(function (global) {
  'use strict';

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function toPercent(value, min, max) {
    if (max <= min) return 0;
    return clamp((value - min) / (max - min), 0, 1) * 100;
  }

  /**
   * @param {HTMLElement|string} root
   * @param {{ value: number, min?: number, max?: number, label?: string, fillPercent?: number, hidden?: boolean }} opts
   */
  function setToolGauge(root, opts) {
    var el = typeof root === 'string' ? document.getElementById(root) : root;
    if (!el || !opts) return;

    var min = opts.min != null ? opts.min : parseFloat(el.getAttribute('data-min') || '0');
    var max = opts.max != null ? opts.max : parseFloat(el.getAttribute('data-max') || '100');
    var pct = toPercent(opts.value, min, max);

    var marker = el.querySelector('.tool-gauge-marker');
    var fill = el.querySelector('.tool-gauge-fill');
    var label = el.querySelector('.tool-gauge-label');

    if (marker) {
      marker.style.insetInlineStart = pct + '%';
      marker.setAttribute('aria-valuenow', String(Math.round(opts.value * 10) / 10));
      marker.setAttribute('aria-valuemin', String(min));
      marker.setAttribute('aria-valuemax', String(max));
    }
    if (fill != null && opts.fillPercent != null) {
      fill.style.width = clamp(opts.fillPercent, 0, 100) + '%';
    }
    if (label && opts.label != null) {
      label.textContent = opts.label;
    }

    if (opts.hidden) {
      el.hidden = true;
      el.classList.remove('is-active');
    } else {
      el.hidden = false;
      el.classList.add('is-active');
    }
  }

  global.dflSetToolGauge = setToolGauge;
})(typeof window !== 'undefined' ? window : this);
