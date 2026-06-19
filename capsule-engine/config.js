/**
 * d4l1-capsule-engine — Configuration
 *
 * ⚠️ SECURITY: Never hardcode passwords in this file.
 * Always set ADMIN_PASSWORD or ADMIN_PASSWORD_HASH via environment variables.
 *
 * To generate a hash for your password, run:
 *   node -e "const c=require('crypto');console.log(c.createHash('sha256').update('YOUR_PASSWORD').digest('hex'))"
 */

const crypto = require('crypto');

function sha256(str) {
  return crypto.createHash('sha256').update(str).digest('hex');
}

module.exports = {
  PORT: process.env.PORT || 3030,

  // Admin username
  ADMIN_USERNAME: process.env.ADMIN_USERNAME || 'admin',

  // SHA-256 hash of admin password — MUST be set via env in production
  // Will be null if no env var provided, causing admin login to fail safely
  ADMIN_PASSWORD_HASH: process.env.ADMIN_PASSWORD_HASH
    || (process.env.ADMIN_PASSWORD ? sha256(process.env.ADMIN_PASSWORD) : null),

  // CORS: which origins can call the public API
  // In production, restrict to your domain
  CORS_ORIGINS: process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',').map(s => s.trim()).filter(Boolean)
    : ['http://localhost', 'https://www.dotforlife.com', 'https://dotforlife.com'],

  // Whether to enforce SSL certificate validation (false for dev, true for production)
  DB_SSL_REJECT_UNAUTHORIZED: process.env.DB_SSL_REJECT_UNAUTHORIZED === 'true',

  // Session expiry in hours
  SESSION_HOURS: parseInt(process.env.SESSION_HOURS || '8'),
};
