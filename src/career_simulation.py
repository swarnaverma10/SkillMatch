import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


def _flan(prompt: str, max_tokens: int = 350) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt[:1400],
        "parameters": {"max_new_tokens": max_tokens, "do_sample": True, "temperature": 0.7}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)
    except Exception as e:
        return f"[Error: {e}]"


def simulate_career_path(resume_text: str, path_a: str, path_b: str) -> dict:
    snippet = resume_text[:500] if resume_text else ""

    def simulate_one(path: str) -> dict:
        salary = _flan(f"What salary in LPA will someone earn in 5 years if they: {path}? Answer with a range like '20-30 LPA':")
        role   = _flan(f"What job title will someone have in 5 years if they: {path}? Answer with just the job title:")
        skills = _flan(f"List 5 skills someone will gain in 5 years if they: {path}. Answer as comma separated values:")
        story  = _flan(f"Describe in 3 sentences the 5 year journey for someone who: {path}\nProfile: {snippet}\nJourney:")
        skill_list = [s.strip() for s in skills.split(",") if s.strip()][:5]
        return {
            "salary": salary.strip() or "15-25 LPA",
            "role":   role.strip() or "Senior Professional",
            "skills_gained": skill_list or ["Leadership", "Domain Expertise", "Communication"],
            "narrative": story.strip()
        }

    verdict = _flan(
        f"Compare two career paths:\nPath A: {path_a}\nPath B: {path_b}\n"
        f"Profile: {snippet}\nWhich path is better and why? 2 sentence answer:"
    )

    return {
        "path_a": simulate_one(path_a),
        "path_b": simulate_one(path_b),
        "verdict": verdict.strip()
    }