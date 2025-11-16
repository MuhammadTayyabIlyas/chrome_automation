# Gmail Skyscanner Email Auto-Delete

Automated script to delete Skyscanner emails from Gmail using PowerShell automation.

## ✅ Working Solution

This automation has been calibrated and verified to work correctly!

### Quick Start

```bash
./run_gmail_complete.sh
```

That's it! The script will:
1. Open Gmail with Skyscanner email search
2. Wait 15 seconds for you to login
3. Automatically click "Select All" checkbox
4. Automatically click "Select all conversations" link
5. Automatically click "Delete" button

## 📍 Verified Coordinates

These coordinates have been tested and verified:

- **Select All Checkbox:** (506, 381)
- **Select All Link:** (600, 410)
- **Delete Button:** (777, 376)

## 📁 Main Files

### Essential Files
- `run_gmail_complete.sh` - **Main script to run** (opens Gmail + runs automation)
- `gmail_auto_delete.ps1` - PowerShell automation script (called by main script)
- `FINAL_COORDINATES.md` - Coordinate documentation
- `README.md` - This file

### Reference Files
- `chrome_gmail.png` - Gmail screenshot for reference
- `gmail_elements_annotated.png` - Annotated screenshot showing elements

## 🚀 Usage

### Basic Usage
```bash
./run_gmail_complete.sh
```

### What Happens:
1. Gmail opens in Chrome with search: `from:no-reply@sender.skyscanner.com`
2. Script waits 15 seconds for you to login (if needed)
3. Automation clicks:
   - Select All checkbox (506, 381)
   - "Select all conversations" link (600, 410)
   - Delete button (777, 376)
4. Emails are deleted!

## ⚙️ Requirements

- **Windows Subsystem for Linux (WSL)** - You're already using it
- **Google Chrome** - Installed on Windows
- **PowerShell** - Pre-installed on Windows
- **Gmail Account** - With Skyscanner emails to delete

## 🎯 How It Works

1. **Opens Chrome** via WSL command
2. **Navigates to Gmail** with pre-filled search query
3. **Waits for login** (15 seconds)
4. **Runs PowerShell script** that:
   - Moves cursor to exact coordinates
   - Clicks each element with 500ms delay
   - Waits between steps for Gmail to respond

## 📝 Notes

- Coordinates are specific to your screen resolution
- Gmail must be maximized for consistent results
- The script pauses between clicks to let Gmail load
- You can watch the cursor move to verify positions

## 🔧 Troubleshooting

### Clicks are off-target
- Make sure Gmail is maximized
- Check your screen resolution hasn't changed
- Verify Gmail layout hasn't updated

### Gmail not opening
- Check Chrome path: `/mnt/c/Program Files/Google/Chrome/Application/chrome.exe`
- Make sure Chrome is installed

### Script doesn't run
- Make sure script is executable: `chmod +x run_gmail_complete.sh`
- Check WSL is working properly

## 🎉 Success!

You now have a fully automated Gmail cleanup tool that:
- ✅ Opens the correct Gmail search
- ✅ Selects all matching emails
- ✅ Deletes them with one command

Enjoy your automated email cleanup! 🚀
