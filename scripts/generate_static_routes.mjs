#!/usr/bin/env node
/** Generate serve.json + _redirects so extensionless URLs map to .html files. */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const SKIP_DIRS = new Set([
  "node_modules",
  ".git",
  "outputs",
  "legacy",
  ".tmp_amer",
  "capsule-engine",
  "system",
  "operating-system",
  "assets/queue",
]);

function shouldSkip(fullPath) {
  const rel = path.relative(ROOT, fullPath).split(path.sep).join("/");
  if (rel.startsWith("assets/queue/")) return true;
  return rel.split("/").some((part) => SKIP_DIRS.has(part));
}

function collectHtmlFiles() {
  const files = [];

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!shouldSkip(full)) walk(full);
      } else if (entry.name.endsWith(".html") && !entry.name.startsWith(".")) {
        if (!shouldSkip(full)) files.push(full);
      }
    }
  }

  walk(ROOT);
  return files.sort();
}

function extensionlessRoute(relPosix) {
  if (relPosix === "index.html") return "/";
  return `/${relPosix.slice(0, -5)}`;
}

// Legacy WordPress (old dotforlife.com gardening site) → closest section.
// Keeps link equity and stops 404s for indexed /YYYY/MM/slug/ permalinks.
const LEGACY_REDIRECTS = [
  { source: "/wp-login.php", destination: "/" },
  { source: "/wp-admin", destination: "/" },
  { source: "/wp-admin/:path*", destination: "/" },
  { source: "/wp-content/:path*", destination: "/" },
  { source: "/wp-includes/:path*", destination: "/" },
  { source: "/category/:path*", destination: "/blog" },
  { source: "/tag/:path*", destination: "/blog" },
  { source: "/feed", destination: "/blog" },
  { source: "/comments/feed", destination: "/blog" },
];
for (let year = 2016; year <= 2025; year++) {
  LEGACY_REDIRECTS.push({ source: `/${year}/:path*`, destination: "/blog" });
}

// Static assets are referenced with ?v=<hash> query strings (cache-busting),
// so they can be cached immutably for a year.
const HEADERS = [
  {
    source: "/styles/**",
    headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
  },
  {
    source: "/scripts/**",
    headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
  },
  {
    source: "/assets/**",
    headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
  },
  {
    source: "/og/**",
    headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
  },
  {
    source: "/**",
    headers: [
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
    ],
  },
];

function main() {
  const rewrites = [];
  const redirectLines = [];

  for (const full of collectHtmlFiles()) {
    const rel = path.relative(ROOT, full).split(path.sep).join("/");
    const route = extensionlessRoute(rel);
    const dest = `/${rel}`;
    if (route === dest) continue;
    rewrites.push({ source: route, destination: dest });
    redirectLines.push(`${route} ${dest} 200`);
  }

  for (const r of LEGACY_REDIRECTS) {
    redirectLines.push(`${r.source} ${r.destination} 301`);
  }

  const serveCfg = { trailingSlash: false, redirects: LEGACY_REDIRECTS, headers: HEADERS, rewrites };
  fs.writeFileSync(
    path.join(ROOT, "serve.json"),
    `${JSON.stringify(serveCfg, null, 2)}\n`,
    "utf8",
  );
  fs.writeFileSync(
    path.join(ROOT, "_redirects"),
    `${redirectLines.join("\n")}\n`,
    "utf8",
  );
  // Cloudflare Pages / Netlify style caching + security headers
  const headerLines = [];
  for (const h of HEADERS) {
    headerLines.push(h.source);
    for (const kv of h.headers) headerLines.push(`  ${kv.key}: ${kv.value}`);
    headerLines.push("");
  }
  fs.writeFileSync(path.join(ROOT, "_headers"), headerLines.join("\n"), "utf8");
  console.log(
    `static routes: ${rewrites.length} rewrites + ${LEGACY_REDIRECTS.length} legacy redirects → serve.json + _redirects + _headers`,
  );
}

main();
