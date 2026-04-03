# src/job_api.py

def fetch_linkedin_jobs(search_query, rows=60):
    return [
        {
            "title": "Junior AI Engineer",
            "companyName": "TechCorp Solutions",
            "location": "India (Remote)",
            "link": "https://linkedin.com/jobs/view/12345"
        },
        {
            "title": "Machine Learning Engineer",
            "companyName": "Innova AI",
            "location": "Bangalore, KA",
            "link": "https://linkedin.com/jobs/view/23456"
        },
        {
            "title": "Python Developer (GenAI)",
            "companyName": "Future Systems",
            "location": "Hyderabad, TS",
            "link": "https://linkedin.com/jobs/view/34567"
        },
        {
            "title": "Data Scientist",
            "companyName": "DataMinds",
            "location": "Remote",
            "link": "https://linkedin.com/jobs/view/45678"
        },
        {
            "title": "Backend Developer (FastAPI)",
            "companyName": "CloudScale",
            "location": "Mumbai, MH",
            "link": "https://linkedin.com/jobs/view/56789"
        }
    ]


def fetch_naukri_jobs(search_query, rows=60):
    return [
        {
            "title": "AI & ML Intern",
            "companyName": "DeepLearning Labs",
            "location": "Pune, MH",
            "url": "https://naukri.com/job/view/98765"
        },
        {
            "title": "Research Assistant (AI)",
            "companyName": "University AI Lab",
            "location": "India (Hybrid)",
            "url": "https://naukri.com/job/view/87654"
        },
        {
            "title": "Software Engineer (NLP)",
            "companyName": "Syntax AI",
            "location": "Chennai, TN",
            "url": "https://naukri.com/job/view/76543"
        }
    ]

