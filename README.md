# 🚀 SkillMatch AI: Premium Career Growth Platform

An intelligent, AI-driven ecosystem that transforms your resume into a strategic career roadmap. SkillMatch AI analyzes your professional profile to provide tailored job recommendations, LinkedIn optimization, and interview readiness.

---

## ✨ Features

- **📑 Intelligent Resume Analysis**: Deep extraction and summarization of your professional experience.
- **🛠️ Skill Gap & Roadmap**: AI-powered analysis of what's missing and a clear path to achieve your career goals.
- **💼 Smart Job Matcher**: Real-time (simulated) job recommendations from LinkedIn and Naukri tailored to your profile.
- **🚀 AI Career Coach**: 
  - **LinkedIn Profile Optimizer**: Strategic suggestions to boost your profile's visibility.
  - **Cover Letter Generator**: Instant, personalized cover letters for your target roles.
- **🎤 Interview Prep Kit**: Predict likely interview questions based on your resume and target jobs.
- **🎨 Modern Premium UI**: A sleek, dark-themed dashboard with glassmorphism and intuitive navigation.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit with Custom CSS (Premium Glassmorphism Theme)
- **AI Engine**: Hugging Face Transformers (FLAN-T5) for local inference
- **PDF Processing**: pdfplumber
- **Backend Logic**: Python
- **API Integration Ready**: Structure prepared for LinkedIn, Naukri, and OpenAI/HuggingFace APIs

---

## 📂 Project Structure

- `app.py`: Main Streamlit application with premium UI.
- `src/helper.py`: AI inference and PDF parsing utilities.
- `src/job_api.py`: Mock API for LinkedIn and Naukri job fetching.
- `.env`: API key configuration.

