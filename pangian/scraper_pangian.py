import os
import asyncio
from playwright.async_api import async_playwright
import json


async def scrape_pangian_jobs():
    jobs = []
    url = "https://pangian.com/remote/job-board"
    
    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=r"D:\one to infinity\scrapper\Crawl4ai\pangian\pangian_auth.json")
        page = await context.new_page()
        
        try:
            # Navigate to the job listings page
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(2000000000)  # Wait for the page to load

            # Wait for job cards to appear
            await page.wait_for_selector('div.job-card', timeout=30000)
            

            # Scroll to load all jobs
            last_height = await page.evaluate("document.body.scrollHeight")
            while True:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                # await page.wait_for_timeout(2000)  # Wait for new content to load
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Extract job cards
            job_cards = await page.query_selector_all("div.job-card")
            
            for card in job_cards:
                try:
                    # Extract job details
                    job_info = await card.query_selector("div.job-info")
                    if not job_info:
                        continue
                    
                    title_elem = await job_info.query_selector("h3")
                    company_elem = await job_info.query_selector("strong")
                    details_elem = await job_info.query_selector("p")
                    
                    # Get job title
                    title = await title_elem.inner_text() if title_elem else "N/A"
                    title = title.strip()
                    
                    # Get company name (first strong element)
                    company = await company_elem.inner_text() if company_elem else "N/A"
                    company = company.strip()
                    
                    # Get salary, location, and job type
                    salary = "N/A"
                    location = "N/A"
                    job_type = "N/A"
                    posted_time = "N/A"
                    
                    if details_elem:
                        details_text = await details_elem.inner_text()
                        details_text = details_text.strip()
                        parts = details_text.split("|")
                        
                        # Extract salary (from span with color)
                        salary_elem = await details_elem.query_selector("span[style*='color: #ff5c5c']")
                        salary = await salary_elem.inner_text() if salary_elem else "N/A"
                        salary = salary.strip()
                        
                        # Extract location and job type
                        if len(parts) >= 2:
                            location_part = parts[1].strip().split(" |")
                            location = location_part[0] if len(location_part) > 0 else "N/A"
                            job_type = location_part[1] if len(location_part) > 1 else "N/A"
                        
                        # Extract posted time
                        posted_time = parts[-1].strip() if len(parts) > 0 else "N/A"
                    
                    # Get job URL
                    job_link_elem = await card.query_selector("a")
                    job_url = await job_link_elem.get_attribute("href") if job_link_elem else "N/A"
                    
                    # Get company logo
                    logo_elem = await card.query_selector("img.company-logo")
                    logo_url = await logo_elem.get_attribute("src") if logo_elem else "N/A"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "salary": salary,
                        "location": location,
                        "job_type": job_type,
                        "posted_time": posted_time,
                        "job_url": job_url,
                        "logo_url": logo_url
                    }
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"Error processing job card: {str(e)}")
                    continue
            
            # Save jobs to JSON file
            with open("pangian_jobs.json", "w", encoding="utf-8") as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            
            print(f"Scraped {len(jobs)} jobs")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up
            await context.close()
            await browser.close()
    
    return jobs

async def main():
    jobs = await scrape_pangian_jobs()

if __name__ == "__main__":
    asyncio.run(main())