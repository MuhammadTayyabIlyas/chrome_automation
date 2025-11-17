#!/bin/bash
# Simple script to open Yahoo Mail and Google Scholar in Windows Chrome from WSL

echo "═══════════════════════════════════════════════════════════"
echo "  Opening Yahoo Mail and Google Scholar in Windows Chrome"
echo "═══════════════════════════════════════════════════════════"

# Chrome arguments to prevent restore prompt
CHROME_ARGS="--disable-session-crashed-bubble --disable-infobars --no-first-run --no-default-browser-check"

# Open Yahoo Mail in Chrome
cmd.exe /c start chrome $CHROME_ARGS "https://mail.yahoo.com"
echo "✅ Opened Yahoo Mail in Chrome"

sleep 2

# Open Google Scholar in a new Chrome tab
cmd.exe /c start chrome "https://scholar.google.com/"
echo "✅ Opened Google Scholar in Chrome"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Both pages are now open in Windows Chrome!"
echo "  You can now login and use Yahoo Mail normally."
echo "═══════════════════════════════════════════════════════════"
