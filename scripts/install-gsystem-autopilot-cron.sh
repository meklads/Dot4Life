#!/bin/bash
# تثبيت تشغيل GSystem Autopilot كل 15 دقيقة على macOS (جهاز التطوير)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/com.dotforlife.gsystem-autopilot.plist"
LOG="$ROOT/outputs/logs/gsystem-autopilot.log"

mkdir -p "$ROOT/outputs/logs"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.dotforlife.gsystem-autopilot</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>python3</string>
    <string>$ROOT/scripts/gsystem_autopilot.py</string>
    <string>--push</string>
    <string>--desktop-notify</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$ROOT</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PYTHONPATH</key>
    <string>$ROOT/scripts</string>
  </dict>
  <key>StartInterval</key>
  <integer>900</integer>
  <key>StandardOutPath</key>
  <string>$LOG</string>
  <key>StandardErrorPath</key>
  <string>$LOG</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✅ GSystem Autopilot كل 15 دقيقة — log: $LOG"
echo "   inbox: $ROOT/operating-system/inbox/"
