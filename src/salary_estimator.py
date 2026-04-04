import os
import re
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


def _flan(prompt: str, max_tokens: int = 350) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt[:1400],
        "parameters": {"max_new_tokens": max_tokens, "do_sample": True, "temperature": 0.5}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)
    except Exception as e:
        return f"[Error: {e}]"


def estimate_salary(resume_text: str, role: str, location: str, experience: int) -> dict:
    salary_raw = _flan(
        f"What is the salary range in LPA for a {role} with {experience} years of experience in {location}, India? "
        f"Give minimum, median, and maximum as three numbers separated by commas.\nAnswer:"
    )

    nums = re.findall(r'\d+\.?\d*', salary_raw)
    if len(nums) >= 3:
        mn, med, mx = nums[0], nums[1], nums[2]
    elif len(nums) == 2:
        mn, med, mx = nums[0], nums[1], str(int(float(nums[1])) + 5)
    elif len(nums) == 1:
        base = int(float(nums[0]))
        mn, med, mx = str(base - 3), str(base), str(base + 5)
    else:
        base = 4 + (experience * 2)
        mn, med, mx = str(base), str(base + 4), str(base + 10)

    insights = _flan(
        f"Explain salary factors for a {role} with {experience} years experience in {location}. "
        f"Include market demand, skills that increase salary, and negotiation tips.\nInsights:"
    )

    return {
        "min": f"{mn} LPA",
        "median": f"{med} LPA",
        "max": f"{mx} LPA",
        "insights": insights
    }