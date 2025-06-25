# from playwright.sync_api import sync_playwright
# import json

# def main():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # Set to False for debugging
#         page = browser.new_page()
#         base_url = "https://weworkremotely.com"

#         try:
#             # Navigate to the page with increased timeout
#             page.goto(base_url, timeout=60000, wait_until="domcontentloaded")

#             # Wait for job listings to load
#             page.wait_for_selector("section.jobs article li.new-listing-container", timeout=60000)

#             # Select all job listing elements
#             job_elements = page.query_selector_all("section.jobs article li.new-listing-container")
#             jobs = []

#             for job_element in job_elements:
#                 # Extract title
#                 title_element = job_element.query_selector(".new-listing__header__title")
#                 title = title_element.inner_text().strip() if title_element else "Unknown"

#                 # Extract apply link (from the <a> within li.new-listing-container)
#                 link_element = job_element.query_selector("a")
#                 job_path = link_element.get_attribute("href") if link_element else "Unknown"
#                 apply_link = f"{base_url}{job_path}" if job_path.startswith("/") else job_path

#                 # Extract company name
#                 company_element = job_element.query_selector(".new-listing__company-name")
#                 company = company_element.inner_text().strip() if company_element else "Unknown"

#                 # Extract location
#                 location_element = job_element.query_selector(".new-listing__company-headquarters")
#                 location = location_element.inner_text().strip() if location_element else "Unknown"

#                 # Extract job type
#                 job_type_element = job_element.query_selector(".new-listing__categories__category")
#                 job_type = job_type_element.inner_text().strip() if job_type_element else "Unknown"

#                 # Append job data
#                 jobs.append({
#                     "title": title,
#                     "applyLink": apply_link,
#                     "company": company,
#                     "location": location,
#                     "jobType": job_type
#                 })

#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             jobs = []

#         finally:
#             browser.close()

#         # Output results in JSON format
#         print(json.dumps(jobs, indent=2))

        

# if __name__ == "__main__":
#     main()


import json
import time
from playwright.sync_api import sync_playwright, TimeoutError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retry_operation(operation, max_attempts=3, delay=2):
    """Retry a Playwright operation with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return operation()
        except TimeoutError as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(delay * (2 ** attempt))
            logger.warning(f"Retrying operation (attempt {attempt + 1}/{max_attempts})")

def scrape_job_details(browser, context, job_data, base_url):
    """Scrape job details from the apply link in a new tab."""
    try:
        # Check if context is still open
        if context.browser is None:
            raise Exception("Browser context is closed")
        
        # Open new tab
        new_page = browser.new_page()
        
        # Navigate to apply link with retry
        new_page.goto(
            job_data['applyLink'], 
            timeout=60000, 
            wait_until="domcontentloaded"
        )
        logger.info(f"Scraping details for {job_data['title']}")

        time.sleep(10)  # Allow time for page to load
        
        # Scrape description
        description = retry_operation(lambda: new_page.query_selector(
            ".lis-container__job__content"
        ))
        job_data['description'] = description.inner_text().strip() if description else "No description available"
        
        return job_data
    except Exception as e:
        logger.error(f"Error scraping details for {job_data['title']}: {str(e)}")
        job_data['description'] = "Error retrieving description"
        return job_data
    finally:
        new_page.close()

def main():
    jobs = []
    base_url = "https://weworkremotely.com"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headless for production
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        try:
            # Navigate to main page with retry
            logger.info("Navigating to main page")
            retry_operation(lambda: page.goto(
                base_url, 
                timeout=60000, 
                wait_until="domcontentloaded"
            ))

            # Wait for job listings
            retry_operation(lambda: page.wait_for_selector(
                "section.jobs article li.new-listing-container", 
                timeout=60000
            ))

            # Extract job listings
            job_elements = page.query_selector_all("section.jobs article li.new-listing-container")
            logger.info(f"Found {len(job_elements)} job listings")

            # Prepare job data
            for job_element in job_elements[:3]:  # Limit to first 10 for testing
                try:
                    title = job_element.query_selector(".new-listing__header__title")
                    company_link = job_element.query_selector("div.tooltip--flag-logo a")
                    apply_link = job_element.query_selector("a[href^='/listings']")
                    company = job_element.query_selector(".new-listing__company-name")
                    location = job_element.query_selector(".new-listing__company-headquarters")
                    job_type = job_element.query_selector(".new-listing__categories__category")

                    job_data = {
                        "title": title.inner_text().strip() if title else "Unknown",
                        "companyLink": f"{base_url}{company_link.get_attribute('href')}" 
                            if company_link and company_link.get_attribute('href').startswith("/") 
                            else company_link.get_attribute('href') if company_link else "Unknown",
                        "applyLink": f"{base_url}{apply_link.get_attribute('href')}" 
                            if apply_link and apply_link.get_attribute('href').startswith("/") 
                            else apply_link.get_attribute('href') if apply_link else "Unknown",
                        "company": company.inner_text().strip() if company else "Unknown",
                        "location": location.inner_text().strip() if location else "Unknown",
                        "jobType": job_type.inner_text().strip() if job_type else "Unknown",
                        "description": ""  # Will be filled later
                    }
                    jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error processing job element: {str(e)}")
                    continue

            # Scrape job details sequentially
            for job_data in jobs:
                if context.browser is None:
                    logger.error("Browser context closed prematurely, stopping detail scraping")
                    break
                job_data = scrape_job_details(browser,context, job_data, base_url)
                time.sleep(1)  # Rate limiting

        except Exception as e:
            logger.error(f"Fatal error occurred: {str(e)}")
            jobs = []
        
        finally:
            context.close()
            browser.close()

    # Save results
    output_file = "jobs_scraped_from_weworkremotely.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(jobs)} jobs to {output_file}")

if __name__ == "__main__":
    main()