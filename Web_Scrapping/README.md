
# Machine Learning Jobs Scraper from Wuzzuf.net

This project is a Python-based web scraper designed to extract Machine Learning job listings from [Wuzzuf.net](https://wuzzuf.net), one of Egypt's leading job portals. It uses the requests and BeautifulSoup libraries to retrieve job data across multiple pages and save it into a structured CSV file.

---

## Project Purpose
This scraper was created to help:
-  Job seekers who want to automate the process of discovering new ML job opportunities
-  Developers who want to learn practical web scraping skills
-  Researchers analyzing job market trends

---

## What This Scraper Does
For every Machine Learning job listing on Wuzzuf, it collects:
-  Job Title
-  Company Name
-  Job Location
-  Posting Date (how many days ago)
-  Tags (general skill/tech terms)
-  Job URL

It repeats this for every page until no more jobs are found, then saves all the data to a CSV file.

---

## Tools & Libraries Used
| Tool | Purpose |
|------|---------|
| requests | To send HTTP GET requests to the website |
| BeautifulSoup (bs4) | To parse and extract data from HTML |
| csv | To store the extracted data into a structured file |
| time.sleep & random.uniform | To simulate human behavior and avoid being blocked |

---

## File Generated
- all_machine_learning_jobs.csv: A comma-separated file containing all scraped job data.

---

## How the Code Works – Step by Step

### 1. Setup
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import uniform
🔍 These are standard libraries used to:
- Send requests to the site
- Parse HTML pages
- Store results
- Randomize delays between requests (important for stealth)

---

### 2. Constants Defined
BASE_URL = "https://wuzzuf.net/search/jobs"
QUERY = "machine learning"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
 We define:
- The base URL for job searching
- The query we’re interested in (machine learning)
- A custom User-Agent header to avoid bot detection

---

### 3. CSV Initialization
with open("all_machine_learning_jobs.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Company", "Location", "Posted", "Tags", "Job URL"])
 This opens (or creates) a CSV file and writes the headers.

---

### 4. Scraping Logic
    page = 0
    total_jobs = 0

    while True:
🔁 The loop runs indefinitely until no more jobs are found.
Each page on Wuzzuf lists 15 jobs, so page * 15 is used to move forward.

        params = {
            "q": QUERY,
            "start": page * 15
        }
This sets the search query and starting index for the next page.

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find_all("div", {"class": "css-1gatmva"})
 We fetch the page, parse its content, and locate all job boxes.

---

### 5. Data Extraction for Each Job
        for job in jobs:
Loop over every job posting.

#### a. Job Title & URL
            title_elem = job.find("h2", {"class": "css-m604qf"})
            title = title_elem.text.strip() if title_elem else "N/A"
            job_link_tag = title_elem.find("a") if title_elem else None
            job_url = f"https://wuzzuf.net{job_link_tag['href']}" if job_link_tag else "N/A"
 We extract the job title and link to its full description.

#### b. Company Name
            company_elem = job.find("a", {"class": "css-17s97q8"})
            company = company_elem.text.strip() if company_elem else "N/A"
 Straightforward: just get the anchor tag with the correct class.
#### c. Location
            location_elem = job.find("span", {"class": "css-5wys0k"})
            location = location_elem.text.strip() if location_elem else "N/A"
 Same logic for location.

#### d. Posting Date
            posted_elem = job.find("div", {"class": "css-do6t5g"})
            posted = posted_elem.text.strip() if posted_elem else "N/A"
 Shows how long ago it was posted (e.g., “3 days ago”).

#### e. Tags (General Skills)
            tags_list = job.find_all("a", {"class": "css-o171kl"})
            tags = ", ".join([tag.text.strip() for tag in tags_list]) if tags_list else "N/A"
 Collect all skills/tags shown under each post (may include tools like Python, SQL, etc.).

#### f. Write to CSV
            writer.writerow([title, company, location, posted, tags, job_url])
 Add the job info as a new row in the CSV file.

---

### 6. Finish One Page
        page += 1
        sleep(uniform(1.5, 2.5))   
 Move to the next page.
 Pause between requests to avoid being blocked by the site.

---

### 7. Wrap-Up
print(f"\n All done! Total jobs scraped: {total_jobs}")
print(" Data saved to 'all_machine_learning_jobs.csv'")
 Print summary when done.

---

## How to Run the Code
### Prerequisites
Ensure you have Python installed, then run:
pip install requests beautifulsoup4
### Run the script
python your_script_name.py
### Output
Check your current directory for all_machine_learning_jobs.csv.

---

## Notes & Tips
- Don’t overrun the site: Wuzzuf may block your IP if you send too many requests too quickly.
- Be respectful: Scraping should follow the website's [robots.txt](https://wuzzuf.net/robots.txt) and terms of use.
- Always test: Websites update their structure; your scraper might break over time.
- Use proxies and error-handling if you're scaling this in real-life applications.

---

## Why This Scraper is Impressive
-  Works across multiple pages automatically
-  Collects all essential info job seekers need
-  Generates clean and structured CSV output
-  A great example of professional scraping using only requests and BeautifulSoup

---

## Built By
A passionate learner who wanted to master web scraping, understand how job sites work under the hood, and build something useful and insightful — line by line, with full understanding of every piece of code ❤️

---

> If you found this project useful or inspiring, feel free to star the repo and share feedback