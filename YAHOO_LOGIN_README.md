# Yahoo Login Demo - Manual Authentication Support

This script demonstrates how to use Playwright to automate Yahoo login with manual user authentication.

## Features

- ✅ Opens Yahoo.com in a visible browser window
- ✅ Automatically clicks "Sign In" button
- ✅ Detects login page
- ✅ Waits for manual user login (up to 5 minutes)
- ✅ Detects when login is complete
- ✅ Continues with automation after successful login

## Installation

### Step 1: Install Playwright

```bash
pip install playwright
```

### Step 2: Install Browser Drivers

```bash
playwright install chromium
```

Or install all browsers:

```bash
playwright install
```

## Usage

### Run the script:

```bash
python3 yahoo_login_demo.py
```

### What happens:

1. **Browser Opens**: A Chromium browser window will open (not headless)
2. **Navigate to Yahoo**: Script navigates to yahoo.com
3. **Click Sign In**: Automatically clicks the "Sign In" button
4. **Manual Login**: Browser pauses and displays a message:
   ```
   🔐 LOGIN PAGE DETECTED
   📋 Please complete login manually in the browser window
   ```
5. **You Login**: Enter your credentials in the visible browser
6. **Script Continues**: Once login is detected, automation resumes
7. **Access Yahoo Mail**: Script navigates to Yahoo Mail as an example

## How It Works

### Login Detection

```python
def is_login_page(page):
    # Checks if URL contains "login" or page has password input
    url_check = "login" in page.url.lower()
    password_input = page.query_selector("input[type='password']") is not None
    return url_check or password_input
```

### Login Completion Detection

```python
def is_logged_in(page):
    # Checks for common logged-in indicators
    logged_in_indicators = [
        'button[aria-label*="account"]',
        'a[href*="logout"]',
        'div[data-ylk*="signout"]'
    ]
    # Returns True if any indicator is found
```

### Waiting Loop

The script checks every 2 seconds for login completion:
- Maximum wait time: 5 minutes (300 seconds)
- Checks if logged-in indicators appear
- Checks if URL changes away from login page

## Customization

### Change Timeout

Edit the `timeout` variable in `main()`:

```python
timeout = 300  # 5 minutes in seconds
```

### Add Custom Automation

After login is detected, add your automation code:

```python
if is_logged_in(page):
    print("✅ Login completed!")

    # Your automation here:
    # Search for emails
    page.fill('input[name="search"]', 'from:skyscanner')

    # Click elements
    page.click('button[aria-label="Search"]')

    # etc.
```

### Use Different Browser

Change `chromium` to `firefox` or `webkit`:

```python
browser = p.firefox.launch(headless=False)
```

## Troubleshooting

### Error: "playwright not found"

Install Playwright:
```bash
pip install playwright
playwright install
```

### Error: "Browser not found"

Install browser drivers:
```bash
playwright install chromium
```

### Login Not Detected

The script might not detect login completion. You can:

1. **Manually check the selectors** for your specific Yahoo account
2. **Add custom detection logic** in `is_logged_in()` function
3. **Increase timeout** if you need more time to login

### Yahoo Blocks Automation

Yahoo might detect automated browsing. To reduce detection:

1. Use stealth plugins
2. Add random delays
3. Use real user profiles

## Example Use Cases

### 1. Mark Skyscanner Emails as Spam

```python
if is_logged_in(page):
    # Search for Skyscanner emails
    page.goto("https://mail.yahoo.com")
    page.fill('input[aria-label="Search"]', 'from:skyscanner')
    page.click('button[aria-label="Search Mail"]')

    # Select all
    page.click('input[type="checkbox"][aria-label="Select all"]')

    # Mark as spam
    page.click('button[title="Spam"]')
```

### 2. Read Unread Emails

```python
if is_logged_in(page):
    page.goto("https://mail.yahoo.com")
    unread = page.query_selector_all('.unread')
    print(f"You have {len(unread)} unread emails")
```

## Security Notes

⚠️ **Important Security Considerations:**

- This script shows the browser window (not headless)
- You manually enter your password
- No credentials are stored in the script
- The script only waits for login, it doesn't capture credentials
- Browser session is temporary and cleared when closed

## Alternative Approach: Save Session

If you want to avoid logging in every time, you can save browser session:

```python
context = browser.new_context(
    storage_state="yahoo_session.json"  # Save session
)

# After login, save the session:
context.storage_state(path="yahoo_session.json")

# Next time, load the session:
context = browser.new_context(
    storage_state="yahoo_session.json"  # Load saved session
)
```

## License

Free to use and modify for educational purposes.

## Credits

Based on Playwright documentation and best practices for manual authentication handling.
