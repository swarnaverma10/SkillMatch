import streamlit as st
from src.helper import extract_text_from_pdf, analyze_resume
from src.ats_scorer import score_ats
from src.job_api import fetch_jobs

st.set_page_config(page_title="SkillMatch AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {
    font-family: 'Sora', sans-serif !important;
    box-sizing: border-box;
}

html, body { overflow-x: hidden; }
.stApp { background: #07070f !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
#MainMenu, footer, header     { visibility: hidden !important; }

/* ─── HERO SECTION ─────────────────────────────────── */
.hero-wrap {
    min-height: 100vh;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 60px 24px 40px;
    position: relative; overflow: hidden; text-align: center;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: -120px; left: 50%; transform: translateX(-50%);
    width: 700px; height: 700px; border-radius: 50%;
    background: radial-gradient(circle, rgba(108,99,255,0.14) 0%, transparent 65%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute; bottom: -100px; right: -100px;
    width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,101,132,0.08) 0%, transparent 65%);
    pointer-events: none;
}
.dot {
    position: absolute; border-radius: 50%;
    background: rgba(108,99,255,0.4);
    animation: floatDot 6s ease-in-out infinite;
}
.dot1 { width:6px; height:6px; top:15%; left:12%; animation-delay:0s; }
.dot2 { width:4px; height:4px; top:30%; right:15%; animation-delay:1s; }
.dot3 { width:8px; height:8px; bottom:25%; left:8%; animation-delay:2s; }
.dot4 { width:5px; height:5px; top:60%; right:10%; animation-delay:0.5s; }
.dot5 { width:3px; height:3px; bottom:15%; right:25%; animation-delay:1.5s; }
@keyframes floatDot {
    0%,100% { transform: translateY(0px); opacity:.4; }
    50%      { transform: translateY(-14px); opacity:1; }
}

