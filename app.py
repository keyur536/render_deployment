# import requests
# from bs4 import BeautifulSoup
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import re
# from datetime import datetime
# import os

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all domains

# # Get API key from environment variable
# SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "a2a35764485dca1d60f2335f58a39770269393d1e21117c64b09094884e497ec")

# class JobScraper:
#     def __init__(self):
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }

#     def scrape_google_jobs(self, query, location=""):
#         """Scrape Google Jobs using SerpAPI"""
#         url = "https://serpapi.com/search"
#         params = {
#             "engine": "google_jobs",
#             "q": f"{query} jobs {location}",
#             "api_key": SERPAPI_KEY  # Using environment variable
#         }
#         try:
#             response = requests.get(url, params=params)
#             data = response.json()

#             jobs = []
#             for job in data.get("jobs_results", []):
#                 jobs.append({
#                     "title": job.get("title"),
#                     "company": job.get("company_name"),
#                     "location": job.get("location"),
#                     "link": f"https://www.google.com/search?q={query.replace(' ', '+')}+jobs+{location.replace(' ', '+')}&ibp=htl;jobs#htidocid={job.get('job_id')}",
#                     "source": "Google Jobs"
#                 })
#             return jobs
#         except Exception as e:
#             print(f"Error scraping Google Jobs: {e}")
#             return []

#     def scrape_indeed(self, query, location=""):
#         """Scrape Indeed for job listings"""
#         try:
#             base_url = "https://www.indeed.com"
#             search_query = query.replace(" ", "+")
#             location_query = location.replace(" ", "+") if location else ""
#             url = f"{base_url}/jobs?q={search_query}&l={location_query}"

#             response = requests.get(url, headers=self.headers)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             job_listings = []
#             job_cards = soup.select('div.job_seen_beacon')

#             for job in job_cards:
#                 try:
#                     title = job.select_one('h2.jobTitle a').text.strip()
#                     company = job.select_one('span.companyName').text.strip()
#                     location = job.select_one('div.companyLocation').text.strip()
#                     description = job.select_one('div.job-snippet').text.strip()
#                     job_id = job['data-jk']

#                     job_listings.append({
#                         'title': title,
#                         'company': company,
#                         'location': location,
#                         'description': description,
#                         'link': f"{base_url}/viewjob?jk={job_id}",
#                         'source': 'Indeed'
#                     })
#                 except Exception as e:
#                     print(f"Error extracting Indeed job: {e}")
#                     continue

#             return job_listings
#         except Exception as e:
#             print(f"Error scraping Indeed: {e}")
#             return []

#     def scrape_linkedin(self, query, location=""):
#         """Scrape LinkedIn for job listings"""
#         try:
#             search_query = query.replace(" ", "%20")
#             location_query = location.replace(" ", "%20") if location else ""
#             url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location_query}"

#             response = requests.get(url, headers=self.headers)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             job_listings = []
#             job_cards = soup.select('div.base-card')

#             for job in job_cards:
#                 try:
#                     title = job.select_one('h3.base-search-card__title').text.strip()
#                     company = job.select_one('h4.base-search-card__subtitle').text.strip()
#                     location = job.select_one('span.job-search-card__location').text.strip()
#                     link = job.select_one('a.base-card__full-link')['href']

#                     job_listings.append({
#                         'title': title,
#                         'company': company,
#                         'location': location,
#                         'description': "Click to view full job details",
#                         'link': link,
#                         'source': 'LinkedIn'
#                     })
#                 except Exception as e:
#                     print(f"Error extracting LinkedIn job: {e}")
#                     continue

#             return job_listings
#         except Exception as e:
#             print(f"Error scraping LinkedIn: {e}")
#             return []

# @app.route('/', methods=['GET'])
# def index():
#     """Root endpoint for health check"""
#     return jsonify({
#         "status": "online",
#         "message": "Job Scraper API is running. Use /api/jobs?query=JOBNAME&location=LOCATION to search for jobs."
#     })

# @app.route('/api/jobs', methods=['GET'])
# def get_jobs():
#     """API endpoint to fetch jobs"""
#     query = request.args.get('query', '')
#     location = request.args.get('location', '')

#     if not query:
#         return jsonify({"error": "Query parameter is required"}), 400

#     scraper = JobScraper()

#     # Scrape jobs from multiple sources
#     google_jobs = scraper.scrape_google_jobs(query, location)
#     indeed_jobs = scraper.scrape_indeed(query, location)
#     linkedin_jobs = scraper.scrape_linkedin(query, location)

