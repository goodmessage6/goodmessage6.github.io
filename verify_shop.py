import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8000/update.html")
        await page.wait_for_timeout(1000)

        # Click main menu shop button
        await page.click('#mainShopButton')
        await page.wait_for_timeout(1000)

        await page.screenshot(path="shop_ui.png")
        print("Screenshot of shop saved to shop_ui.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
