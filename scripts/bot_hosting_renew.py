#!/usr/bin/env python3
"""Bot-Hosting renewal - login and click renew."""
import os
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def renew_bot_hosting():
    email = os.environ.get('BOTHOSTING_EMAIL')
    password = os.environ.get('BOTHOSTING_PASSWORD')
    if not email or not password:
        return "SKIP: BOTHOSTING_EMAIL/PASSWORD not set"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        try:
            page = browser.new_page()
            logger.info("Navigating to bot-hosting.net...")
            page.goto('https://bot-hosting.net/', timeout=60000, wait_until='domcontentloaded')
            page.wait_for_timeout(3000)
            logger.info(f"Page title: {page.title()}")

            # Find and click login
            # (Bot-Hosting uses a login page, adapt selectors as needed)
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                '#email',
            ]
            pwd_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password',
            ]

            email_filled = False
            for sel in email_selectors:
                try:
                    if page.locator(sel).count() > 0:
                        page.fill(sel, email, timeout=10000)
                        email_filled = True
                        break
                except Exception:
                    continue
            if not email_filled:
                return "FAIL: email input not found"

            for sel in pwd_selectors:
                try:
                    if page.locator(sel).count() > 0:
                        page.fill(sel, password, timeout=10000)
                        break
                except Exception:
                    continue

            page.keyboard.press('Enter')
            page.wait_for_timeout(8000)

            # Navigate to billing page and look for renew button
            page.goto('https://bot-hosting.net/a/billings', timeout=60000)
            page.wait_for_timeout(5000)

            content = page.content().lower()
            if 'renew' in content:
                # Try to click renew
                try:
                    page.click('button:has-text("Renew")', timeout=10000)
                    page.wait_for_timeout(5000)
                    return "OK: renew clicked"
                except Exception as e:
                    return f"FAIL: renew button not clickable: {e}"
            return "UNKNOWN: no renew button found"
        except Exception as e:
            logger.exception("Bot-Hosting renewal exception")
            return f"ERROR: {e}"
        finally:
            browser.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(renew_bot_hosting())
