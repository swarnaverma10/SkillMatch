# src/job_api.py
# Dummy job data (Apify removed)

def fetch_linkedin_jobs(search_query, rows=60):
    return [
        {
            "title": "Junior AI Engineer",
            "company": "TechCorp",
            "location": "India",
            "applyLink": "https://example.com"
        },
        {
            "title": "Python Developer",
            "company": "StartupX",
            "location": "Remote",
            "applyLink": "https://example.com"
        },
        {
            "title": "Data Analyst",
            "company": "AnalyticsHub",
            "location": "Bangalore",
            "applyLink": "https://example.com"
        }
    ]


def fetch_naukri_jobs(search_query, rows=60):
    return [
        {
            "title": "Machine Learning Intern",
            "company": "AI Labs",
            "location": "India",
            "applyLink": "https://example.com"
        },
        {
            "title": "Software Engineer (Python)",
            "company": "GlobalTech",
            "location": "Hybrid",
            "applyLink": "https://example.com"
        }
    ]

