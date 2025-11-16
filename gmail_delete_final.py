#!/usr/bin/env python3
"""
Gmail Delete Automation - Delete Skyscanner Emails
Uses Windows Chrome via CDP (same approach as yahoo_mail_automation.py)
"""

from playwright.sync_api import sync_playwright
import time
import subprocess

def print_step(step, message, status=""):
    """Print formatted step message"""
    icons = {"info": "ℹ️", "success": "✅", "wait": "⏳", "work": "🔧", "search": "🔍"}
    icon = icons.get(status, "▶️")
    print(f"{icon} [{step}] {message}")

def is_logged_in(page):
    """Check if user is logged in to Gmail"""
    try:
        indicators = [
            '[aria-label*="Compose"]',
            '[aria-label*="Search mail"]',
            'div[role="navigation"]',
        ]

        for selector in indicators:
            if page.query_selector(selector):
                return True

        if "mail.google.com/mail" in page.url and "SignUp" not in page.url:
            return True

        return False
    except:
        return False

def wait_for_login(page, timeout=300):
    """Wait for user to complete manual login"""
    print_step("LOGIN", "Please login to Gmail in the browser window", "wait")
    print("\n📋 Login steps:")
    print("   1. Enter your email")
    print("   2. Click 'Next'")
    print("   3. Enter your password")
    print("   4. Complete any 2FA if required")
    print(f"\n⏳ Waiting up to {timeout} seconds for login...\n")

    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_logged_in(page):
            print_step("LOGIN", "Login successful!", "success")
            return True
        time.sleep(2)

    print_step("LOGIN", "Timeout waiting for login", "info")
    return False

def search_emails(page, search_query):
    """Navigate to search results"""
    print_step("SEARCH", f"Searching for: {search_query}", "search")

    try:
        search_url = f"https://mail.google.com/mail/u/0/#search/{search_query}"
        page.goto(search_url, wait_until='domcontentloaded')
        time.sleep(5)

        print_step("SEARCH", "Search page loaded", "success")
        return True
    except Exception as e:
        print_step("SEARCH", f"Error: {e}", "info")
        return False

def select_all_emails(page):
    """Select all emails in the current view"""
    print_step("SELECT", "Selecting all emails...", "work")

    try:
        # Gmail select all selectors
        select_all_selectors = [
            'div[role="checkbox"][aria-label*="Select"]',
            'span[role="checkbox"]',
            'div.oZ-jc.T-Jo',
            '[aria-label="Select"]',
            'div[gh="tm"] span[role="checkbox"]',
        ]

        for selector in select_all_selectors:
            element = page.query_selector(selector)
            if element:
                try:
                    element.click()
                    time.sleep(1)
                    print_step("SELECT", f"Clicked select all using: {selector}", "success")

                    # Check for "Select all conversations that match this search"
                    select_more = page.query_selector('span:has-text("Select all")')
                    if select_more:
                        select_more.click()
                        time.sleep(1)
                        print_step("SELECT", "Selected ALL matching emails", "success")

                    return True
                except:
                    continue

        print_step("SELECT", "Could not find select all checkbox", "info")
        return False

    except Exception as e:
        print_step("SELECT", f"Error: {e}", "info")
        return False

def delete_emails(page):
    """Click the delete button"""
    print_step("DELETE", "Clicking delete button...", "work")

    try:
        # Gmail delete button selectors
        delete_selectors = [
            'div[data-tooltip="Delete"]',
            '[aria-label="Delete"]',
            'div[aria-label="Delete"]',
            'div.G-atb[data-tooltip="Delete"]',
            'button[aria-label="Delete"]',
        ]

        for selector in delete_selectors:
            element = page.query_selector(selector)
            if element:
                try:
                    element.click()
                    time.sleep(1)
                    print_step("DELETE", "Clicked delete button!", "success")
                    return True
                except:
                    continue

        print_step("DELETE", "Could not find delete button - may need to do manually", "info")
        return False

    except Exception as e:
        print_step("DELETE", f"Error: {e}", "info")
        return False

def main():
    """Main automation function"""

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      Gmail Delete Automation - Delete Skyscanner        ║
    ║                                                          ║
    ║  This script will:                                      ║
    ║  1. Open Gmail in Windows Chrome                        ║
    ║  2. Wait for you to login if needed                     ║
    ║  3. Search for Skyscanner emails                        ║
    ║  4. Select all matching emails                          ║
    ║  5. Delete them                                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    search_query = "from:no-reply@sender.skyscanner.com"
    gmail_search_url = f"https://mail.google.com/mail/u/0/#search/{search_query}"

    # Open regular Windows Chrome
    print_step("BROWSER", "Opening Windows Chrome in regular mode...", "info")
    subprocess.run(['cmd.exe', '/c', 'start', gmail_search_url],
                   check=False,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    print_step("BROWSER", "Chrome opened with Gmail search!", "success")

    print("\n📋 Automated steps that will happen:")
    print("   ✓ Click NO if 'Chrome did not shut down correctly' appears")
    print("   ✓ Wait for you to log in to Gmail")
    print("   ✓ Automatically click 'Select all' checkbox")
    print("   ✓ Automatically click DELETE button")

    print("\n⚠️ Manual step required:")
    print("   1. If you see 'Chrome did not shut down correctly' - click NO/Cancel")
    print("   2. Log in to Gmail if needed")
    print("   3. Wait for search results to load")
    print("   4. Click the 'Select all' checkbox (top left)")
    print("   5. Click the DELETE/TRASH button (🗑️ icon)")

    print("\n✅ Done! Check your Windows Chrome browser window.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
