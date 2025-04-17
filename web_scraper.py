import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import logging
import argparse
from datetime import datetime
import os

# ------------------ Logging Setup ------------------ #
logging.basicConfig(
    filename='web_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------ Scraping Function ------------------ #
def scrape_jobs():
    url = "https://vacancymail.co.zw/jobs/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully accessed {url}")
    except requests.RequestException as e:
        logging.error(f"Network error: {e}")
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = soup.find_all('article')

        jobs = []
        for job in job_listings:
            try:
                title = job.find('h2').get_text(strip=True)
                company = job.find('span', class_='company').get_text(strip=True)
                location = job.find('span', class_='location').get_text(strip=True)
                expiry_date = job.find('span', class_='expiry-date').get_text(strip=True)
                description_tag = job.find('div', class_='job-description')
                description = description_tag.get_text(strip=True) if description_tag else "No description provided"

                jobs.append({
                    'Job Title': title,
                    'Company': company,
                    'Location': location,
                    'Expiry Date': expiry_date,
                    'Job Description': description
                })

            except AttributeError as e:
                logging.warning(f"Skipped a job due to missing fields: {e}")
                continue

        if not jobs:
            logging.warning("No job listings were scraped.")
            return

        df = pd.DataFrame(jobs)
        df.drop_duplicates(inplace=True)

        # Create output directory if it doesn't exist
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)

        # Create filenames with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_file = os.path.join(output_dir, f'scraped_jobs_{timestamp}.csv')
        json_file = os.path.join(output_dir, f'scraped_jobs_{timestamp}.json')

        df.to_csv(csv_file, index=False)
        df.to_json(json_file, orient='records', indent=2)

        logging.info(f"Scraped {len(df)} job(s). Saved to {csv_file} and {json_file}.")
        print(f"✅ Saved CSV: {csv_file}")

    except Exception as e:
        logging.error(f"Failed to process the page: {e}")

# ------------------ Scheduling ------------------ #
def schedule_scrape(interval: str):
    try:
        if interval == 'daily':
            schedule.every().day.at("10:00").do(scrape_jobs)
            logging.info("Scheduled for daily scraping at 10:00.")
        elif interval == 'hourly':
            schedule.every().hour.do(scrape_jobs)
            logging.info("Scheduled for hourly scraping.")
        else:
            logging.warning(f"Invalid interval: {interval}")
            return

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logging.error(f"Scheduling error: {e}")

# ------------------ CLI Interface ------------------ #
def parse_args():
    parser = argparse.ArgumentParser(description="Web scraper for Zimbabwe job listings.")
    parser.add_argument('--run', action='store_true', help='Run the scraper once immediately.')
    parser.add_argument('--schedule', choices=['hourly', 'daily'], help='Schedule scraping at intervals.')
    return parser.parse_args()

# ------------------ Entry Point ------------------ #
if __name__ == "__main__":
    args = parse_args()
    if args.run:
        scrape_jobs()
    if args.schedule:
        schedule_scrape(args.schedule)
    if not args.run and not args.schedule:
        print("⚠️  Use --run to run immediately or --schedule hourly/daily to schedule it.")
        logging.warning("No action specified. Use --run or --schedule.")               
        