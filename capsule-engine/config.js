/**
 * d4l1-capsule-engine — Configuration
 *
 * SETUP: Change ADMIN_PASSWORD below (or set via environment variable).
 * The value stored here is a SHA-256 hash of the password.
 *
 * To generate a hash for your password, run:
 *   node -e "const c=require('crypto');console.log(c.createHash('sha256').update('YOUR_PASSWORD').digest('hex'))"
 *
 * Default password: dotforlife2026
 * (change before deploying to production!)
 */

const crypto = require('crypto');

function sha256(str) {
  return crypto.createHash('sha256').update(str).digest('hex');
}

module.exports = {
  PORT: process.env.PORT || 3030,

  // SHA-256 hash of admin password
  // Default: dotforlife2026  →  change before going live
  ADMIN_PASSWORD_HASH: process.env.ADMIN_PASSWORD_HASH
    || sha256(process.env.ADMIN_PASSWORD || 'dotforlife2026'),

  // CORS: which origins can call the public API
  // In production, restrict to your domain
  CORS_ORIGINS: (process.env.CORS_ORIGINS || 'http://localhost,https://www.dotforlife.com,https://dotforlife.com').split(','),

  // Session expiry in hours
  SESSION_HOURS: parseInt(process.env.SESSION_HOURS || '8'),
};
