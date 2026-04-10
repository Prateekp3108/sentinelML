import streamlit as st
import time
from textwrap import dedent
from modules.auth import _encode_token, get_tier, get_user, is_logged_in, logout, persist_to_query, require_auth
from modules.model_loader import load_model, format_param_count

st.set_page_config(
    page_title="SentinelML — Audit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def render_html(html: str) -> None:
    st.markdown(dedent(html), unsafe_allow_html=True)


# ── INIT SESSION STATE EARLY ──────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

require_auth()


auth_param = ""
user = st.session_state.get("user")
tier = st.session_state.get("user_tier")
if user:
    token = _encode_token({"user": user, "tier": tier})
    auth_param = f"?auth={token}"

documentation_href = f"/documentation{auth_param}" if auth_param else "/documentation"
about_href = f"/about{auth_param}" if auth_param else "/about"
login_href = f"/login{auth_param}" if auth_param else "/login"

# ── SOFT AUTH CHECK ───────────────────────────────────────────────────────
if not is_logged_in():
    render_html(f"""
    <div style="max-width:500px;margin:8rem auto;text-align:center;
    padding:2rem">
        <div style="font-family:'Geist Mono',monospace;font-size:1rem;
        font-weight:700;color:#0a0a0a;margin-bottom:1rem">SENTINEL(ML)</div>
        <div style="font-family:'Geist',sans-serif;font-size:0.9rem;
        color:#888;margin-bottom:2rem">
            Your session expired. Please sign in again.
        </div>
        <a href="{login_href}" target="_self" style="background:#0a0a0a;
        color:#F7F6F0;font-family:'Geist',sans-serif;font-size:0.875rem;
        font-weight:500;padding:0.65rem 1.5rem;border-radius:7px;
        text-decoration:none">Sign in →</a>
    </div>
    """)
    st.stop()

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #F7F6F0;
    font-family: 'Geist', sans-serif;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

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
div[data-testid="stVerticalBlockSeparator"] { display: none !important; }
div[data-testid="stHorizontalBlock"] { gap: 0.75rem !important; }

/* ── NAVBAR ── */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: rgba(247, 246, 240, 0.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.08);
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
}

.navbar-left { 
    display: flex; 
    align-items: center; 
    gap: 2.5rem; 
}

.navbar-right { 
    display: flex; 
    align-items: center; 
    gap: 1rem; 
}

.navbar-user {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.navbar-user-name {
    font-family: 'Geist', sans-serif;
    font-size: 0.825rem;
    color: #444 !important;
}

.navbar-tier {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    background: rgba(0,0,0,0.04);
}

.navbar-logo {
    font-family: 'Geist Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #0a0a0a !important;
    text-decoration: none !important;
}

.navbar-links {
    display: flex;
    align-items: center;
    gap: 1.8rem;
}

.navbar-link {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #555 !important;
    text-decoration: none !important;
    cursor: pointer;
}

.navbar-back {
    background: transparent;
    color: #0a0a0a !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.45rem 1.1rem;
    border-radius: 6px;
    text-decoration: none !important;
    border: 1px solid rgba(0,0,0,0.15);
    cursor: pointer;
}

.back-link {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #bbb !important;
    text-decoration: none !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 1.2rem;
    margin-top: 1rem;
}

.back-link:hover { color: #666 !important; }

.page-title {
    font-family: 'Geist', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #0a0a0a !important;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 0.4rem;
}

.page-subtitle {
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    color: #888 !important;
    line-height: 1.6;
    margin-bottom: 2rem;
}

.header-divider {
    width: 100%;
    height: 1px;
    background: rgba(0,0,0,0.07);
    margin-bottom: 2.5rem;
}

.step-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    color: #bbb !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.step-title {
    font-family: 'Geist', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #0a0a0a !important;
    margin-bottom: 0.25rem;
}

.step-desc {
    font-family: 'Geist', sans-serif;
    font-size: 0.825rem;
    color: #999 !important;
    margin-bottom: 0.85rem;
}

.step-divider {
    width: 100%;
    height: 1px;
    background: rgba(0,0,0,0.06);
    margin: 2rem 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(0,0,0,0.07);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 0.75rem;
}

.stat-card {
    background: #fff;
    padding: 1.1rem 1.25rem;
}

.stat-value {
    font-family: 'Geist Mono', monospace;
    font-size: 1.35rem;
    font-weight: 600;
    color: #0a0a0a !important;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.stat-label {
    font-family: 'Geist', sans-serif;
    font-size: 0.65rem;
    color: #aaa !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.layer-list {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    max-height: 220px;
    overflow-y: auto;
    margin-top: 0.6rem;
}

.layer-row {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    color: #555 !important;
    padding: 0.45rem 1.1rem;
    border-bottom: 1px solid rgba(0,0,0,0.04);
}

.layer-row:last-child { border-bottom: none; }

div[data-testid="stFileUploadDropzone"] {
    border-radius: 10px !important;
    padding: 1.5rem !important;
}

.stButton button {
    background: #0a0a0a !important;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.25rem !important;
    border-radius: 7px !important;
    border: none !important;
    width: auto !important;
    min-width: 180px !important;
    transition: opacity 0.15s !important;
}

.stButton button:hover { opacity: 0.8 !important; }

.results-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 1rem;
}

