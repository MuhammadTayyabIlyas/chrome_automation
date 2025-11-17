#!/bin/bash

# Gmail Delete Skyscanner Emails - Run Script

echo "Setting up environment for Gmail automation..."

# Activate virtual environment if it exists, or use system Python
if [ -d "playwright_venv" ]; then
    echo "Activating playwright virtual environment..."
    source playwright_venv/bin/activate
else
    echo "No virtual environment found, using system Python..."
fi

# Make sure playwright is installed
echo "Checking Playwright installation..."
python3 -c "import playwright" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Playwright not found. Installing..."
    pip3 install playwright
    playwright install chromium
fi

# Run the script
echo ""
echo "Starting Gmail automation script..."
echo ""
python3 gmail_delete_skyscanner.py
