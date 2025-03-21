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
# import requests
# from bs4 import BeautifulSoup
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from datetime import datetime
# import os
# import time

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# # Environment variables for API keys
# SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "a2a35764485dca1d60f2335f58a39770269393d1e21117c64b09094884e497ec")
# RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "d21c1eee73mshbc332e6681e8810p1ef5afjsn6e665e83b7d6")
# ACTIVE_JOBS_HOST = "upwork-jobs-api2.p.rapidapi.com"

# class JobScraper:
#     def __init__(self):
#         self.scraping_headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Accept-Language': 'en-US,en;q=0.9'
#         }
        
#         self.api_headers = {
#             "x-rapidapi-key": RAPIDAPI_KEY,
#             "x-rapidapi-host": ACTIVE_JOBS_HOST
#         }

#     # ----------- Web Scraping Methods -----------
#     def scrape_google_jobs(self, query, location=""):
#         """Scrape Google Jobs using SerpAPI"""
#         url = "https://serpapi.com/search"
#         params = {
#             "engine": "google_jobs",
#             "q": f"{query} jobs {location}",
#             "api_key": SERPAPI_KEY
#         }
#         try:
#             response = requests.get(url, params=params)
#             data = response.json()
#             return [self._format_google_job(job) for job in data.get("jobs_results", [])]
#         except Exception as e:
#             print(f"Google Jobs Error: {e}")
#             return []

#     def scrape_indeed(self, query, location=""):
#         """Scrape Indeed directly (fallback)"""
#         try:
#             base_url = "https://www.indeed.com"
#             search_query = query.replace(" ", "+")
#             location_query = location.replace(" ", "+") if location else ""
#             url = f"{base_url}/jobs?q={search_query}&l={location_query}"

#             response = requests.get(url, headers=self.scraping_headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             return [self._format_indeed_job(job) for job in soup.select('div.cardOutline, div.job_seen_beacon')]
#         except Exception as e:
#             print(f"Indeed Scraping Error: {e}")
#             return []

#     def scrape_linkedin(self, query, location=""):
#         """Scrape LinkedIn directly"""
#         try:
#             search_query = query.replace(" ", "%20")
#             location_query = location.replace(" ", "%20") if location else ""
#             url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location_query}"

#             response = requests.get(url, headers=self.scraping_headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             return [self._format_linkedin_job(job) for job in soup.select('div.base-card')]
#         except Exception as e:
#             print(f"LinkedIn Error: {e}")
#             return []

#     # ----------- API Methods -----------
#     def scrape_active_jobs_db(self, query, location=""):
#         """Active Jobs DB API implementation"""
#         url = "https://upwork-jobs-api2.p.rapidapi.com/active-freelance-7d"
#         querystring = {
#             "search": f'"{query}"',
#             "location_filter": f'"{location}"' if location else ""
#         }
#         try:
#             response = requests.get(url, headers=self.api_headers, params=querystring)
#             response.raise_for_status()
#             return [self._format_active_job(job) for job in response.json().get('data', [])]
#         except Exception as e:
#             print(f"Active Jobs DB Error: {e}")
#             return []

#     def scrape_indeed_api(self, query, location=""):
#         """Indeed API via RapidAPI"""
#         url = "https://apidojo-indeed-search.p.rapidapi.com/apidojo"
#         params = {
#             "searchterms": query,
#             "location": location,
#             "sort": "relevance",
#             "country": "us",
#             "radius": "50"
#         }
#         try:
#             response = requests.get(url, headers={
#                 **self.api_headers,
#                 "x-rapidapi-host": "apidojo-indeed-search.p.rapidapi.com"
#             }, params=params)
#             return [self._format_indeed_api_job(job) for job in response.json().get("hits", [])]
#         except Exception as e:
#             print(f"Indeed API Error: {e}")
#             return []

#     # ----------- Formatting Methods -----------
#     def _format_google_job(self, job):
#         return {
#             "title": job.get("title"),
#             "company": job.get("company_name"),
#             "location": job.get("location"),
#             "link": f"https://www.google.com/search?q={job.get('title').replace(' ', '+')}+jobs&ibp=htl;jobs#htidocid={job.get('job_id')}",
#             "source": "Google Jobs"
#         }

#     def _format_indeed_job(self, job):
#         try:
#             return {
#                 "title": job.select_one('h2.jobTitle a').text.strip(),
#                 "company": job.select_one('span.companyName').text.strip(),
#                 "location": job.select_one('div.companyLocation').text.strip(),
#                 "link": f"https://www.indeed.com/viewjob?jk={job.get('data-jk')}",
#                 "source": "Indeed"
#             }
#         except Exception as e:
#             print(f"Format Indeed Error: {e}")
#             return None

#     def _format_linkedin_job(self, job):
#         try:
#             return {
#                 "title": job.select_one('h3.base-search-card__title').text.strip(),
#                 "company": job.select_one('h4.base-search-card__subtitle').text.strip(),
#                 "location": job.select_one('span.job-search-card__location').text.strip(),
#                 "link": job.select_one('a.base-card__full-link')['href'],
#                 "source": "LinkedIn"
#             }
#         except Exception as e:
#             print(f"Format LinkedIn Error: {e}")
#             return None

