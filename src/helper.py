import os
import requests
import pdfplumber
import re

HF_API_KEY = os.getenv("HF_API_KEY", "")
MODEL = "google/flan-t5-large"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"


def _flan(prompt: str, max_tokens: int = 400) -> str:
    """Core FLAN-T5 call via HuggingFace Router API."""
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt[:1400],
        "parameters": {
            "max_new_tokens": max_tokens,
            "do_sample": True,
            "temperature": 0.7
        }
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        if isinstance(result, dict) and "error" in result:
            return f"[Model warming up, retry in 20 sec: {result['error']}]"
        return str(result)
    except Exception as e:
        return f"[Error: {e}]"


def extract_text_from_pdf(uploaded_file) -> str:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        return f"[PDF Error: {e}]"


def analyze_resume(text: str) -> dict:
    snippet = text[:900]
    name       = _flan(f"What is the candidate's full name in this resume?\nResume: {snippet}\nName:")
    summary    = _flan(f"Write a 2 sentence professional summary for:\n{snippet}")
    skills_raw = _flan(f"List top 10 skills from this resume as comma separated values:\n{snippet}")
    exp_raw    = _flan(f"How many years of experience does this person have? Answer with a number only:\n{snippet}")

    skills = [s.strip() for s in skills_raw.split(",") if s.strip()][:12]
    try:
        match = re.search(r'\d+', exp_raw)
        years = int(match.group()) if match else 0
    except Exception:
        years = 0

    return {
        "name": name.strip() or "Your Profile",
        "summary": summary.strip(),
        "skills": skills,
        "years_experience": years,
    }


def generate_skill_gap(resume_text: str, target_role: str) -> str:
    return _flan(
        f"Analyze this resume for the role: {target_role}\n"
        f"Resume: {resume_text[:700]}\n\n"
        f"1. Matching skills:\n2. Missing skills:\n3. Top 3 action items:",
        max_tokens=400
    )


def generate_roadmap(resume_text: str, goal: str) -> str:
    return _flan(
        f"Create a 6 month career roadmap to achieve: {goal}\n"
        f"Profile: {resume_text[:500]}\n\n"
        f"Month 1-2:\nMonth 3-4:\nMonth 5-6:",
        max_tokens=400
    )