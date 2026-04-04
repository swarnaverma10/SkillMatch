import os
import io
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


def generate_cover_letter(resume_text: str, company: str, role: str, tone: str, highlight: str) -> str:
    return _flan(
        f"Write a {tone.lower()} cover letter for {role} at {company}.\n"
        f"Key achievement: {highlight}\n"
        f"Resume: {resume_text[:600]}\n\nCover Letter:",
        max_tokens=500
    )


def generate_thankyou_email(interviewer: str, company: str, role: str, topic: str) -> str:
    return _flan(
        f"Write a professional thank you email after an interview.\n"
        f"Interviewer: {interviewer or 'the team'}\n"
        f"Company: {company or 'the company'}\n"
        f"Role: {role or 'the position'}\n"
        f"Topic discussed: {topic or 'the company vision'}\n\nSubject: [subject]\n\nEmail:",
        max_tokens=400
    )


def generate_resume_pdf(resume_text: str, name: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_CENTER

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        accent = colors.HexColor('#6c63ff')
        name_style = ParagraphStyle('Name', parent=styles['Normal'],
            fontSize=22, fontName='Helvetica-Bold', textColor=accent, alignment=TA_CENTER, spaceAfter=4)
        heading_style = ParagraphStyle('H', parent=styles['Normal'],
            fontSize=12, fontName='Helvetica-Bold', textColor=accent, spaceBefore=12, spaceAfter=4)
        body_style = ParagraphStyle('B', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=5)

        story = [Paragraph(name or "Resume", name_style),
                 HRFlowable(width="100%", thickness=2, color=accent), Spacer(1, 10)]

        for section in resume_text.split('\n\n'):
            if not section.strip():
                continue
            lines = section.strip().split('\n')
            if lines[0].isupper() or len(lines[0]) < 50:
                story.append(Paragraph(lines[0], heading_style))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#333355')))
                story.append(Spacer(1, 4))
                for line in lines[1:]:
                    if line.strip():
                        story.append(Paragraph(f"• {line.strip()}", body_style))
            else:
                for line in lines:
                    if line.strip():
                        story.append(Paragraph(line.strip(), body_style))
            story.append(Spacer(1, 6))

        doc.build(story)
        return buffer.getvalue()
    except ImportError:
        return resume_text.encode('utf-8')
    except Exception as e:
        return f"PDF error: {e}".encode('utf-8')