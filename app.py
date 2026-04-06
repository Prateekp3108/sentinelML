import streamlit as st
import streamlit.components.v1 as components
from modules.auth import _encode_token, get_tier, get_user, is_logged_in, logout, persist_to_query, require_auth
from modules.model_loader import load_model, format_param_count

st.set_page_config(
    page_title="SentinelML",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

auth_param = ""
user = st.session_state.get("user")
tier = st.session_state.get("user_tier")
if user:
    token = _encode_token({"user": user, "tier": tier})
    auth_param = f"?auth={token}"

home_href = f"/{auth_param}" if auth_param else "/"
documentation_href = f"/documentation{auth_param}" if auth_param else "/documentation"
about_href = f"/about{auth_param}" if auth_param else "/about"
audit_href = f"/audit{auth_param}" if auth_param else "/audit"

# ── INIT SESSION STATE EARLY ──────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

require_auth()
persist_to_query()

# ── AUTH GUARD ────────────────────────────────────────────────────────────
if not is_logged_in():
    st.switch_page("pages/login.py")
    st.stop()

# ── SESSION STATE ─────────────────────────────────────────────────────────
if "model_result" not in st.session_state:
    st.session_state.model_result = None
if "attack_results" not in st.session_state:
    st.session_state.attack_results = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp { background: #F7F6F0; font-family: 'Geist', sans-serif; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: rgba(247, 246, 240, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.08);
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2.5rem;
}

.navbar-left { display: flex; align-items: center; gap: 2.5rem; }

.navbar-logo {
    font-family: 'Geist Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #0a0a0a !important;
    text-decoration: none !important;
    letter-spacing: -0.5px;
}

.navbar-links { display: flex; align-items: center; gap: 1.8rem; }

.navbar-link {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #555 !important;
    text-decoration: none !important;
    cursor: pointer;
}

.navbar-right { display: flex; align-items: center; gap: 1rem; }

.navbar-github {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #444 !important;
    text-decoration: none !important;
}

.navbar-cta {
    background: #0a0a0a;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.45rem 1.1rem;
    border-radius: 6px;
    text-decoration: none !important;
    cursor: pointer;
    transition: opacity 0.15s;
}

a.navbar-cta, a.navbar-cta:visited, a.navbar-cta:hover {
    color: #F7F6F0 !important;
    text-decoration: none !important;
}

.navbar-cta:hover { opacity: 0.85; }
a.navbar-link, a.navbar-github { color: inherit !important; text-decoration: none !important; }

.hero-section {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 8rem 2rem 4rem;
    background: #F7F6F0;
}

.hero-eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-eyebrow::before, .hero-eyebrow::after {
    content: ''; width: 24px; height: 1px; background: #bbb;
}

.hero-title {
    font-family: 'Geist', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 700;
    color: #0a0a0a;
    line-height: 1.05;
    letter-spacing: -3px;
    margin-bottom: 1.5rem;
    max-width: 900px;
}

.hero-title span { color: #888; }

.hero-description {
    font-family: 'Geist', sans-serif;
    font-size: 1.125rem;
    color: #555;
    line-height: 1.6;
    max-width: 560px;
    margin-bottom: 2.5rem;
}

.hero-buttons {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 4rem;
}

.btn-primary {
    background: #0a0a0a;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.65rem 1.5rem;
    border-radius: 7px;
    text-decoration: none !important;
    border: 1px solid #0a0a0a;
    display: inline-block;
}

.btn-secondary {
    background: transparent;
    color: #0a0a0a !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    padding: 0.65rem 1.5rem;
    border-radius: 7px;
    text-decoration: none !important;
    border: 1px solid rgba(0,0,0,0.15);
    display: inline-block;
}

.section-divider { width: 100%; height: 1px; background: rgba(0,0,0,0.08); margin: 0; }

.features-section { background: #F7F6F0; padding: 6rem 2.5rem; }

.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2px;
    max-width: 1100px;
    margin: 3rem auto 0;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(0,0,0,0.08);
}

.feature-card { background: #F7F6F0; padding: 2rem; }
.feature-icon { font-size: 1.4rem; margin-bottom: 1rem; }

.feature-title {
    font-family: 'Geist', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.5rem;
}

.feature-desc {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #666;
    line-height: 1.6;
}

.section-header { text-align: center; max-width: 1100px; margin: 0 auto; }

.section-eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #888 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.section-title {
    font-family: 'Geist', sans-serif;
    font-size: clamp(1.8rem, 3vw, 2.5rem);
    font-weight: 700;
    color: #0a0a0a !important;
    letter-spacing: -1.5px;
    line-height: 1.1;
}

.footer {
    background: #0a0a0a;
    color: #666;
    padding: 3rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.footer-logo { font-family: 'Geist Mono', monospace; font-size: 0.9rem; color: #F7F6F0; font-weight: 700; }
.footer-copy { font-family: 'Geist', sans-serif; font-size: 0.8rem; color: #555; }

.stButton button {
    background: #0a0a0a !important;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.5rem !important;
    border-radius: 7px !important;
    border: none !important;
    transition: opacity 0.15s !important;
}

.stButton button:hover { opacity: 0.8 !important; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── USER INFO FOR NAVBAR ──────────────────────────────────────────────────
user = get_user()
tier = get_tier()

tier_colors = {"student": "#276749", "engineer": "#1a56db", "redteam": "#c0392b"}
tier_labels = {"student": "Student", "engineer": "Engineer", "redteam": "Red Team"}
tier_color  = tier_colors.get(tier, "#888")
tier_label  = tier_labels.get(tier, "")
avatar      = user.get("avatar_url", "") if user else ""
login_name  = user.get("login", "") if user else ""

# ── NAVBAR ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <a class="navbar-logo" href="{home_href}" target="_self">SENTINEL(ML)</a>
        <div class="navbar-links">
            <a class="navbar-link" href="{documentation_href}" target="_self">Documentation</a>
            <a class="navbar-link" href="{about_href}" target="_self">About</a>
        </div>
    </div>
    <div class="navbar-right">
        <a class="navbar-github" href="https://github.com/Prateekp3108/sentinelML" target="_blank">
            <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
                <path d="M16 2.667C8.636 2.667 2.667 8.636 2.667 16c0 5.893 3.827 10.893 9.12 12.667.667.107.88-.307.88-.667v-2.253c-3.693.8-4.48-1.587-4.48-1.587-.613-1.547-1.48-1.96-1.48-1.96-1.213-.827.093-.8.093-.8 1.333.093 2.04 1.373 2.04 1.373 1.16 2.027 3.12 1.427 3.88 1.107.12-.867.467-1.453.84-1.787-2.96-.333-6.067-1.48-6.067-6.56 0-1.48.507-2.667 1.373-3.613-.133-.333-.6-1.72.133-3.52 0 0 1.12-.36 3.667 1.36 1.053-.293 2.2-.44 3.333-.44 1.133 0 2.28.147 3.333.44 2.547-1.72 3.667-1.36 3.667-1.36.733 1.8.267 3.187.133 3.52.867.947 1.373 2.133 1.373 3.613 0 5.093-3.107 6.213-6.067 6.547.48.413.92 1.227.92 2.467v3.653c0 .36.213.787.893.667C25.52 26.88 29.333 21.893 29.333 16 29.333 8.636 23.364 2.667 16 2.667Z" fill="#444"/>
            </svg>
            GitHub
        </a>
        <img src="{avatar}" width="26" height="26"
             style="border-radius:50%;border:1px solid rgba(0,0,0,0.1)"/>
        <span style="font-family:'Geist',sans-serif;font-size:0.825rem;color:#444">
            {login_name}</span>
        <span style="font-family:'Geist Mono',monospace;font-size:0.65rem;
        color:{tier_color};background:rgba(0,0,0,0.04);padding:0.2rem 0.6rem;
        border-radius:999px;border:1px solid {tier_color}30">{tier_label}</span>
        <a class="navbar-cta" href="{audit_href}" target="_self">Run Audit →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-eyebrow">ML Security Auditor</div>
    <h1 class="hero-title">
        Audit your models.<br><span>Before attackers do.</span>
    </h1>
    <p class="hero-description">
        SentinelML automatically tests your PyTorch models against
        adversarial attacks and neural Trojan detection — giving you
        a full security report.
    </p>
    <div class="hero-buttons">
        <a class="btn-primary" href="{audit_href}" target="_self">Start Audit →</a>
        <a class="btn-secondary" href="{documentation_href}" target="_self">Read the docs →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── VISUALIZATION ─────────────────────────────────────────────────────────
components.html("""
<div style="display:flex;justify-content:center;padding:0 2rem 3rem;background:#F7F6F0;font-family:'Geist Mono',monospace">
<div style="width:100%;max-width:800px;background:#fff;border:1px solid rgba(0,0,0,0.08);border-radius:12px;padding:2rem;box-shadow:0 4px 24px rgba(0,0,0,0.04)">
    <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;color:#aaa;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:1rem">// sentinelml audit pipeline</div>
    <svg width="100%" viewBox="0 0 580 330">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>
      <text x="72"  y="18" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:9px;fill:#bbb;letter-spacing:1.5px">THREATS</text>
      <text x="290" y="18" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:9px;fill:#bbb;letter-spacing:1.5px">ENGINE</text>
      <text x="500" y="18" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:9px;fill:#bbb;letter-spacing:1.5px">OUTPUTS</text>
      <line x1="148" y1="10" x2="148" y2="310" stroke="#0a0a0a" stroke-width="0.5" stroke-dasharray="3 4" opacity="0.12"/>
      <line x1="408" y1="10" x2="408" y2="310" stroke="#0a0a0a" stroke-width="0.5" stroke-dasharray="3 4" opacity="0.12"/>
      <rect x="8"  y="32"  width="118" height="34" rx="6" fill="#fef0ef" stroke="#f5c6c2" stroke-width="0.5"/>
      <text x="67" y="44"  text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#c0392b">FGSM attack</text>
      <text x="67" y="57"  text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#c0392b;opacity:0.7">one-step gradient</text>
      <rect x="8"  y="78"  width="118" height="34" rx="6" fill="#fef0ef" stroke="#f5c6c2" stroke-width="0.5"/>
      <text x="67" y="90"  text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#c0392b">BIM attack</text>
      <text x="67" y="103" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#c0392b;opacity:0.7">iterative perturbation</text>
      <rect x="8"  y="124" width="118" height="34" rx="6" fill="#fef0ef" stroke="#f5c6c2" stroke-width="0.5"/>
      <text x="67" y="136" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#c0392b">DeepFool</text>
      <text x="67" y="149" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#c0392b;opacity:0.7">min perturbation</text>
      <rect x="8"  y="170" width="118" height="34" rx="6" fill="#fffbeb" stroke="#f6e05e" stroke-width="0.5"/>
      <text x="67" y="182" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#b7791f">Neural Trojan</text>
      <text x="67" y="195" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#b7791f;opacity:0.7">backdoor trigger</text>
      <line x1="126" y1="49"  x2="172" y2="118" stroke="#c0392b" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.4"/>
      <line x1="126" y1="95"  x2="172" y2="128" stroke="#c0392b" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.4"/>
      <line x1="126" y1="141" x2="172" y2="138" stroke="#c0392b" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.4"/>
      <line x1="126" y1="187" x2="172" y2="150" stroke="#b7791f" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.4"/>
      <rect x="162" y="68" width="236" height="174" rx="12" fill="#fff" stroke="#0a0a0a" stroke-width="1" opacity="0.9"/>
      <text x="280" y="90"  text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:10px;font-weight:700;fill:#0a0a0a;letter-spacing:1px">SENTINEL(ML)</text>
      <text x="280" y="104" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:8px;fill:#888">security audit engine</text>
      <rect x="178" y="114" width="204" height="22" rx="4" fill="#f5f5f5" stroke="#e0e0e0" stroke-width="0.5"/>
      <text x="280" y="125" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#555">adversarial attack suite</text>
      <rect x="178" y="142" width="204" height="22" rx="4" fill="#f5f5f5" stroke="#e0e0e0" stroke-width="0.5"/>
      <text x="280" y="153" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#555">neural cleanse detector</text>
      <rect x="178" y="170" width="204" height="22" rx="4" fill="#f5f5f5" stroke="#e0e0e0" stroke-width="0.5"/>
      <text x="280" y="181" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#555">MRR defense layer</text>
      <rect x="178" y="198" width="204" height="22" rx="4" fill="#f0fff4" stroke="#c6f6d5" stroke-width="0.5"/>
      <text x="280" y="209" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#276749">llama 3.3 70b AI analysis</text>
      <line x1="398" y1="130" x2="422" y2="108" stroke="#0a0a0a" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.3"/>
      <line x1="398" y1="150" x2="422" y2="158" stroke="#0a0a0a" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.3"/>
      <line x1="398" y1="170" x2="422" y2="208" stroke="#0a0a0a" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.3"/>
      <line x1="398" y1="205" x2="422" y2="258" stroke="#276749" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.3"/>
      <rect x="422" y="88"  width="150" height="34" rx="6" fill="#f0fff4" stroke="#c6f6d5" stroke-width="0.5"/>
      <text x="497" y="100" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#276749">robustness score</text>
      <text x="497" y="113" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#276749;opacity:0.7">0 - 100 rating</text>
      <rect x="422" y="138" width="150" height="34" rx="6" fill="#ebf8ff" stroke="#bee3f8" stroke-width="0.5"/>
      <text x="497" y="150" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#2b6cb0">trojan verdict</text>
      <text x="497" y="163" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#2b6cb0;opacity:0.7">clean / detected</text>
      <rect x="422" y="188" width="150" height="34" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="0.5"/>
      <text x="497" y="200" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#444">PDF report</text>
      <text x="497" y="213" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#888">audit documentation</text>
      <rect x="422" y="238" width="150" height="34" rx="6" fill="#f0fff4" stroke="#c6f6d5" stroke-width="0.5"/>
      <text x="497" y="250" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#276749">AI recommendations</text>
      <text x="497" y="263" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#276749;opacity:0.7">tier-aware advice</text>
      <rect x="178" y="268" width="108" height="34" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="0.5"/>
      <text x="232" y="280" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#0a0a0a">your model</text>
      <text x="232" y="293" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#888">.pt / .pth file</text>
      <rect x="294" y="268" width="108" height="34" rx="6" fill="#f0fff4" stroke="#c6f6d5" stroke-width="0.5"/>
      <text x="348" y="280" text-anchor="middle" style="font-family:'Geist',sans-serif;font-size:9px;font-weight:600;fill:#276749">source code</text>
      <text x="348" y="293" text-anchor="middle" style="font-family:'Geist Mono',monospace;font-size:8px;fill:#276749;opacity:0.8">.py file (optional)</text>
      <line x1="232" y1="268" x2="232" y2="244" stroke="#0a0a0a" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.25"/>
      <line x1="348" y1="268" x2="348" y2="244" stroke="#276749" stroke-width="0.8" marker-end="url(#arrow)" opacity="0.25"/>
    </svg>
</div>
</div>
""", height=420, scrolling=False)

# ── FEATURES ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="features-section">
    <div class="section-header">
        <div class="section-eyebrow">What SentinelML does</div>
        <h2 class="section-title">Three layers of<br>model security testing</h2>
    </div>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">⚔️</div>
            <div class="feature-title">Adversarial Attack Testing</div>
            <div class="feature-desc">
                Runs FGSM, BIM, and DeepFool attacks against your model
                to measure how easily it can be fooled by crafted inputs.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Neural Trojan Detection</div>
            <div class="feature-desc">
                Uses Neural Cleanse and MAD anomaly scoring to detect
                hidden backdoor triggers embedded during training.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">AI Security Report</div>
            <div class="feature-desc">
                Generates tier-aware AI recommendations and a full PDF
                report with robustness scores and actionable fixes.
            </div>
        </div>
    </div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ── LOGOUT BUTTON ─────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([3, 1, 3])
with btn_col:
    if st.button("Sign out", key="logout_home"):
        logout()
        st.switch_page("pages/login.py")

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-divider"></div>
<div class="footer">
    <div class="footer-logo">SENTINEL(ML)</div>
    <div class="footer-copy">Built for ML security research</div>
</div>
""", unsafe_allow_html=True)
