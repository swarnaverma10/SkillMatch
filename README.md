# 🚀 SkillMatch AI — Career Intelligence Platform

<div align="center">

![SkillMatch AI](https://img.shields.io/badge/SkillMatch-AI-6c63ff?style=for-the-badge&logo=rocket&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-43e97b?style=for-the-badge)
![No API Key](https://img.shields.io/badge/No%20API%20Key-Required-ffb347?style=for-the-badge)

**A sleek, rule-based career intelligence platform that analyzes your resume, scores it against job descriptions, and matches you with real job opportunities — all without any paid API.**

[🌐 Live Demo](#) &nbsp;·&nbsp; [📸 Screenshots](#screenshots) &nbsp;·&nbsp; [🚀 Deploy](#deployment) &nbsp;·&nbsp; [📂 Project Structure](#project-structure)

</div>

---

## ✨ Features

### 📑 Resume Analyzer
- Extracts your **name, email, phone** directly from your PDF
- Detects **20+ skill categories** — Programming, Web, AI/ML, Cloud, Databases, Tools
- Shows **years of experience** and **education** automatically
- Categorized skill badges with color-coded sections
- Raw resume text viewer for verification

### 🎯 ATS Score Checker
- **Keyword matching** between your resume and any job description
- Returns a **0–100 ATS compatibility score**
- Shows **matched keywords** (green) and **missing keywords** (red)
- Provides **actionable tips** to improve your score
- Works instantly — no API, no delay

### 💼 Job Matcher
- **6 role categories** with real Indian company listings:
  - Data Scientist, ML Engineer, Full Stack Developer
  - Software Engineer, Python Developer, Frontend Developer, DevOps Engineer
- Jobs from **Google, Amazon, Microsoft, Flipkart, Zomato, Razorpay, Swiggy, PhonePe, CRED, Meesho, Freshworks, Zoho** and more
- **Match score** calculated based on your resume skills
- Shows **salary range, location, source** (LinkedIn/Naukri/Indeed)

---

## 🖼️ Screenshots

| Home Page | Resume Analyzer |
|-----------|----------------|
| Animated hero, upload zone, feature cards | Skill categories, profile card, metrics |

| ATS Score Checker | Job Matcher |
|-------------------|-------------|
| Score ring, matched/missing keywords, tips | Job cards with match %, salary, company |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Custom CSS (Dark Theme) |
| **AI Engine** | Rule-based NLP (No API needed) |
| **PDF Parsing** | pdfplumber |
| **Charts** | Plotly |
| **Font** | Sora (Google Fonts) |
| **Deployment** | Streamlit Community Cloud |

---

## 📂 Project Structure

```
SKILLMATCH-AI/
│
├── app.py                      # Main Streamlit application
│
├── src/
│   ├── __init__.py
│   ├── helper.py               # PDF extraction + resume analysis (rule-based)
│   ├── ats_scorer.py           # ATS keyword matching algorithm
│   └── job_api.py              # Job listings database + match scoring
│
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (empty — no API needed)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## ⚡ Local Setup

### Prerequisites
- Python 3.9 or higher
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/skillmatch-ai.git
cd skillmatch-ai
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

> ✅ **No API key needed!** The app runs fully offline using rule-based algorithms.

---

## 🚀 Deployment

### Deploy on Streamlit Community Cloud (Free)

**Streamlit Community Cloud** is the easiest and **completely free** way to deploy this app.

#### Step 1 — Push to GitHub
```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit — SkillMatch AI"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/skillmatch-ai.git
git branch -M main
git push -u origin main
```

#### Step 2 — Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in the details:
   - **Repository:** `YOUR_USERNAME/skillmatch-ai`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**

> 🎉 Your app will be live at `https://YOUR_USERNAME-skillmatch-ai-app-XXXX.streamlit.app`

#### Step 3 — (Optional) Add secrets
Since this app needs **no API keys**, you can skip this step entirely.

If you add API keys in the future:
- Go to your app → **Settings** → **Secrets**
- Add key-value pairs there (never put API keys in code!)

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pdfplumber>=0.10.3
python-dotenv>=1.0.1
plotly>=5.20.0
reportlab>=4.1.0
```

---

## 🔧 How It Works (No AI API)

### Resume Analysis — Rule-Based NLP
```
PDF Upload → pdfplumber extracts text → 
Regex finds name/email/phone → 
Pattern matching against 80+ skill keywords → 
Experience years extracted via regex patterns
```

### ATS Scoring — Keyword Matching
```
Resume text → Tokenize → Remove stopwords → Extract keywords
Job Description → Same process
Score = (matched keywords / total JD keywords) × 100
Missing = JD keywords not found in resume
```

### Job Matching — Database + Scoring
```
User enters role → Match to 7 role categories →
Return relevant company listings →
Calculate match score based on skill overlap with resume
```

---

## 🎨 Customization

### Add more jobs
Edit `src/job_api.py` — add entries to `JOB_DATA` dict:
```python
"your role": [
    {
        "title": "Job Title",
        "company": "Company Name",
        "location": "City",
        "desc": "Job description...",
        "skills": ["Skill1", "Skill2"],
        "salary": "X-Y LPA"
    },
]
```

### Add more skills to detect
Edit `src/helper.py` — add to `SKILLS_DB` list:
```python
SKILLS_DB = [
    "YourNewSkill",
    # ... existing skills
]
```

### Change theme colors
Edit the CSS in `app.py`:
```css
/* Primary accent */
background: linear-gradient(135deg, #6c63ff, #8b5cf6)

/* Change to your color */
background: linear-gradient(135deg, #your-color, #your-color-2)
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit: `git commit -m "Add amazing feature"`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👨‍💻 Author

Built with ❤️ using Streamlit and Python.

If this project helped you, consider giving it a ⭐ on GitHub!

---

<div align="center">
<b>SkillMatch AI</b> — Land your dream job with smarter career tools 🚀
</div>