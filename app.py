import streamlit as st
import os
from dotenv import load_dotenv
from src.helper import extract_text_from_pdf, analyze_resume, generate_skill_gap, generate_roadmap
from src.job_api import fetch_jobs
from src.ats_scorer import score_ats
from src.salary_estimator import estimate_salary
from src.resume_rewriter import rewrite_resume
from src.interview_prep import generate_interview_questions, generate_star_answer, generate_company_briefing
from src.doc_generator import generate_cover_letter, generate_resume_pdf, generate_thankyou_email
from src.career_simulation import simulate_career_path
from src.application_tracker import render_tracker
from src.skill_dashboard import render_skill_dashboard

load_dotenv()

st.set_page_config(page_title="SkillMatch AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background: #0d0d14 !important; }

/* ── Force sidebar always visible ── */
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
    transform: none !important;
    visibility: visible !important;
    min-width: 270px !important;
    max-width: 270px !important;
    background: #08080f !important;
    border-right: 1px solid #16162a !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* ── All sidebar text color ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div { color: #b0b0c8; }

/* ── Sidebar nav buttons — reset all gradient from main ── */
section[data-testid="stSidebar"] .stButton { margin: 1px 8px !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    color: #6a6a8a !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    text-align: left !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
    transition: all 0.15s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(108,99,255,0.10) !important;
    color: #d0d0f0 !important;
    border-color: rgba(108,99,255,0.20) !important;
    transform: none !important;
    opacity: 1 !important;
}
/* Active page — type="primary" */
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
    background: rgba(108,99,255,0.15) !important;
    border-left: 3px solid #6c63ff !important;
    border-color: rgba(108,99,255,0.35) !important;
    color: #c0b8ff !important;
    font-weight: 600 !important;
    border-radius: 0 10px 10px 0 !important;
    padding-left: 11px !important;
}

/* ── Sidebar file uploader ── */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(108,99,255,0.05) !important;
    border: 1px dashed rgba(108,99,255,0.22) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    font-size: 0.78rem !important;
    color: #7878a0 !important;
}

/* ════════════════════════════
   MAIN CONTENT
════════════════════════════ */
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px; }

