# email = "zxcvbnm78956123@gmail.com"
# password = "ASDFGHJKLzxcvbnm789456123@"

import os

import asyncio
from playwright.async_api import async_playwright

async def login_to_workingnomads(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:

            # Navigate to the login page
            await page.goto("https://pangian.com/remote/job-board")

            await page.wait_for_timeout(1000)  # Wait for the page to load

            # Click the cookies accept button
            cookies_button = await page.wait_for_selector('button[class="btn btn-primary"]', timeout=10000)
            await cookies_button.click()

            # # Wait for the login button to appear and click it
            # await page.wait_for_timeout(2000)  # Wait for the login button to be

            login_button = await page.wait_for_selector('button.btn.header-item.waves-effect.p-0', timeout=10000)
            await login_button.click()

            # Wait for the login form to appear
            await page.wait_for_selector('input[id="email"]', timeout=10000)



            # Fill in the email and password fields
            await page.fill('input[id="email"]', email)
            await page.fill('input[id="password"]', password)

            # Click the login button
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)  # Wait for the login process to complete

            # Save storage state to auth.json
            await context.storage_state(path=r"D:\one to infinity\scrapper\Crawl4ai\pangian\pangian_auth.json")


        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up
            await context.close()
            await browser.close()



email = "zxcvbnm78956123@gmail.com"
password = "ASDFGHJKLzxcvbnm789456123@"

asyncio.run(login_to_workingnomads(email, password))

