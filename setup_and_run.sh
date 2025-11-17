#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Yahoo Login Demo - Setup & Run                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install Playwright
echo "📦 Installing Playwright..."
pip3 install playwright

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright"
    exit 1
fi

echo "✓ Playwright installed"
echo ""

# Install browser drivers
echo "🌐 Installing Chromium browser driver..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Chromium driver"
    exit 1
fi

echo "✓ Chromium driver installed"
echo ""

# Make the Python script executable
chmod +x yahoo_login_demo.py

echo "╔════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Running Yahoo Login Demo..."
echo ""

# Run the script
python3 yahoo_login_demo.py
