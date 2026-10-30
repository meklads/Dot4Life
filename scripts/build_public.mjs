/**
 * Build the public site folder (_site) that the server serves.
 * Copies the repo root but leaves out internal files: team docs, reports,
 * QA scripts, Python/Markdown files and build config, so they are never
 * reachable on dotforlife.com.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "_site");

const EXCLUDED_DIRS = new Set([
  ".git", ".github", "node_modules", "_site",
  "operating-system", "reports", "outputs", "skills", "legacy",
  "capsule-engine", "visual-governance",
]);
const EXCLUDED_EXT = new Set([".md", ".py", ".pyc", ".cjs", ".mjs", ".sh", ".csv", ".log", ".bak", ".toml"]);
const EXCLUDED_FILES = new Set(["package.json", "package-lock.json", ".gitignore", ".DS_Store"]);

fs.rmSync(OUT, { recursive: true, force: true });

let copied = 0;
const filter = (src) => {
  const rel = path.relative(ROOT, src);
  const parts = rel.split(path.sep);
  if (parts.some((p) => EXCLUDED_DIRS.has(p))) return false;
  const base = parts[parts.length - 1];
  if (EXCLUDED_FILES.has(base)) return false;
  if (EXCLUDED_EXT.has(path.extname(base).toLowerCase())) return false;
  if (fs.statSync(src).isFile()) copied++;
  return true;
};
fs.mkdirSync(OUT);
for (const entry of fs.readdirSync(ROOT)) {
  const src = path.join(ROOT, entry);
  if (!filter(src)) continue;
  fs.cpSync(src, path.join(OUT, entry), { recursive: true, filter });
}

if (!fs.existsSync(path.join(OUT, "index.html")) || !fs.existsSync(path.join(OUT, "serve.json"))) {
  console.error("build_public: index.html or serve.json missing from _site");
  process.exit(1);
}
console.log(`build_public: ${copied} files copied to _site`);
