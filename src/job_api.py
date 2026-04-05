import re
import random
import urllib.parse

# Real LinkedIn/Naukri search URLs generator
def _linkedin_url(title, company, location):
    q = urllib.parse.quote_plus(f"{title} {company}")
    loc = urllib.parse.quote_plus(location or "India")
    return f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}"

def _naukri_url(title, location):
    t = title.lower().replace(" ", "-")
    loc = (location or "india").lower().replace(" ", "-")
    return f"https://www.naukri.com/{t}-jobs-in-{loc}"

def _indeed_url(title, company, location):
    q = urllib.parse.quote_plus(f"{title} {company}")
    loc = urllib.parse.quote_plus(location or "India")
    return f"https://in.indeed.com/jobs?q={q}&l={loc}"

JOB_DATA = {
    "data scientist": [
        {"title":"Data Scientist","company":"Flipkart","location":"Bangalore","desc":"Work on recommendation systems and customer behavior analytics using ML models.","skills":["Python","Machine Learning","SQL","Pandas","Scikit-learn"],"salary":"18-28 LPA"},
        {"title":"Data Scientist","company":"Swiggy","location":"Bangalore","desc":"Build predictive models for delivery time estimation and demand forecasting.","skills":["Python","Deep Learning","TensorFlow","SQL","Statistics"],"salary":"20-30 LPA"},
        {"title":"Senior Data Scientist","company":"Paytm","location":"Noida","desc":"Lead fraud detection and risk scoring models for financial transactions.","skills":["Python","Machine Learning","Spark","SQL","NLP"],"salary":"25-40 LPA"},
        {"title":"Data Scientist","company":"Zomato","location":"Gurugram","desc":"Develop personalization algorithms and food recommendation engines.","skills":["Python","Machine Learning","Pandas","A/B Testing","SQL"],"salary":"16-26 LPA"},
        {"title":"ML Data Scientist","company":"Razorpay","location":"Bangalore","desc":"Build ML pipelines for payment fraud detection and credit risk.","skills":["Python","Machine Learning","MLOps","SQL","Docker"],"salary":"22-35 LPA"},
        {"title":"Data Scientist","company":"CRED","location":"Bangalore","desc":"Work on credit scoring and member behavior modeling.","skills":["Python","Statistics","SQL","Machine Learning","R"],"salary":"20-32 LPA"},
    ],
    "software engineer": [
        {"title":"Software Engineer","company":"Google","location":"Hyderabad","desc":"Design and build scalable backend services for Google Cloud platform.","skills":["Python","Java","Go","Distributed Systems","SQL"],"salary":"30-50 LPA"},
        {"title":"SDE II","company":"Amazon","location":"Bangalore","desc":"Build microservices for AWS infrastructure and customer-facing APIs.","skills":["Java","AWS","Microservices","SQL","Python"],"salary":"28-45 LPA"},
        {"title":"Software Engineer","company":"Microsoft","location":"Hyderabad","desc":"Develop features for Microsoft Azure cloud services and developer tools.","skills":["C#","Azure","Python","TypeScript","REST API"],"salary":"25-42 LPA"},
        {"title":"Backend Engineer","company":"Razorpay","location":"Bangalore","desc":"Build high-performance payment APIs handling millions of transactions daily.","skills":["Go","Node.js","PostgreSQL","Redis","Docker"],"salary":"20-35 LPA"},
        {"title":"Full Stack Engineer","company":"Meesho","location":"Bangalore","desc":"Own end-to-end features for seller dashboard and buyer experience.","skills":["React","Node.js","Python","MongoDB","AWS"],"salary":"18-30 LPA"},
        {"title":"Software Engineer","company":"Freshworks","location":"Chennai","desc":"Build SaaS CRM features used by thousands of businesses worldwide.","skills":["Ruby","React","PostgreSQL","AWS","Git"],"salary":"15-25 LPA"},
    ],
    "full stack developer": [
        {"title":"Full Stack Developer","company":"Zoho","location":"Chennai","desc":"Build and maintain cloud-based SaaS products used by millions globally.","skills":["React","Node.js","Java","MySQL","REST API"],"salary":"12-22 LPA"},
        {"title":"Full Stack Engineer","company":"PhonePe","location":"Bangalore","desc":"Develop mobile and web apps for India's largest UPI payment platform.","skills":["React","Python","Django","PostgreSQL","AWS"],"salary":"18-30 LPA"},
        {"title":"Full Stack Developer","company":"Meesho","location":"Bangalore","desc":"Build seller and buyer facing features for India's social commerce platform.","skills":["React","Node.js","MongoDB","Redis","Docker"],"salary":"15-25 LPA"},
        {"title":"MERN Stack Developer","company":"Startup Hub","location":"Remote","desc":"Work on a fast-growing edtech product used by 500K+ students.","skills":["MongoDB","Express","React","Node.js","AWS"],"salary":"10-18 LPA"},
        {"title":"Full Stack Engineer","company":"Infosys","location":"Pune","desc":"Develop enterprise web applications for global banking clients.","skills":["Angular","Java","Spring","Oracle","Docker"],"salary":"8-15 LPA"},
    ],
    "python developer": [
        {"title":"Python Developer","company":"Freshworks","location":"Chennai","desc":"Build automation scripts and backend APIs for SaaS CRM platform.","skills":["Python","Django","PostgreSQL","REST API","Git"],"salary":"10-18 LPA"},
        {"title":"Python Backend Engineer","company":"Razorpay","location":"Bangalore","desc":"Build high-performance Python microservices for payment processing.","skills":["Python","FastAPI","PostgreSQL","Redis","Docker"],"salary":"18-30 LPA"},
        {"title":"Python Developer","company":"Wipro","location":"Bangalore","desc":"Develop data pipelines and automation tools for enterprise clients.","skills":["Python","SQL","ETL","Pandas","Linux"],"salary":"8-14 LPA"},
        {"title":"Senior Python Developer","company":"Zomato","location":"Gurugram","desc":"Build scalable backend for food delivery and logistics management.","skills":["Python","Django","Celery","PostgreSQL","AWS"],"salary":"20-32 LPA"},
    ],
    "machine learning engineer": [
        {"title":"ML Engineer","company":"Google","location":"Hyderabad","desc":"Build and deploy large-scale ML models for Google Search and Ads.","skills":["Python","TensorFlow","MLOps","Kubernetes","SQL"],"salary":"35-55 LPA"},
        {"title":"ML Engineer","company":"Flipkart","location":"Bangalore","desc":"Develop recommendation and ranking models for e-commerce search.","skills":["Python","Machine Learning","Spark","Docker","SQL"],"salary":"25-40 LPA"},
        {"title":"Applied ML Engineer","company":"CRED","location":"Bangalore","desc":"Build credit risk and fraud detection ML models for fintech platform.","skills":["Python","Machine Learning","MLflow","PostgreSQL","AWS"],"salary":"22-38 LPA"},
        {"title":"ML Engineer","company":"Swiggy","location":"Bangalore","desc":"Build real-time ML systems for delivery optimization and ETA prediction.","skills":["Python","Machine Learning","Kafka","TensorFlow","Go"],"salary":"20-35 LPA"},
    ],
    "frontend developer": [
        {"title":"Frontend Developer","company":"Zepto","location":"Mumbai","desc":"Build lightning-fast React interfaces for India's 10-minute grocery delivery app.","skills":["React","TypeScript","CSS","Redux","REST API"],"salary":"12-22 LPA"},
        {"title":"React Developer","company":"PhonePe","location":"Bangalore","desc":"Build and optimize the PhonePe web app used by 500M+ users.","skills":["React","JavaScript","TypeScript","HTML","CSS"],"salary":"15-26 LPA"},
        {"title":"UI Developer","company":"Infosys","location":"Pune","desc":"Develop responsive UI components for global banking enterprise clients.","skills":["Angular","TypeScript","HTML","CSS","JavaScript"],"salary":"8-15 LPA"},
        {"title":"Frontend Engineer","company":"Meesho","location":"Bangalore","desc":"Own the buyer-facing product experience across web and mobile.","skills":["React","Next.js","TypeScript","CSS","Figma"],"salary":"14-24 LPA"},
    ],
    "devops engineer": [
        {"title":"DevOps Engineer","company":"Amazon","location":"Bangalore","desc":"Manage CI/CD pipelines and infrastructure for AWS services.","skills":["AWS","Docker","Kubernetes","Terraform","Python"],"salary":"18-32 LPA"},
        {"title":"Site Reliability Engineer","company":"Flipkart","location":"Bangalore","desc":"Ensure 99.99% uptime for India's largest e-commerce platform.","skills":["Kubernetes","Docker","Linux","Python","Prometheus"],"salary":"20-35 LPA"},
        {"title":"DevOps Engineer","company":"Infosys","location":"Pune","desc":"Build and maintain CI/CD pipelines for enterprise cloud migration projects.","skills":["Jenkins","Docker","AWS","Ansible","Linux"],"salary":"10-18 LPA"},
    ],
}

