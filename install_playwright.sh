#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Playwright Full Installation Script                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root/sudo
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please do NOT run this script with sudo"
    echo "   The script will ask for sudo when needed"
    exit 1
fi

# Step 1: Install system packages
echo "═══════════════════════════════════════════════════════"
echo "Step 1: Installing system dependencies"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📦 This requires sudo to install python3-venv and python3-pip"
echo ""

sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

if [ $? -ne 0 ]; then
    echo "❌ Failed to install system packages"
    exit 1
fi

echo "✅ System packages installed"
echo ""

# Step 2: Create virtual environment
echo "═══════════════════════════════════════════════════════"
echo "Step 2: Creating Python virtual environment"
echo "═══════════════════════════════════════════════════════"
echo ""

cd /home/tayyabcheema777/ali

if [ -d "playwright_venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "   Delete and recreate? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf playwright_venv
        echo "🗑️  Deleted old virtual environment"
    else
        echo "ℹ️  Using existing virtual environment"
    fi
fi

if [ ! -d "playwright_venv" ]; then
    python3 -m venv playwright_venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment ready"
fi

echo ""

# Step 3: Activate and install Playwright
echo "═══════════════════════════════════════════════════════"
echo "Step 3: Installing Playwright"
echo "═══════════════════════════════════════════════════════"
echo ""

source playwright_venv/bin/activate

pip install --upgrade pip
pip install playwright

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright"
    exit 1
fi

echo "✅ Playwright installed"
echo ""

# Step 4: Install browser drivers
echo "═══════════════════════════════════════════════════════"
echo "Step 4: Installing Chromium browser driver"
echo "═══════════════════════════════════════════════════════"
echo ""

playwright install chromium

if [ $? -ne 0 ]; then
    echo "⚠️  Playwright installed but browser installation may need system dependencies"
    echo "📦 Attempting to install browser dependencies..."
    sudo playwright install-deps chromium
    playwright install chromium
fi

echo "✅ Chromium browser installed"
echo ""

# Step 5: Create activation script
echo "═══════════════════════════════════════════════════════"
echo "Step 5: Creating activation script"
echo "═══════════════════════════════════════════════════════"
echo ""

cat > activate_playwright.sh << 'ACTIVATE_SCRIPT'
#!/bin/bash
cd /home/tayyabcheema777/ali
source playwright_venv/bin/activate
echo "✅ Playwright environment activated!"
echo ""
echo "You can now run:"
echo "  python yahoo_login_demo.py"
echo ""
ACTIVATE_SCRIPT

chmod +x activate_playwright.sh

echo "✅ Activation script created: activate_playwright.sh"
echo ""

# Step 6: Test installation
echo "═══════════════════════════════════════════════════════"
echo "Step 6: Testing Playwright installation"
echo "═══════════════════════════════════════════════════════"
echo ""

python -c "from playwright.sync_api import sync_playwright; print('✅ Playwright import successful!')"

if [ $? -ne 0 ]; then
    echo "❌ Playwright test failed"
    exit 1
fi

echo ""

# Final summary
echo "╔════════════════════════════════════════════════════════╗"
echo "║              Installation Complete! 🎉                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Summary:"
echo "   ✅ System packages installed"
echo "   ✅ Virtual environment created"
echo "   ✅ Playwright installed"
echo "   ✅ Chromium browser installed"
echo "   ✅ Ready to use!"
echo ""
echo "🚀 To run the Yahoo automation:"
echo ""
echo "   Method 1 - Direct run:"
echo "   $ source playwright_venv/bin/activate"
echo "   $ python yahoo_login_demo.py"
echo ""
echo "   Method 2 - Using activation script:"
echo "   $ ./activate_playwright.sh"
echo "   $ python yahoo_login_demo.py"
echo ""
echo "   Method 3 - One command:"
echo "   $ playwright_venv/bin/python yahoo_login_demo.py"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
