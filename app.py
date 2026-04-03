import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="SkillMatch AI | Your Career Growth Partner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .card {
        background: rgba(30, 41, 59, 0.7);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        border-color: rgba(96, 165, 250, 0.5);
    }
    
    .job-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 8px;
    }
    
    .company-name {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 12px;
    }
    
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(96, 165, 250, 0.2);
        color: #60a5fa;
        margin-right: 8px;
    }
    
    .highlight-box {
        padding: 20px;
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #60a5fa;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        font-weight: 600;
        padding: 10px 24px;
        border-radius: 8px;
        width: 100%;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        gap: 4px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        color: #60a5fa !important;
        border-bottom-color: #60a5fa !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Content ---
st.markdown('<h1 class="main-header">SkillMatch AI</h1>', unsafe_allow_html=True)
st.markdown("### Elevate your career with AI-driven insights and opportunities.")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/rocket.png", width=150)
    st.title("Settings & Prefs")
    
    st.markdown("---")
    job_location = st.selectbox("Target Location", ["Global", "India", "Remote", "USA", "Europe"])
    job_type = st.multiselect("Job Type", ["Full-time", "Internship", "Contract"], default=["Full-time"])
    num_results = st.slider("Results to fetch", 5, 50, 15)
    
    st.markdown("---")
    st.info("Upload your resume to unlock all features.")

# --- File Upload ---
uploaded_file = st.file_uploader("Drop your resume here (PDF format)", type=["pdf"])

if uploaded_file:
    # Use session state to store analysis results and avoid re-runs
    if 'analysis_done' not in st.session_state:
        with st.spinner("🚀 Analyzing your professional profile..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Heavy lifting with local T5
            st.session_state.resume_text = resume_text
            st.session_state.summary = ask_openai(f"Summarize this resume highlighting the skills, education, and experience:\n\n{resume_text}")
            st.session_state.gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed: \n\n{resume_text}")
            st.session_state.roadmap = ask_openai(f"Suggest a future roadmap to improve this person's career prospects (Skills, certifications): \n\n{resume_text}")
            
            # Extract keywords for jobs
            st.session_state.keywords = ask_openai(f"Suggest 5 best job titles or keywords based on this: {st.session_state.summary}. Output as comma separated list only.")
            
            st.session_state.analysis_done = True
            st.success("✅ Analysis Ready!")

    # --- Main Dashboard Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Insights", "💼 Job Matcher", "🚀 Career Coach", "🎤 Prep Kit"])

    with tab1:
        st.header("Resume Intelligence")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.subheader("📑 Professional Summary")
            st.write(st.session_state.summary)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.subheader("🛠️ Skill Analysis")
            st.write(st.session_state.gaps)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📈 Career Roadmap")
            st.write(st.session_state.roadmap)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.header("Top Career Matches")
        search_keywords = st.session_state.keywords.replace("\n", "").strip()
        
        if st.button("🔄 Refresh Recommendations"):
            with st.spinner("Scanning LinkedIn & Naukri..."):
                st.session_state.links = fetch_linkedin_jobs(search_keywords, rows=num_results)
                st.session_state.naukri = fetch_naukri_jobs(search_keywords, rows=num_results)
        
        if 'links' in st.session_state:
            st.subheader(f"Recommendations for: `{search_keywords}`")
            
            # Display LinkedIn Jobs
            st.markdown("#### 🔹 LinkedIn Opportunities")
            l_cols = st.columns(3)
            for i, job in enumerate(st.session_state.links):
                with l_cols[i % 3]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="job-title">{job.get('title')}</div>
                            <div class="company-name">{job.get('companyName')}</div>
                            <div class="tag">📍 {job.get('location')}</div>
                            <div style='margin-top:15px'>
                                <a href="{job.get('link')}" target="_blank" style="text-decoration:none; color:#60a5fa; font-weight:bold;">View Listing →</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Display Naukri Jobs
            st.markdown("#### 🔹 Naukri Jobs (India)")
            n_cols = st.columns(3)
            for i, job in enumerate(st.session_state.naukri):
                with n_cols[i % 3]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="job-title">{job.get('title')}</div>
                            <div class="company-name">{job.get('companyName')}</div>
                            <div class="tag">📍 {job.get('location')}</div>
                            <div style='margin-top:15px'>
                                <a href="{job.get('url')}" target="_blank" style="text-decoration:none; color:#a78bfa; font-weight:bold;">Apply Now →</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    with tab3:
        st.header("AI Career Coach")
        coach_opt = st.radio("Choose a tool", ["LinkedIn Optimizer", "Tailored Cover Letter"], horizontal=True)
        
        if coach_opt == "LinkedIn Optimizer":
            if st.button("Generate Optimization Suggestions"):
                with st.spinner("Analyzing LinkedIn standards..."):
                    opt_tips = ask_openai(f"Suggest 3 improvements for a LinkedIn profile based on this resume: {st.session_state.resume_text}")
                    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                    st.subheader("💡 Strategic LinkedIn Improvements")
                    st.write(opt_tips)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("Generate Cover Letter"):
                with st.spinner("Drafting your personalized letter..."):
                    letter = ask_openai(f"Write a short, professional cover letter for a {search_keywords} role based on this resume: {st.session_state.resume_text}")
                    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                    st.subheader("📄 Your Draft Cover Letter")
                    st.text_area("", value=letter, height=300)
                    st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.header("Interview Readiness")
        st.write("Prepare for your next big interview with AI-generated questions.")
        
        if st.button("Generate Mock Questions"):
            with st.spinner("Predicting interviewer logic..."):
                questions = ask_openai(f"Generate 5 likely interview questions for a {search_keywords} role based on this resume: {st.session_state.resume_text}")
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.subheader("❓ Likely Interview Questions")
                st.write(questions)
                st.markdown('</div>', unsafe_allow_html=True)
                st.info("💡 Tip: Use the STAR (Situation, Task, Action, Result) method to answer these!")

else:
    # Catchy landing state
    st.markdown("---")
    st.warning("👈 Please upload your resume to get started.")
    
    # Feature highlights
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.markdown('<div class="card"><h3>🔍 Smart Matching</h3><p>Find the best jobs on LinkedIn & Naukri tailored to your skills.</p></div>', unsafe_allow_html=True)
    with fcol2:
        st.markdown('<div class="card"><h3>✨ AI Enhancements</h3><p>Optimize your LinkedIn profile and generate cover letters instantly.</p></div>', unsafe_allow_html=True)
    with fcol3:
        st.markdown('<div class="card"><h3>🏆 Interview Prep</h3><p>Practice with questions generated specifically from your experience.</p></div>', unsafe_allow_html=True)