#     def _format_active_job(self, job):
#         return {
#             "title": job.get("job_title"),
#             "company": job.get("company_name"),
#             "location": job.get("location"),
#             "link": job.get("job_url"),
#             "source": "ActiveJobsDB"
#         }

#     def _format_indeed_api_job(self, job):
#         return {
#             "title": job.get("jobTitle"),
#             "company": job.get("companyName"),
#             "location": job.get("location"),
#             "link": job.get("url"),
#             "source": "Indeed API"
#         }

# @app.route('/api/jobs', methods=['GET'])
# def get_jobs():
#     query = request.args.get('query', '')
#     location = request.args.get('location', '')

#     if not query:
#         return jsonify({"error": "Query parameter is required"}), 400

#     scraper = JobScraper()
    
#     try:
#         # Web scraping sources
#         google_jobs = scraper.scrape_google_jobs(query, location)
#         indeed_jobs = list(filter(None, scraper.scrape_indeed(query, location)))
#         linkedin_jobs = list(filter(None, scraper.scrape_linkedin(query, location)))
        
#         # API sources
#         active_jobs = scraper.scrape_active_jobs_db(query, location)
#         indeed_api_jobs = scraper.scrape_indeed_api(query, location)
        
#         # Combine all results
#         all_jobs = google_jobs + indeed_jobs + linkedin_jobs + active_jobs + indeed_api_jobs
        
#         return jsonify({
#             "timestamp": datetime.now().isoformat(),
#             "query": query,
#             "location": location,
#             "count": len(all_jobs),
#             "jobs": all_jobs
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=False, host='0.0.0.0', port=port)

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Environment variables for API keys
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "your_serpapi_key")

class JobScraper:
    def __init__(self):
        self.scraping_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    # ----------- Web Scraping Methods -----------
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
            return [self._format_google_job(job) for job in data.get("jobs_results", [])]
        except Exception as e:
            print(f"Google Jobs Error: {e}")
            return []

    def scrape_linkedin(self, query, location=""):
        """Scrape LinkedIn directly"""
        try:
            search_query = query.replace(" ", "%20")
            location_query = location.replace(" ", "%20") if location else ""
            url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location_query}"

            response = requests.get(url, headers=self.scraping_headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return [self._format_linkedin_job(job) for job in soup.select('div.base-card')]
        except Exception as e:
            print(f"LinkedIn Error: {e}")
            return []

    # ----------- Microsoft Jobs API -----------
    def scrape_microsoft_jobs(self, query, location=""):
        """Scrape Microsoft Careers using their internal API"""
        try:
            url = "https://careers.microsoft.com/widgets"
            params = {
                'lang': 'en_us',
                'deviceType': 'desktop',
                'country': 'us',
                'pageName': 'search-results',
                'sortBy': 'Most recent',
                'q': query,
                'location': location
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                **self.scraping_headers
            }

            response = requests.post(url, headers=headers, data=params)
            response.raise_for_status()
            
            jobs = []
            data = response.json()
            
            for job in data.get('jobs', []):
                jobs.append({
                    "title": job.get('title'),
                    "company": "Microsoft",
                    "location": ", ".join(job.get('locations', [])),
                    "link": f"https://careers.microsoft.com{job.get('applyUrl')}",
                    "source": "Microsoft Careers"
                })
            
            return jobs

        except Exception as e:
            print(f"Microsoft Jobs API Error: {e}")
            return []

    # ----------- Formatting Methods -----------
    def _format_google_job(self, job):
        return {
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "link": f"https://www.google.com/search?q={job.get('title').replace(' ', '+')}+jobs&ibp=htl;jobs#htidocid={job.get('job_id')}",
            "source": "Google Jobs"
        }

    def _format_linkedin_job(self, job):
        try:
            return {
                "title": job.select_one('h3.base-search-card__title').text.strip(),
                "company": job.select_one('h4.base-search-card__subtitle').text.strip(),
                "location": job.select_one('span.job-search-card__location').text.strip(),
                "link": job.select_one('a.base-card__full-link')['href'],
                "source": "LinkedIn"
            }
        except Exception as e:
            print(f"Format LinkedIn Error: {e}")
            return None

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    query = request.args.get('query', '')
    location = request.args.get('location', '')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    scraper = JobScraper()
    
    try:
        # Web scraping sources
        google_jobs = scraper.scrape_google_jobs(query, location)
        linkedin_jobs = list(filter(None, scraper.scrape_linkedin(query, location)))
        microsoft_jobs = scraper.scrape_microsoft_jobs(query, location)
        
        # Combine all results
        all_jobs = google_jobs + linkedin_jobs + microsoft_jobs
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "location": location,
            "count": len(all_jobs),
            "jobs": all_jobs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)