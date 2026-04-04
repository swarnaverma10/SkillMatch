import os
import random
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"

COMPANIES = [
    ("Google", "Bangalore"), ("Microsoft", "Hyderabad"), ("Amazon", "Bangalore"),
    ("Flipkart", "Bangalore"), ("Zomato", "Gurugram"), ("Razorpay", "Bangalore"),
    ("Infosys", "Pune"), ("Wipro", "Chennai"), ("Swiggy", "Bangalore"),
    ("PhonePe", "Bangalore"), ("Paytm", "Noida"), ("CRED", "Bangalore"),
    ("Meesho", "Bangalore"), ("Freshworks", "Chennai"), ("Zoho", "Chennai")
]


def _flan(prompt: str, max_tokens: int = 200) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt[:1000],
        "parameters": {"max_new_tokens": max_tokens, "do_sample": True, "temperature": 0.8}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return ""
    except Exception:
        return ""


def fetch_jobs(role: str, location: str, resume_text: str) -> list:
    if not role:
        role = "Software Engineer"

    skills_raw = _flan(f"List 5 skills needed for {role} as comma separated values:")
    common_skills = [s.strip() for s in skills_raw.split(",") if s.strip()][:5]
    if not common_skills:
        common_skills = ["Problem Solving", "Communication", "Python", "SQL", "Teamwork"]

    jobs = []
    selected = random.sample(COMPANIES, min(6, len(COMPANIES)))

    for company_name, company_city in selected:
        job_location = location if location else company_city
        desc = _flan(f"Write 2 sentences describing a {role} job at {company_name}:")
        if not desc:
            desc = f"Join {company_name} as a {role} and work on impactful projects with a talented team."

        job_skills = random.sample(common_skills, min(4, len(common_skills)))
        job_skills.append(random.choice(["Git", "Agile", "REST APIs", "Linux", "Docker"]))

        salary_min = 8 + random.randint(0, 20)
        salary_max = salary_min + random.randint(5, 15)

        jobs.append({
            "title": role,
            "company": company_name,
            "location": job_location,
            "description": desc,
            "required_skills": job_skills,
            "salary_range": f"{salary_min}-{salary_max} LPA",
            "source": random.choice(["LinkedIn", "Naukri"]),
            "posted": random.choice(["Today", "Yesterday", "2 days ago", "1 week ago"]),
            "match_score": random.randint(62, 94)
        })

    jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return jobs