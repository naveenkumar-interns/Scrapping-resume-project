import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_remotewoman_jobs():
    jobs = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to the job listings page
        await page.goto("https://remotewoman.com/remote-developer-jobs/")
        
        # Wait for initial job listings to load
        await page.wait_for_selector("li.job_listing")
        
        # Click "Load more listings" button until no more jobs are loaded
        while True:
            try:
                load_more_button = await page.query_selector("a.load_more_jobs")
                if not load_more_button or not await load_more_button.is_visible():
                    break
                
                # Get current number of jobs
                current_job_count = len(await page.query_selector_all("li.job_listing"))
                
                # Click the button and wait for new jobs to load
                await load_more_button.click()
                
                # Wait for new jobs to appear or timeout
                try:
                    await page.wait_for_function(
                        f"document.querySelectorAll('li.job_listing').length > {current_job_count}",
                        timeout=5000
                    )
                except:
                    # No new jobs loaded, break the loop
                    break
            except Exception as e:
                print(f"Error loading more jobs: {e}")
                break
        
        # Get all job listing elements
        job_elements = await page.query_selector_all("li.job_listing")
        
        for job in job_elements:
            try:
                # Extract job details
                job_data = {
                    "title": (await (await job.query_selector("h3.job_listing-title")).inner_text()).strip() if await job.query_selector("h3.job_listing-title") else "",
                    "company": (await (await job.query_selector("div.job_listing-company strong")).inner_text()).strip() if await job.query_selector("div.job_listing-company strong") else "",
                    "location": (await (await job.query_selector("div.job_listing-location a.google_map_link")).inner_text()).strip() if await job.query_selector("div.job_listing-location a.google_map_link") else "",
                    "job_type": (await (await job.query_selector("li.job_listing-type")).inner_text()).strip() if await job.query_selector("li.job_listing-type") else "",
                    "date_posted": (await (await job.query_selector("li.job_listing-date")).inner_text()).strip() if await job.query_selector("li.job_listing-date") else "",
                    "job_url": await (await job.query_selector("a.job_listing-clickbox")).get_attribute("href") if await job.query_selector("a.job_listing-clickbox") else "",
                    "logo_url": await (await job.query_selector("img.company_logo")).get_attribute("src") if await job.query_selector("img.company_logo") else ""
                }
                jobs.append(job_data)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        await browser.close()
    
    # Save to JSON file
    with open("remotewoman_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    return jobs

async def main():
    scraped_jobs = await scrape_remotewoman_jobs()
    print(f"Scraped {len(scraped_jobs)} jobs")
    for job in scraped_jobs:
        print(json.dumps(job, indent=2))

if __name__ == "__main__":
    asyncio.run(main())



