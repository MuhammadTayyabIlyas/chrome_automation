#!/usr/bin/env python3
"""
Yahoo Mail Automation - Mark Skyscanner Emails as Spam
This script:
1. Opens Yahoo Mail in a controlled browser
2. Waits for you to login manually
3. Searches for Skyscanner emails
4. Selects all matching emails
5. Marks them as spam automatically
"""

from playwright.sync_api import sync_playwright
import time
import subprocess
import os

def print_step(step, message, status=""):
    """Print formatted step message"""
    icons = {"info": "ℹ️", "success": "✅", "wait": "⏳", "work": "🔧", "search": "🔍"}
    icon = icons.get(status, "▶️")
    print(f"{icon} [{step}] {message}")

def is_logged_in(page):
    """Check if user is logged in to Yahoo Mail"""
    try:
        # Check for common Yahoo Mail logged-in indicators
        indicators = [
            '[data-test-id="app-canvas"]',  # Yahoo Mail main canvas
            'button[data-test-id="compose-button"]',  # Compose button
            '[aria-label*="mailbox"]',  # Mailbox elements
            'button[aria-label*="Settings"]'  # Settings button
        ]

        for selector in indicators:
            if page.query_selector(selector):
                return True

        # Also check URL
        if "mail.yahoo.com/d/" in page.url:
            return True

        return False
    except:
        return False

def wait_for_login(page, timeout=300):
    """Wait for user to complete manual login"""
    print_step("LOGIN", "Please login to Yahoo Mail in the browser window", "wait")
    print("\n📋 Login steps:")
    print("   1. Enter your email/username")
    print("   2. Enter your password")
    print("   3. Complete any 2FA/verification")
    print(f"\n⏳ Waiting up to {timeout//60} minutes for login...\n")

    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_logged_in(page):
            print_step("LOGIN", "Login successful!", "success")
            return True

        # Check if URL changed away from login
        if "mail.yahoo.com" in page.url and "login" not in page.url.lower():
            time.sleep(2)  # Give it a moment to load
            if is_logged_in(page):
                print_step("LOGIN", "Login successful!", "success")
                return True

        time.sleep(2)

    print_step("LOGIN", "Login timeout reached", "info")
    return False

def search_for_skyscanner(page):
    """Search for Skyscanner emails"""
    print_step("SEARCH", "Searching for Skyscanner emails...", "search")

    try:
        # Navigate to search with query
        search_url = "https://mail.yahoo.com/d/search/keyword=from%253Askyscanner"
        page.goto(search_url, wait_until='domcontentloaded')

        # Wait for search results to load
        time.sleep(3)

        print_step("SEARCH", "Search page loaded", "success")
        return True
    except Exception as e:
        print_step("SEARCH", f"Error: {e}", "info")
        return False

def select_all_emails(page):
    """Select all emails in the current view"""
    print_step("SELECT", "Selecting all emails...", "work")

    try:
        # Try different selectors for "Select All" checkbox
        select_all_selectors = [
            'input[type="checkbox"][aria-label*="Select"]',
            'button[aria-label*="Select all"]',
            '[data-test-id="select-all-checkbox"]',
            'input[data-test-id="bulk-action-checkbox"]',
            'span[role="checkbox"]',
            'input[type="checkbox"]'
        ]

        for selector in select_all_selectors:
            element = page.query_selector(selector)
            if element:
                try:
                    element.click()
                    time.sleep(1)
                    print_step("SELECT", f"Clicked select all using: {selector}", "success")

                    # Check if there's a "Select all X conversations" link
                    select_more = page.query_selector('button:has-text("Select all"), a:has-text("Select all")')
                    if select_more:
                        select_more.click()
                        time.sleep(1)
                        print_step("SELECT", "Selected ALL conversations (not just visible)", "success")

                    return True
                except:
                    continue

        print_step("SELECT", "Could not find select all checkbox", "info")
        return False

    except Exception as e:
        print_step("SELECT", f"Error: {e}", "info")
        return False

def mark_as_spam(page):
    """Mark selected emails as spam"""
    print_step("SPAM", "Marking emails as spam...", "work")

    try:
        # Try different selectors for spam button
        spam_selectors = [
            'button[data-test-id="spam-button"]',
            'button[aria-label*="Spam"]',
            'button[title*="Spam"]',
            'button:has-text("Spam")',
            '[data-test-id="toolbar-spam"]'
        ]

        for selector in spam_selectors:
            element = page.query_selector(selector)
            if element:
                try:
                    element.click()
                    time.sleep(1)
                    print_step("SPAM", "Clicked spam button!", "success")
                    return True
                except:
                    continue

        print_step("SPAM", "Could not find spam button - may need to do manually", "info")
        return False

    except Exception as e:
        print_step("SPAM", f"Error: {e}", "info")
        return False

