#!/usr/bin/env python3
"""
Yahoo Mail Automation - Mark Skyscanner Emails as Spam (Selenium Version)
This script:
1. Opens Yahoo Mail and Google Scholar in Windows Chrome
2. Waits for you to login manually
3. Searches for Skyscanner emails
4. Selects all matching emails
5. Marks them as spam automatically
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def print_step(step, message, status=""):
    """Print formatted step message"""
    icons = {"info": "ℹ️", "success": "✅", "wait": "⏳", "work": "🔧", "search": "🔍"}
    icon = icons.get(status, "▶️")
    print(f"{icon} [{step}] {message}")

def is_logged_in(driver):
    """Check if user is logged in to Yahoo Mail"""
    try:
        # Check for common Yahoo Mail logged-in indicators
        indicators = [
            '[data-test-id="app-canvas"]',
            'button[data-test-id="compose-button"]',
            '[aria-label*="mailbox"]',
            'button[aria-label*="Settings"]'
        ]

        for selector in indicators:
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
                return True
            except:
                continue

        # Also check URL
        if "mail.yahoo.com/d/" in driver.current_url:
            return True

        return False
    except:
        return False

def wait_for_login(driver, timeout=300):
    """Wait for user to complete manual login"""
    print_step("LOGIN", "Please login to Yahoo Mail in the browser window", "wait")
    print("\n📋 Login steps:")
    print("   1. Enter your email/username")
    print("   2. Enter your password")
    print("   3. Complete any 2FA/verification")
    print(f"\n⏳ Waiting up to {timeout//60} minutes for login...\n")

    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_logged_in(driver):
            print_step("LOGIN", "Login successful!", "success")
            return True

        # Check if URL changed away from login
        if "mail.yahoo.com" in driver.current_url and "login" not in driver.current_url.lower():
            time.sleep(2)
            if is_logged_in(driver):
                print_step("LOGIN", "Login successful!", "success")
                return True

        time.sleep(2)

    print_step("LOGIN", "Login timeout reached", "info")
    return False

def search_for_skyscanner(driver):
    """Search for Skyscanner emails"""
    print_step("SEARCH", "Searching for Skyscanner emails...", "search")

    try:
        # Navigate to search with query
        search_url = "https://mail.yahoo.com/d/search/keyword=from%253Askyscanner"
        driver.get(search_url)
        time.sleep(3)

        print_step("SEARCH", "Search page loaded", "success")
        return True
    except Exception as e:
        print_step("SEARCH", f"Error: {e}", "info")
        return False

def select_all_emails(driver):
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
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                time.sleep(1)
                print_step("SELECT", f"Clicked select all using: {selector}", "success")

                # Check if there's a "Select all X conversations" link
                try:
                    select_more = driver.find_element(By.XPATH, "//button[contains(text(), 'Select all')] | //a[contains(text(), 'Select all')]")
                    select_more.click()
                    time.sleep(1)
                    print_step("SELECT", "Selected ALL conversations (not just visible)", "success")
                except:
                    pass

                return True
            except:
                continue

        print_step("SELECT", "Could not find select all checkbox", "info")
        return False

    except Exception as e:
        print_step("SELECT", f"Error: {e}", "info")
        return False

def mark_as_spam(driver):
    """Mark selected emails as spam"""
    print_step("SPAM", "Marking emails as spam...", "work")

    try:
        # Try different selectors for spam button
        spam_selectors = [
            'button[data-test-id="spam-button"]',
            'button[aria-label*="Spam"]',
            'button[title*="Spam"]',
            '[data-test-id="toolbar-spam"]'
        ]

        for selector in spam_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                time.sleep(1)
                print_step("SPAM", "Clicked spam button!", "success")
                return True
            except:
                continue

        # Try by text
        try:
            element = driver.find_element(By.XPATH, "//button[contains(text(), 'Spam')]")
            element.click()
            time.sleep(1)
            print_step("SPAM", "Clicked spam button!", "success")
            return True
        except:
            pass

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

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.binary_location = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

    # Add arguments for WSL compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9223")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Set WSL-specific preferences
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    print_step("BROWSER", "Setting up ChromeDriver...", "info")

    # Create driver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print_step("BROWSER", "Launching Windows Chrome from WSL...", "info")

    try:
        print_step("BROWSER", "Windows Chrome launched successfully!", "success")

        # Open Yahoo Mail
        print_step("NAVIGATE", "Opening Yahoo Mail...", "info")
        driver.get("https://mail.yahoo.com")
        time.sleep(2)
        print_step("NAVIGATE", "Yahoo Mail loaded", "success")

        # Open Google Scholar in new tab
        print_step("NAVIGATE", "Opening Google Scholar in new tab...", "info")
        driver.execute_script("window.open('https://scholar.google.com/');")
        time.sleep(2)
        print_step("NAVIGATE", "Google Scholar loaded", "success")

        # Switch back to Yahoo Mail tab (first tab)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        # Wait for manual login
        if not wait_for_login(driver, timeout=300):
            print("\n⚠️  Login not detected. Please ensure you're logged in.")
            print("   Press Ctrl+C to exit or wait for manual continuation...")
            time.sleep(10)

        time.sleep(2)

        # Search for Skyscanner emails
        if search_for_skyscanner(driver):
            time.sleep(3)

            # Select all emails
            if select_all_emails(driver):
                time.sleep(2)

                # Mark as spam
                if mark_as_spam(driver):
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
        print("\n💡 Browser will stay open for 60 seconds for you to verify...")
        print("   (Close manually or wait)")
        time.sleep(60)

    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        print("\n🧹 Closing browser...")
        try:
            driver.quit()
        except:
            pass
        print("✨ Done!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