#     # Combine results
#     all_jobs = google_jobs + indeed_jobs + linkedin_jobs

#     # Add timestamp
#     timestamp = datetime.now().isoformat()

#     return jsonify({
#         "timestamp": timestamp,
#         "query": query,
#         "location": location,
#         "count": len(all_jobs),
#         "jobs": all_jobs
#     })

# if __name__ == '__main__':
#     # Use PORT environment variable for cloud deployment
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=False, host='0.0.0.0', port=port)

import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
import os
import time  # For rate limiting

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get API key from environment variable
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "a2a35764485dca1d60f2335f58a39770269393d1e21117c64b09094884e497ec")

class JobScraper:
    def __init__(self):
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def scrape_google_jobs(self, query, location=""):
        """Scrape Google Jobs using SerpAPI"""
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_jobs",
            "q": f"{query} jobs {location}",
            "api_key": SERPAPI_KEY
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()

            jobs = []
            for job in data.get("jobs_results", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "link": f"https://www.google.com/search?q={query.replace(' ', '+')}+jobs+{location.replace(' ', '+')}&ibp=htl;jobs#htidocid={job.get('job_id')}",
                    "source": "Google Jobs"
                })
            return jobs
        except Exception as e:
            print(f"Google Jobs Error: {str(e)}")
            return []

    def scrape_indeed(self, query, location=""):
        """Scrape Indeed for job listings with enhanced anti-bot measures"""
        try:
            base_url = "https://www.indeed.com"
            search_query = query.replace(" ", "+")
            location_query = location.replace(" ", "+") if location else ""
            url = f"{base_url}/jobs?q={search_query}&l={location_query}"

            # Enhanced headers for Indeed
            headers = {
                **self.base_headers,
                'Referer': 'https://www.google.com/',
                'DNT': '1'
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = []

            # Updated CSS selector for Indeed's current layout
            job_cards = soup.select('div.cardOutline, div.job_seen_beacon')

            for job in job_cards:
                try:
                    title_elem = job.select_one('h2.jobTitle a')
                    company_elem = job.select_one('span.companyName')
                    location_elem = job.select_one('div.companyLocation')
                    
                    # Validate elements before processing
                    if not all([title_elem, company_elem, location_elem]):
                        continue

                    job_id = job.get('data-jk') or job.get('id', '').split('-')[-1]
                    
                    job_listings.append({
                        'title': title_elem.text.strip(),
                        'company': company_elem.text.strip(),
                        'location': location_elem.text.strip(),
                        'link': f"{base_url}/viewjob?jk={job_id}",
                        'source': 'Indeed'
                    })
                    
                    # Rate limiting to avoid blocking
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Indeed Job Processing Error: {str(e)}")
                    continue

            return job_listings

        except requests.HTTPError as e:
            print(f"Indeed HTTP Error ({e.response.status_code}): {url}")
            return []
        except Exception as e:
            print(f"Indeed General Error: {str(e)}")
            return []

    def scrape_linkedin(self, query, location=""):
        """Scrape LinkedIn for job listings"""
        try:
            search_query = query.replace(" ", "%20")
            location_query = location.replace(" ", "%20") if location else ""
            url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location_query}"

            response = requests.get(url, headers=self.base_headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            job_listings = []
            job_cards = soup.select('div.base-card')

            for job in job_cards:
                try:
                    title = job.select_one('h3.base-search-card__title').text.strip()
                    company = job.select_one('h4.base-search-card__subtitle').text.strip()
                    location = job.select_one('span.job-search-card__location').text.strip()
                    link = job.select_one('a.base-card__full-link')['href']

                    job_listings.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'link': link,
                        'source': 'LinkedIn'
                    })
                except Exception as e:
                    print(f"LinkedIn Job Error: {str(e)}")
                    continue

            return job_listings
        except Exception as e:
            print(f"LinkedIn General Error: {str(e)}")
            return []

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "message": "Job Scraper API is running. Use /api/jobs?query=JOBNAME&location=LOCATION to search."
    })

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    query = request.args.get('query', '')
    location = request.args.get('location', '')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    scraper = JobScraper()

    # Scrape from all sources
    try:
        google_jobs = scraper.scrape_google_jobs(query, location)
        indeed_jobs = scraper.scrape_indeed(query, location)
        linkedin_jobs = scraper.scrape_linkedin(query, location)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    all_jobs = google_jobs + indeed_jobs + linkedin_jobs

    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "location": location,
        "count": len(all_jobs),
        "jobs": all_jobs
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)