import os
import requests
from jobspy import scrape_jobs
import pandas as pd

# This pulls your Secret from GitHub
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_notification(job_title, company, job_url):
    message = f"🚨 *New Job Drop!* 🚨\n*Role:* {job_title}\n*Company:* {company}\n*Link:* <{job_url}|Apply Here>"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def check_for_jobs():
    # Searching for your specific niche to avoid high competition
    search_term = '("UX Designer" OR "Human Factors") AND (Accessibility OR 508 OR WCAG)'
    
    print(f"Searching for: {search_term}...")
    
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor", "google"],
            search_term=search_term,
            location="Sterling, VA",
            distance=25,
            hours_old=72, # Looking back 3 days for our first run
            results_wanted=10,
        )

        if not jobs.empty:
            print(f"Found {len(jobs)} jobs! Sending to Slack...")
            for index, row in jobs.iterrows():
                send_slack_notification(row['title'], row['company'], row['job_url'])
        else:
            print("No new jobs found matching those keywords.")
    except Exception as e:
        print(f"Scraping error: {e}")

if __name__ == "__main__":
    check_for_jobs()
