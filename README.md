# 🇿🇼 Zimbabwe Job Listings Web Scraper

This Python script scrapes job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/) and saves the data into CSV and JSON files. You can run the script once or schedule it to run daily or hourly using command-line arguments.

---

Features

- Scrapes job title, company, location, expiry date, and description
- Saves jobs to timestamped CSV and JSON files
- Handles missing data gracefully
- Logs activity in `web_scraper.log`
- Can be run once or scheduled to run automatically

---

## Technologies Used

- Python 3
- `requests` for fetching webpages
- `BeautifulSoup` for HTML parsing
- `pandas` for data handling and saving
- `schedule` for periodic scraping
- `argparse` for command-line interaction
- `logging` for error tracking

---

Getting Started

### Requirements

- Python 3.6+
- Install dependencies:

```bash
pip install -r requirements.txt
