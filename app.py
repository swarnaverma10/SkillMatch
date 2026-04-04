import streamlit as st
from src.helper import extract_text_from_pdf, analyze_resume
from src.ats_scorer import score_ats
from src.job_api import fetch_jobs

st.set_page_config(page_title="SkillMatch AI", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg:      #05050d;
  --bg2:     #0b0b18;
  --bg3:     #0f0f1e;
  --border:  #17172a;
  --borda:   rgba(108,99,255,0.28);
  --acc:     #6c63ff;
  --acc2:    #ff6584;
  --acc3:    #43e97b;
  --text:    #e8e8f4;
  --muted:   #50506a;
  --muted2:  #2a2a42;
}

* { font-family:'DM Sans',sans-serif !important; box-sizing:border-box; margin:0; padding:0; }
h1,h2,h3 { font-family:'Syne',sans-serif !important; }

.stApp { background:var(--bg) !important; }
.block-container { padding:0 !important; max-width:100% !important; }
#MainMenu,footer,header { visibility:hidden !important; }
[data-testid="stToolbar"],[data-testid="stDecoration"] { display:none !important; }

/* ── SIDEBAR ALWAYS VISIBLE ── */
[data-testid="collapsedControl"] { display:none !important; }
section[data-testid="stSidebar"] {
  background:var(--bg2) !important;
  border-right:1px solid var(--border) !important;
  min-width:260px !important; max-width:260px !important;
  transform:none !important; visibility:visible !important;
}
section[data-testid="stSidebar"] > div { padding:0 !important; }
[data-testid="stSidebarNav"] { display:none !important; }

