import asyncio
from playwright.async_api import async_playwright

async def main():
    profile_dir = "/home/toby/openmanus_browser_profiles/jupiter"

    async with async_playwright() as p:
        # Launch persistent context
        browser = await p.chromium.launch_persistent_context(
            profile_dir,
            headless=False,
            args=[
                "--profile-directory=Profile1",
                "--enable-features=NetworkService",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )

        # Open page and navigate
        page = await browser.new_page()
        await page.goto("https://jup.ag/perps")
        print(f"Navigated to {page.url}")

        # Keep browser open to test persistence
        input("Press Enter to close browser...")
        await browser.close()

asyncio.run(main())
