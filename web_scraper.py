import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

# ------------------ Logging Setup ------------------ #
logging.basicConfig(
    filename='job_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------ Scraping Function ------------------ #
def scrape_and_save_jobs():
    url = "https://vacancymail.co.zw/jobs/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Successfully accessed the site.")
    except requests.RequestException as e:
        logging.error(f"Network error: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('a', class_='job-listing')

    jobs = []

    for job in listings:
        try:
            title = job.find('h3', class_='job-listing-title').get_text(strip=True)

            # Company might be in h4 or only as alt of the logo
            company_tag = job.find('h4', class_='job-listing-company')
            if company_tag:
                company = company_tag.get_text(strip=True)
            else:
                logo = job.find('div', class_='job-listing-company-logo').find('img')
                company = logo['alt'].strip() if logo and 'alt' in logo.attrs else 'Unknown'

            location = job.find('li').get_text(strip=True)
            description = job.find('p', class_='job-listing-text').get_text(strip=True)

            # Get expiry
            footer = job.find('div', class_='job-listing-footer')
            expiry = 'N/A'
            for li in footer.find_all('li'):
                if 'Expires' in li.text:
                    expiry = li.get_text(strip=True).replace('Expires', '').strip()
                    break

            jobs.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Expiry Date": expiry,
                "Description": description
            })

        except Exception as e:
            logging.warning(f"Skipped a listing due to error: {e}")
            continue

    if jobs:
        df = pd.DataFrame(jobs)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scraped_jobs_{timestamp}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(jobs)} jobs to {filename}")
        print(f"✅ Scraped and saved {len(jobs)} jobs to {filename}")
    else:
        logging.warning("No jobs found.")

# ------------------ Run Scraper ------------------ #
if __name__ == "__main__":
    scrape_and_save_jobs()
          
        
