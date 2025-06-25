import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_arc_jobs():
    jobs = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to the job listings page
        await page.goto("https://arc.dev/remote-jobs")
        
        # Wait for initial job listings to load
        await page.wait_for_selector("div.job-card")
        
        
        # Get all job listing elements
        job_elements = await page.query_selector_all("div.job-card")
        
        for job in job_elements:
            try:
                # Extract skills (categories like JavaScript, Node.js)
                skill_elements = await job.query_selector_all("a.category")
                skills = [await skill.inner_text() for skill in skill_elements]
                
                # Extract salary range
                salary_element = await job.query_selector("div.sc-ab809d0b-0")
                salary = (await salary_element.inner_text()).strip() if salary_element else ""
                
                # Extract job details
                job_data = {
                    "title": (await (await job.query_selector("a.job-title")).inner_text()).strip() if await job.query_selector("a.job-title") else "",
                    "company": (await (await job.query_selector("div.company-name")).inner_text()).strip() if await job.query_selector("div.company-name") else "",
                    "job_type": (await (await job.query_selector("div.job-type")).inner_text()).strip() if await job.query_selector("div.job-type") else "",
                    "experience_level": (await (await job.query_selector("div.experience-level")).inner_text()).strip() if await job.query_selector("div.experience-level") else "",
                    "salary_range": salary,
                    "skills": skills,
                    "location": (await (await job.query_selector("div.bottom-information span")).inner_text()).strip() if await job.query_selector("div.bottom-information span") else "",
                    "hiring_status": (await (await job.query_selector("span.actively-hiring")).inner_text()).strip() if await job.query_selector("span.actively-hiring") else "",
                    "job_url": f"https://arc.dev{(await (await job.query_selector('a.job-title')).get_attribute('href')).strip()}" if await job.query_selector("a.job-title") else "",
                    "logo_url": await (await job.query_selector("img")).get_attribute("src") if await job.query_selector("img") else ""
                }
                jobs.append(job_data)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        await browser.close()
    
    # Save to JSON file
    with open("arc_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    return jobs

async def main():
    scraped_jobs = await scrape_arc_jobs()
    print(f"Scraped {len(scraped_jobs)} jobs")
    for job in scraped_jobs:
        print(json.dumps(job, indent=2))

if __name__ == "__main__":
    asyncio.run(main())