.sm-card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 22px;
    margin: 8px 0;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.sm-card:hover { border-color: #6c63ff; box-shadow: 0 0 24px rgba(108,99,255,0.12); }

.sm-metric {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}
.sm-metric-val { font-size: 2rem; font-weight: 700; color: #6c63ff; line-height: 1.1; }
.sm-metric-label { font-size: 0.7rem; color: #666688; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.sm-badge {
    display: inline-block;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.75rem;
    color: #a89fff;
    margin: 2px;
}

.sm-page-title { font-size: 1.6rem; font-weight: 700; color: #f0f0f8; margin-bottom: 4px; }
.sm-page-sub { font-size: 0.85rem; color: #666688; margin-bottom: 22px; }

.sm-output {
    background: #0a0a10;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 18px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem;
    color: #c0c0d8;
    white-space: pre-wrap;
    max-height: 380px;
    overflow-y: auto;
    line-height: 1.6;
}

.sm-star {
    background: #13131f;
    border-left: 3px solid #6c63ff;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
}

.sm-job {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 18px 20px;
    margin: 10px 0;
    transition: border-color 0.2s;
}
.sm-job:hover { border-color: #6c63ff; }

/* Main content buttons only */
.block-container .stButton > button {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    padding: 9px 22px !important;
    transition: opacity 0.2s, transform 0.2s !important;
    font-size: 0.88rem !important;
}
.block-container .stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #13131f !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 9px !important;
    color: #e0e0f0 !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.15) !important;
}

.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1e1e30 !important; }
.stTabs [data-baseweb="tab"] { color: #666688 !important; font-size: 0.88rem !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { color: #6c63ff !important; border-bottom-color: #6c63ff !important; }

hr { border-color: #1e1e30 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0d0d14; }
::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 3px; }
.stSuccess { background: rgba(67,233,123,0.08) !important; border-color: rgba(67,233,123,0.2) !important; }
#MainMenu, footer, header { visibility: hidden !important; }
.grad { background: linear-gradient(135deg,#6c63ff,#ff6584,#43e97b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("resume_text",""),("resume_data",{}),("jobs",[]),("applications",[]),("active_page","Dashboard")]:
    if k not in st.session_state:
        st.session_state[k] = v

NAV = [
    ("🏠", "Dashboard"),
    ("📑", "Resume Analyzer"),
    ("🎯", "ATS Score Checker"),
    ("💰", "Salary Estimator"),
    ("✍️", "Resume Rewriter"),
    ("💼", "Job Matcher"),
    ("🎤", "Interview Prep"),
    ("📄", "Document Generator"),
    ("🔮", "5-Year Career Sim"),
    ("📊", "Application Tracker"),
    ("📈", "Skill Dashboard"),
]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand header
    st.markdown("""
    <div style="padding:20px 16px 16px;border-bottom:1px solid #13132a;margin-bottom:10px;display:flex;align-items:center;gap:12px;">
        <div style="width:38px;height:38px;background:linear-gradient(135deg,#6c63ff,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex-shrink:0;">🚀</div>
        <div>
            <div style="font-size:1rem;font-weight:700;color:#f0f0f8;line-height:1.2;">SkillMatch AI</div>
            <div style="font-size:0.68rem;color:#6c63ff;letter-spacing:.4px;">Premium Career Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resume upload
    st.markdown("<div style='font-size:0.67rem;color:#383858;text-transform:uppercase;letter-spacing:1.4px;font-weight:600;padding:0 10px;margin-bottom:6px;'>Resume</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded:
        with st.spinner("Reading resume..."):
            text = extract_text_from_pdf(uploaded)
            st.session_state.resume_text = text
            st.session_state.resume_data = analyze_resume(text)

    # Resume status
    if st.session_state.resume_text:
        w = len(st.session_state.resume_text.split())
        sc = len(st.session_state.resume_data.get('skills', []))
        st.markdown(f"""
        <div style="margin:8px 8px 14px;padding:10px 12px;background:rgba(67,233,123,0.07);border:1px solid rgba(67,233,123,0.18);border-radius:10px;display:flex;align-items:center;gap:10px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#43e97b;box-shadow:0 0 6px #43e97b;flex-shrink:0;"></div>
            <div>
                <div style="font-size:0.76rem;font-weight:600;color:#43e97b !important;">Resume Active</div>
                <div style="font-size:0.69rem;color:#4a7a5a !important;">{w} words · {sc} skills</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin:8px 8px 14px;padding:9px 12px;background:rgba(255,101,132,0.06);border:1px dashed rgba(255,101,132,0.22);border-radius:10px;">
            <div style="font-size:0.75rem;color:#ff6584 !important;">⬆ Upload a PDF to begin</div>
        </div>""", unsafe_allow_html=True)

    # Nav label
    st.markdown("<div style='font-size:0.67rem;color:#383858;text-transform:uppercase;letter-spacing:1.4px;font-weight:600;padding:0 10px;margin-bottom:4px;'>Navigation</div>", unsafe_allow_html=True)

    # Nav buttons
    for icon, label in NAV:
        is_active = st.session_state.active_page == label
        clicked = st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )
        if clicked:
            st.session_state.active_page = label
            st.rerun()

    # Pills + footer
    apps_count = len(st.session_state.applications)
    st.markdown(f"""
    <div style="margin:14px 8px 0;display:flex;gap:5px;flex-wrap:wrap;">
        <span style="background:rgba(108,99,255,0.10);border:1px solid rgba(108,99,255,0.20);border-radius:20px;padding:3px 10px;font-size:0.69rem;color:#8880c8;">11 features</span>
        <span style="background:rgba(108,99,255,0.10);border:1px solid rgba(108,99,255,0.20);border-radius:20px;padding:3px 10px;font-size:0.69rem;color:#8880c8;">{apps_count} tracked</span>
        <span style="background:rgba(108,99,255,0.10);border:1px solid rgba(108,99,255,0.20);border-radius:20px;padding:3px 10px;font-size:0.69rem;color:#8880c8;">FLAN-T5</span>
    </div>
    <div style="padding:14px 16px;border-top:1px solid #13132a;margin-top:14px;text-align:center;">
        <div style="font-size:0.67rem;color:#2e2e50;line-height:1.7;">
            Powered by FLAN-T5 · v1.0<br>
            <span style="color:#6c63ff;">SkillMatch AI</span> · Premium
        </div>
    </div>""", unsafe_allow_html=True)

# ── Page routing ───────────────────────────────────────────────────────────────
page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.markdown("""
    <div style="padding:10px 0 30px 0;">
        <div style="font-size:2.8rem;font-weight:800;line-height:1.15;color:#f0f0f8;">
            Your Career,<br><span class="grad">Supercharged by AI.</span>
        </div>
        <div style="font-size:1rem;color:#666688;margin-top:12px;">
            Upload your resume and unlock your complete career intelligence suite.
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, val, lbl, clr in [
        (c1,"11","AI Features","#6c63ff"),
        (c2,str(len(st.session_state.applications)),"Jobs Tracked","#43e97b"),
        (c3,"✅" if st.session_state.resume_text else "○","Resume","#ff6584"),
        (c4,"FLAN-T5","AI Engine","#ffb347"),
    ]:
        with col:
            st.markdown(f"""<div class="sm-metric">
                <div class="sm-metric-val" style="color:{clr};font-size:1.6rem;">{val}</div>
                <div class="sm-metric-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    features = [
        ("📑","Resume Analyzer","AI extracts skills, experience & achievements"),
        ("🎯","ATS Score Checker","See how your resume ranks against job descriptions"),
        ("💰","Salary Estimator","Predict your market salary by role & location"),
        ("✍️","Resume Rewriter","AI rewrites bullets for maximum impact"),
        ("🎤","Interview Prep","Mock questions, STAR answers & company briefings"),
        ("📄","Document Generator","Cover letters, thank-you emails & PDF resume"),
        ("🔮","5-Year Career Sim","Simulate two career paths side by side"),
        ("📊","Application Tracker","Kanban board for all your job applications"),
        ("📈","Skill Dashboard","Visual breakdown of your skill landscape"),
    ]
    cols = st.columns(3)
    for i,(icon,title,desc) in enumerate(features):
        with cols[i%3]:
            st.markdown(f"""<div class="sm-card">
                <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
                <div style="font-weight:600;font-size:0.95rem;color:#e0e0f0;margin-bottom:5px;">{title}</div>
                <div style="font-size:0.8rem;color:#555570;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👈 Upload your resume from the sidebar to get started!")

# ══════════════════════════════════════════════════════════════════════════════
# RESUME ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resume Analyzer":
    st.markdown('<div class="sm-page-title">📑 Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Deep AI extraction of your professional profile</div>', unsafe_allow_html=True)
    if not st.session_state.resume_text:
        st.warning("⬅️ Please upload your resume from the sidebar first.")
    else:
        data = st.session_state.resume_data
        tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔍 Skill Gap", "🗺️ Roadmap"])
        with tab1:
            c1,c2 = st.columns([3,1])
            with c1:
                st.markdown(f"""<div class="sm-card">
                    <div style="font-size:1.1rem;font-weight:700;color:#e0e0f0;margin-bottom:8px;">👤 {data.get('name','Your Profile')}</div>
                    <div style="font-size:0.88rem;color:#999ab8;line-height:1.6;">{data.get('summary','AI analysis complete.')}</div>
                    <div style="margin-top:14px;">{"".join([f'<span class="sm-badge">{s}</span>' for s in data.get('skills',[])])}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="sm-metric" style="margin-bottom:10px;">
                    <div class="sm-metric-val">{data.get('years_experience','?')}</div>
                    <div class="sm-metric-label">Years Exp.</div>
                </div>
                <div class="sm-metric">
                    <div class="sm-metric-val" style="color:#43e97b;">{len(data.get('skills',[]))}</div>
                    <div class="sm-metric-label">Skills Found</div>
                </div>""", unsafe_allow_html=True)
        with tab2:
            role = st.text_input("🎯 Target Role", placeholder="e.g. Senior Data Scientist")
            if st.button("Analyze Gap", use_container_width=True) and role:
                with st.spinner("Analyzing skill gaps..."):
                    gap = generate_skill_gap(st.session_state.resume_text, role)
                st.markdown(f'<div class="sm-output">{gap}</div>', unsafe_allow_html=True)
        with tab3:
            goal = st.text_input("🏆 Career Goal", placeholder="e.g. Become ML Engineer at FAANG")
            if st.button("Build Roadmap", use_container_width=True) and goal:
                with st.spinner("Building roadmap..."):
                    roadmap = generate_roadmap(st.session_state.resume_text, goal)
                st.markdown(f'<div class="sm-output">{roadmap}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ATS SCORE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ATS Score Checker":
    st.markdown('<div class="sm-page-title">🎯 ATS Score Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">See exactly how your resume performs against ATS systems</div>', unsafe_allow_html=True)
    if not st.session_state.resume_text:
        st.warning("⬅️ Please upload your resume from the sidebar first.")
    else:
        jd = st.text_area("📋 Paste Job Description", height=200, placeholder="Paste the full job description here...")
        if st.button("🔍 Analyze ATS Score", use_container_width=True) and jd:
            with st.spinner("Running ATS analysis..."):
                result = score_ats(st.session_state.resume_text, jd)
            score = result.get("score", 0)
            clr = "#43e97b" if score>=70 else "#ffb347" if score>=50 else "#ff6584"
            lbl = "Excellent ✅" if score>=70 else "Needs Work ⚠️" if score>=50 else "Critical ❌"
            c1,c2 = st.columns([1,2])
            with c1:
                st.markdown(f"""<div class="sm-card" style="text-align:center;padding:30px 20px;">
                    <div style="font-size:0.72rem;color:#444460;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">ATS Score</div>
                    <div style="font-size:4rem;font-weight:800;color:{clr};line-height:1;">{score}%</div>
                    <div style="font-size:0.85rem;color:{clr};margin-top:8px;">{lbl}</div>
                    <div style="margin-top:16px;height:6px;background:#1e1e30;border-radius:3px;">
                        <div style="width:{score}%;height:100%;background:{clr};border-radius:3px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="sm-card" style="height:100%;">
                    <div style="font-weight:600;color:#e0e0f0;margin-bottom:12px;">📊 Breakdown</div>
                    <div style="font-size:0.85rem;color:#999ab8;white-space:pre-wrap;line-height:1.7;">{result.get('breakdown','')}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="sm-card" style="margin-top:4px;">
                <div style="font-weight:600;color:#e0e0f0;margin-bottom:10px;">💡 Recommendations</div>
                <div style="font-size:0.85rem;color:#999ab8;white-space:pre-wrap;line-height:1.7;">{result.get('recommendations','')}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SALARY ESTIMATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Salary Estimator":
    st.markdown('<div class="sm-page-title">💰 Salary Estimator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Predict your market salary based on role, location & experience</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: role = st.text_input("💼 Target Role", placeholder="e.g. Data Scientist")
    with c2: location = st.text_input("📍 Location", placeholder="e.g. Bangalore")
    with c3: exp = st.number_input("📅 Years of Experience", 0, 40, 3)
    if st.button("💰 Estimate My Salary", use_container_width=True) and role:
        with st.spinner("Calculating..."):
            result = estimate_salary(st.session_state.resume_text, role, location, exp)
        c1,c2,c3 = st.columns(3)
        for col, lbl, key, clr in [(c1,"Minimum","min","#ff6584"),(c2,"Expected","median","#43e97b"),(c3,"Maximum","max","#6c63ff")]:
            with col:
                st.markdown(f"""<div class="sm-metric">
                    <div class="sm-metric-val" style="color:{clr};font-size:1.8rem;">{result.get(key,'?')}</div>
                    <div class="sm-metric-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="sm-card" style="margin-top:16px;">
            <div style="font-weight:600;color:#e0e0f0;margin-bottom:10px;">📊 Market Insights</div>
            <div style="font-size:0.85rem;color:#999ab8;white-space:pre-wrap;line-height:1.7;">{result.get('insights','')}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESUME REWRITER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resume Rewriter":
    st.markdown('<div class="sm-page-title">✍️ Resume Rewriter</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">AI rewrites your resume bullets for maximum impact</div>', unsafe_allow_html=True)
    if not st.session_state.resume_text:
        st.warning("⬅️ Please upload your resume from the sidebar first.")
    else:
        c1,c2 = st.columns(2)
        with c1: target = st.text_input("🎯 Target Role (optional)", placeholder="e.g. Product Manager")
        with c2: focus = st.selectbox("🔧 Rewrite Focus", ["Impact & Metrics","Leadership & Ownership","Technical Depth","ATS Keyword Optimization","Executive Level"])
        if st.button("✨ Rewrite My Resume", use_container_width=True):
            with st.spinner("Rewriting for maximum impact..."):
                rewritten = rewrite_resume(st.session_state.resume_text, target, focus)
            c1,c2 = st.columns(2)
            with c1:
                st.markdown('<div style="font-weight:600;color:#666688;margin-bottom:8px;">📄 Original</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sm-output">{st.session_state.resume_text[:2000]}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div style="font-weight:600;color:#6c63ff;margin-bottom:8px;">✨ AI Rewritten</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sm-output">{rewritten}</div>', unsafe_allow_html=True)
            st.download_button("⬇️ Download Rewritten Resume", rewritten, file_name="rewritten_resume.txt", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# JOB MATCHER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Job Matcher":
    st.markdown('<div class="sm-page-title">💼 Smart Job Matcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">AI-matched job listings tailored to your profile</div>', unsafe_allow_html=True)
    if not st.session_state.resume_text:
        st.warning("⬅️ Please upload your resume from the sidebar first.")
    else:
        c1,c2 = st.columns(2)
        with c1: role_q = st.text_input("🔍 Role", placeholder="e.g. Machine Learning Engineer")
        with c2: loc_q  = st.text_input("📍 Location", placeholder="e.g. Bangalore / Remote")
        if st.button("🔍 Find Jobs", use_container_width=True):
            with st.spinner("Searching..."):
                st.session_state.jobs = fetch_jobs(role_q, loc_q, st.session_state.resume_text)
        for job in st.session_state.jobs:
            score = job.get('match_score',0)
            clr = "#43e97b" if score>=80 else "#ffb347" if score>=65 else "#ff6584"
            badges = "".join([f'<span class="sm-badge">{s}</span>' for s in job.get('required_skills',[])])
            src_clr = "#6c63ff" if job.get('source')=="LinkedIn" else "#ff6584"
            st.markdown(f"""<div class="sm-job">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="flex:1;">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                            <span style="font-weight:700;font-size:1rem;color:#e0e0f0;">{job.get('title','')}</span>
                            <span style="font-size:0.7rem;color:{src_clr};background:rgba(108,99,255,0.1);padding:2px 8px;border-radius:10px;">{job.get('source','')}</span>
                        </div>
                        <div style="font-size:0.82rem;color:#666688;">{job.get('company','')} · {job.get('location','')} · {job.get('posted','')}</div>
                        <div style="font-size:0.82rem;color:#999ab8;margin-top:8px;line-height:1.5;">{job.get('description','')[:180]}</div>
                        <div style="margin-top:10px;">{badges}</div>
                    </div>
                    <div style="text-align:center;min-width:80px;padding-left:16px;">
                        <div style="font-size:1.8rem;font-weight:800;color:{clr};">{score}%</div>
                        <div style="font-size:0.68rem;color:#444460;text-transform:uppercase;letter-spacing:.5px;">Match</div>
                        <div style="font-size:0.78rem;color:#43e97b;margin-top:4px;">{job.get('salary_range','')}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW PREP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Interview Prep":
    st.markdown('<div class="sm-page-title">🎤 Interview Prep Kit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Mock questions, STAR builder & company briefings</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["❓ Mock Questions","⭐ STAR Builder","🏢 Company Briefing"])
    with tab1:
        c1,c2 = st.columns(2)
        with c1: iq_role = st.text_input("Target Role", placeholder="e.g. Backend Engineer", key="iq_role")
        with c2: qtypes = st.multiselect("Question Types", ["Technical","Behavioral","Situational","Leadership"], default=["Technical","Behavioral"])
        if st.button("Generate Questions", use_container_width=True) and iq_role:
            with st.spinner("Generating..."):
                questions = generate_interview_questions(st.session_state.resume_text, iq_role, qtypes)
            for i,q in enumerate(questions,1):
                type_clr = {"Technical":"#6c63ff","Behavioral":"#43e97b","Situational":"#ffb347","Leadership":"#ff6584"}.get(q.get('type',''),"#6c63ff")
                st.markdown(f"""<div class="sm-card" style="margin:8px 0;">
                    <span style="font-size:0.7rem;color:{type_clr};font-weight:600;text-transform:uppercase;">Q{i} · {q.get('type','')}</span>
                    <div style="font-weight:600;color:#e0e0f0;font-size:0.92rem;margin:8px 0;">{q.get('question','')}</div>
                    <div style="font-size:0.8rem;color:#555570;">💡 {q.get('tip','')}</div>
                </div>""", unsafe_allow_html=True)
    with tab2:
        situation = st.text_area("Describe a work situation", placeholder="e.g. Led a team to deliver a critical project under tight deadline...", height=120)
        target_q  = st.text_input("Interview question to answer", placeholder="e.g. Tell me about a time you showed leadership")
        if st.button("Build STAR Answer", use_container_width=True) and situation:
            with st.spinner("Structuring..."):
                star = generate_star_answer(situation, target_q)
            for lbl, key, clr in [("📍 Situation","situation","#6c63ff"),("🎯 Task","task","#ff6584"),("⚡ Action","action","#43e97b"),("🏆 Result","result","#ffb347")]:
                st.markdown(f"""<div class="sm-star">
                    <div style="font-weight:700;color:{clr};font-size:0.82rem;margin-bottom:6px;">{lbl}</div>
                    <div style="font-size:0.88rem;color:#c0c0d8;line-height:1.6;">{star.get(key,'')}</div>
                </div>""", unsafe_allow_html=True)
    with tab3:
        c1,c2 = st.columns(2)
        with c1: company = st.text_input("Company", placeholder="e.g. Google, Infosys, Zomato")
        with c2: c_role  = st.text_input("Applying for", placeholder="e.g. Software Engineer")
        if st.button("Generate Briefing", use_container_width=True) and company:
            with st.spinner("Researching..."):
                briefing = generate_company_briefing(company, c_role)
            st.markdown(f"""<div class="sm-card">
                <div style="font-weight:700;font-size:1rem;color:#e0e0f0;margin-bottom:12px;">🏢 {company} — Interview Briefing</div>
                <div style="font-size:0.85rem;color:#999ab8;white-space:pre-wrap;line-height:1.7;">{briefing}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Document Generator":
    st.markdown('<div class="sm-page-title">📄 Document Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Generate polished career documents in seconds</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["📝 Cover Letter","📧 Thank You Email","📄 PDF Resume"])
    with tab1:
        c1,c2 = st.columns(2)
        with c1:
            cl_co   = st.text_input("Company", placeholder="e.g. Amazon")
            cl_role = st.text_input("Role", placeholder="e.g. Data Engineer")
        with c2:
            cl_tone = st.selectbox("Tone", ["Professional","Enthusiastic","Concise","Creative"])
            cl_highlight = st.text_input("Key achievement", placeholder="e.g. Built ML pipeline saving $2M")
        if st.button("✨ Generate Cover Letter", use_container_width=True):
            if not st.session_state.resume_text: st.warning("Upload resume first!")
            else:
                with st.spinner("Writing..."):
                    letter = generate_cover_letter(st.session_state.resume_text, cl_co, cl_role, cl_tone, cl_highlight)
                st.markdown(f'<div class="sm-output">{letter}</div>', unsafe_allow_html=True)
                st.download_button("⬇️ Download", letter, file_name="cover_letter.txt", use_container_width=True)
    with tab2:
        c1,c2 = st.columns(2)
        with c1:
            ty_name = st.text_input("Interviewer Name", placeholder="e.g. Rahul Sharma")
            ty_co   = st.text_input("Company", placeholder="e.g. Flipkart", key="ty_co")
        with c2:
            ty_role  = st.text_input("Role", placeholder="e.g. Product Manager", key="ty_role")
            ty_topic = st.text_input("Topic discussed", placeholder="e.g. AI strategy for 2025")
        if st.button("✉️ Generate Email", use_container_width=True):
            with st.spinner("Writing..."):
                email = generate_thankyou_email(ty_name, ty_co, ty_role, ty_topic)
            st.markdown(f'<div class="sm-output">{email}</div>', unsafe_allow_html=True)
            st.download_button("⬇️ Download", email, file_name="thankyou_email.txt", use_container_width=True)
    with tab3:
        pdf_name = st.text_input("Your Full Name", placeholder="e.g. Arjun Sharma")
        if st.button("📄 Generate PDF Resume", use_container_width=True):
            if not st.session_state.resume_text: st.warning("Upload resume first!")
            else:
                with st.spinner("Building PDF..."):
                    pdf_bytes = generate_resume_pdf(st.session_state.resume_text, pdf_name)
                st.download_button("⬇️ Download PDF", pdf_bytes, file_name="resume.pdf", mime="application/pdf", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5-YEAR SIM
# ══════════════════════════════════════════════════════════════════════════════
elif page == "5-Year Career Sim":
    st.markdown('<div class="sm-page-title">🔮 5-Year Career Simulation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Simulate two career paths and see where you end up in 2030</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:0.85rem;font-weight:600;color:#6c63ff;margin-bottom:6px;">🔵 Path A</div>', unsafe_allow_html=True)
        path_a = st.text_input("Path A", placeholder="e.g. Stay and get promoted to Senior Engineer", label_visibility="collapsed")
    with c2:
        st.markdown('<div style="font-size:0.85rem;font-weight:600;color:#ff6584;margin-bottom:6px;">🔴 Path B</div>', unsafe_allow_html=True)
        path_b = st.text_input("Path B", placeholder="e.g. Join a startup as founding engineer", label_visibility="collapsed")
    if st.button("🔮 Simulate Both Paths", use_container_width=True) and path_a and path_b:
        with st.spinner("Simulating your future..."):
            sim = simulate_career_path(st.session_state.resume_text, path_a, path_b)
        c1,c2 = st.columns(2)
        for col, key, clr, lbl in [(c1,"path_a","#6c63ff","Path A"),(c2,"path_b","#ff6584","Path B")]:
            with col:
                d = sim.get(key,{})
                badges = "".join([f'<span class="sm-badge">{s}</span>' for s in d.get('skills_gained',[])])
                st.markdown(f"""<div class="sm-card">
                    <div style="font-weight:700;color:{clr};margin-bottom:16px;">🔮 {lbl} — 2030</div>
                    <div style="margin-bottom:14px;">
                        <div style="font-size:0.7rem;color:#444460;text-transform:uppercase;letter-spacing:1px;">Projected Salary</div>
                        <div style="font-size:1.8rem;font-weight:800;color:{clr};margin-top:2px;">{d.get('salary','?')}</div>
                    </div>
                    <div style="margin-bottom:14px;">
                        <div style="font-size:0.7rem;color:#444460;text-transform:uppercase;letter-spacing:1px;">Likely Role</div>
                        <div style="font-weight:600;color:#e0e0f0;margin-top:2px;">{d.get('role','?')}</div>
                    </div>
                    <div style="margin-bottom:14px;">
                        <div style="font-size:0.7rem;color:#444460;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Skills Gained</div>
                        {badges}
                    </div>
                    <div style="font-size:0.83rem;color:#999ab8;line-height:1.6;">{d.get('narrative','')}</div>
                </div>""", unsafe_allow_html=True)
        if sim.get("verdict"):
            st.markdown(f"""<div class="sm-card" style="border-color:rgba(67,233,123,0.2);margin-top:4px;">
                <div style="font-weight:700;color:#43e97b;margin-bottom:8px;">🏆 AI Verdict</div>
                <div style="font-size:0.88rem;color:#c0c0d8;line-height:1.6;">{sim['verdict']}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Application Tracker":
    st.markdown('<div class="sm-page-title">📊 Application Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Kanban board for managing all your job applications</div>', unsafe_allow_html=True)
    render_tracker()

# ══════════════════════════════════════════════════════════════════════════════
# SKILL DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Skill Dashboard":
    st.markdown('<div class="sm-page-title">📈 Skill Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sm-page-sub">Visual breakdown of your skill landscape & market demand</div>', unsafe_allow_html=True)
    if not st.session_state.resume_text:
        st.warning("⬅️ Please upload your resume from the sidebar first.")
    else:
        render_skill_dashboard(st.session_state.resume_data)