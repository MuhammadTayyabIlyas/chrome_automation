# Quick Playwright Installation Guide

## ⚡ Fast Installation (Copy & Paste These Commands)

Open your terminal and run these commands one by one:

```bash
# Step 1: Install system packages (requires your password)
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip

# Step 2: Go to the project directory
cd /home/tayyabcheema777/ali

# Step 3: Run the installation script
./install_playwright.sh
```

That's it! The script will handle everything else.

---

## 🎯 Or Run This ONE Command

```bash
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip && cd /home/tayyabcheema777/ali && ./install_playwright.sh
```

---

## ✅ After Installation

Run the Yahoo Mail automation:

```bash
cd /home/tayyabcheema777/ali
source playwright_venv/bin/activate
python yahoo_mail_automation.py
```

Or use the shortcut:

```bash
cd /home/tayyabcheema777/ali
./run_yahoo_automation.sh
```

---

## 🤔 What Will Happen?

1. **Browser Opens** - A Chromium browser window will open (visible, not headless)
2. **Goes to Yahoo Mail** - Automatically navigates to mail.yahoo.com
3. **Waits for Login** - You login manually (the script pauses)
4. **Script Detects Login** - Automatically detects when you're logged in
5. **Searches Emails** - Searches for "from:skyscanner"
6. **Selects All** - Clicks the "Select All" checkbox
7. **Marks as Spam** - Clicks the "Mark as Spam" button
8. **Done!** - All Skyscanner emails are now spam

---

## 🔧 Troubleshooting

### Error: "sudo: command not found"
You're probably not on Linux/WSL. Try:
```bash
python3 -m pip install playwright --user
python3 -m playwright install chromium
```

### Error: "permission denied"
Make the script executable:
```bash
chmod +x install_playwright.sh
```

### Error: "playwright: command not found"
Activate the virtual environment first:
```bash
source playwright_venv/bin/activate
```

---

## 📖 What You're Installing

- **python3-venv** - Creates isolated Python environments
- **python3-pip** - Python package installer
- **playwright** - Browser automation library
- **chromium** - The browser Playwright will control

Total size: ~200-300 MB

---

## 🚀 Ready? Run This Now!

```bash
sudo apt-get install -y python3-venv python3-pip && cd /home/tayyabcheema777/ali && ./install_playwright.sh
```
