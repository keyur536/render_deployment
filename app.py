import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Environment variables
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "a2a35764485dca1d60f2335f58a39770269393d1e21117c64b09094884e497ec")

class JobScraper:
    def __init__(self):
        self.scraping_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def get_manual_entry(self):
        """Your custom entry to show first"""
        return [{
            "title": "Mobile Developer (Flutter/Dart) | Location: Mumbai | 10 March",
            "company": "Mverse Technologies",
            "location": "Mumbai, Maharashtra, India",
            "link": "https://www.naukri.com/job-listings-flutter-developer-mverse-technologies-mumbai-mumbai-suburban-mumbai-all-areas-0-to-2-years-100325007726",
            "source": "naukri.com"
        },
        {
            "title": "Mobile App Developer In-Office Job (full time) | Location: Noida | 18 March",
            "company": "Avaronn",
            "location": "Mumbai, Maharashtra, India",
            "link": "https://cuvette.tech/app/public/job/67d7c9da534b5fae43196761",
            "source": "cuvette"
        }]

    def scrape_google_jobs(self, query, location=""):
        """Google Jobs via SerpAPI"""
        try:
            params = {
                "engine": "google_jobs",
                "q": f"{query} jobs {location}",
                "api_key": SERPAPI_KEY
            }
            response = requests.get("https://serpapi.com/search", params=params)
            return [{
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "link": f"https://www.google.com/search?q={query}+jobs+{location}&ibp=htl;jobs",
                "source": "Google Jobs"
            } for job in response.json().get("jobs_results", [])]
        except Exception as e:
            print(f"Google Jobs Error: {e}")
            return []

    def scrape_linkedin(self, query, location=""):
        """LinkedIn Jobs scraper"""
        try:
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query}&location={location}"
            response = requests.get(url, headers=self.scraping_headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            jobs = []
            for job in soup.select('li'):
                try:
                    jobs.append({
                        "title": job.select_one('h3.base-search-card__title').text.strip(),
                        "company": job.select_one('h4.base-search-card__subtitle').text.strip(),
                        "location": job.select_one('span.job-search-card__location').text.strip(),
                        "link": job.select_one('a.base-card__full-link')['href'],
                        "source": "LinkedIn"
                    })
                except Exception as e:
                    print(f"LinkedIn parse error: {e}")
            return jobs
        except Exception as e:
            print(f"LinkedIn failed: {str(e)}")
            return []

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    query = request.args.get('query', '').strip()
    location = request.args.get('location', '').strip()

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    scraper = JobScraper()
    
    try:
        # Get manual entry first
        manual_jobs = scraper.get_manual_entry()
        
        # Get other sources
        google_jobs = scraper.scrape_google_jobs(query, location)
        linkedin_jobs = scraper.scrape_linkedin(query, location)
        
        # Combine results with manual entry first
        all_jobs = manual_jobs + google_jobs + linkedin_jobs
        
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
