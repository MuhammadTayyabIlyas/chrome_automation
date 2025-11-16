#!/bin/bash
# Complete Gmail automation - Opens Gmail and runs PowerShell automation

echo "════════════════════════════════════════════════════════"
echo "  Gmail Complete Automation"
echo "════════════════════════════════════════════════════════"
echo ""

# Step 1: Open Gmail with search
echo "Step 1: Opening Gmail with Skyscanner search..."
cmd.exe /c start chrome "https://mail.google.com/mail/u/0/#search/from%3Ano-reply%40sender.skyscanner.com"
echo "✅ Gmail opened!"

# Wait for page load
echo ""
echo "Step 2: Waiting for page to load..."
echo "   Please login if needed and wait for search results"
echo ""
echo "⏳ Waiting 15 seconds for you to login and page to load..."
sleep 15

# Step 3: Run PowerShell automation
echo ""
echo "Step 3: Running automation to click Select All and Delete..."
echo ""

# Convert path to Windows format and run PowerShell script
WIN_PATH=$(wslpath -w "$(pwd)/gmail_auto_delete.ps1")
powershell.exe -ExecutionPolicy Bypass -File "$WIN_PATH"

echo ""
echo "✅ Complete! Check your Gmail window."
