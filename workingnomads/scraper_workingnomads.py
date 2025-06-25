# import asyncio
# from playwright.async_api import async_playwright
# import json
# from datetime import datetime
# import uuid

# async def scrape_workingnomads_jobs():
#     jobs = []
#     url = "https://www.workingnomads.com/remote-software-engineering-jobs"
    
#     async with async_playwright() as p:
#         # Launch headless Chromium browser
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         )
#         page = await context.new_page()
        
#         try:
#             # Navigate to the job listings page
#             await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
#             # Wait for job listings to load
#             await page.wait_for_selector('div.job-desktop', timeout=30000)
            
#             # Get all job listing elements
#             job_elements = await page.query_selector_all('div.job-desktop')
            
#             for job_element in job_elements:
#                 job = {}
#                 job['id'] = str(uuid.uuid4())
#                 job['scraped_at'] = datetime.utcnow().isoformat()
                
#                 # Extract job title
#                 title_element = await job_element.query_selector('h4 a.open-button')
#                 job['title'] = await title_element.inner_text() if title_element else "N/A"
                
#                 # Extract company
#                 company_element = await job_element.query_selector('div.company a')
#                 job['company'] = await company_element.inner_text() if company_element else "N/A"
                
#                 # Extract category
#                 category_element = await job_element.query_selector('span.category')
#                 job['category'] = await category_element.inner_text() if category_element else "N/A"
                
#                 # Extract posting date
#                 date_element = await job_element.query_selector('div.date')
#                 job['posted_date'] = await date_element.inner_text() if date_element else "N/A"
                
#                 # Extract location
#                 location_element = await job_element.query_selector('div.box:has(i.fa-map-marker) span')
#                 job['location'] = await location_element.inner_text() if location_element else "N/A"
                
#                 # Extract job type
#                 job_type_element = await job_element.query_selector('div.box:has(i.fa-clock-o) span')
#                 job['job_type'] = await job_type_element.inner_text() if job_type_element else "N/A"
                
#                 # Extract tags
#                 tag_elements = await job_element.query_selector_all('div.box:has(i.fa-tags) a')
#                 job['tags'] = [await tag.inner_text() for tag in tag_elements] if tag_elements else []
                
#                 # Extract job URL
#                 link_element = await job_element.query_selector('h4 a.open-button')
#                 job['url'] = await link_element.get_attribute('href') if link_element else "N/A"
#                 if job['url'] != "N/A" and not job['url'].startswith('http'):
#                     job['url'] = f"https://www.workingnomads.com{job['url']}"
                
#                 jobs.append(job)
            
#             # Save results to JSON file
#             with open('workingnomads_jobs.json', 'w', encoding='utf-8') as f:
#                 json.dump(jobs, f, indent=2, ensure_ascii=False)
            
#             print(f"Scraped {len(jobs)} jobs and saved to workingnomads_jobs.json")
            
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
        
#         finally:
#             # Clean up
#             await context.close()
#             await browser.close()
    
#     return jobs

# async def main():
#     await scrape_workingnomads_jobs()

# if __name__ == "__main__":
#     asyncio.run(main())



import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
import uuid

async def scrape_workingnomads_jobs():
    jobs = []
    url = "https://www.workingnomads.com/remote-software-engineering-jobs"
    
    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # Navigate to the job listings page
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for job listings to load
            await page.wait_for_selector('div.job-desktop', timeout=30000)
            
            # Click "Show more jobs" div until no more jobs are loaded

            # show_more_div = await page.query_selector('div.show-more[ng-click="loadMore()"]')
            await page.wait_for_timeout(2000)  # Wait for new jobs to load
            while True:
                show_more_div = await page.query_selector('div.show-more[ng-show="loadMoreShow"]')
                # if await show_more_div.get_attribute('class') == 'show-more ng-hide':
                #     print("No more jobs to load.")
                #     break
                k = await show_more_div.get_attribute('class')
                if k == 'show-more ng-hide':
                    print("No more jobs to load.")
                    break
                    

                else :
                    await show_more_div.click()
                # await page.wait_for_timeout(2000)  # Wait for new jobs to load


            
            # Get all job listing elements, excluding .job-desktop__bookmark
            job_elements = await page.query_selector_all('div.job-desktop:not(.job-desktop__bookmark)')
            print(f"Found {len(job_elements)} job listings")
            
            for job_element in job_elements:
                # Verify it's a valid job listing by checking for job title
                title_element = await job_element.query_selector('h4 a.open-button')
                if not title_element:
                    continue  # Skip non-job elements
                
                job = {}
                job['id'] = str(uuid.uuid4())
                job['scraped_at'] = datetime.utcnow().isoformat()
                
                # Extract job title
                job['title'] = await title_element.inner_text() if title_element else "N/A"
                
                # Extract company and company link
                company_element = await job_element.query_selector('div.company a')
                if company_element:
                    job['company'] = await company_element.inner_text()
                    company_href = await company_element.get_attribute('href')
                    job['company_link'] = f"https://www.workingnomads.com{company_href}" if company_href else "N/A"
                else:
                    job['company'] = "N/A"
                    job['company_link'] = "N/A"
                
                # Extract category
                category_element = await job_element.query_selector('span.category')
                job['category'] = await category_element.inner_text() if category_element else "N/A"
                
                # Extract posting date
                date_element = await job_element.query_selector('div.date')
                job['posted_date'] = await date_element.inner_text() if date_element else "N/A"
                
                # Extract location
                location_element = await job_element.query_selector('div.box:has(i.fa-map-marker) span')
                job['location'] = await location_element.inner_text() if location_element else "N/A"
                
                # Extract job type
                job_type_element = await job_element.query_selector('div.box:has(i.fa-clock-o) span')
                job['job_type'] = await job_type_element.inner_text() if job_type_element else "N/A"
                
                # Extract tags
                tag_elements = await job_element.query_selector_all('div.box:has(i.fa-tags) a')
                job['tags'] = [await tag.inner_text() for tag in tag_elements] if tag_elements else []
                
                # Extract job URL
                link_element = await job_element.query_selector('h4 a.open-button')
                job['url'] = await link_element.get_attribute('href') if link_element else "N/A"
                if job['url'] != "N/A" and not job['url'].startswith('http'):
                    job['url'] = f"https://www.workingnomads.com{job['url']}"
                
                jobs.append(job)
            
            # Save results to JSON file
            with open('workingnomads_jobs.json', 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            
            print(f"Scraped {len(jobs)} jobs and saved to workingnomads_jobs.json")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up
            await context.close()
            await browser.close()
    
    return jobs

async def main():
    await scrape_workingnomads_jobs()

if __name__ == "__main__":
    asyncio.run(main())