#!/usr/bin/env python3
"""
Gmail Auto Delete - Use PyAutoGUI to click Select All and Delete
UPDATED with precise coordinates from ui-element-locator

This script:
1. Moves cursor to Select All checkbox (505, 176)
2. Clicks it
3. Waits 2 seconds
4. Clicks 'Select all conversations' link (743, 351)
5. Waits 2 seconds
6. Moves cursor to Delete button (614, 283)
7. Clicks it

Coordinates are pixel-perfect center points!
"""

import pyautogui
import time

def print_step(step, message, status=""):
    """Print formatted step message"""
    icons = {"info": "ℹ️", "success": "✅", "wait": "⏳", "work": "🔧"}
    icon = icons.get(status, "▶️")
    print(f"{icon} [{step}] {message}")

def main():
    """Automate Gmail deletion with PyAutoGUI"""

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     Gmail Auto Delete - PyAutoGUI (PRECISE)             ║
    ║                                                          ║
    ║  This script will:                                      ║
    ║  1. Click Select All checkbox at (505, 176)             ║
    ║  2. Wait 2 seconds                                      ║
    ║  3. Click 'Select all conversations' at (743, 351)      ║
    ║  4. Wait 2 seconds                                      ║
    ║  5. Click Delete button at (614, 283)                   ║
    ║                                                          ║
    ║  Pixel-perfect coordinates from ui-element-locator!     ║
    ║  ⚠️  Make sure Gmail is open and visible!               ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Countdown before starting
    print_step("PREPARE", "Starting automation in 3 seconds...", "wait")
    print("   Make sure Gmail window is visible and active!")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    print("\n" + "="*60)

    # Step 1: Click Select All checkbox (PRECISE)
    print_step("STEP 1", "Moving cursor to Select All checkbox (505, 176)", "work")
    pyautogui.moveTo(505, 176, duration=0.5)
    time.sleep(0.5)

    print_step("STEP 1", "Clicking Select All checkbox", "work")
    pyautogui.click()
    print_step("STEP 1", "Select All checkbox clicked!", "success")

    # Wait for selection
    print_step("WAIT", "Waiting 2 seconds for emails to be selected...", "wait")
    time.sleep(2)

    # Step 2: Click "Select all conversations" link
    print_step("STEP 2", "Moving to 'Select all conversations' link (743, 351)", "work")
    pyautogui.moveTo(743, 351, duration=0.5)
    time.sleep(0.5)

    print_step("STEP 2", "Clicking to select ALL conversations", "work")
    pyautogui.click()
    print_step("STEP 2", "'Select all' link clicked!", "success")

    print_step("WAIT", "Waiting 2 seconds...", "wait")
    time.sleep(2)

    # Step 3: Click Delete button (PRECISE)
    print_step("STEP 3", "Moving cursor to Delete button (614, 283)", "work")
    pyautogui.moveTo(614, 283, duration=0.5)
    time.sleep(0.5)

    print_step("STEP 3", "Clicking Delete button", "work")
    pyautogui.click()
    print_step("STEP 3", "Delete button clicked!", "success")

    print("\n" + "="*60)
    print_step("DONE", "Automation completed!", "success")
    print("="*60)
    print("\n💡 Check your Gmail to verify emails were deleted.")

if __name__ == "__main__":
    try:
        # Get screen size for verification
        width, height = pyautogui.size()
        print(f"\n📏 Screen size: {width}x{height}")

        # Safety check
        current_x, current_y = pyautogui.position()
        print(f"🖱️  Current cursor position: ({current_x}, {current_y})\n")

        main()

    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
