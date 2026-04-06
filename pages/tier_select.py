import streamlit as st
from modules.auth import is_logged_in, get_user, has_selected_tier

st.set_page_config(
    page_title="SentinelML — Choose your tier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Guard ─────────────────────────────────────────────────────────────────
if not is_logged_in():
    st.switch_page("pages/login.py")

if has_selected_tier():
    st.switch_page("app.py")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }
.stApp { background: #F7F6F0; font-family: 'Geist', sans-serif; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] { display: none; }
.stDeployButton { display: none; }
.stMarkdown { margin: 0 !important; padding: 0 !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
[data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }

.tier-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 1.5rem;
    cursor: pointer;
    transition: border-color 0.15s, box-shadow 0.15s;
    margin-bottom: 0.75rem;
}

.tier-card:hover {
    border-color: rgba(0,0,0,0.2);
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.tier-card-selected {
    border-color: #0a0a0a !important;
    box-shadow: 0 0 0 1px #0a0a0a !important;
}

.stButton button {
    background: #0a0a0a !important;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 1.5rem !important;
    border-radius: 7px !important;
    border: none !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────
if "selected_tier_temp" not in st.session_state:
    st.session_state.selected_tier_temp = None

user  = get_user()
login = user.get("login", "there") if user else "there"

# ── PAGE ──────────────────────────────────────────────────────────────────
_, col, _ = st.columns([2, 4, 2])

with col:
    st.markdown(f"""
    <div style="padding:5rem 0 2rem">
        <div style="font-family:'Geist Mono',monospace;font-size:0.65rem;
        color:#bbb;letter-spacing:2.5px;text-transform:uppercase;
        margin-bottom:0.75rem">One-time setup</div>

        <div style="font-family:'Geist',sans-serif;font-size:1.8rem;
        font-weight:700;color:#0a0a0a;letter-spacing:-1px;
        line-height:1.15;margin-bottom:0.5rem">
            Hey {login}, how do you identify?
        </div>

        <div style="font-family:'Geist',sans-serif;font-size:0.9rem;
        color:#888;line-height:1.6;margin-bottom:2.5rem">
            This sets the depth of your AI security analysis.
            You won't be asked again.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TIER CARDS ────────────────────────────────────────────────────────
    tiers = [
        {
            "id":    "student",
            "label": "Student / Researcher",
            "color": "#276749",
            "bg":    "#f0fff4",
            "border":"#c6f6d5",
            "desc":  "Plain English explanations, real-world impact, and beginner-friendly suggestions. No jargon.",
            "gets":  ["Vulnerability explanation in simple terms", "Real-world risk examples", "3 actionable beginner fixes"]
        },
        {
            "id":    "engineer",
            "label": "ML Engineer",
            "color": "#1a56db",
            "bg":    "#ebf4ff",
            "border":"#bee3f8",
            "desc":  "Technical breakdown with exact code changes, defense strategies, and priority-ordered fixes.",
            "gets":  ["Per-attack technical analysis", "Before/after code snippets", "Defense parameters and architecture advice"]
        },
        {
            "id":    "redteam",
            "label": "Red Team Analyst",
            "color": "#c0392b",
            "bg":    "#fef0ef",
            "border":"#f5c6c2",
            "desc":  "Full threat model, complete rewritten source code with security fixes, and CVE-style findings.",
            "gets":  ["Full threat model for deployment", "Complete hardened source code", "CVE-style vulnerability report"]
        },
    ]

    for tier in tiers:
        is_selected = st.session_state.selected_tier_temp == tier["id"]
        selected_style = (
            f"border:1.5px solid {tier['color']};"
            f"box-shadow:0 0 0 1px {tier['color']};"
            if is_selected else ""
        )

        gets_html = "".join([
            f'<div style="font-family:\'Geist\',sans-serif;font-size:0.78rem;'
            f'color:#666;padding:0.2rem 0;display:flex;gap:0.5rem">'
            f'<span style="color:{tier["color"]}">✓</span>{g}</div>'
            for g in tier["gets"]
        ])

        st.markdown(f"""
        <div class="tier-card" style="{selected_style}">
            <div style="display:flex;align-items:center;
            justify-content:space-between;margin-bottom:0.5rem">
                <div style="display:flex;align-items:center;gap:0.6rem">
                    <div style="width:8px;height:8px;border-radius:50%;
                    background:{tier['color']}"></div>
                    <div style="font-family:'Geist',sans-serif;font-size:0.95rem;
                    font-weight:600;color:#0a0a0a">{tier['label']}</div>
                </div>
                {"<div style='width:16px;height:16px;border-radius:50%;background:#0a0a0a;display:flex;align-items:center;justify-content:center'><div style='width:6px;height:6px;border-radius:50%;background:#fff'></div></div>" if is_selected else "<div style='width:16px;height:16px;border-radius:50%;border:1.5px solid #ddd'></div>"}
            </div>
            <div style="font-family:'Geist',sans-serif;font-size:0.825rem;
            color:#888;line-height:1.5;margin-bottom:0.75rem">
            {tier['desc']}</div>
            <div style="background:{tier['bg']};border:1px solid {tier['border']};
            border-radius:8px;padding:0.75rem 1rem">
                {gets_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            f"Select {tier['label']}",
            key=f"tier_{tier['id']}",
            use_container_width=True
        ):
            st.session_state.selected_tier_temp = tier["id"]
            st.rerun()

    # ── CONFIRM BUTTON ────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    if st.session_state.selected_tier_temp:
        if st.button("Continue →", key="confirm_tier", use_container_width=True):
            st.session_state.user_tier = st.session_state.selected_tier_temp
            st.session_state.pop("selected_tier_temp", None)
            st.switch_page("app.py")
    else:
        st.markdown("""
        <div style="font-family:'Geist Mono',monospace;font-size:0.72rem;
        color:#bbb;text-align:center;padding:0.75rem 0">
        Select a tier above to continue
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:4rem'></div>", unsafe_allow_html=True)