POSTED = ["Today","Yesterday","2 days ago","3 days ago","1 week ago"]

def _match_score(resume_text, job_skills):
    if not resume_text:
        return random.randint(50, 75)
    r = resume_text.lower()
    matched = sum(1 for s in job_skills if s.lower() in r)
    base = int((matched / max(len(job_skills), 1)) * 100)
    return min(98, max(40, base + random.randint(-5, 5)))

def fetch_jobs(role, location, resume_text):
    role_lower = role.lower().strip()
    matched_cat = None
    best = 0
    for cat in JOB_DATA:
        overlap = sum(1 for w in cat.split() if w in role_lower)
        if overlap > best:
            best = overlap
            matched_cat = cat
    if not matched_cat or best == 0:
        matched_cat = "software engineer"

    results = []
    for job in JOB_DATA[matched_cat]:
        loc = location if location else job["location"]
        score = _match_score(resume_text, job["skills"])

        # Generate real search URLs
        li_url  = _linkedin_url(job["title"], job["company"], loc)
        nk_url  = _naukri_url(job["title"], loc)
        ind_url = _indeed_url(job["title"], job["company"], loc)

        results.append({
            "title":           job["title"],
            "company":         job["company"],
            "location":        loc,
            "description":     job["desc"],
            "required_skills": job["skills"],
            "salary_range":    job["salary"],
            "posted":          random.choice(POSTED),
            "match_score":     score,
            "linkedin_url":    li_url,
            "naukri_url":      nk_url,
            "indeed_url":      ind_url,
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results