from playwright.sync_api import sync_playwright
import os
import time

def capture_screenshots():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # 1. Landing Page
        print("Capturing Landing Page...")
        page.goto("http://localhost:10000")
        page.screenshot(path="screenshots/landing.png")

        # 2. Dev Page
        print("Capturing Dev Page...")
        page.goto("http://localhost:10000/dev")
        page.screenshot(path="screenshots/dev.png")

        # 3. Chat Page
        print("Capturing Chat Page...")
        page.goto("http://localhost:10000/chat")
        page.wait_for_selector(".sidebar")
        page.screenshot(path="screenshots/chat.png")

        # 4. Chat Page with Message
        print("Capturing Chat Page (Active)...")
        # Ensure fresh state for screenshot
        page.evaluate("localStorage.clear()")
        page.reload()
        page.wait_for_selector("#userInput")

        page.fill("#userInput", "Hello GHAi")
        page.click("#sendBtn")

        # Wait for user message
        page.wait_for_selector(".message.user")
        # Give a moment for the 'Thinking' or response to potentially appear/stabilize
        time.sleep(1)
        page.screenshot(path="screenshots/chat_active.png")

        browser.close()

if __name__ == "__main__":
    capture_screenshots()