section[data-testid="stSidebar"] .stButton { margin:2px 10px !important; }
section[data-testid="stSidebar"] .stButton > button {
  background:transparent !important; border:1px solid transparent !important;
  border-radius:10px !important; color:var(--muted) !important;
  font-size:0.83rem !important; font-weight:500 !important;
  padding:10px 14px !important; text-align:left !important;
  width:100% !important; box-shadow:none !important;
  transform:none !important; transition:all 0.18s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background:rgba(108,99,255,0.10) !important; color:var(--text) !important;
  border-color:rgba(108,99,255,0.22) !important; transform:none !important; opacity:1 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
  background:rgba(108,99,255,0.14) !important;
  border-left:3px solid var(--acc) !important;
  border-color:rgba(108,99,255,0.30) !important;
  color:#c4bcff !important; font-weight:600 !important;
  border-radius:0 10px 10px 0 !important; padding-left:11px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  background:rgba(108,99,255,0.04) !important;
  border:1px dashed rgba(108,99,255,0.25) !important;
  border-radius:10px !important; padding:4px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {
  background:rgba(108,99,255,0.04) !important;
  border:1px dashed rgba(108,99,255,0.25) !important; border-radius:10px !important;
}

/* ── LANDING ── */
.lp-wrap {
  padding:68px 32px 52px; text-align:center; position:relative; overflow:hidden;
}
.lp-grid {
  position:absolute; inset:0; pointer-events:none;
  background-image:linear-gradient(rgba(108,99,255,0.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(108,99,255,0.04) 1px,transparent 1px);
  background-size:52px 52px; animation:gridDrift 22s linear infinite;
}
@keyframes gridDrift { to { background-position:52px 52px; } }
.orb1 {
  position:absolute; width:440px; height:440px; border-radius:50%;
  top:-160px; left:50%; transform:translateX(-50%);
  background:radial-gradient(circle,rgba(108,99,255,0.17) 0%,transparent 65%);
  animation:breathe 5s ease-in-out infinite; pointer-events:none;
}
.orb2 {
  position:absolute; width:260px; height:260px; border-radius:50%;
  top:30px; left:18%; pointer-events:none;
  background:radial-gradient(circle,rgba(255,101,132,0.09) 0%,transparent 65%);
  animation:breathe 7s ease-in-out infinite reverse;
}
.orb3 {
  position:absolute; width:260px; height:260px; border-radius:50%;
  top:30px; right:18%; pointer-events:none;
  background:radial-gradient(circle,rgba(67,233,123,0.08) 0%,transparent 65%);
  animation:breathe 6s ease-in-out infinite 2s;
}
@keyframes breathe { 0%,100%{transform:scale(1);opacity:.8;} 50%{transform:scale(1.12);opacity:1;} }
.lp-chip {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(108,99,255,0.10); border:1px solid rgba(108,99,255,0.28);
  border-radius:40px; padding:7px 18px; margin-bottom:28px;
  animation:fadeDown 0.6s ease both;
}
.lp-dot { width:7px; height:7px; border-radius:50%; background:var(--acc3); animation:blink 2s ease infinite; }
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}
.lp-chip-txt { font-size:0.79rem; font-weight:600; color:#a89fff; letter-spacing:.4px; }
@keyframes fadeDown { from{opacity:0;transform:translateY(-14px);} to{opacity:1;transform:translateY(0);} }
.lp-title {
  font-family:'Syne',sans-serif !important;
  font-size:3.8rem; font-weight:800; line-height:1.1; color:var(--text);
  margin-bottom:20px; animation:fadeUp 0.7s ease 0.1s both;
}
.grad { background:linear-gradient(135deg,#6c63ff 0%,#ff6584 45%,#43e97b 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.lp-sub { font-size:1.05rem; color:var(--muted); line-height:1.7; max-width:500px; margin:0 auto 44px; animation:fadeUp 0.7s ease 0.2s both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }

/* ── PAGE WRAP ── */
.page-wrap { padding:36px 52px 72px; max-width:1080px; margin:0 auto; }
.pg-title { font-family:'Syne',sans-serif !important; font-size:1.75rem; font-weight:800; color:var(--text); margin-bottom:4px; }
.pg-sub { font-size:0.85rem; color:var(--muted); margin-bottom:28px; }

/* ── CARDS ── */
.card { background:var(--bg3); border:1px solid var(--border); border-radius:16px; padding:22px; transition:border-color 0.2s; }
.feat-card {
  background:var(--bg3); border:1px solid var(--border);
  border-radius:18px; padding:30px 22px; text-align:center;
  transition:all 0.22s; position:relative; overflow:hidden;
}
.feat-card::before { content:''; position:absolute; inset:0; opacity:0;
  background:radial-gradient(circle at 50% 0%,rgba(108,99,255,0.12),transparent 65%); transition:opacity 0.3s; }
.feat-card:hover { border-color:var(--borda); transform:translateY(-5px); box-shadow:0 20px 48px rgba(108,99,255,0.13); }
.feat-card:hover::before { opacity:1; }
.feat-icon { font-size:2.4rem; margin-bottom:16px; }
.feat-title { font-family:'Syne',sans-serif !important; font-size:1rem; font-weight:700; color:var(--text); margin-bottom:8px; }
.feat-desc { font-size:0.79rem; color:var(--muted); line-height:1.6; margin-bottom:16px; }
.feat-pill { display:inline-block; padding:4px 14px; background:rgba(108,99,255,0.10); border:1px solid rgba(108,99,255,0.20); border-radius:20px; font-size:0.72rem; color:#a89fff; }

/* ── METRIC ── */
.metric { background:var(--bg3); border:1px solid var(--border); border-radius:14px; padding:20px; text-align:center; }
.metric-val { font-family:'Syne',sans-serif !important; font-size:2.2rem; font-weight:800; line-height:1; }
.metric-label { font-size:0.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:1.2px; margin-top:7px; }

/* ── BADGES ── */
.badge { display:inline-block; background:rgba(108,99,255,0.10); border:1px solid rgba(108,99,255,0.20); border-radius:20px; padding:4px 13px; font-size:0.77rem; color:#a89fff; margin:3px; }
.badge.green { background:rgba(67,233,123,0.08); border-color:rgba(67,233,123,0.22); color:var(--acc3); }
.badge.red { background:rgba(255,101,132,0.08); border-color:rgba(255,101,132,0.22); color:var(--acc2); }

/* ── SKILL SECTION ── */
.skill-sec { background:var(--bg3); border:1px solid var(--border); border-radius:13px; padding:16px 18px; margin:8px 0; }
.skill-cat { font-size:0.67rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; margin-bottom:10px; }

/* ── SCORE BAR ── */
.score-bg { height:8px; background:var(--border); border-radius:4px; margin-top:14px; }
.score-fill { height:100%; border-radius:4px; }

/* ── TIP ── */
.tip { padding:12px 16px; background:rgba(108,99,255,0.05); border-left:3px solid var(--acc); border-radius:0 8px 8px 0; font-size:0.83rem; color:#c8c8e8; margin:7px 0; line-height:1.55; }

/* ── JOB CARDS ── */
.job-card { background:var(--bg3); border:1px solid var(--border); border-radius:16px; padding:22px; margin:12px 0; transition:all 0.2s; }
.job-card:hover { border-color:var(--borda); transform:translateY(-2px); box-shadow:0 12px 36px rgba(108,99,255,0.10); }
.job-link {
  display:inline-flex; align-items:center; gap:6px;
  padding:7px 16px; border-radius:8px; font-size:0.8rem; font-weight:600;
  text-decoration:none; margin-top:10px; margin-right:6px; transition:all 0.18s;
}
.job-link.linkedin { background:rgba(10,102,194,0.15); border:1px solid rgba(10,102,194,0.35); color:#5ba4f5; }
.job-link.naukri   { background:rgba(255,101,132,0.12); border:1px solid rgba(255,101,132,0.30); color:#ff8fa3; }
.job-link.indeed   { background:rgba(67,233,123,0.10); border:1px solid rgba(67,233,123,0.28); color:var(--acc3); }
.job-link.google   { background:rgba(108,99,255,0.10); border:1px solid rgba(108,99,255,0.25); color:#a89fff; }
.job-link:hover { opacity:.8; transform:translateY(-1px); }

/* ── ST OVERRIDES ── */
.block-container .stButton > button {
  background:linear-gradient(135deg,#6c63ff,#8b5cf6) !important;
  color:#fff !important; border:none !important; border-radius:10px !important;
  font-weight:600 !important; padding:10px 22px !important; font-size:0.87rem !important;
  transition:opacity 0.2s,transform 0.15s !important;
}
.block-container .stButton > button:hover { opacity:.85 !important; transform:translateY(-1px) !important; }
.stTextInput input,.stTextArea textarea {
  background:var(--bg3) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--text) !important; font-size:0.88rem !important;
}
.stTextInput input:focus,.stTextArea textarea:focus {
  border-color:var(--acc) !important; box-shadow:0 0 0 3px rgba(108,99,255,0.12) !important;
}
[data-testid="stFileUploadDropzone"] {
  background:rgba(108,99,255,0.04) !important; border:2px dashed rgba(108,99,255,0.30) !important; border-radius:14px !important;
}
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"]      { color:var(--muted) !important; font-size:0.88rem !important; }
.stTabs [aria-selected="true"]    { color:var(--acc) !important; border-bottom-color:var(--acc) !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:#2a2a4a; border-radius:3px; }

@media(max-width:768px) {
  .lp-title { font-size:2.2rem !important; }
  .page-wrap { padding:24px 18px 48px !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Session ───────────────────────────────────────────────────────────────────
for k,v in [("resume_text",""),("resume_data",{}),("jobs",[]),("active_page","Home")]:
    if k not in st.session_state: st.session_state[k] = v

NAV = [("🏠","Home"),("📑","Resume Analyzer"),("🎯","ATS Score"),("💼","Job Matcher")]

def make_job_links(job):
    tq  = job.get('title','').replace(' ','+')
    cq  = job.get('company','').replace(' ','+')
    lq  = job.get('location','').replace(' ','+')
    src = job.get('source','').lower()
    if 'linkedin' in src:
        primary = f'<a href="https://www.linkedin.com/jobs/search/?keywords={tq}+{cq}" target="_blank" class="job-link linkedin">🔗 View on LinkedIn</a>'
    elif 'naukri' in src:
        slug = job.get('title','').lower().replace(' ','-')
        primary = f'<a href="https://www.naukri.com/{slug}-jobs" target="_blank" class="job-link naukri">🔗 View on Naukri</a>'
    else:
        primary = f'<a href="https://in.indeed.com/jobs?q={tq}&l={lq}" target="_blank" class="job-link indeed">🔗 View on Indeed</a>'
    google = f'<a href="https://www.google.com/search?q={tq}+{cq}+job" target="_blank" class="job-link google">🔍 Google Jobs</a>'
    return primary + google

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:22px 16px 18px;border-bottom:1px solid #12122a;margin-bottom:10px;">
      <div style="display:flex;align-items:center;gap:11px;">
        <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#6c63ff,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🚀</div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:#f0f0f8;">SkillMatch AI</div>
          <div style="font-size:0.67rem;color:#6c63ff;letter-spacing:.5px;margin-top:1px;">Career Intelligence</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.63rem;color:#28284a;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;padding:0 10px;margin-bottom:6px;'>Resume</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded:
        with st.spinner("Analyzing..."):
            t = extract_text_from_pdf(uploaded)
            st.session_state.resume_text = t
            st.session_state.resume_data = analyze_resume(t)

    if st.session_state.resume_text:
        w  = len(st.session_state.resume_text.split())
        sc = len(st.session_state.resume_data.get('skills',[]))
        nm = st.session_state.resume_data.get('name','')[:16]
        st.markdown(f"""
        <div style="margin:8px 8px 14px;padding:11px 13px;background:rgba(67,233,123,0.07);border:1px solid rgba(67,233,123,0.18);border-radius:11px;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#43e97b;box-shadow:0 0 6px #43e97b;"></div>
            <span style="font-size:0.74rem;font-weight:700;color:#43e97b;">Resume Active</span>
          </div>
          <div style="font-size:0.69rem;color:#3a6848;padding-left:15px;">{nm} · {w} words · {sc} skills</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin:8px 8px 14px;padding:9px 12px;background:rgba(255,101,132,0.06);border:1px dashed rgba(255,101,132,0.22);border-radius:10px;">
          <div style="font-size:0.74rem;color:#ff6584;">⬆ Drop your PDF resume above</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.63rem;color:#28284a;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;padding:0 10px;margin-bottom:4px;'>Menu</div>", unsafe_allow_html=True)

    for icon, label in NAV:
        is_active = st.session_state.active_page == label
        if st.button(f"{icon}  {label}", key=f"sb_{label}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_page = label
            st.rerun()

    st.markdown("""
    <div style="padding:16px 14px;border-top:1px solid #12122a;margin-top:20px;text-align:center;">
      <div style="font-size:0.66rem;color:#1e1e38;line-height:1.9;">
        Powered by FLAN-T5<br><span style="color:#6c63ff;">SkillMatch AI</span> · v2.0
      </div>
    </div>""", unsafe_allow_html=True)

page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    st.markdown("""
    <div class="lp-wrap">
      <div class="lp-grid"></div>
      <div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
      <div class="lp-chip">
        <div class="lp-dot"></div>
        <span class="lp-chip-txt">AI-Powered · Resume Intelligence · Live Job Links</span>
      </div>
      <div class="lp-title">Land Your Dream Job<br>with <span class="grad">Smarter Career Tools</span></div>
      <div class="lp-sub">Upload your resume once. Get instant skill analysis, ATS scoring, and matched jobs with direct apply links.</div>
    </div>""", unsafe_allow_html=True)

    col_l,col_c,col_r = st.columns([1,1.6,1])
    with col_c:
        st.markdown("""
        <div style="text-align:center;margin-bottom:14px;">
          <div style="font-size:2.6rem;margin-bottom:8px;">📄</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#f0f0f8;margin-bottom:4px;">Upload Your Resume</div>
          <div style="font-size:0.78rem;color:#50506a;">PDF only · Analyzed instantly</div>
        </div>""", unsafe_allow_html=True)
        hu = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="home_up")
        if hu:
            with st.spinner("Analyzing..."):
                t = extract_text_from_pdf(hu)
                st.session_state.resume_text = t
                st.session_state.resume_data = analyze_resume(t)
            st.success("✅ Done! Navigate using the sidebar.")

    if st.session_state.resume_text:
        d = st.session_state.resume_data
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        s1,s2,s3,s4 = st.columns(4)
        for col,val,lbl,clr in [
            (s1,str(d.get('years_experience','0')),"Years Exp.","#6c63ff"),
            (s2,str(len(d.get('skills',[]))),"Skills Found","#43e97b"),
            (s3,d.get('name','—')[:13],"Candidate","#ffb347"),
            (s4,"✅ Ready","AI Status","#ff6584"),
        ]:
            with col:
                st.markdown(f'<div class="metric"><div class="metric-val" style="color:{clr};font-size:1.3rem;">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin:56px 0 22px;">
      <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#f0f0f8;">Three Powerful Tools</div>
      <div style="font-size:0.85rem;color:#50506a;margin-top:6px;">Everything you need to win your next role</div>
    </div>""", unsafe_allow_html=True)

    fc1,fc2,fc3 = st.columns(3)
    for col,icon,title,desc,pill,pg in [
        (fc1,"📑","Resume Analyzer","AI extracts skills, experience, education & contact info automatically.","Skill Extraction","Resume Analyzer"),
        (fc2,"🎯","ATS Score","Paste any JD and get a live keyword match score with gaps & tips.","ATS Matching","ATS Score"),
        (fc3,"💼","Job Matcher","Matched jobs from LinkedIn, Naukri & Indeed with direct clickable apply links.","Live Job Links","Job Matcher"),
    ]:
        with col:
            st.markdown(f'<div class="feat-card"><div class="feat-icon">{icon}</div><div class="feat-title">{title}</div><div class="feat-desc">{desc}</div><div class="feat-pill">{pill}</div></div>', unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"feat_{pg}", use_container_width=True):
                st.session_state.active_page = pg; st.rerun()

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESUME ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resume Analyzer":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown('<div class="pg-title">📑 Resume Analyzer</div><div class="pg-sub">AI-powered skill & profile extraction</div>', unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.markdown('<div class="card" style="text-align:center;padding:64px;"><div style="font-size:3rem;margin-bottom:16px;">📄</div><div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e0e0f0;margin-bottom:8px;">No Resume Uploaded</div><div style="font-size:0.84rem;color:#50506a;">Upload your PDF from the sidebar first.</div></div>', unsafe_allow_html=True)
    else:
        data   = st.session_state.resume_data
        skills = data.get("skills",[])

        st.markdown(f"""<div class="card" style="margin-bottom:20px;display:flex;align-items:center;gap:18px;">
          <div style="width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#6c63ff,#ff6584);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">👤</div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:#f0f0f8;">{data.get('name','Candidate')}</div>
            <div style="display:flex;gap:18px;margin-top:5px;flex-wrap:wrap;">
              {"<span style='font-size:0.8rem;color:#50506a;'>📧 "+data.get('email','')+"</span>" if data.get('email') else ""}
              {"<span style='font-size:0.8rem;color:#50506a;'>📞 "+data.get('phone','')+"</span>" if data.get('phone') else ""}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        mc1,mc2,mc3 = st.columns(3)
        with mc1: st.markdown(f'<div class="metric"><div class="metric-val" style="color:#6c63ff;">{data.get("years_experience","0")}</div><div class="metric-label">Years Exp.</div></div>', unsafe_allow_html=True)
        with mc2: st.markdown(f'<div class="metric"><div class="metric-val" style="color:#43e97b;">{len(skills)}</div><div class="metric-label">Skills Found</div></div>', unsafe_allow_html=True)
        with mc3:
            edu = data.get('education','Not detected')
            st.markdown(f'<div class="metric"><div style="font-size:0.85rem;font-weight:600;color:#ffb347;margin-top:6px;line-height:1.4;">{edu[:36] if edu else "N/A"}</div><div class="metric-label" style="margin-top:8px;">Education</div></div>', unsafe_allow_html=True)

        if skills:
            st.markdown("<div style='margin:26px 0 12px;font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#f0f0f8;'>🔑 Detected Skills</div>", unsafe_allow_html=True)
            cats = {
                "💻 Programming":   (["Python","Java","JavaScript","TypeScript","C++","C#","C","Go","Rust","Ruby","PHP","Swift","Kotlin","R","Scala","MATLAB"],"#6c63ff"),
                "🌐 Web & Mobile":  (["React","Angular","Vue","Node.js","Django","Flask","FastAPI","HTML","CSS","Next.js","Express","Android","iOS","Spring"],"#43e97b"),
                "🤖 AI & Data":     (["Machine Learning","Deep Learning","NLP","TensorFlow","PyTorch","Pandas","NumPy","Data Analysis","Data Science","Computer Vision","Scikit-learn","Keras","BERT","LLM","Hugging Face","OpenCV"],"#ff6584"),
                "☁️ Cloud & DevOps":(["AWS","Azure","GCP","Docker","Kubernetes","CI/CD","Git","GitHub","Linux","Jenkins","Terraform","Ansible"],"#ffb347"),
                "🗄️ Databases":     (["SQL","MySQL","PostgreSQL","MongoDB","Redis","Firebase","Oracle","SQLite","Elasticsearch","DynamoDB","Cassandra"],"#00d4aa"),
                "🛠️ Tools":         (["Agile","Scrum","Jira","Figma","Spark","Kafka","Power BI","Tableau","Excel","Postman","Selenium","Unity"],"#a78bfa"),
            }
            skill_set = set(s.lower() for s in skills)
            categorized = set()
            for cat_name,(cat_skills,clr) in cats.items():
                matched = [s for s in cat_skills if s.lower() in skill_set]
                if matched:
                    categorized.update(s.lower() for s in matched)
                    badges = "".join([f'<span class="badge">{s}</span>' for s in matched])
                    st.markdown(f'<div class="skill-sec"><div class="skill-cat" style="color:{clr};">{cat_name}</div><div>{badges}</div></div>', unsafe_allow_html=True)
            others = [s for s in skills if s.lower() not in categorized]
            if others:
                badges = "".join([f'<span class="badge">{s}</span>' for s in others])
                st.markdown(f'<div class="skill-sec"><div class="skill-cat" style="color:#888;">🔖 Other</div><div>{badges}</div></div>', unsafe_allow_html=True)

        with st.expander("📄 Raw Resume Text"):
            st.text_area("", st.session_state.resume_text[:3000], height=200, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ATS SCORE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ATS Score":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown('<div class="pg-title">🎯 ATS Score Checker</div><div class="pg-sub">Paste any job description to see your keyword match score</div>', unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.markdown('<div class="card" style="text-align:center;padding:64px;"><div style="font-size:3rem;margin-bottom:16px;">📄</div><div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e0e0f0;margin-bottom:8px;">No Resume Uploaded</div><div style="font-size:0.84rem;color:#50506a;">Upload your PDF from the sidebar first.</div></div>', unsafe_allow_html=True)
    else:
        jd = st.text_area("📋 Paste Job Description", height=220, placeholder="Paste the full job description — responsibilities, requirements, skills...")
        if st.button("🔍 Check My ATS Score", use_container_width=True) and jd.strip():
            result = score_ats(st.session_state.resume_text, jd)
            score  = result["score"]
            clr    = "#43e97b" if score>=70 else "#ffb347" if score>=50 else "#ff6584"
            lbl    = "Excellent ✅" if score>=70 else "Needs Work ⚠️" if score>=50 else "Low Match ❌"
            msg    = ("Great — well-optimized!" if score>=70 else "Add more keywords." if score>=50 else "Major gaps. Tailor your resume.")

            c1,c2 = st.columns([1,1.8])
            with c1:
                st.markdown(f"""<div class="card" style="text-align:center;padding:38px 20px;">
                  <div style="font-size:0.62rem;color:#2a2a42;text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;">ATS Match Score</div>
                  <div style="font-family:'Syne',sans-serif;font-size:5.5rem;font-weight:800;color:{clr};line-height:1;">{score}%</div>
                  <div style="font-size:0.88rem;color:{clr};margin-top:10px;font-weight:600;">{lbl}</div>
                  <div class="score-bg"><div class="score-fill" style="width:{score}%;background:{clr};"></div></div>
                  <div style="font-size:0.77rem;color:#50506a;margin-top:14px;line-height:1.55;">{msg}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                matched = result.get("matched",[])
                missing = result.get("missing",[])
                mb = "".join([f'<span class="badge green">{k}</span>' for k in matched])
                xb = "".join([f'<span class="badge red">{k}</span>' for k in missing])
                st.markdown(f"""<div class="card" style="height:100%;">
                  <div style="margin-bottom:18px;">
                    <div style="font-size:0.68rem;color:#43e97b;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">✅ Matched ({len(matched)})</div>
                    <div>{mb or "<span style='color:#2a2a42;font-size:0.82rem;'>None yet</span>"}</div>
                  </div>
                  <div style="border-top:1px solid #17172a;padding-top:16px;">
                    <div style="font-size:0.68rem;color:#ff6584;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">❌ Missing ({len(missing)})</div>
                    <div>{xb or "<span style='color:#43e97b;font-size:0.82rem;'>Perfect match!</span>"}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            tips = result.get("tips",[])
            if tips:
                st.markdown("<div style='margin:22px 0 10px;font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#f0f0f8;'>💡 How to Improve</div>", unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<div class="tip">→ {tip}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# JOB MATCHER — clickable links
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Job Matcher":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown('<div class="pg-title">💼 Job Matcher</div><div class="pg-sub">AI-matched jobs with direct links to LinkedIn, Naukri & Indeed</div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1: role = st.text_input("🔍 Target Role", placeholder="e.g. Data Scientist, ML Engineer, Full Stack Dev")
    with c2: loc  = st.text_input("📍 Location", placeholder="e.g. Bangalore, Remote, Mumbai")

    if st.button("🔍 Find Matching Jobs", use_container_width=True) and role.strip():
        with st.spinner("Finding best matches..."):
            st.session_state.jobs = fetch_jobs(role, loc, st.session_state.resume_text)

    if st.session_state.jobs:
        jobs = st.session_state.jobs
        best = jobs[0]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:20px;padding:14px 20px;background:var(--bg3);border:1px solid var(--border);border-radius:12px;margin-bottom:20px;flex-wrap:wrap;">
          <div><div style="font-size:0.64rem;color:#50506a;text-transform:uppercase;letter-spacing:1px;">Results</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#f0f0f8;margin-top:2px;">{len(jobs)} jobs · "{role}"</div></div>
          <div style="width:1px;height:32px;background:var(--border);"></div>
          <div><div style="font-size:0.64rem;color:#50506a;text-transform:uppercase;letter-spacing:1px;">Best Match</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#43e97b;margin-top:2px;">{best['match_score']}% — {best['company']}</div></div>
          <div style="margin-left:auto;font-size:0.77rem;color:#50506a;">Click links below each job to apply →</div>
        </div>""", unsafe_allow_html=True)

        for job in jobs:
            score   = job.get("match_score",0)
            clr     = "#43e97b" if score>=80 else "#ffb347" if score>=65 else "#ff6584"
            src     = job.get("source","")
            src_clr = "#5ba4f5" if "linkedin" in src.lower() else "#ff8fa3" if "naukri" in src.lower() else "#43e97b"
            badges  = "".join([f'<span class="badge">{s}</span>' for s in job.get("required_skills",[])])
            links   = make_job_links(job)

            st.markdown(f"""<div class="job-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">
                <div style="flex:1;min-width:0;">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap;">
                    <span style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:#f0f0f8;">{job.get('title','')}</span>
                    <span style="font-size:0.7rem;padding:3px 10px;border-radius:20px;color:{src_clr};background:rgba(108,99,255,0.06);border:1px solid rgba(108,99,255,0.14);">{src}</span>
                    <span style="font-size:0.7rem;color:#2a2a42;">🕐 {job.get('posted','')}</span>
                  </div>
                  <div style="font-size:0.83rem;color:#50506a;display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;">
                    <span>🏢 <b style="color:#c0c0d8;">{job.get('company','')}</b></span>
                    <span>📍 {job.get('location','')}</span>
                    <span>💰 <b style="color:#43e97b;">{job.get('salary_range','')}</b></span>
                  </div>
                  <div style="font-size:0.82rem;color:#50506a;line-height:1.65;margin-bottom:14px;">{job.get('description','')[:240]}</div>
                  <div style="margin-bottom:10px;">{badges}</div>
                  <div>{links}</div>
                </div>
                <div style="flex-shrink:0;text-align:center;min-width:80px;background:rgba(108,99,255,0.05);border:1px solid rgba(108,99,255,0.12);border-radius:12px;padding:16px 12px;">
                  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:{clr};line-height:1;">{score}%</div>
                  <div style="font-size:0.62rem;color:#2a2a42;text-transform:uppercase;letter-spacing:.5px;margin-top:4px;">Match</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    elif not st.session_state.jobs:
        st.markdown("""<div class="card" style="text-align:center;padding:64px;">
          <div style="font-size:3rem;margin-bottom:16px;">🔍</div>
          <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#e0e0f0;margin-bottom:10px;">Ready to Search</div>
          <div style="font-size:0.84rem;color:#50506a;">Try: <b style="color:#a89fff;">Data Scientist</b> &nbsp;·&nbsp; <b style="color:#a89fff;">Full Stack Dev</b> &nbsp;·&nbsp; <b style="color:#a89fff;">ML Engineer</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)