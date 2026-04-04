import streamlit as st
import plotly.graph_objects as go
import random

MARKET_DEMAND = {
    "Python": 95, "Machine Learning": 92, "SQL": 88, "AWS": 85,
    "React": 83, "Docker": 80, "Kubernetes": 78, "TensorFlow": 75,
    "Data Analysis": 82, "NLP": 70, "Java": 72, "Node.js": 74,
    "TypeScript": 79, "Go": 65, "Deep Learning": 77, "Spark": 68,
    "Power BI": 71, "Tableau": 69, "Leadership": 90, "Communication": 88,
    "Project Management": 84, "Agile": 82, "FastAPI": 68, "Django": 65,
    "Flask": 64, "MongoDB": 70, "PostgreSQL": 75, "Excel": 66,
}

SKILL_CATEGORIES = {
    "AI/ML": ["Machine Learning", "Deep Learning", "TensorFlow", "NLP", "Computer Vision"],
    "Cloud": ["AWS", "Docker", "Kubernetes"],
    "Data": ["SQL", "Data Analysis", "Power BI", "Tableau", "Spark", "PostgreSQL", "MongoDB"],
    "Programming": ["Python", "Java", "Node.js", "TypeScript", "Go", "Flask", "FastAPI", "Django"],
    "Frontend": ["React", "TypeScript"],
    "Soft Skills": ["Leadership", "Communication", "Project Management", "Agile"]
}


def render_skill_dashboard(resume_data: dict):
    skills = resume_data.get("skills", [])
    if not skills:
        st.warning("No skills extracted. Please re-run Resume Analyzer.")
        return

    tab1, tab2, tab3 = st.tabs(["🕸️ Skill Radar", "📊 Market Demand", "🗂️ Categories"])

    with tab1:
        top_skills = skills[:8]
        your_scores = [random.randint(65, 95) for _ in top_skills]
        market_scores = [MARKET_DEMAND.get(s, random.randint(50, 85)) for s in top_skills]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=your_scores + [your_scores[0]], theta=top_skills + [top_skills[0]],
            fill='toself', name='Your Level',
            line_color='#6c63ff', fillcolor='rgba(108,99,255,0.2)'
        ))
        fig.add_trace(go.Scatterpolar(
            r=market_scores + [market_scores[0]], theta=top_skills + [top_skills[0]],
            fill='toself', name='Market Demand',
            line_color='#43e97b', fillcolor='rgba(67,233,123,0.1)'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.08)', tickfont=dict(color='#8888aa')),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.08)', tickfont=dict(color='#c0c0d8'))
            ),
            showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c0c0d8', family='Space Grotesk'), height=420,
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        pairs = sorted([(s, MARKET_DEMAND.get(s, random.randint(50, 80))) for s in skills], key=lambda x: x[1], reverse=True)
        names = [p[0] for p in pairs]
        vals  = [p[1] for p in pairs]
        bar_colors = ['#43e97b' if v >= 80 else '#ffb347' if v >= 60 else '#ff6584' for v in vals]

        fig2 = go.Figure(go.Bar(
            x=vals, y=names, orientation='h',
            marker_color=bar_colors,
            text=[f"{v}%" for v in vals], textposition='outside',
            textfont=dict(color='#c0c0d8', size=11)
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,17,24,0.8)',
            font=dict(color='#c0c0d8', family='Space Grotesk'),
            xaxis=dict(range=[0, 110], gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#8888aa')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#c0c0d8')),
            height=max(300, len(skills) * 35), margin=dict(l=10, r=60, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div style='font-size:0.8rem; color:#8888aa'>
            <span style='color:#43e97b'>●</span> High (80+) &nbsp;
            <span style='color:#ffb347'>●</span> Medium (60-79) &nbsp;
            <span style='color:#ff6584'>●</span> Lower (&lt;60)
        </div>""", unsafe_allow_html=True)

    with tab3:
        your_set = set(s.lower() for s in skills)
        cat_counts = {}
        for cat, cat_skills in SKILL_CATEGORIES.items():
            matched = [s for s in cat_skills if s.lower() in your_set]
            if matched:
                cat_counts[cat] = (len(matched), matched)

        categorized = set(s.lower() for cs in SKILL_CATEGORIES.values() for s in cs)
        others = [s for s in skills if s.lower() not in categorized]
        if others:
            cat_counts["Other"] = (len(others), others)

        cat_colors = ['#6c63ff', '#43e97b', '#ff6584', '#ffb347', '#00d4aa', '#a78bfa', '#f472b6']
        col1, col2 = st.columns([1, 1])

        with col1:
            fig3 = go.Figure(go.Pie(
                labels=list(cat_counts.keys()),
                values=[v[0] for v in cat_counts.values()],
                hole=0.55,
                marker_colors=cat_colors[:len(cat_counts)],
                textinfo='label+percent',
                textfont=dict(color='white', size=11)
            ))
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#c0c0d8', family='Space Grotesk'),
                showlegend=False, height=300, margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            for i, (cat, (count, matched)) in enumerate(cat_counts.items()):
                color = cat_colors[i % len(cat_colors)]
                badges = "".join([f"<span class='skill-badge'>{s}</span>" for s in matched])
                st.markdown(f"""
                <div style='margin-bottom:14px'>
                    <div style='display:flex; align-items:center; gap:8px; margin-bottom:4px'>
                        <span style='color:{color}'>●</span>
                        <span style='font-weight:600; font-size:0.9rem'>{cat}</span>
                        <span style='color:#8888aa; font-size:0.8rem'>({count})</span>
                    </div>
                    <div>{badges}</div>
                </div>""", unsafe_allow_html=True)