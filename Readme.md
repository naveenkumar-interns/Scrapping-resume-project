# Job Scraping Project

## Overview
This project includes six web scraping scripts to extract job listings from various platforms: Arc.dev, General, Jobspresso, Pangian, Remote Woman, and We Work Remotely, with an additional scraper for Working Nomads. Using Playwright and Python, each script collects job details like title, company, salary range, skills, location, and more, saving the data in JSON format.

## Features
- Scrapes jobs from six unique job boards.
- Extracts:
  - Job title
  - Company name
  - Job type
  - Experience level
  - Salary range
  - Required skills
  - Location
  - Hiring status
  - Job URL and logo URL
- Saves data as JSON files.
- Includes error handling.
- Uses asynchronous execution.

## Prerequisites
- **Python 3.8+**
- **Playwright** with browser binaries
- Required packages:
  - `playwright`
  - `asyncio`
  - `json`

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/naveenkumar-interns/Scrapping-resume-project.git
   cd Scrapping-resume-project
   ```

2. **Set up a virtual environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Usage
1. **Run a specific scraper**:
   Navigate to the folder and execute the script. Example for Arc.dev:
   ```bash
   cd arc_dev
   python arc_scraper.py
   ```
   Output is saved to `arc_jobs.json`.

2. **Output**:
   - Each script creates a JSON file (e.g., `arc_jobs.json`).
   - Console displays job count and details.

3. **Run all scrapers**:
   Execute manually or automate:
   ```bash
   cd arc_dev && python arc_scraper.py
   cd ../general && python general_scraper.py
   cd ../jobspresso && python jobspresso_scraper.py
   cd ../pangian && python pangian_scraper.py
   cd ../remotewoman && python remotewoman_scraper.py
   cd ../weworkremotely && python weworkremotely_scraper.py
   cd ../workingnomads && python workingnomads_scraper.py
   ```

## Project Structure
```
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
└── requirements.txt        # Dependencies
```

## Notes
- **Error Handling**: Skips problematic listings.
- **Headless Mode**: Default is headless (editable in scripts).
- **Terms of Service**: Respect website policies; add delays if needed.
- **Scalability**: Add new scrapers with matching structure.
