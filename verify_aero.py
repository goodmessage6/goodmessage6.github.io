import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8000/update.html")
        await page.wait_for_timeout(1000)

        # Click start
        await page.click('#startButton')
        await page.wait_for_timeout(500)

        # Dev mode sequence
        keys = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a']
        for k in keys:
            await page.keyboard.press(k)
            await page.wait_for_timeout(100)

        await page.wait_for_timeout(500)

        # Press V to summon Aero
        await page.keyboard.press('v')
        await page.wait_for_timeout(2000) # Wait for drop animation

        # Jump up
        await page.keyboard.press('ArrowUp')
        await page.wait_for_timeout(500)

        # Shoot
        await page.keyboard.press('Space')
        await page.wait_for_timeout(200)

        await page.screenshot(path="aero_vehicle.png")
        print("Screenshot saved to aero_vehicle.png")

        # Press V to eject
        await page.keyboard.press('v')
        await page.wait_for_timeout(500)

        await page.screenshot(path="aero_ejected.png")
        print("Screenshot saved to aero_ejected.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
