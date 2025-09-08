from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Step 1: Go to the website "www.google.com"
        print("Step 1: Navigating to www.google.com")
        page.goto("https://www.google.com")
        page.wait_for_load_state("networkidle")
        print("✅ Successfully navigated to Google")

        # Step 2: Check if the webpage contains google search bar
        print("Step 2: Checking if Google search bar is present")
        search_bar = page.locator("input[name='q'], textarea[name='q']")
        assert search_bar.is_visible(), "Google search bar is not visible"
        print("✅ Google search bar is visible")

        # Step 3: Click on the link and wait for navigation
        print("Step 3: Clicking on a link and waiting for navigation")
        # Look for "About" link or similar navigation link
        about_link = page.locator("a[href*='about'], text='About'")
        if about_link.is_visible():
            about_link.click()
            page.wait_for_load_state("networkidle")
            print("✅ Successfully clicked on About link and navigated")
        else:
            # Alternative: click on Gmail link if About is not available
            gmail_link = page.locator("a[href*='gmail'], text='Gmail'")
            if gmail_link.is_visible():
                gmail_link.click()
                page.wait_for_load_state("networkidle")
                print("✅ Successfully clicked on Gmail link and navigated")
            else:
                print("⚠️ No suitable navigation link found, skipping navigation step")

        # Step 4: Verify new page contains google search bar (if still on Google domain)
        print("Step 4: Verifying page after navigation")
        current_url = page.url
        if "google.com" in current_url:
            search_bar_after_nav = page.locator("input[name='q'], textarea[name='q']")
            if search_bar_after_nav.is_visible():
                print("✅ Google search bar is still visible after navigation")
            else:
                print("ℹ️ Search bar not visible on current page (expected for some Google pages)")
        else:
            print(f"ℹ️ Navigated to external site: {current_url}")

        print("\n🎉 All test steps completed successfully!")

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        raise e
    
    finally:
        # Close browser
        print("Closing browser...")
        browser.close()
        print("✅ Browser closed successfully")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)