.attack-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.25rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.attack-row:last-child { border-bottom: none; }

.attack-name {
    font-family: 'Geist Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: #0a0a0a !important;
}

.attack-detail {
    font-family: 'Geist', sans-serif;
    font-size: 0.75rem;
    color: #aaa !important;
    margin-top: 0.15rem;
}

.badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    padding: 0.28rem 0.7rem;
    border-radius: 999px;
    white-space: nowrap;
}

.badge-fail { background: #fef0ef; color: #c0392b !important; }
.badge-pass { background: #f0fff4; color: #276749 !important; }
.badge-warn { background: #fffbeb; color: #b7791f !important; }

.score-block {
    background: #fafafa;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin-top: 0.75rem;
    margin-bottom: 1rem;
}

.score-num {
    font-family: 'Geist Mono', monospace;
    font-size: 4.5rem;
    font-weight: 700;
    letter-spacing: -3px;
    line-height: 1;
}

.score-sub {
    font-family: 'Geist', sans-serif;
    font-size: 0.65rem;
    color: #ccc !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

.score-lbl {
    font-family: 'Geist', sans-serif;
    font-size: 0.72rem;
    color: #aaa !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.5rem;
}

.status-line {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    color: #aaa !important;
    padding: 0.35rem 0;
}

.error-box {
    font-family: 'Geist Mono', monospace;
    font-size: 0.78rem;
    color: #c0392b !important;
    padding: 0.9rem 1.1rem;
    background: #fef0ef;
    border-radius: 8px;
    border: 1px solid #f5c6c2;
    margin-top: 0.75rem;
}

/* ── TROJAN RESULTS ── */
.trojan-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 1rem;
}

.trojan-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.trojan-verdict {
    font-family: 'Geist', sans-serif;
    font-size: 1rem;
    font-weight: 600;
}

.trojan-verdict-sub {
    font-family: 'Geist', sans-serif;
    font-size: 0.78rem;
    color: #aaa !important;
    margin-top: 0.2rem;
}

.trojan-stat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.04);
}

.trojan-stat-row:last-child { border-bottom: none; }

.trojan-stat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    color: #888 !important;
}

