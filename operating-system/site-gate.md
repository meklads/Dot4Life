# Site gate (pre-launch password)

Protects the public GitHub Pages site until official launch.

## How it works

- `scripts/site-gate.js` runs on every HTML page (blocking, in `<head>`).
- Password is checked via SHA-256 hash — **plain password is not stored in the repo**.
- Successful login persists in `sessionStorage` for the browser tab/session.

## Launch publicly

In `scripts/site-gate.js`, set:

```js
var SITE_GATE_ENABLED = false;
```

Commit, push, and redeploy. Remove or leave gate code in place (disabled).

Also restore `robots.txt` to allow crawling (see comment at top of file for pre-launch state).

## Change password

1. Generate new hash: `echo -n 'YOUR_PASSWORD' | shasum -a 256`
2. Update `GATE_PASSWORD_HASH` in `scripts/site-gate.js`
3. Bump `GATE_STORAGE_KEY` (e.g. `v2`) so old sessions invalidate

## Security note

This is **casual preview protection** for a static site, not enterprise-grade auth. Determined users can bypass client-side gates. For stronger protection, use Cloudflare Access or Netlify password protection.
