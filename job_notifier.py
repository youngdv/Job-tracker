import os
import requests
from jobspy import scrape_jobs
import pandas as pd

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_notification(job_title, company, job_url):
    message = f"🚨 *New Job Drop!* 🚨\n*Role:* {job_title}\n*Company:* {company}\n*Link:* <{job_url}|Apply Here>"
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def check_for_jobs():
    search_term = '("UX Designer" OR "Product Designer" OR "Human Factors") AND (Accessibility OR 508 OR WCAG) -Poly -Polygraph -TS/SCI -Clearance -Security'
    
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor", "google"],
            search_term=search_term,
            location="Sterling, VA",
            distance=25,
            hours_old=72,
            results_wanted=20,
        )

        if not jobs.empty:
            # 1. Update the Website (index.html)
            html_table = jobs[['title', 'company', 'job_url']].to_html(render_links=True, index=False)
            with open("index.html", "w") as f:
                f.write(f"<html><body><h1>Destinee's Job Board</h1>{html_table}</body></html>")
            
            # 2. Still send notifications to Slack
            for index, row in jobs.iterrows():
                send_slack_notification(row['title'], row['company'], row['job_url'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_for_jobs()
