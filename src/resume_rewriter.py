import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


def _flan(prompt: str, max_tokens: int = 450) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt[:1400],
        "parameters": {"max_new_tokens": max_tokens, "do_sample": True, "temperature": 0.8}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)
    except Exception as e:
        return f"[Error: {e}]"


def rewrite_resume(resume_text: str, target_role: str = "", focus: str = "Impact & Metrics") -> str:
    focus_guide = {
        "Impact & Metrics": "Add numbers and measurable results to every bullet point. Use strong action verbs.",
        "Leadership & Ownership": "Emphasize team leadership, ownership, and decision making.",
        "Technical Depth": "Highlight technical skills, system design, and engineering complexity.",
        "ATS Keyword Optimization": "Add industry standard keywords and skill terms for ATS systems.",
        "Executive Level": "Use business impact language, focus on strategy and revenue."
    }
    instruction = focus_guide.get(focus, "Make it more impactful.")
    role_text = f"for a {target_role} role" if target_role else ""

    return _flan(
        f"Rewrite this resume {role_text} to be more impactful. {instruction}\n\n"
        f"Original resume:\n{resume_text[:900]}\n\nImproved version:",
        max_tokens=500
    )