.trojan-stat-value {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    color: #0a0a0a !important;
    font-weight: 500;
}
</style>
""")

persist_to_query()

# ── SESSION STATE ─────────────────────────────────────────────────────────
if "model_result" not in st.session_state:
    st.session_state.model_result = None
if "attack_results" not in st.session_state:
    st.session_state.attack_results = None
if "trojan_results" not in st.session_state:
    st.session_state.trojan_results = None
if "ai_response" not in st.session_state:
    st.session_state.ai_response = None
if "ai_tier" not in st.session_state:
    st.session_state.ai_tier = None

# ── NAVBAR ────────────────────────────────────────────────────────────────
user = get_user()
tier = get_tier()
tier_colors = {"student": "#276749", "engineer": "#1a56db", "redteam": "#c0392b"}
tier_labels = {"student": "Student", "engineer": "Engineer", "redteam": "Red Team"}
tier_color  = tier_colors.get(tier, "#888")
tier_label  = tier_labels.get(tier, "")

render_html(f"""
<div class="navbar">
    <div class="navbar-left">
        <a class="navbar-logo" href="/" target="_self">SENTINEL(ML)</a>
        <div class="navbar-links">
            <a class="navbar-link" href="{documentation_href}" target="_self">Documentation</a>
            <a class="navbar-link" href="{about_href}" target="_self">About</a>
        </div>
    </div>
    <div class="navbar-right" style="display:flex;align-items:center;gap:1rem">
    <a class="navbar-github" href="https://github.com/Prateekp3108/sentinelML" target="_blank">
        <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
            <path d="M16 2.667C8.636 2.667 2.667 8.636 2.667 16c0 5.893 3.827 10.893 9.12 12.667.667.107.88-.307.88-.667v-2.253c-3.693.8-4.48-1.587-4.48-1.587-.613-1.547-1.48-1.96-1.48-1.96-1.213-.827.093-.8.093-.8 1.333.093 2.04 1.373 2.04 1.373 1.16 2.027 3.12 1.427 3.88 1.107.12-.867.467-1.453.84-1.787-2.96-.333-6.067-1.48-6.067-6.56 0-1.48.507-2.667 1.373-3.613-.133-.333-.6-1.72.133-3.52 0 0 1.12-.36 3.667 1.36 1.053-.293 2.2-.44 3.333-.44 1.133 0 2.28.147 3.333.44 2.547-1.72 3.667-1.36 3.667-1.36.733 1.8.267 3.187.133 3.52.867.947 1.373 2.133 1.373 3.613 0 5.093-3.107 6.213-6.067 6.547.48.413.92 1.227.92 2.467v3.653c0 .36.213.787.893.667C25.52 26.88 29.333 21.893 29.333 16 29.333 8.636 23.364 2.667 16 2.667Z" fill="#444"/>
        </svg>
        GitHub
    </a>
    <div class="navbar-user">
        <div class="navbar-user-name">{user.get('login', '') if user else ''}</div>
        <div class="navbar-tier" style="color:{tier_color};border:1px solid {tier_color}40">
            {tier_label}
        </div>
    </div>
