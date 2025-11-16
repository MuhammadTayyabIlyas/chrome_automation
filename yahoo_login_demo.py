#!/usr/bin/env python3
"""
Yahoo Login Demo with Manual Authentication - Windows 11 Chrome Compatible
This script:
1. Opens Yahoo Mail directly in Chrome
2. Checks if already logged in
3. Handles cookie consent
4. Waits for manual verification code entry
5. Provides extended time for 2FA/verification
"""

from playwright.sync_api import sync_playwright
import time
import os
import platform

def is_login_page(page):
    """
    Check if current page is a login page
    Returns True if URL contains 'login' or page has password input
    """
    try:
        url_check = "login" in page.url.lower()
        password_input = page.query_selector("input[type='password']") is not None
        email_input = page.query_selector("input[type='email'], input[name='username']") is not None
        return url_check or password_input or email_input
    except:
        return False

def is_logged_in(page):
    """
    Check if user is logged in to Yahoo Mail
    """
    try:
        # Check for Yahoo Mail specific logged-in indicators
        logged_in_indicators = [
            '[data-test-id="app-canvas"]',  # Yahoo Mail main canvas
            'button[data-test-id="compose-button"]',  # Compose button
            '[aria-label*="Inbox"]',  # Inbox label
            'button[aria-label*="Settings"]',  # Settings button
            '[data-test-id="message-list"]',  # Message list
        ]

        for selector in logged_in_indicators:
            if page.query_selector(selector):
                return True

        # Also check URL pattern for logged-in state
        if "mail.yahoo.com/d/" in page.url:
            return True

        return False
    except:
        return False

def accept_cookies(page):
    """
    Try to accept cookie consent if present
    """
    print("🍪 Checking for cookie consent banner...")

    cookie_selectors = [
        'button:has-text("Accept")',
        'button:has-text("Accept all")',
        'button:has-text("Agree")',
        'button:has-text("I agree")',
        'button[name="agree"]',
        'button[name="accept"]',
        'button.accept',
        'button#consent-accept',
        '[class*="accept"][class*="cookie"]',
        '[class*="consent-accept"]'
    ]

    for selector in cookie_selectors:
        try:
            element = page.query_selector(selector)
            if element and element.is_visible():
                print(f"✓ Found cookie consent button: {selector}")
                element.click()
                time.sleep(2)
                print("✓ Cookie consent accepted")
                return True
        except:
            continue

    print("ℹ️  No cookie consent banner found (or already accepted)")
    return False