def main():
    """Main automation function"""

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     Yahoo Mail Automation - Mark Skyscanner as Spam      ║
    ║                                                          ║
    ║  This script will:                                      ║
    ║  1. Open Yahoo Mail and Google Scholar                  ║
    ║  2. Wait for you to login to Yahoo                      ║
    ║  3. Search for Skyscanner emails                        ║
    ║  4. Select all matching emails                          ║
    ║  5. Mark them as spam                                   ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    with sync_playwright() as p:
        # Launch browser using remote debugging
        print_step("BROWSER", "Launching Windows Chrome from WSL...", "info")

        # Kill any existing Chrome instances to start fresh
        try:
            subprocess.run(['taskkill.exe', '/F', '/IM', 'chrome.exe'],
                         stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            time.sleep(1)
        except:
            pass

        # Launch Chrome using PowerShell with remote debugging enabled
        chrome_exe = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        ps_command = f'Start-Process -FilePath "{chrome_exe}" -ArgumentList "--remote-debugging-port=9222","--user-data-dir=C:\\temp\\chrome-debug","--no-first-run","--no-default-browser-check"'

        try:
            subprocess.Popen(['powershell.exe', '-Command', ps_command],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_step("BROWSER", "Chrome process started, waiting for debugging port...", "info")

            # Wait for Chrome to be ready (retry connection)
            browser = None
            for attempt in range(10):
                try:
                    time.sleep(2)
                    browser = p.chromium.connect_over_cdp("http://localhost:9222")
                    print_step("BROWSER", "Connected to Windows Chrome!", "success")
                    break
                except Exception as retry_error:
                    if attempt < 9:
                        print(f"   Retry {attempt + 1}/10...")
                    else:
                        raise retry_error

            if not browser:
                raise Exception("Failed to connect to Chrome after 10 attempts")

        except Exception as e:
            print_step("BROWSER", f"Could not launch/connect to Chrome: {e}", "info")
            print_step("BROWSER", "ERROR: Make sure Chrome is not already running", "info")
            raise

        # Get the default context (Chrome already running)
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
        else:
            context = browser.new_context(
                viewport={'width': 1400, 'height': 900}
            )

        # Open Yahoo Mail in first page
        page = context.new_page()
        print_step("NAVIGATE", "Opening Yahoo Mail...", "info")
        page.goto("https://mail.yahoo.com", wait_until='domcontentloaded')
        time.sleep(2)
        print_step("NAVIGATE", "Yahoo Mail loaded", "success")

        # Open Google Scholar in second page
        scholar_page = context.new_page()
        print_step("NAVIGATE", "Opening Google Scholar...", "info")
        scholar_page.goto("https://scholar.google.com/", wait_until='domcontentloaded')
        time.sleep(2)
        print_step("NAVIGATE", "Google Scholar loaded", "success")

        # Switch back to Yahoo Mail page for login and automation
        page.bring_to_front()
        time.sleep(1)

        # Wait for manual login
        if not wait_for_login(page, timeout=300):
            print("\n⚠️  Login not detected. Please ensure you're logged in.")
            print("   Press Ctrl+C to exit or wait for manual continuation...")
            time.sleep(10)

        time.sleep(2)

        # Search for Skyscanner emails
        if search_for_skyscanner(page):
            time.sleep(3)

            # Select all emails
            if select_all_emails(page):
                time.sleep(2)

                # Mark as spam
                if mark_as_spam(page):
                    print("\n" + "="*60)
                    print("🎉 SUCCESS! Skyscanner emails marked as spam!")
                    print("="*60)
                else:
                    print("\n" + "="*60)
                    print("⚠️  Could not find spam button automatically.")
                    print("   Please click the 'Spam' button manually in the browser.")
                    print("="*60)
            else:
                print("\n" + "="*60)
                print("⚠️  Could not select all emails automatically.")
                print("   Please:")
                print("   1. Click the checkbox to select all emails")
                print("   2. Click 'Select all X conversations' if shown")
                print("   3. Click the 'Spam' button")
                print("="*60)

        # Keep browser open for user to verify
        print("\n💡 Browser will stay open for 30 seconds for you to verify...")
        print("   (Close manually or wait)")
        time.sleep(30)

        # Cleanup
        print("\n🧹 Disconnecting from browser...")
        try:
            browser.close()
        except:
            pass
        print("✨ Done! (Chrome will remain open)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