@keyframes slideDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes slideUp {
    from { opacity:0; transform:translateY(24px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes rotateSlow { to { transform: rotate(360deg); } }

.hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800; line-height: 1.1;
    color: #f2f2fc; margin-bottom: 20px;
    letter-spacing: -1px;
    animation: slideUp 0.65s ease 0.1s both;
}
.hero-title .grad {
    background: linear-gradient(135deg, #6c63ff 0%, #ff6584 55%, #43e97b 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub {
    font-size: clamp(0.95rem, 1.8vw, 1.1rem);
    color: #55556a; line-height: 1.7; max-width: 520px;
    margin: 0 auto 44px;
    animation: slideUp 0.65s ease 0.2s both;
}

/* ─── UPLOAD BOX ── */
[data-testid="stFileUploadDropzone"] {
    background: linear-gradient(135deg, rgba(108,99,255,0.06), rgba(255,101,132,0.04)) !important;
    border: 2px dashed rgba(108,99,255,0.4) !important;
    border-radius: 16px !important;
    padding: 28px 20px !important;
    transition: all 0.3s !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(108,99,255,0.1) !important;
    border-color: #6c63ff !important;
    box-shadow: 0 0 30px rgba(108,99,255,0.15) !important;
}
[data-testid="stFileUploadDropzone"] p { color: #666688 !important; font-size: 0.85rem !important; }
[data-testid="stFileUploadDropzone"] button {
    background: rgba(108,99,255,0.15) !important;
    border: 1px solid rgba(108,99,255,0.4) !important;
    color: #a89fff !important; border-radius: 8px !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    padding: 7px 18px !important;
}

/* ─── STATS ── */
.stat-chip {
    background: #0f0f1c; border: 1px solid #1a1a2e;
    border-radius: 12px; padding: 14px 22px; text-align: center; min-width: 110px;
}
.stat-val   { font-size: 1.6rem; font-weight: 800; }
.stat-label { font-size: 0.68rem; color: #444460; text-transform:uppercase; letter-spacing:1px; margin-top:4px; }

/* ─── FEATURE CARDS ── */
.feat-card {
    background: rgba(15, 15, 28, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px; padding: 32px 24px; text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden;
}
.feat-card:hover {
    border-color: rgba(108,99,255,0.6);
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 24px 60px rgba(108,99,255,0.2);
}
.feat-icon-wrap {
    width: 60px; height: 60px; border-radius: 16px; margin: 0 auto 18px;
    background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(255,101,132,0.1));
    border: 1px solid rgba(108,99,255,0.2);
    display: flex; align-items: center; justify-content: center; font-size: 1.7rem;
}
.feat-title { font-size: 1rem; font-weight: 700; color: #e8e8f8; margin-bottom: 10px; }
.feat-desc  { font-size: 0.8rem; color: #444468; line-height: 1.6; margin-bottom: 18px; }
.feat-tag {
    display: inline-block; padding: 4px 14px;
    background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px; font-size: 0.72rem; color: #a89fff; margin-bottom: 20px;
}

/* ─── INNER PAGES ── */
.page-wrap { padding: 36px 40px 60px; max-width: 1060px; margin: 0 auto; }
.page-title {
    font-size: clamp(1.6rem, 3vw, 2.2rem);
    font-weight: 800; color: #f2f2fc;
    letter-spacing: -0.5px; margin-bottom: 6px;
}
.page-sub { font-size: 0.88rem; color: #444460; margin-bottom: 32px; }

.card {
    background: rgba(15, 15, 28, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px; padding: 24px;
    transition: all 0.3s ease;
}
.card:hover { border-color: rgba(108,99,255,0.3); box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
.metric {
    background: rgba(15, 15, 28, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px; padding: 22px 16px; text-align: center; transition: all 0.2s;
}
.metric:hover { transform: translateY(-3px); border-color: rgba(108,99,255,0.4); }
.metric-val   { font-size: 2rem; font-weight: 800; line-height: 1; }
.metric-label { font-size: 0.68rem; color: #333350; text-transform:uppercase; letter-spacing:1.2px; margin-top:8px; }

.badge {
    display: inline-block;
    background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px; padding: 4px 13px;
    font-size: 0.78rem; color: #a89fff; margin: 3px;
}
.badge.green { background:rgba(67,233,123,0.08); border-color:rgba(67,233,123,0.22); color:#43e97b; }
.badge.red   { background:rgba(255,101,132,0.08); border-color:rgba(255,101,132,0.22); color:#ff6584; }

.skill-sec {
    background: #0f0f1c; border: 1px solid #1a1a2e;
    border-radius: 14px; padding: 18px 20px; margin: 8px 0;
}
.skill-cat-label {
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;
}

.sbar-bg   { height:8px; background:#1a1a2e; border-radius:4px; margin-top:14px; }
.sbar-fill { height:100%; border-radius:4px; }

.tip {
    padding: 13px 18px;
    background: rgba(108,99,255,0.05); border-left: 3px solid #6c63ff;
    border-radius: 0 10px 10px 0; font-size: 0.84rem; color: #c0c0d8;
    margin: 6px 0; line-height: 1.55;
}

/* ─── JOB CARD ── */
.job-card {
    background: rgba(15, 15, 28, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px; padding: 22px 24px; margin: 12px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.job-card:hover { border-color: rgba(108,99,255,0.5); transform: translateY(-4px); box-shadow: 0 16px 40px rgba(108,99,255,0.15); }

/* ─── APPLY LINKS ── */
.apply-links { display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
.alink {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 7px 14px; border-radius: 8px;
    font-size: 0.78rem; font-weight: 600;
    text-decoration: none !important;
    transition: all 0.18s;
}
.alink:hover { transform: translateY(-1px); filter: brightness(1.15); }
.alink-li  { background:rgba(10,102,194,0.15); border:1px solid rgba(10,102,194,0.35); color:#5baeff !important; }
.alink-nk  { background:rgba(255,101,132,0.12); border:1px solid rgba(255,101,132,0.30); color:#ff6584 !important; }
.alink-ind { background:rgba(67,233,123,0.10); border:1px solid rgba(67,233,123,0.28); color:#43e97b !important; }
.alink-g   { background:rgba(255,180,0,0.10); border:1px solid rgba(255,180,0,0.25); color:#ffb347 !important; }
.alink-gd  { background:rgba(12, 170, 65,0.10); border:1px solid rgba(12, 170, 65,0.25); color:#0caa41 !important; }

/* ─── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    color: #fff !important; border: none !important;
    border-radius: 11px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 10px 24px !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover { opacity:.85 !important; transform:translateY(-1px) !important; }

.stTextInput input, .stTextArea textarea {
    background: #0f0f1c !important; border: 1px solid #1a1a2e !important;
    border-radius: 11px !important; color: #e0e0f0 !important; font-size: 0.88rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6c63ff !important; box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important;
}
.stTextInput label, .stTextArea label { color: #888 !important; font-size: 0.82rem !important; }

.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid #1a1a2e !important; }
.stTabs [data-baseweb="tab"]      { color:#444460 !important; font-size:0.88rem !important; font-weight:500 !important; }
.stTabs [aria-selected="true"]    { color:#6c63ff !important; border-bottom-color:#6c63ff !important; }
.streamlit-expanderHeader { color: #666688 !important; font-size: 0.85rem !important; }

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:#2a2a4a; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────
for k, v in [("resume_text",""), ("resume_data",{}), ("jobs",[]), ("page","home")]:
    if k not in st.session_state:
        st.session_state[k] = v

p = st.session_state.page

# ══════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════
if p == "home":
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

    # Brand pill
    st.markdown(
        "<div style='text-align:center;margin-bottom:28px;'>"
        "<span style='display:inline-flex;align-items:center;gap:10px;"
        "background:rgba(108,99,255,0.12);border:1px solid rgba(108,99,255,0.3);"
        "border-radius:50px;padding:8px 22px;font-size:0.82rem;font-weight:600;color:#a89fff;letter-spacing:.4px;'>"
        "🚀&nbsp; SkillMatch AI &nbsp;·&nbsp; Career Intelligence Platform"
        "</span></div>",
        unsafe_allow_html=True
    )

    # Hero title
    st.markdown(
        "<div style='text-align:center;font-size:clamp(2.2rem,4.5vw,3.8rem);"
        "font-weight:800;line-height:1.12;color:#f2f2fc;letter-spacing:-1px;margin-bottom:18px;'>"
        "Land Your Dream Job<br>"
        "<span style='background:linear-gradient(135deg,#6c63ff,#ff6584,#43e97b);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>"
        "with Smarter Career Tools"
        "</span></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='text-align:center;font-size:1rem;color:#555570;line-height:1.7;"
        "max-width:500px;margin:0 auto 44px;'>"
        "Upload your resume once. Get instant skill analysis,<br>"
        "ATS scoring &amp; perfectly matched job listings."
        "</div>",
        unsafe_allow_html=True
    )

    # Nav buttons
    _, c1, c2, c3, _ = st.columns([2, 1, 1, 1, 2])
    with c1:
        if st.button("📑 Analyzer", use_container_width=True, key="hn_a"):
            st.session_state.page = "analyzer"; st.rerun()
    with c2:
        if st.button("🎯 ATS Score", use_container_width=True, key="hn_b"):
            st.session_state.page = "ats"; st.rerun()
    with c3:
        if st.button("💼 Jobs", use_container_width=True, key="hn_c"):
            st.session_state.page = "jobs"; st.rerun()

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # Upload
    _, uc, _ = st.columns([1.2, 2, 1.2])
    with uc:
        st.markdown(
            "<div style='text-align:center;padding:20px 0 16px;'>"
            "<div style='font-size:2.4rem;margin-bottom:10px;'>📄</div>"
            "<div style='font-size:1rem;font-weight:700;color:#e0e0f0;margin-bottom:4px;'>Upload Your Resume</div>"
            "<div style='font-size:0.78rem;color:#444460;'>PDF only &nbsp;·&nbsp; Analyzed instantly &nbsp;·&nbsp; 100% private</div>"
            "</div>",
            unsafe_allow_html=True
        )
        up = st.file_uploader("Upload PDF Resume", type=["pdf"], label_visibility="collapsed")
        if up:
            with st.spinner("Analyzing your resume..."):
                t = extract_text_from_pdf(up)
                st.session_state.resume_text = t
                st.session_state.resume_data = analyze_resume(t)
                
                # Auto-fetch jobs based on predicted role
                if 'predicted_role' in st.session_state.resume_data:
                    st.session_state.jobs = fetch_jobs(st.session_state.resume_data['predicted_role'], "", t)
                    
            st.success("✅ Resume analyzed! We've automatically found best-matched jobs for you. Click 'Jobs' to view.")

    # Stats
    if st.session_state.resume_text:
        d = st.session_state.resume_data
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        for col, val, lbl, clr in [
            (s1, str(d.get('years_experience','0')), "Years Exp.",   "#6c63ff"),
            (s2, str(len(d.get('skills', []))),      "Skills Found", "#43e97b"),
            (s3, (d.get('name','—') or '—')[:16],    "Candidate",    "#ffb347"),
            (s4, d.get('predicted_role', '—')[:20],  "Predicted Role","#ff6584"),
        ]:
            with col:
                st.markdown(f"""<div class="stat-chip">
                    <div class="stat-val" style="color:{clr};">{val}</div>
                    <div class="stat-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div style="text-align:center;padding:56px 0 24px;">
        <div style="font-size:1.8rem;font-weight:800;color:#f2f2fc;letter-spacing:-.5px;">Everything You Need</div>
        <div style="font-size:0.88rem;color:#444460;margin-top:8px;">Three powerful tools. Zero complexity. Auto-matching with Indeed, Naukri & Glassdoor.</div>
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    for col, icon, title, desc, tag, pg in [
        (fc1,"📑","Resume Analyzer","AI extracts skills, experience, education & contact info automatically.","Skill Extraction","analyzer"),
        (fc2,"🎯","ATS Score","Paste any JD and get a live keyword match score with gaps & tips.","ATS Matching","ats"),
        (fc3,"💼","Job Matcher","Auto-matches jobs from LinkedIn, Naukri, Indeed & Glassdoor.","Live Job Links","jobs"),
    ]:
        with col:
            st.markdown(f"""<div class="feat-card">
                <div class="feat-icon-wrap">{icon}</div>
                <div class="feat-title">{title}</div>
                <div class="feat-desc">{desc}</div>
                <div class="feat-tag">{tag}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"feat_{pg}", use_container_width=True):
                st.session_state.page = pg; st.rerun()

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# INNER PAGE NAV
# ══════════════════════════════════════════════════════════
else:
    n1, n2, n3, n4, n5 = st.columns([0.6, 1, 1, 1, 5])
    with n1:
        if st.button("← Home", key="nb_home"):
            st.session_state.page = "home"; st.rerun()
    with n2:
        if st.button("📑 Analyzer", key="nb_a", use_container_width=True):
            st.session_state.page = "analyzer"; st.rerun()
    with n3:
        if st.button("🎯 ATS Score", key="nb_b", use_container_width=True):
            st.session_state.page = "ats"; st.rerun()
    with n4:
        if st.button("💼 Jobs", key="nb_c", use_container_width=True):
            st.session_state.page = "jobs"; st.rerun()
    st.markdown("<hr style='border:none;border-top:1px solid #1a1a2e;margin:0;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# RESUME ANALYZER
# ══════════════════════════════════════════════════════════
if p == "analyzer":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>📑 Resume Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>AI-powered skill &amp; profile extraction</div>", unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.markdown("""<div class="card" style="text-align:center;padding:60px;">
            <div style="font-size:3rem;margin-bottom:16px;">📄</div>
            <div style="font-size:1rem;font-weight:700;color:#e0e0f0;margin-bottom:8px;">No Resume Uploaded</div>
            <div style="font-size:0.85rem;color:#444460;">Go back to Home and upload your PDF resume first.</div>
        </div>""", unsafe_allow_html=True)
    else:
        data   = st.session_state.resume_data
        skills = data.get("skills", [])

        st.markdown(f"""<div class="card" style="margin-bottom:20px;display:flex;align-items:center;gap:18px;">
            <div style="width:56px;height:56px;border-radius:50%;flex-shrink:0;
                background:linear-gradient(135deg,#6c63ff,#ff6584);
                display:flex;align-items:center;justify-content:center;font-size:1.5rem;">👤</div>
            <div>
                <div style="font-size:1.1rem;font-weight:700;color:#f2f2fc;margin-bottom:6px;">{data.get('name','Candidate')}</div>
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                    {"<span style='font-size:0.8rem;color:#555570;'>📧 "+data.get('email','')+"</span>" if data.get('email') else ""}
                    {"<span style='font-size:0.8rem;color:#555570;'>📞 "+data.get('phone','')+"</span>" if data.get('phone') else ""}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(f"""<div class="metric">
                <div class="metric-val" style="color:#6c63ff;">{data.get('years_experience','0')}</div>
                <div class="metric-label">Years Experience</div>
            </div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""<div class="metric">
                <div class="metric-val" style="color:#43e97b;">{len(skills)}</div>
                <div class="metric-label">Skills Detected</div>
            </div>""", unsafe_allow_html=True)
        with mc3:
            edu = data.get('education','Not detected')
            st.markdown(f"""<div class="metric">
                <div style="font-size:0.85rem;font-weight:600;color:#ffb347;margin-top:4px;line-height:1.4;">{edu[:35] if edu else 'N/A'}</div>
                <div class="metric-label" style="margin-top:10px;">Education</div>
            </div>""", unsafe_allow_html=True)

        if skills:
            st.markdown("<div style='margin:28px 0 14px;font-size:1rem;font-weight:700;color:#f2f2fc;'>🔑 Detected Skills</div>", unsafe_allow_html=True)
            cats = {
                "💻 Programming":   (["Python","Java","JavaScript","TypeScript","C++","C#","C","Go","Rust","Ruby","PHP","Swift","Kotlin","R","Scala","MATLAB"], "#6c63ff"),
                "🌐 Web & Mobile":  (["React","Angular","Vue","Node.js","Django","Flask","FastAPI","HTML","CSS","Next.js","Express","Android","iOS","Spring"], "#43e97b"),
                "🤖 AI & Data":     (["Machine Learning","Deep Learning","NLP","TensorFlow","PyTorch","Pandas","NumPy","Data Analysis","Data Science","Computer Vision","Scikit-learn","Keras","BERT","LLM","Hugging Face","OpenCV"], "#ff6584"),
                "☁️ Cloud & DevOps":(["AWS","Azure","GCP","Docker","Kubernetes","CI/CD","Git","GitHub","Linux","Jenkins","Terraform","Ansible"], "#ffb347"),
                "🗄️ Databases":     (["SQL","MySQL","PostgreSQL","MongoDB","Redis","Firebase","Oracle","SQLite","Elasticsearch","DynamoDB","Cassandra"], "#00d4aa"),
                "🛠️ Tools":         (["Agile","Scrum","Jira","Figma","Spark","Kafka","Power BI","Tableau","Excel","Postman","Selenium","Unity"], "#a78bfa"),
            }
            skill_set = {s.lower() for s in skills}
            all_cat   = set()
            for cat, (cskills, clr) in cats.items():
                matched = [s for s in cskills if s.lower() in skill_set]
                if matched:
                    all_cat.update(s.lower() for s in matched)
                    badges = "".join([f'<span class="badge">{s}</span>' for s in matched])
                    st.markdown(f"""<div class="skill-sec">
                        <div class="skill-cat-label" style="color:{clr};">{cat}</div>
                        <div>{badges}</div>
                    </div>""", unsafe_allow_html=True)
            others = [s for s in skills if s.lower() not in all_cat]
            if others:
                badges = "".join([f'<span class="badge">{s}</span>' for s in others])
                st.markdown(f"""<div class="skill-sec">
                    <div class="skill-cat-label" style="color:#666688;">🔖 Other Skills</div>
                    <div>{badges}</div>
                </div>""", unsafe_allow_html=True)

        with st.expander("📄 View Raw Resume Text"):
            st.text_area("", st.session_state.resume_text[:3000], height=200, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ATS SCORE
# ══════════════════════════════════════════════════════════
elif p == "ats":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>🎯 ATS Score Checker</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Paste any job description to see your keyword match score</div>", unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.markdown("""<div class="card" style="text-align:center;padding:60px;">
            <div style="font-size:3rem;margin-bottom:16px;">📄</div>
            <div style="font-size:1rem;font-weight:700;color:#e0e0f0;margin-bottom:8px;">No Resume Found</div>
            <div style="font-size:0.85rem;color:#444460;">Go to Home and upload your resume first.</div>
        </div>""", unsafe_allow_html=True)
    else:
        jd = st.text_area("📋 Paste Job Description", height=200,
            placeholder="Paste the full job description — responsibilities, requirements, skills needed...")
        if st.button("🔍 Check My ATS Score", use_container_width=True) and jd.strip():
            result = score_ats(st.session_state.resume_text, jd)
            score  = result["score"]
            clr    = "#43e97b" if score>=70 else "#ffb347" if score>=50 else "#ff6584"
            lbl    = "Excellent Match ✅" if score>=70 else "Needs Improvement ⚠️" if score>=50 else "Low Match ❌"
            msg    = ("Your resume is well-optimized for this role!" if score>=70
                      else "Add more relevant keywords to improve chances." if score>=50
                      else "Major gaps found — tailor your resume to this JD.")

            c1, c2 = st.columns([1, 1.8])
            with c1:
                st.markdown(f"""<div class="card" style="text-align:center;padding:40px 20px;">
                    <div style="font-size:0.65rem;color:#333350;text-transform:uppercase;letter-spacing:2px;margin-bottom:16px;">ATS Match Score</div>
                    <div style="font-size:5.5rem;font-weight:800;color:{clr};line-height:1;">{score}%</div>
                    <div style="font-size:0.9rem;color:{clr};margin-top:10px;font-weight:600;">{lbl}</div>
                    <div class="sbar-bg"><div class="sbar-fill" style="width:{score}%;background:{clr};"></div></div>
                    <div style="font-size:0.78rem;color:#444460;margin-top:16px;line-height:1.5;">{msg}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                matched = result.get("matched", [])
                missing = result.get("missing", [])
                m = "".join([f'<span class="badge green">{k}</span>' for k in matched])
                x = "".join([f'<span class="badge red">{k}</span>'   for k in missing])
                st.markdown(f"""<div class="card" style="height:100%;">
                    <div style="margin-bottom:20px;">
                        <div style="font-size:0.7rem;color:#43e97b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">✅ Matched ({len(matched)})</div>
                        {m or "<span style='color:#333350;font-size:0.82rem;'>None matched</span>"}
                    </div>
                    <div style="border-top:1px solid #1a1a2e;padding-top:18px;">
                        <div style="font-size:0.7rem;color:#ff6584;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">❌ Missing ({len(missing)})</div>
                        {x or "<span style='color:#43e97b;font-size:0.82rem;'>No gaps — great match!</span>"}
                    </div>
                </div>""", unsafe_allow_html=True)

            tips = result.get("tips", [])
            if tips:
                st.markdown("<div style='margin:24px 0 10px;font-size:1rem;font-weight:700;color:#f2f2fc;'>💡 How to Improve Your Score</div>", unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<div class="tip">→ {tip}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# JOB MATCHER — role-specific jobs + correct apply links
# ══════════════════════════════════════════════════════════
elif p == "jobs":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>💼 Job Matcher</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Role-specific jobs with direct apply links to LinkedIn, Naukri &amp; Indeed</div>", unsafe_allow_html=True)

    default_role = st.session_state.resume_data.get('predicted_role', '') if st.session_state.resume_data else ''

    c1, c2 = st.columns(2)
    with c1:
        role = st.text_input("🔍 Target Role", value=default_role,
            placeholder="e.g. ML Engineer, Data Scientist, Full Stack Developer, DevOps...")
    with c2:
        loc = st.text_input("📍 Location (optional)",
            placeholder="e.g. Bangalore, Remote, Mumbai, Delhi...")

    if st.button("🔍 Find Matching Jobs", use_container_width=True) and role.strip():
        with st.spinner(f"Finding {role} jobs..."):
            st.session_state.jobs = fetch_jobs(role, loc, st.session_state.resume_text)

    if st.session_state.jobs:
        jobs = st.session_state.jobs
        best = jobs[0]

        # Summary bar
        st.markdown(f"""<div style="display:flex;align-items:center;gap:24px;margin-bottom:22px;
            padding:16px 22px;background:#0f0f1c;border:1px solid #1a1a2e;border-radius:14px;flex-wrap:wrap;">
            <div>
                <div style="font-size:0.68rem;color:#333350;text-transform:uppercase;letter-spacing:1px;">Results</div>
                <div style="font-size:1rem;font-weight:700;color:#f2f2fc;margin-top:3px;">{len(jobs)} {jobs[0]['title']} jobs found</div>
            </div>
            <div style="width:1px;height:34px;background:#1a1a2e;"></div>
            <div>
                <div style="font-size:0.68rem;color:#333350;text-transform:uppercase;letter-spacing:1px;">Best Match</div>
                <div style="font-size:1rem;font-weight:700;color:#43e97b;margin-top:3px;">{best['match_score']}% — {best['company']}</div>
            </div>
            <div style="width:1px;height:34px;background:#1a1a2e;"></div>
            <div>
                <div style="font-size:0.68rem;color:#333350;text-transform:uppercase;letter-spacing:1px;">Apply via</div>
                <div style="font-size:0.85rem;font-weight:600;color:#a89fff;margin-top:3px;">LinkedIn · Naukri · Indeed · Google</div>
            </div>
        </div>""", unsafe_allow_html=True)

        for job in jobs:
            score  = job.get("match_score", 0)
            clr    = "#43e97b" if score>=80 else "#ffb347" if score>=65 else "#ff6584"
            badges = "".join([f'<span class="badge">{s}</span>' for s in job.get("required_skills", [])])

            # All 4 links come pre-built from job_api.py
            li_url  = job.get("linkedin_url", "#")
            nk_url  = job.get("naukri_url",   "#")
            ind_url = job.get("indeed_url",   "#")
            gd_url  = job.get("glassdoor_url", "#")
            g_url   = job.get("google_url",   "#")

            # Source tag color
            src = job.get("source","")
            src_colors = {
                "LinkedIn": ("rgba(10,102,194,0.12)","rgba(10,102,194,0.30)","#5baeff"),
                "Naukri":   ("rgba(255,101,132,0.10)","rgba(255,101,132,0.28)","#ff8fa3"),
                "Indeed":   ("rgba(67,233,123,0.08)", "rgba(67,233,123,0.24)","#43e97b"),
            }
            s_bg, s_bd, s_tc = src_colors.get(src, ("rgba(108,99,255,0.10)","rgba(108,99,255,0.25)","#a89fff"))

            job_html = f"""<div class="job-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">

                    <div style="flex:1;min-width:0;">
                        <!-- Header -->
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap;">
                            <span style="font-size:1.02rem;font-weight:700;color:#f2f2fc;">{job.get('title','')}</span>
                            <span style="font-size:0.7rem;padding:3px 10px;border-radius:20px;
                                background:{s_bg};border:1px solid {s_bd};color:{s_tc};">{src}</span>
                            <span style="font-size:0.7rem;color:#333350;">🕐 {job.get('posted','')}</span>
                        </div>

                        <!-- Meta -->
                        <div style="font-size:0.83rem;color:#555570;margin-bottom:12px;display:flex;gap:18px;flex-wrap:wrap;">
                            <span>🏢 <b style="color:#c0c0d8;">{job.get('company','')}</b></span>
                            <span>📍 {job.get('location','')}</span>
                            <span>💰 <b style="color:#43e97b;">{job.get('salary_range','')}</b></span>
                        </div>

                        <!-- Description -->
                        <div style="font-size:0.83rem;color:#555570;line-height:1.65;margin-bottom:14px;">
                            {job.get('description','')[:240]}
                        </div>

                        <!-- Skill badges -->
                        <div style="margin-bottom:14px;">{badges}</div>

                        <!-- Apply links — all 5 platforms -->
                        <div class="apply-links">
                            <a href="{li_url}"  target="_blank" class="alink alink-li">🔗 LinkedIn</a>
                            <a href="{nk_url}"  target="_blank" class="alink alink-nk">🔗 Naukri</a>
                            <a href="{ind_url}" target="_blank" class="alink alink-ind">🔗 Indeed</a>
                            <a href="{gd_url}"  target="_blank" class="alink alink-gd">🔗 Glassdoor</a>
                            <a href="{g_url}"   target="_blank" class="alink alink-g">🔍 Google</a>
                        </div>
                    </div>

                    <!-- Match score -->
                    <div style="flex-shrink:0;text-align:center;min-width:82px;
                        background:rgba(108,99,255,0.06);border:1px solid rgba(108,99,255,0.12);
                        border-radius:14px;padding:18px 14px;">
                        <div style="font-size:2.2rem;font-weight:800;color:{clr};line-height:1;">{score}%</div>
                        <div style="font-size:0.62rem;color:#333350;text-transform:uppercase;letter-spacing:.5px;margin-top:5px;">Match</div>
                        <div style="margin-top:10px;height:4px;background:#1a1a2e;border-radius:2px;overflow:hidden;">
                            <div style="width:{score}%;height:100%;background:{clr};border-radius:2px;"></div>
                        </div>
                    </div>
                </div>
            </div>"""
            flat_html = "".join([line.strip() for line in job_html.split('\n')])
            st.markdown(flat_html, unsafe_allow_html=True)

    elif not st.session_state.jobs:
        st.markdown("""<div class="card" style="text-align:center;padding:60px;">
            <div style="font-size:3rem;margin-bottom:14px;">🔍</div>
            <div style="font-size:1rem;font-weight:700;color:#e0e0f0;margin-bottom:10px;">Ready to Search</div>
            <div style="font-size:0.85rem;color:#444460;line-height:2;">
                <b style="color:#a89fff;">ML Engineer</b> · <b style="color:#a89fff;">Data Scientist</b> · <b style="color:#a89fff;">Full Stack Developer</b><br>
                <b style="color:#a89fff;">Frontend Developer</b> · <b style="color:#a89fff;">DevOps Engineer</b> · <b style="color:#a89fff;">Android Developer</b><br>
                <b style="color:#a89fff;">Product Manager</b> · <b style="color:#a89fff;">UI UX Designer</b> · <b style="color:#a89fff;">QA Engineer</b>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)