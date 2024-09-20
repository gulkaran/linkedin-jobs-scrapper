from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import csv
import time

# incognito mode for Chrome
chrome_options = Options()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

url = "https://www.linkedin.com/jobs/search?keywords=Software%20%22intern%22%20OR%20%22co-op%22&location=Canada&geoId=101174742&f_TPR=r86400&position=1&pageNum=0"
driver.get(url)

time.sleep(3)

driver.get(url)

WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list")))

# Initialize CSV file
with open('linkedin_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Employer', 'Description'])

    # Iterate through job listings
    job_listings = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list > li")
    for job in job_listings:
        # Click on the job listing
        job.click()
        time.sleep(2)  # Wait for job details to load

        # Get the page source after clicking
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract job details
        try:
            job_title = soup.find('h2', class_='top-card-layout__title').text.strip()
            employer = soup.find('a', class_='topcard__org-name-link').text.strip()
            description = soup.find('div', class_='show-more-less-html__markup').text.strip()
            link = driver.current_url

            # Write to CSV
            writer.writerow([job_title, employer, link, description])
        except AttributeError:
            print("Failed to extract details for a job listing. Skipping...")

        time.sleep(1)  # Pause between job listings

# Close the browser
driver.quit()