from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{os.path.abspath('index.html')}")

    # Give it some time to load
    time.sleep(1)

    # Set coins manually using javascript evaluate (to avoid dev mode giving aero vehicle)
    page.evaluate("updatePersistentCoins(9999);")
    time.sleep(0.5)

    # Open shop from main menu
    page.click('#mainShopButton')
    time.sleep(0.5)

    # Take screenshot of the new shop UI
    page.screenshot(path="shop_ufo_ui.png")

    # Click Buy UFO
    page.click('#btnUfo')
    time.sleep(0.5)

    # Close shop
    page.click('#closeShopBtn')
    time.sleep(0.5)

    # Start game
    page.click('#startButton')
    time.sleep(0.5)

    # Summon Vehicle (UFO)
    page.keyboard.press('KeyV')
    time.sleep(1.5) # Wait for drop animation

    # Move mouse to aim and shoot
    page.mouse.move(500, 300)
    page.mouse.down()
    time.sleep(0.2)
    page.mouse.up()

    # Take screenshot of UFO in action
    page.screenshot(path="ufo_vehicle.png")

    browser.close()