def main():
    with sync_playwright() as p:
        # Detect Windows 11 and use Chrome if available
        print("🚀 Launching browser...")
        print(f"ℹ️  Platform: {platform.system()}")

        # Launch with Chrome channel for Windows 11
        browser_args = {
            'headless': False,  # Show browser window
            'slow_mo': 300,     # Slow down operations for visibility
            'args': [
                '--start-maximized',  # Start maximized
                '--disable-blink-features=AutomationControlled',  # Less detectable
            ]
        }

        # Use your specific Chrome installation
        print("🌐 Launching your Chrome browser...")
        try:
            # Path to your Chrome browser
            chrome_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

            browser = p.chromium.launch(
                executable_path=chrome_path,
                **browser_args
            )
            print("✓ Chrome browser launched successfully!")
        except Exception as e:
            print(f"⚠️  Could not launch Chrome at {chrome_path}")
            print(f"   Error: {e}")
            print("   Trying default Chromium...")
            browser = p.chromium.launch(**browser_args)

        # Create browser context with larger viewport
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Create new page
        page = context.new_page()

        # STEP 1: Try Yahoo Mail directly first
        print("\n" + "="*60)
        print("STEP 1: Checking Yahoo Mail directly...")
        print("="*60)
        print("📬 Navigating to Yahoo Mail...")

        try:
            page.goto("https://mail.yahoo.com", wait_until='domcontentloaded', timeout=30000)
            time.sleep(5)  # Give page time to load

            # Check if already logged in
            if is_logged_in(page):
                print("✅ Already logged in! Inbox opened successfully!")
                print("\n" + "="*60)
                print("🎉 SUCCESS - You're in your Yahoo Mail inbox!")
                print("="*60)

                # Keep browser open for user
                print("\n💡 Browser will stay open for 2 minutes...")
                print("   (Close manually when done)")
                time.sleep(120)
                browser.close()
                return

            print("ℹ️  Not logged in yet. Checking login page...")

        except Exception as e:
            print(f"⚠️  Error loading Yahoo Mail: {e}")

        time.sleep(3)

        # STEP 2: Accept cookies if present
        print("\n" + "="*60)
        print("STEP 2: Handling cookie consent...")
        print("="*60)
        accept_cookies(page)
        time.sleep(2)

        # STEP 3: Check if we need to sign in
        print("\n" + "="*60)
        print("STEP 3: Checking login status...")
        print("="*60)

        if not is_logged_in(page):
            # Try to find and click "Sign In" button
            print("🔍 Looking for Sign In button...")
            sign_in_selectors = [
                'a:has-text("Sign in")',
                'button:has-text("Sign in")',
                'a[href*="login"]',
                'a.sign-in',
                '#ybarAccountMenu',
                '[data-ylk*="sign"]'
            ]

            clicked = False
            for selector in sign_in_selectors:
                try:
                    element = page.wait_for_selector(selector, timeout=3000)
                    if element and element.is_visible():
                        print(f"✓ Found sign in button: {selector}")
                        element.click()
                        clicked = True
                        time.sleep(3)
                        break
                except:
                    continue

            if not clicked:
                print("⚠️  Could not find sign in button automatically")
                print("📌 Please click 'Sign In' manually in the browser window")
                time.sleep(5)

        # STEP 4: Wait for manual login with verification code support
        if is_login_page(page) or not is_logged_in(page):
            print("\n" + "="*60)
            print("🔐 LOGIN REQUIRED")
            print("="*60)
            print("\n📋 Please complete login in the browser window:")
            print("   1. Enter your email/username")
            print("   2. Click 'Next'")
            print("   3. Enter your password")
            print("   4. Click 'Next'")
            print("   5. ⚠️  IMPORTANT: Enter verification code when prompted")
            print("   6. Complete any additional security steps")
            print("\n⏳ Waiting for login completion (timeout: 10 minutes)...\n")
            print("💡 Take your time - the script will wait for verification codes!\n")

            # Extended timeout for verification code entry
            start_time = time.time()
            timeout = 600  # 10 minutes for verification code

            check_count = 0
            while time.time() - start_time < timeout:
                try:
                    if is_logged_in(page):
                        print("\n✅ Login successful! Inbox detected!")
                        break

                    # Check if URL indicates successful login
                    if "mail.yahoo.com/d/" in page.url:
                        print("\n✅ Successfully navigated to inbox!")
                        break

                    # Also check if no longer on login page
                    if not is_login_page(page) and "mail.yahoo.com" in page.url:
                        time.sleep(3)  # Give it time to fully load
                        if is_logged_in(page):
                            print("\n✅ Login successful!")
                            break

                    # Progress indicator every 30 seconds
                    check_count += 1
                    if check_count % 15 == 0:  # Every 30 seconds (15 * 2 sec)
                        elapsed = int(time.time() - start_time)
                        remaining = timeout - elapsed
                        print(f"⏳ Still waiting... ({remaining//60}m {remaining%60}s remaining)")

                    time.sleep(2)  # Check every 2 seconds
                except Exception as e:
                    print(f"⚠️  Check error (continuing): {e}")
                    time.sleep(2)
            else:
                print("\n⏱️  Timeout waiting for login (10 minutes elapsed)")
                print("💡 Keeping browser open in case you're still logging in...")
                time.sleep(30)
                browser.close()
                return

        print("\n" + "="*60)
        print("🎉 LOGIN COMPLETED - YAHOO MAIL READY!")
        print("="*60)

        # Verify we're in the inbox
        try:
            current_url = page.url
            print(f"\n📍 Current URL: {current_url}")

            if "mail.yahoo.com" in current_url:
                print("✓ Successfully in Yahoo Mail")

        except Exception as e:
            print(f"ℹ️  {e}")

        # Keep browser open for user interaction
        print("\n💡 Browser will stay open for 5 minutes...")
        print("   (You can close it manually or wait)")
        print("   The automation is complete - you can use your inbox now!")
        time.sleep(300)

        # Cleanup
        print("\n🧹 Closing browser...")
        browser.close()
        print("✨ Done!")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   Yahoo Mail Automation - Windows 11 Chrome Compatible   ║
    ║                                                          ║
    ║   This enhanced script will:                            ║
    ║   1. Open Yahoo Mail directly (checks if logged in)     ║
    ║   2. Accept cookie consent if needed                    ║
    ║   3. Click Sign In only if necessary                    ║
    ║   4. Wait 10 minutes for verification code entry        ║
    ║   5. Detect successful login to inbox                   ║
    ║                                                          ║
    ║   ⚠️  Designed for Windows 11 with Chrome browser        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
