#!/bin/bash

cd /home/tayyabcheema777/ali

if [ ! -d "playwright_venv" ]; then
    echo "❌ Playwright not installed yet!"
    echo ""
    echo "Please run: ./install_playwright.sh"
    echo ""
    exit 1
fi

source playwright_venv/bin/activate
python yahoo_mail_automation.py
