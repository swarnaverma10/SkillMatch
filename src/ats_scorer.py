import os
import re
import requests

HF_API_KEY = os.getenv("HF_API_KEY", "")
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"


def _flan(prompt: str, max_tokens: int = 350) -> str:
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt[:1400],
        "parameters": {"max_new_tokens": max_tokens, "do_sample": False}
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=40)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)
    except Exception as e:
        return f"[Error: {e}]"


def score_ats(resume_text: str, job_description: str) -> dict:
    resume_snip = resume_text[:600]
    jd_snip = job_description[:600]

    score_raw = _flan(
        f"Rate how well this resume matches this job description on a scale of 0 to 100. "
        f"Answer with only a number.\nJob: {jd_snip}\nResume: {resume_snip}\nScore:"
    )
    try:
        match = re.search(r'\d+', score_raw)
        score = int(match.group()) if match else 60
        score = min(100, max(0, score))
    except Exception:
        score = 60

    matched_raw = _flan(
        f"List keywords present in BOTH the job description and resume, comma separated.\n"
        f"Job: {jd_snip}\nResume: {resume_snip}\nMatched keywords:"
    )
    missing_raw = _flan(
        f"List important keywords from the job description NOT found in the resume, comma separated.\n"
        f"Job: {jd_snip}\nResume: {resume_snip}\nMissing keywords:"
    )
    recs = _flan(
        f"Give 5 specific tips to improve this resume for this job.\n"
        f"Job: {jd_snip}\nResume: {resume_snip}\nTips:"
    )

    matched = [k.strip() for k in matched_raw.split(",") if k.strip()][:8]
    missing = [k.strip() for k in missing_raw.split(",") if k.strip()][:8]

    breakdown = (
        f"Keyword Match: {len(matched)} keywords found\n"
        f"Missing Keywords: {len(missing)} important terms absent\n"
        f"Matched: {', '.join(matched) if matched else 'None found'}\n"
        f"Missing: {', '.join(missing) if missing else 'None found'}"
    )

    return {
        "score": score,
        "breakdown": breakdown,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "recommendations": recs
    }