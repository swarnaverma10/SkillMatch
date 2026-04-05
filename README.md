# 🚀 SkillMatch AI — Career Intelligence Platform

<div align="center">

![SkillMatch AI](https://img.shields.io/badge/SkillMatch-AI-6c63ff?style=for-the-badge&logo=rocket&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-43e97b?style=for-the-badge)
![No API Key](https://img.shields.io/badge/No%20API%20Key-Required-ffb347?style=for-the-badge)

**A sleek, rule-based career intelligence platform that analyzes your resume, scores it against job descriptions, and matches you with real job opportunities — all without any paid API.**

[🌐 Live Demo](https://skillmatch-ai-628c.onrender.com) &nbsp;·&nbsp; [📸 Screenshots](#screenshots) &nbsp;·&nbsp; [🚀 Deploy](#deployment) &nbsp;·&nbsp; [📂 Project Structure](#project-structure)

</div>

---

## ✨ Features

### 📑 Resume Analyzer
- Extracts your **name, email, phone** directly from your PDF
- Detects **20+ skill categories** — Programming, Web, AI/ML, Cloud, Databases, Tools
- **Auto-Role Prediction**: Automatically predicts your target job role based on detected skills
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
- **Smart Apply Links**: Direct, pre-built links to **LinkedIn, Naukri, Indeed, and Glassdoor**
- **Match score** calculated based on your resume skills
- Shows **salary range, location, source** (LinkedIn/Naukri/Indeed/Glassdoor)

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
| **Font** | Sora (Google Fonts) |
| **Deployment** | Render (Web Service) |

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

### Option 1 — Deploy on Render (Recommended)

Render is extremely stable for Streamlit apps.

#### Step 1 — Push to GitHub
Ensure your code is on GitHub.

#### Step 2 — Create Web Service on Render
1. Go to **[dashboard.render.com](https://dashboard.render.com)**
2. Click **"New +"** → **"Web Service"**
3. Select this repository
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Click **"Create Web Service"**

### Option 2 — Deploy on Streamlit Community Cloud (Free)

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub and click **"New app"**
3. Repository: `YOUR_USERNAME/skillmatch-ai`, Main file: `app.py`
4. Click **"Deploy!"**

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