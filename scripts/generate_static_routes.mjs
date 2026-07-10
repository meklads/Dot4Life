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

  const serveCfg = { trailingSlash: false, rewrites };
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
  console.log(
    `static routes: ${rewrites.length} rewrites → serve.json + _redirects`,
  );
}

main();
