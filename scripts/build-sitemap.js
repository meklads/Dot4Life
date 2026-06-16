#!/usr/bin/env node
/* ═════════════════════════════════════════════════════
   build-sitemap.js — Sitemap Generator
   Reads /articles.json and generates sitemap-content.xml
   Run: node scripts/build-sitemap.js
   ═════════════════════════════════════════════════════ */

const fs = require('fs');
const path = require('path');

const JSON_PATH = path.join(__dirname, '..', 'articles.json');
const OUTPUT_PATH = path.join(__dirname, '..', 'sitemap-content.xml');
const BASE_URL = 'https://www.dotforlife.com';

// Static pages to include in sitemap
const STATIC_PAGES = [
  { url: '/', priority: '1.0', changefreq: 'daily' },
  { url: '/health.html', priority: '0.9', changefreq: 'weekly' },
  { url: '/finance.html', priority: '0.9', changefreq: 'weekly' },
  { url: '/real-estate.html', priority: '0.9', changefreq: 'weekly' },
  { url: '/travel.html', priority: '0.9', changefreq: 'weekly' },
  { url: '/islamic.html', priority: '0.9', changefreq: 'weekly' },
  { url: '/family.html', priority: '0.8', changefreq: 'weekly' },
  { url: '/fitness.html', priority: '0.8', changefreq: 'weekly' },
  { url: '/productivity.html', priority: '0.7', changefreq: 'weekly' },
  { url: '/plants.html', priority: '0.7', changefreq: 'weekly' },
  { url: '/about.html', priority: '0.5', changefreq: 'monthly' },
  { url: '/our-vision.html', priority: '0.5', changefreq: 'monthly' },
  { url: '/blog.html', priority: '0.8', changefreq: 'daily' },
  { url: '/archive.html', priority: '0.7', changefreq: 'daily' },
  { url: '/library.html', priority: '0.6', changefreq: 'weekly' },
  { url: '/pregnancy-journey.html', priority: '0.8', changefreq: 'weekly' },
];

// Tool pages
const TOOL_PAGES = [
  '/tools/bmi-calculator.html', '/tools/calorie-calculator.html',
  '/tools/water-calculator.html', '/tools/body-fat-calculator.html',
  '/tools/pregnancy-calculator.html', '/tools/age-calculator.html',
  '/tools/one-rep-max.html', '/tools/ramadan-calorie-calculator.html',
  '/tools/mortgage-calculator.html', '/tools/salary-calculator.html',
  '/tools/savings-goal.html', '/tools/monthly-budget.html',
  '/tools/roi-calculator.html', '/tools/rental-yield-calculator.html',
  '/tools/currency-converter.html', '/tools/travel-budget.html',
  '/tools/packing-checklist.html', '/tools/travel-tips.html',
  '/tools/prayer-times.html', '/tools/qibla.html',
  '/tools/zakat-calculator.html', '/tools/hijri-converter.html',
  '/tools/inheritance-calculator.html',
];

function buildSitemap() {
  if (!fs.existsSync(JSON_PATH)) {
    console.error('articles.json not found at', JSON_PATH);
    process.exit(1);
  }

  const articles = JSON.parse(fs.readFileSync(JSON_PATH, 'utf-8'));
  if (!Array.isArray(articles)) {
    console.error('articles.json is not an array');
    process.exit(1);
  }

  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
  xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n';
  xml += '  xmlns:xhtml="http://www.w3.org/1999/xhtml">\n';

  // Static pages
  STATIC_PAGES.forEach(function(page) {
    xml += '  <url>\n';
    xml += '    <loc>' + BASE_URL + page.url + '</loc>\n';
    xml += '    <priority>' + page.priority + '</priority>\n';
    xml += '    <changefreq>' + page.changefreq + '</changefreq>\n';
    xml += '  </url>\n';
  });

  // Tool pages
  TOOL_PAGES.forEach(function(toolUrl) {
    xml += '  <url>\n';
    xml += '    <loc>' + BASE_URL + toolUrl + '</loc>\n';
    xml += '    <priority>0.6</priority>\n';
    xml += '    <changefreq>monthly</changefreq>\n';
    xml += '  </url>\n';
  });

  // Articles
  articles.forEach(function(article) {
    var url = article.url || '';
    var urlEn = article.url_en || '';
    var date = article.date || new Date().toISOString().split('T')[0];

    if (!url) return;

    xml += '  <url>\n';
    xml += '    <loc>' + BASE_URL + url + '</loc>\n';
    xml += '    <lastmod>' + date + '</lastmod>\n';
    xml += '    <priority>0.7</priority>\n';
    xml += '    <changefreq>monthly</changefreq>\n';
    // hreflang alternate if English version exists
    if (urlEn && urlEn !== url) {
      xml += '    <xhtml:link rel="alternate" hreflang="en" href="' + BASE_URL + urlEn + '"/>\n';
      xml += '    <xhtml:link rel="alternate" hreflang="ar" href="' + BASE_URL + url + '"/>\n';
    } else {
      xml += '    <xhtml:link rel="alternate" hreflang="x-default" href="' + BASE_URL + url + '"/>\n';
    }
    xml += '  </url>\n';

    // Also add the English version as separate URL
    if (urlEn && urlEn !== url) {
      xml += '  <url>\n';
      xml += '    <loc>' + BASE_URL + urlEn + '</loc>\n';
      xml += '    <lastmod>' + date + '</lastmod>\n';
      xml += '    <priority>0.7</priority>\n';
      xml += '    <changefreq>monthly</changefreq>\n';
      xml += '    <xhtml:link rel="alternate" hreflang="en" href="' + BASE_URL + urlEn + '"/>\n';
      xml += '    <xhtml:link rel="alternate" hreflang="ar" href="' + BASE_URL + url + '"/>\n';
      xml += '  </url>\n';
    }
  });

  xml += '</urlset>\n';

  fs.writeFileSync(OUTPUT_PATH, xml, 'utf-8');
  console.log('sitemap-content.xml generated with ' +
    (STATIC_PAGES.length + TOOL_PAGES.length + articles.length) + ' URLs');
  console.log('Output:', OUTPUT_PATH);
}

buildSitemap();
