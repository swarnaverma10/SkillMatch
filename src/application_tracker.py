import streamlit as st
from datetime import datetime

STATUSES = ["🔖 Saved", "📤 Applied", "📞 Screening", "🎤 Interview", "🏆 Offer", "❌ Rejected"]
STATUS_COLORS = {
    "🔖 Saved": "#8888aa",
    "📤 Applied": "#6c63ff",
    "📞 Screening": "#ffb347",
    "🎤 Interview": "#43e97b",
    "🏆 Offer": "#00d4aa",
    "❌ Rejected": "#ff6584"
}


def render_tracker():
    with st.expander("➕ Add New Application", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_company = st.text_input("Company", placeholder="e.g. Google", key="new_company")
            new_role = st.text_input("Role", placeholder="e.g. SWE II", key="new_role")
        with col2:
            new_location = st.text_input("Location", placeholder="e.g. Bangalore", key="new_loc")
            new_salary = st.text_input("Expected Salary", placeholder="e.g. 25 LPA", key="new_sal")
        with col3:
            new_status = st.selectbox("Status", STATUSES, key="new_status")
            new_notes = st.text_area("Notes", placeholder="Referral? JD link?", height=80, key="new_notes")

        if st.button("➕ Add Application") and new_company and new_role:
            st.session_state.applications.append({
                "id": len(st.session_state.applications),
                "company": new_company,
                "role": new_role,
                "location": new_location,
                "salary": new_salary,
                "status": new_status,
                "notes": new_notes,
                "date": datetime.now().strftime("%b %d, %Y")
            })
            st.success(f"✅ Added {new_role} at {new_company}!")
            st.rerun()

    if not st.session_state.applications:
        st.markdown("""
        <div style='text-align:center; padding:60px; color:#8888aa'>
            <div style='font-size:3rem'>📋</div>
            <div style='margin-top:12px'>No applications yet. Add your first one above!</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Stats
    total = len(st.session_state.applications)
    offers = sum(1 for a in st.session_state.applications if "Offer" in a["status"])
    interviews = sum(1 for a in st.session_state.applications if "Interview" in a["status"])
    applied = sum(1 for a in st.session_state.applications if "Applied" in a["status"])

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, color in [
        (c1, "Total", total, "#6c63ff"),
        (c2, "Applied", applied, "#6c63ff"),
        (c3, "Interviews", interviews, "#43e97b"),
        (c4, "Offers 🎉", offers, "#00d4aa")
    ]:
        with col:
            st.markdown(f"""<div class='metric-box'>
                <div class='metric-value' style='color:{color}'>{value}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Kanban board
    board_statuses = ["📤 Applied", "📞 Screening", "🎤 Interview", "🏆 Offer"]
    cols = st.columns(4)
    for col, status in zip(cols, board_statuses):
        with col:
            color = STATUS_COLORS.get(status, "#8888aa")
            apps_in_col = [a for a in st.session_state.applications if a["status"] == status]
            st.markdown(f"""
            <div style='font-weight:600; font-size:0.85rem; color:{color};
                        border-bottom:2px solid {color}; padding-bottom:8px; margin-bottom:12px'>
                {status} ({len(apps_in_col)})
            </div>""", unsafe_allow_html=True)

            for app in apps_in_col:
                st.markdown(f"""
                <div class='feature-card' style='padding:14px'>
                    <div style='font-weight:600; font-size:0.9rem'>{app["company"]}</div>
                    <div style='color:#8888aa; font-size:0.78rem'>{app["role"]}</div>
                    {f'<div style="color:#8888aa;font-size:0.75rem">📍 {app["location"]}</div>' if app.get("location") else ""}
                    {f'<div style="color:#43e97b;font-size:0.75rem">💰 {app["salary"]}</div>' if app.get("salary") else ""}
                    <div style='color:#555570; font-size:0.72rem; margin-top:6px'>📅 {app["date"]}</div>
                </div>""", unsafe_allow_html=True)

    # Table view
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 View All Applications"):
        for i, app in enumerate(st.session_state.applications):
            c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])
            with c1: st.write(f"**{app['company']}**")
            with c2: st.write(app['role'])
            with c3:
                color = STATUS_COLORS.get(app['status'], '#8888aa')
                st.markdown(f"<span style='color:{color}'>{app['status']}</span>", unsafe_allow_html=True)
            with c4:
                new_s = st.selectbox("", STATUSES, index=STATUSES.index(app['status']),
                    key=f"status_{i}", label_visibility="collapsed")
                if new_s != app['status']:
                    st.session_state.applications[i]['status'] = new_s
                    st.rerun()
            with c5:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.applications.pop(i)
                    st.rerun()