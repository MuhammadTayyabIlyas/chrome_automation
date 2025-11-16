#!/usr/bin/env python3
"""
Gmail Automation - Delete Skyscanner Emails (Selenium Version)
This script:
1. Opens Gmail in Windows Chrome
2. Waits for you to login manually
3. Searches for no-reply@sender.skyscanner.com emails
4. Selects all matching emails
5. Deletes them automatically
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
    """Check if user is logged in to Gmail"""
    try:
        # Check for common Gmail logged-in indicators
        indicators = [
            '[aria-label*="Compose"]',
            '[aria-label*="Search mail"]',
            'div[role="navigation"]',
            '[gh="tm"]'
        ]

        for selector in indicators:
            try:
                driver.find_element(By.CSS_SELECTOR, selector)
                return True
            except:
                continue

        # Also check URL
        if "mail.google.com/mail" in driver.current_url and "SignUp" not in driver.current_url:
            return True

        return False
    except:
        return False

def wait_for_login(driver, timeout=300):
    """Wait for user to complete manual login"""
    print_step("LOGIN", "Please login to Gmail in the browser window", "wait")
    print("\n📋 Login steps:")
    print("   1. Enter your email")
    print("   2. Click 'Next'")
    print("   3. Enter your password")
    print("   4. Complete any 2FA if required")
    print(f"\n⏳ Waiting up to {timeout//60} minutes for login...\n")

    start_time = time.time()

    while time.time() - start_time < timeout:
        if is_logged_in(driver):
            print_step("LOGIN", "Login successful!", "success")
            return True

        # Check if URL changed away from login
        if "mail.google.com" in driver.current_url and "signin" not in driver.current_url.lower():
            time.sleep(2)
            if is_logged_in(driver):
                print_step("LOGIN", "Login successful!", "success")
                return True

        time.sleep(2)

    print_step("LOGIN", "Login timeout reached", "info")
    return False

def search_for_skyscanner(driver):
    """Search for Skyscanner emails"""
    print_step("SEARCH", "Searching for no-reply@sender.skyscanner.com emails...", "search")

    try:
        # Navigate to search with query
        search_url = "https://mail.google.com/mail/u/0/#search/from%3Ano-reply%40sender.skyscanner.com"
        driver.get(search_url)
        time.sleep(5)

        print_step("SEARCH", "Search page loaded", "success")
        return True
    except Exception as e:
        print_step("SEARCH", f"Error: {e}", "info")
        return False

def select_all_emails(driver):
    """Select all emails in the current view"""
    print_step("SELECT", "Selecting all emails...", "work")

    try:
        # Gmail select all selectors
        select_all_selectors = [
            'div[role="checkbox"][aria-label*="Select"]',
            'span[role="checkbox"]',
            'div.oZ-jc.T-Jo',
            '[aria-label="Select"]',
            'div[gh="tm"] span[role="checkbox"]'
        ]

        for selector in select_all_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                time.sleep(1)
                print_step("SELECT", f"Clicked select all using: {selector}", "success")

                # Check if there's a "Select all conversations that match this search" link
                try:
                    select_more = driver.find_element(By.XPATH, "//span[contains(text(), 'Select all')]")
                    select_more.click()
                    time.sleep(1)
                    print_step("SELECT", "Selected ALL matching conversations", "success")
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

def delete_emails(driver):
    """Delete selected emails"""
    print_step("DELETE", "Deleting emails...", "work")

    try:
        # Gmail delete button selectors
        delete_selectors = [
            'div[data-tooltip="Delete"]',
            '[aria-label="Delete"]',
            'div[aria-label="Delete"]',
            'div.G-atb[data-tooltip="Delete"]',
            'button[aria-label="Delete"]'
        ]

        for selector in delete_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                time.sleep(1)
                print_step("DELETE", "Clicked delete button!", "success")
                return True
            except:
                continue

        # Try by text or title
        try:
            element = driver.find_element(By.XPATH, "//div[@aria-label='Delete' or @data-tooltip='Delete']")
            element.click()
            time.sleep(1)
            print_step("DELETE", "Clicked delete button!", "success")
            return True
        except:
            pass

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
    ║       Gmail Automation - Delete Skyscanner Emails       ║
    ║                                                          ║
    ║  This script will:                                      ║
    ║  1. Open Gmail                                          ║
    ║  2. Wait for you to login to Gmail                      ║
    ║  3. Search for no-reply@sender.skyscanner.com           ║
    ║  4. Select all matching emails                          ║
    ║  5. Delete them                                         ║
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

        # Open Gmail
        print_step("NAVIGATE", "Opening Gmail...", "info")
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        time.sleep(3)
        print_step("NAVIGATE", "Gmail loaded", "success")

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

                # Delete emails
                if delete_emails(driver):
                    print("\n" + "="*60)
                    print("🎉 SUCCESS! Skyscanner emails deleted!")
                    print("="*60)
                else:
                    print("\n" + "="*60)
                    print("⚠️  Could not find delete button automatically.")
                    print("   Please click the 'Delete' button (trash icon) manually in the browser.")
                    print("="*60)
            else:
                print("\n" + "="*60)
                print("⚠️  Could not select all emails automatically.")
                print("   Please:")
                print("   1. Click the checkbox to select all emails")
                print("   2. Click 'Select all conversations that match this search' if shown")
                print("   3. Click the 'Delete' button (trash icon)")
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