</div>
</div>
""")

render_html("<div style='height:56px'></div>")

# ── SINGLE CENTERED COLUMN ────────────────────────────────────────────────
_, main, _ = st.columns([2, 6, 2])

with main:

    nav_col, _ = st.columns([1, 9])
    with nav_col:
        if st.button("<- Home", key="audit_home"):
            st.switch_page("app.py")

    # ── PAGE HEADER ───────────────────────────────────────────────────────
    render_html("""
    <div style="padding:2.5rem 0 0">
        <div class="page-title">Security Audit</div>
        <div class="page-subtitle">
            Upload your PyTorch model to test it against adversarial
            attacks and neural Trojan detection.
        </div>
        <div class="header-divider"></div>
        <div class="step-label">Step 01</div>
        <div class="step-title">Upload your model</div>
        <div class="step-desc">PyTorch .pt or .pth — saved with torch.save(model, path)</div>
    </div>
    """)

    # ── FILE UPLOADER ─────────────────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "Upload", type=["pt", "pth"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        size_mb = round(uploaded_file.size / 1024 / 1024, 1)
        st.markdown(
            f'<div class="status-line">↳ {uploaded_file.name} '
            f'<span style="color:#ccc">({size_mb} MB)</span></div>',
            unsafe_allow_html=True
        )

    if uploaded_file is not None and st.session_state.model_result is None:

        progress_container = st.empty()

        stages = [
            (0.15, "Reading file..."),
            (0.35, "Deserializing model..."),
            (0.55, "Detecting architecture..."),
            (0.75, "Counting parameters..."),
            (0.90, "Probing input size..."),
        ]

        def render_progress(pct, label):
            bar_filled = int(pct * 28)
            bar_empty  = 28 - bar_filled
            bar        = "█" * bar_filled + "░" * bar_empty
            percent    = int(pct * 100)
            progress_container.markdown(f"""
            <div style="padding:1.5rem 0 0.5rem">
                <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                color:#aaa;letter-spacing:1px;margin-bottom:0.6rem">ANALYZING MODEL</div>
                <div style="font-family:'Geist Mono',monospace;font-size:0.75rem;
                color:#0a0a0a;letter-spacing:0.5px;margin-bottom:0.5rem">
                    {bar}
                    <span style="color:#bbb;margin-left:0.75rem">{percent}%</span>
                </div>
                <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                color:#bbb">↳ {label}</div>
            </div>
            """, unsafe_allow_html=True)

        import time

        for pct, label in stages:
            render_progress(pct, label)
            time.sleep(0.3)

        render_progress(0.95, "Finalizing...")
        st.session_state.model_result   = load_model(uploaded_file)
        st.session_state.attack_results = None
        st.session_state.trojan_results = None
        st.session_state.ai_response = None
        st.session_state.ai_tier     = None

        render_progress(1.0, "Done")
        time.sleep(0.4)
        progress_container.empty()

    if uploaded_file is None:
        st.session_state.model_result   = None
        st.session_state.attack_results = None
        st.session_state.trojan_results = None
        st.session_state.ai_response = None
        st.session_state.ai_tier     = None

    # ── STEPS 2+ ──────────────────────────────────────────────────────────
    if st.session_state.model_result is not None:
        result = st.session_state.model_result

        if result["success"]:

            # ── STEP 02: MODEL OVERVIEW ───────────────────────────────────
            st.markdown(f"""
            <div class="step-divider"></div>
            <div class="step-label">Step 02</div>
            <div class="step-title">Model overview</div>
            <div class="step-desc">Detected architecture details</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{format_param_count(result["total_params"])}</div>
                    <div class="stat-label">Parameters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{result["num_layers"]}</div>
                    <div class="stat-label">Layers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{result["num_classes"] or "?"}</div>
                    <div class="stat-label">Classes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{f'{result["input_size"]}px' if result["input_size"] else "?"}</div>
                    <div class="stat-label">Input Size</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── LAYER LIST ────────────────────────────────────────────────
            layer_rows_html = ""
            for i, name in enumerate(result["layer_names"]):
                layer_rows_html += f'<div class="layer-row">{i+1:02d}. {name}</div>'

            st.markdown(f"""
            <div style="margin-top:1.25rem">
                <div class="step-label" style="margin-bottom:0.6rem">Layer Architecture</div>
                <div class="layer-list">{layer_rows_html}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── STEP 03: RUN TESTS ────────────────────────────────────────
            st.markdown("""
            <div class="step-divider"></div>
            <div class="step-label">Step 03</div>
            <div class="step-title">Run security tests</div>
            <div class="step-desc">Choose which modules to run</div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns(2)
            with b1:
                run_adv  = st.button(" Adversarial Test")
            with b2:
                run_troj = st.button(" Trojan Detection")

            # ── ADVERSARIAL ───────────────────────────────────────────────
            if run_adv:
                if result["input_size"] and result["num_classes"]:

                    atk_container = st.empty()

                    def render_attack_progress(pct, label):
                        bar_filled = int(pct * 28)
                        bar_empty  = 28 - bar_filled
                        bar        = "█" * bar_filled + "░" * bar_empty
                        percent    = int(pct * 100)
                        atk_container.markdown(f"""
                        <div style="padding:1rem 0 0.5rem">
                            <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                            color:#aaa;letter-spacing:1px;margin-bottom:0.6rem">
                                RUNNING SECURITY TESTS</div>
                            <div style="font-family:'Geist Mono',monospace;font-size:0.75rem;
                            color:#0a0a0a;letter-spacing:0.5px;margin-bottom:0.5rem">
                                {bar}
                                <span style="color:#bbb;margin-left:0.75rem">{percent}%</span>
                            </div>
                            <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                            color:#bbb">↳ {label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    from modules.adversarial import run_adversarial_tests

                    attack_stages = {
                        "Preparing test image...":    0.10,
                        "Running FGSM attack...":     0.20,
                        "FGSM complete":              0.35,
                        "FGSM failed":                0.35,
                        "Running BIM attack...":      0.45,
                        "BIM complete":               0.62,
                        "BIM failed":                 0.62,
                        "Running DeepFool attack...": 0.72,
                        "DeepFool complete":          0.88,
                        "DeepFool failed":            0.88,
                        "Scoring results...":         0.95,
                    }

                    def update_adv_status(msg):
                        pct = attack_stages.get(msg, 0.5)
                        render_attack_progress(pct, msg)

                    render_attack_progress(0.05, "Initializing...")

                    st.session_state.attack_results = run_adversarial_tests(
                        model=result["model"],
                        input_size=result["input_size"],
                        num_classes=result["num_classes"],
                        status_callback=update_adv_status
                    )

                    render_attack_progress(1.0, "All tests complete")
                    time.sleep(0.5)
                    atk_container.empty()

            # ── TROJAN DETECTION ──────────────────────────────────────────
            if run_troj:
                if result["input_size"] and result["num_classes"]:

                    troj_container = st.empty()

                    def render_trojan_progress(pct, label):
                        bar_filled = int(pct * 28)
                        bar_empty  = 28 - bar_filled
                        bar        = "█" * bar_filled + "░" * bar_empty
                        percent    = int(pct * 100)
                        troj_container.markdown(f"""
                        <div style="padding:1rem 0 0.5rem">
                            <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                            color:#aaa;letter-spacing:1px;margin-bottom:0.6rem">
                                SCANNING FOR TROJANS</div>
                            <div style="font-family:'Geist Mono',monospace;font-size:0.75rem;
                            color:#0a0a0a;letter-spacing:0.5px;margin-bottom:0.5rem">
                                {bar}
                                <span style="color:#bbb;margin-left:0.75rem">{percent}%</span>
                            </div>
                            <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                            color:#bbb">↳ {label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    from modules.trojan_detector import run_trojan_detection

                    classes_to_scan = min(result["num_classes"], 10)

                    trojan_stages = {
                        f"Scanning {classes_to_scan} classes for backdoor triggers...": 0.05,
                        f"Analysing class 1 of {classes_to_scan}...":  0.10,
                        f"Analysing class 2 of {classes_to_scan}...":  0.20,
                        f"Analysing class 3 of {classes_to_scan}...":  0.30,
                        f"Analysing class 4 of {classes_to_scan}...":  0.38,
                        f"Analysing class 5 of {classes_to_scan}...":  0.46,
                        f"Analysing class 6 of {classes_to_scan}...":  0.54,
                        f"Analysing class 7 of {classes_to_scan}...":  0.62,
                        f"Analysing class 8 of {classes_to_scan}...":  0.70,
                        f"Analysing class 9 of {classes_to_scan}...":  0.78,
                        f"Analysing class 10 of {classes_to_scan}...": 0.86,
                        "Computing anomaly index...":                   0.93,
                        "Trojan scan complete":                         1.00,
                    }

                    def update_trojan_status(msg):
                        pct = trojan_stages.get(msg, 0.5)
                        render_trojan_progress(pct, msg)

                    render_trojan_progress(0.02, "Initializing Neural Cleanse...")

                    st.session_state.trojan_results = run_trojan_detection(
                        model=result["model"],
                        input_size=result["input_size"],
                        num_classes=result["num_classes"],
                        status_callback=update_trojan_status
                    )

                    render_trojan_progress(1.0, "Scan complete")
                    time.sleep(0.5)
                    troj_container.empty()

            # ── ADVERSARIAL RESULTS ───────────────────────────────────────
            if st.session_state.attack_results is not None:
                ar          = st.session_state.attack_results
                score       = ar["robustness_score"]
                score_color = (
                    "#276749" if score >= 70
                    else "#b7791f" if score >= 40
                    else "#c0392b"
                )

                attack_meta = {
                    "fgsm":     ("FGSM",     "Fast Gradient Sign — one-step"),
                    "bim":      ("BIM",      "Basic Iterative — 10 iterations"),
                    "deepfool": ("DeepFool", "Minimum perturbation"),
                }

                rows_html = ""
                for key, (atk_name, detail) in attack_meta.items():
                    r = ar[key]
                    if "error" in r:
                        badge = '<span class="badge badge-warn">⚠ Error</span>'
                    elif r["success"]:
                        conf  = (f"{r.get('original_conf','?')}% → "
                                 f"{r.get('adversarial_conf','?')}%")
                        badge = (f'<span class="badge badge-fail">'
                                 f'✗ Fooled &nbsp;{conf}</span>')
                    else:
                        badge = '<span class="badge badge-pass">✓ Resisted</span>'

                    rows_html += (
                        f'<div class="attack-row">'
                        f'<div><div class="attack-name">{atk_name}</div>'
                        f'<div class="attack-detail">{detail}</div></div>'
                        f'{badge}</div>'
                    )

                st.markdown(f"""
                <div class="step-divider"></div>
                <div class="step-label">Adversarial Results</div>
                <div class="step-title">Attack test report</div>
                <div class="score-block">
                    <div class="score-num" style="color:{score_color}">{score}</div>
                    <div class="score-sub">out of 100</div>
                    <div class="score-lbl">Robustness Score</div>
                </div>
                <div class="results-box">{rows_html}</div>
                """, unsafe_allow_html=True)

            # ── TROJAN RESULTS ────────────────────────────────────────────
            if st.session_state.trojan_results is not None:
                tr = st.session_state.trojan_results

                if tr.get("error"):
                    st.markdown(
                        f'<div class="error-box">✗ Trojan scan error: {tr["error"]}</div>',
                        unsafe_allow_html=True)
                else:
                    detected      = tr["trojan_detected"]
                    verdict_color = "#c0392b" if detected else "#276749"
                    verdict_text  = "⚠ Trojan Detected" if detected else "✓ No Trojan Found"
                    verdict_sub   = (
                        f"Confidence: {tr['confidence']} — "
                        f"Suspected target class: {tr['suspected_target_class']}"
                        if detected else
                        "No suspicious backdoor triggers found across scanned classes"
                    )

                    # Norm bars
                    norms     = tr["trigger_norms"]
                    max_norm  = max(norms) if norms else 1
                    norm_rows = ""
                    for i, n in enumerate(norms):
                        bar_pct    = int((n / max_norm) * 100)
                        is_suspect = (detected and i == tr["suspected_target_class"])
                        bar_color  = "#c0392b" if is_suspect else "#0a0a0a"
                        norm_rows += (
                            f'<div class="trojan-stat-row">'
                            f'<div class="trojan-stat-label">'
                            f'{"⚠ " if is_suspect else ""}Class {i:02d}</div>'
                            f'<div style="flex:1;margin:0 1rem;height:4px;'
                            f'background:rgba(0,0,0,0.06);border-radius:2px">'
                            f'<div style="width:{bar_pct}%;height:100%;'
                            f'background:{bar_color};border-radius:2px"></div></div>'
                            f'<div class="trojan-stat-value">{n:.4f}</div>'
                            f'</div>'
                        )

                    st.markdown(f"""
                    <div class="step-divider"></div>
                    <div class="step-label">Trojan Results</div>
                    <div class="step-title">Backdoor scan report</div>
                    <div class="trojan-box">
                        <div class="trojan-header">
                            <div>
                                <div class="trojan-verdict"
                                style="color:{verdict_color} !important">
                                {verdict_text}</div>
                                <div class="trojan-verdict-sub">{verdict_sub}</div>
                            </div>
                            <span class="badge {'badge-fail' if detected else 'badge-pass'}">
                                Anomaly Index: {tr['anomaly_index']}
                            </span>
                        </div>
                        <div class="trojan-stat-row">
                            <div class="trojan-stat-label">Classes scanned</div>
                            <div class="trojan-stat-value">{tr['classes_scanned']}</div>
                        </div>
                        <div class="trojan-stat-row">
                            <div class="trojan-stat-label">Detection method</div>
                            <div class="trojan-stat-value">Neural Cleanse (MAD scoring)</div>
                        </div>
                        <div class="trojan-stat-row">
                            <div class="trojan-stat-label">Anomaly threshold</div>
                            <div class="trojan-stat-value">2.0</div>
                        </div>
                        <div style="padding:0.8rem 1.5rem 0.2rem">
                            <div class="step-label" style="margin-bottom:0.5rem">
                                Trigger norm per class — smaller = more suspicious
                            </div>
                            {norm_rows}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # ── DOWNLOAD REPORT ───────────────────────────────────────────
            if st.session_state.attack_results is not None or st.session_state.trojan_results is not None:
                st.markdown("""
                <div class="step-divider"></div>
                <div class="step-label">Export</div>
                <div class="step-title">Download report</div>
                <div class="step-desc">Full audit results as a PDF</div>
                """, unsafe_allow_html=True)

                from modules.report_generator import generate_report

                pdf_bytes = generate_report(
                    model_result=result,
                    attack_results=st.session_state.attack_results,
                    trojan_results=st.session_state.trojan_results
                )

                st.download_button(
                    label="⬇  Download PDF Report",
                    data=pdf_bytes,
                    file_name="sentinelml_audit_report.pdf",
                    mime="application/pdf"
                )

            # ── STEP 04: AI ANALYSIS ──────────────────────────────────────
            if st.session_state.attack_results is not None or st.session_state.trojan_results is not None:
                st.markdown("""
                <div class="step-divider"></div>
                <div class="step-label">Step 04</div>
                <div class="step-title">AI Security Analysis</div>
                <div class="step-desc">Upload your model source code for
                personalised recommendations</div>
                """, unsafe_allow_html=True)

                tier = get_tier()  # already set from login — no need to ask again

                tier_labels = {
                    "student":  "🟢 Student / Researcher",
                    "engineer": "🔵 ML Engineer",
                    "redteam":  "🔴 Red Team Analyst"
                }
                st.markdown(f"""
                <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                color:#aaa;padding:0.4rem 0">
                ↳ Analysis tier: {tier_labels.get(tier, tier)}
                </div>
                """, unsafe_allow_html=True)

                source_file = st.file_uploader(
                    "Upload model source code (.py) — optional",
                    type=["py"],
                    label_visibility="visible",
                    key="source_uploader"
                )

                if st.button(" Generate AI Analysis"):
                    from modules.ai_advisor import (
                        build_audit_summary, call_gemini, call_gemini_no_code
                    )

                    ai_container = st.empty()

                    def render_ai_progress(pct, label):
                        bar_filled = int(pct * 28)
                        bar_empty  = 28 - bar_filled
                        bar        = "█" * bar_filled + "░" * bar_empty
                        percent    = int(pct * 100)
                        ai_container.markdown(f"""
                        <div style="padding:1rem 0 0.5rem">
                            <div style="font-family:'Geist Mono',monospace;
                            font-size:0.7rem;color:#aaa;letter-spacing:1px;
                            margin-bottom:0.6rem">RUNNING AI ANALYSIS</div>
                            <div style="font-family:'Geist Mono',monospace;
                            font-size:0.75rem;color:#0a0a0a;letter-spacing:0.5px;
                            margin-bottom:0.5rem">
                                {bar}
                                <span style="color:#bbb;margin-left:0.75rem">
                                {percent}%</span>
                            </div>
                            <div style="font-family:'Geist Mono',monospace;
                            font-size:0.7rem;color:#bbb">↳ {label}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    ai_stages = {
                        "Connecting to Gemini...":       0.2,
                        "Analyzing vulnerabilities...":  0.5,
                        "Analyzing audit results...":    0.5,
                        "Generating recommendations...": 0.85,
                    }

                    def update_ai_status(msg):
                        pct = ai_stages.get(msg, 0.4)
                        render_ai_progress(pct, msg)

                    render_ai_progress(0.05, "Building audit summary...")
                    audit_summary = build_audit_summary(
                        model_result=result,
                        attack_results=st.session_state.attack_results,
                        trojan_results=st.session_state.trojan_results
                    )

                    if source_file is not None:
                        source_code = source_file.read().decode("utf-8")
                        ai_response = call_gemini(
                            audit_summary=audit_summary,
                            source_code=source_code,
                            tier=tier,
                            status_callback=update_ai_status
                        )
                    else:
                        ai_response = call_gemini_no_code(
                            audit_summary=audit_summary,
                            tier=tier,
                            status_callback=update_ai_status
                        )

                    render_ai_progress(1.0, "Analysis complete")
                    time.sleep(0.4)
                    ai_container.empty()

                    st.session_state.ai_response = ai_response
                    st.session_state.ai_tier     = tier
                    st.toast("✅ AI analysis ready!", icon="✅")

                if st.session_state.get("ai_response"):
                    tier_colors = {
                        "student":  "#276749",
                        "engineer": "#1a56db",
                        "redteam":  "#c0392b"
                    }
                    tier_labels = {
                        "student":  "Student Analysis",
                        "engineer": "Engineer Analysis",
                        "redteam":  "Red Team Analysis"
                    }
                    t     = st.session_state.get("ai_tier", "engineer")
                    color = tier_colors.get(t, "#0a0a0a")
                    label = tier_labels.get(t, "AI Analysis")

                    st.markdown(f"""
                    <div style="margin-top:1rem">
                        <div class="step-label" style="color:{color} !important;
                        margin-bottom:0.5rem">{label}</div>
                        <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);
                        border-radius:10px;padding:1.5rem;font-family:'Geist',sans-serif;
                        font-size:0.875rem;color:#444;line-height:1.7;
                        white-space:pre-wrap">{st.session_state.ai_response}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if t == "redteam" and source_file is not None:
                        st.download_button(
                            label="⬇  Download AI Analysis ",
                            data=st.session_state.ai_response,
                            file_name="model_hardened.py",
                            mime="text/plain"
                        )

        else:
            st.markdown(
                f'<div class="error-box">✗ {result["error"]}</div>',
                unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

    if st.button("Sign out", key="logout_audit"):
        logout()
        st.switch_page("pages/login.py")
    # bottom breathing room
    st.markdown("<div style='height:5rem'></div>", unsafe_allow_html=True)
