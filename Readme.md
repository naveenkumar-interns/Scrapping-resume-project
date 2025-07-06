
Job Scraping Project
Overview
This project contains six web scraping scripts to extract job listings from various online platforms: Arc.dev, General, Jobspresso, Pangian, Remote Woman, and We Work Remotely, with an additional folder for Working Nomads. Each script uses Playwright for browser automation and Python for scripting, collecting details like job title, company, salary range, skills, location, and more. The scraped data is saved in JSON format for further use.
Features

Scrapes job listings from six distinct job boards.
Extracts key job details:
Job title
Company name
Job type
Experience level
Salary range
Required skills
Location
Hiring status
Job URL and company logo URL


Saves data in JSON format.
Includes error handling for robust scraping.
Asynchronous execution for efficiency.

Prerequisites

Python 3.8+
Playwright and its browser binaries
Required Python packages:
playwright
asyncio
json



Installation

Clone the repository:
git clone https://github.com/naveenkumar-interns/job-scraping-project.git
cd job-scraping-project


Set up a virtual environment (optional):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt
playwright install  # Installs browser binaries



Usage

Run a specific scraper:Navigate to the respective folder and run the script. For example, for Arc.dev:
cd arc_dev
python arc_scraper.py

This saves output to arc_jobs.json.

Output:

Each script generates a JSON file (e.g., arc_jobs.json) with scraped data.
Console output shows the number of jobs scraped and their details.


Running all scrapers:Execute each script manually or automate with a script:
cd arc_dev && python arc_scraper.py
cd ../general && python general_scraper.py
cd ../jobspresso && python jobspresso_scraper.py
cd ../pangian && python pangian_scraper.py
cd ../remotewoman && python remotewoman_scraper.py
cd ../weworkremotely && python weworkremotely_scraper.py
cd ../workingnomads && python workingnomads_scraper.py



Project Structure
job-scraping-project/
├── arc_dev/                # Scraper for Arc.dev
│   └── arc_scraper.py
├── general/                # Scraper for General
│   └── general_scraper.py
├── jobspresso/             # Scraper for Jobspresso
│   └── jobspresso_scraper.py
├── pangian/                # Scraper for Pangian
│   └── pangian_scraper.py
├── remotewoman/            # Scraper for Remote Woman
│   └── remotewoman_scraper.py
├── weworkremotely/         # Scraper for We Work Remotely
│   └── weworkremotely_scraper.py
├── workingnomads/          # Scraper for Working Nomads
│   └── workingnomads_scraper.py
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies

Notes

Error Handling: Scripts skip problematic listings and continue.
Headless Mode: Runs in headless mode by default (editable in scripts).
Terms of Service: Respect target websites' policies; add delays if needed.
Scalability: Add new scrapers by mirroring existing folder structure.

