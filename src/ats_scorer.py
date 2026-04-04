import re

STOP_WORDS = {"the","and","or","in","of","to","a","an","is","are","we","for","you","with",
              "as","at","by","our","your","will","be","have","has","this","that","from",
              "on","it","its","their","they","all","also","but","not","can","more","about",
              "who","what","when","how","which","than","do","if","any","both","each","few"}


def _extract_keywords(text: str) -> set:
    """Extract meaningful keywords from text."""
    text = text.lower()
    # Remove special chars
    text = re.sub(r'[^\w\s\+#]', ' ', text)
    words = text.split()
    # Filter stop words and short words
    keywords = set()
    for w in words:
        w = w.strip()
        if len(w) > 2 and w not in STOP_WORDS and not w.isdigit():
            keywords.add(w)

    # Also extract bigrams (2-word phrases) for tech terms
    tokens = text.split()
    for i in range(len(tokens) - 1):
        bigram = tokens[i] + " " + tokens[i+1]
        if tokens[i] not in STOP_WORDS and tokens[i+1] not in STOP_WORDS:
            keywords.add(bigram)

    return keywords


def score_ats(resume_text: str, job_description: str) -> dict:
    """Rule-based ATS scoring — no API needed."""
    resume_kw = _extract_keywords(resume_text)
    jd_kw     = _extract_keywords(job_description)

    # Matched = keywords in JD that also appear in resume
    matched = sorted([k for k in jd_kw if k in resume_kw and len(k) > 3])[:20]
    missing = sorted([k for k in jd_kw if k not in resume_kw and len(k) > 3])[:20]

    # Score = % of JD keywords found in resume
    if len(jd_kw) == 0:
        score = 0
    else:
        score = min(100, int((len(matched) / max(len(jd_kw), 1)) * 100 * 2.5))
        score = min(score, 95)  # cap at 95

    # Generate tips
    tips = []
    if score < 50:
        tips.append("Your resume has low keyword overlap with this JD. Try adding more role-specific terms.")
    if missing[:5]:
        tips.append(f"Add these missing keywords: {', '.join(missing[:5])}")
    if score >= 70:
        tips.append("Good match! Make sure your experience bullets use action verbs with metrics.")
    tips.append("Avoid using tables or graphics in your resume — ATS systems may not read them.")
    tips.append("Use the exact job title from the JD somewhere in your resume.")

    return {
        "score":   score,
        "matched": matched[:15],
        "missing": missing[:15],
        "tips":    tips,
    }