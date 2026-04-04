import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


def _flan(prompt: str, max_tokens: int = 400) -> str:
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


def generate_interview_questions(resume_text: str, role: str, types: list) -> list:
    types_str = ", ".join(types) if types else "Technical, Behavioral"
    snippet = resume_text[:600] if resume_text else ""

    raw = _flan(
        f"Generate 6 interview questions for a {role} candidate. "
        f"Types: {types_str}. Resume: {snippet}\n"
        f"Write each question numbered 1-6:",
        max_tokens=400
    )

    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    questions = []
    q_types = (types * 3) if types else ["Technical", "Behavioral"] * 3

    for i, line in enumerate(lines[:6]):
        clean = line.lstrip("0123456789.-) ").strip()
        if clean:
            questions.append({
                "question": clean,
                "type": q_types[i % len(q_types)],
                "tip": "Use the STAR method and be specific with examples."
            })

    if not questions:
        questions = [
            {"question": f"Tell me about your experience with {role}.", "type": "Behavioral", "tip": "Use STAR method."},
            {"question": "Describe a challenging project you worked on.", "type": "Situational", "tip": "Focus on actions and results."},
            {"question": "What are your greatest technical strengths?", "type": "Technical", "tip": "Give concrete examples."},
        ]
    return questions


def generate_star_answer(situation: str, target_question: str) -> dict:
    return {
        "situation": _flan(f"Rewrite as a compelling interview situation in 2 sentences:\n{situation}\nSituation:"),
        "task":      _flan(f"What was the specific task or responsibility in this situation?\n{situation}\nTask:"),
        "action":    _flan(f"What specific actions did this person take?\n{situation}\nActions:"),
        "result":    _flan(f"What positive results came from handling this?\n{situation}\nResults:")
    }


def generate_company_briefing(company: str, role: str) -> str:
    return _flan(
        f"Create an interview prep guide for {company} for the role {role}.\n"
        f"1. About the company\n2. What they look for\n3. Questions to ask\n4. Key tips\nGuide:",
        max_tokens=450
    )