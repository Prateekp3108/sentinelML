import streamlit as st
from modules.model_loader import load_model, format_param_count

st.set_page_config(
    page_title="SentinelML",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #F7F6F0;
    font-family: 'Geist', sans-serif;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── NAVBAR ── */
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

.navbar-left {
    display: flex;
    align-items: center;
    gap: 2.5rem;
}

.navbar-logo {
    font-family: 'Geist Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #0a0a0a;
    letter-spacing: -0.5px;
    text-decoration: none;
}

.navbar-links {
    display: flex;
    align-items: center;
    gap: 1.8rem;
}

.navbar-link {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 400;
    color: #444;
    text-decoration: none;
    cursor: pointer;
    transition: color 0.15s;
}

.navbar-link:hover { color: #0a0a0a; }

.navbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.navbar-github {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #444;
    text-decoration: none;
    cursor: pointer;
}

.navbar-cta {
    background: #0a0a0a;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.45rem 1.1rem;
    border-radius: 6px;
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.15s;
}

.navbar-cta:hover { opacity: 0.85; }

/* ── HERO SECTION ── */
.hero-section {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 8rem 2rem 4rem;
    background: #F7F6F0;
    position: relative;
    overflow: hidden;
}

.hero-eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    font-weight: 400;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-eyebrow::before,
.hero-eyebrow::after {
    content: '';
    width: 24px;
    height: 1px;
    background: #bbb;
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

.hero-title span {
    color: #888;
}

.hero-description {
    font-family: 'Geist', sans-serif;
    font-size: 1.125rem;
    font-weight: 400;
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
    cursor: pointer;
    transition: opacity 0.15s;
    border: 1px solid #0a0a0a;
    display: inline-block;
}

.btn-secondary {
    background: transparent;
    color: #0a0a0a !important;
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    font-weight: 400;
    padding: 0.65rem 1.5rem;
    border-radius: 7px;
    text-decoration: none !important;
    cursor: pointer;
    border: 1px solid rgba(0,0,0,0.15);
    transition: border-color 0.15s;
    display: inline-block;
}

.btn-primary:hover { opacity: 0.85; }
.btn-secondary:hover { border-color: rgba(0,0,0,0.4); }


/* ── VISUALIZATION ── */
.viz-container {
    width: 100%;
    max-width: 800px;
    background: #fff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
}

.viz-title {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #aaa;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    text-align: left;
}

.viz-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.viz-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #666;
    width: 80px;
    text-align: right;
    flex-shrink: 0;
}

.viz-bar-bg {
    flex: 1;
    height: 8px;
    background: #f0f0f0;
    border-radius: 4px;
    overflow: hidden;
}

.viz-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}

.viz-pct {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #333;
    width: 36px;
    text-align: right;
    flex-shrink: 0;
}

.viz-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}

.viz-badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    border: 1px solid;
}

.badge-red { color: #c0392b; border-color: #e8a09a; background: #fef0ef; }
.badge-yellow { color: #b7791f; border-color: #e8d5a3; background: #fffbeb; }
.badge-green { color: #276749; border-color: #9ae6b4; background: #f0fff4; }

/* ── DIVIDER ── */
.section-divider {
    width: 100%;
    height: 1px;
    background: rgba(0,0,0,0.08);
    margin: 0;
}

/* ── FEATURES SECTION ── */
.features-section {
    background: #F7F6F0;
    padding: 6rem 2.5rem;
}

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

.feature-card {
    background: #F7F6F0;
    padding: 2rem;
}

.feature-icon {
    font-size: 1.4rem;
    margin-bottom: 1rem;
}

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

/* ── SECTION HEADERS ── */
.section-header {
    text-align: center;
    max-width: 1100px;
    margin: 0 auto;
}

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

/* ── AUDIT SECTION ── */
.audit-section {
    background: #fff;
    padding: 6rem 2.5rem;
    border-top: 1px solid rgba(0,0,0,0.08);
}

.audit-inner {
    max-width: 760px;
    margin: 0 auto;
}

.audit-step {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #aaa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.audit-label {
    font-family: 'Geist', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0a0a0a;
    letter-spacing: -0.5px;
    margin-bottom: 0.4rem;
}

.audit-sublabel {
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    color: #777;
    margin-bottom: 1.5rem;
}

/* Override Streamlit upload styling */
div[data-testid="stFileUploadDropzone"] {
    background: #fafafa !important;
    border: 1.5px dashed rgba(0,0,0,0.15) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s !important;
}

div[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(0,0,0,0.35) !important;
}

div[data-testid="stFileUploadDropzone"] * {
    font-family: 'Geist', sans-serif !important;
    color: #666 !important;
}

/* ── RESULT CARDS ── */
.result-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 10px;
    overflow: hidden;
    margin: 1.5rem 0;
}

.result-card {
    background: #fff;
    padding: 1.25rem 1.5rem;
}

.result-value {
    font-family: 'Geist Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #0a0a0a;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.result-label {
    font-family: 'Geist', sans-serif;
    font-size: 0.75rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── ATTACK RESULTS ── */
.attack-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(0,0,0,0.06);
}

.attack-row:last-child { border-bottom: none; }

.attack-name {
    font-family: 'Geist Mono', monospace;
    font-size: 0.8rem;
    color: #0a0a0a;
    font-weight: 500;
}

.attack-detail {
    font-family: 'Geist', sans-serif;
    font-size: 0.8rem;
    color: #888;
    margin-top: 0.2rem;
}

.attack-status {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}

.status-fail { background: #fef0ef; color: #c0392b; }
.status-pass { background: #f0fff4; color: #276749; }

/* ── SCORE DISPLAY ── */
.score-display {
    text-align: center;
    padding: 2.5rem;
    background: #fafafa;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 10px;
    margin: 1.5rem 0;
}

.score-number {
    font-family: 'Geist Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    letter-spacing: -2px;
    line-height: 1;
}

.score-label {
    font-family: 'Geist', sans-serif;
    font-size: 0.8rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.5rem;
}

/* ── ACTION BUTTONS ── */
.stButton button {
    background: #0a0a0a !important;
    color: #F7F6F0 !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.5rem !important;
    border-radius: 7px !important;
    border: none !important;
    width: 100% !important;
    transition: opacity 0.15s !important;
    letter-spacing: 0 !important;
}

.stButton button:hover { opacity: 0.8 !important; }

/* ── FOOTER ── */
.footer {
    background: #0a0a0a;
    color: #666;
    padding: 3rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.footer-logo {
    font-family: 'Geist Mono', monospace;
    font-size: 0.9rem;
    color: #F7F6F0;
    font-weight: 700;
}

.footer-copy {
    font-family: 'Geist', sans-serif;
    font-size: 0.8rem;
    color: #555;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────────────
if "model_result" not in st.session_state:
    st.session_state.model_result = None
if "attack_results" not in st.session_state:
    st.session_state.attack_results = None

# ── NAVBAR ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="navbar-left">
        <span class="navbar-logo">SENTINEL(ML)</span>
        <div class="navbar-links">
            <span class="navbar-link">Documentation</span>
            <span class="navbar-link">About</span>
        </div>
    </div>
    <div class="navbar-right">
        <span class="navbar-github">
            <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
                <path d="M16 2.667C8.636 2.667 2.667 8.636 2.667 16c0 5.893 3.827 10.893 9.12 12.667.667.107.88-.307.88-.667v-2.253c-3.693.8-4.48-1.587-4.48-1.587-.613-1.547-1.48-1.96-1.48-1.96-1.213-.827.093-.8.093-.8 1.333.093 2.04 1.373 2.04 1.373 1.16 2.027 3.12 1.427 3.88 1.107.12-.867.467-1.453.84-1.787-2.96-.333-6.067-1.48-6.067-6.56 0-1.48.507-2.667 1.373-3.613-.133-.333-.6-1.72.133-3.52 0 0 1.12-.36 3.667 1.36 1.053-.293 2.2-.44 3.333-.44 1.133 0 2.28.147 3.333.44 2.547-1.72 3.667-1.36 3.667-1.36.733 1.8.267 3.187.133 3.52.867.947 1.373 2.133 1.373 3.613 0 5.093-3.107 6.213-6.067 6.547.48.413.92 1.227.92 2.467v3.653c0 .36.213.787.893.667C25.52 26.88 29.333 21.893 29.333 16 29.333 8.636 23.364 2.667 16 2.667Z" fill="#444"/>
            </svg>
            GitHub
        </span>
        <a class="navbar-cta" href="#audit">Run Audit →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO SECTION ─────────────────────────────────────────────────────────
# Hero text
st.markdown("""
<div class="hero-section">
    <div class="hero-eyebrow">ML Security Auditor</div>
    <h1 class="hero-title">
        Audit your models.<br><span>Before attackers do.</span>
    </h1>
    <p class="hero-description">
        SentinelML automatically tests your PyTorch models against 
        adversarial attacks and neural Trojan detection — giving you 
        a full security report in minutes.
    </p>
    <div class="hero-buttons">
    <a class="btn-primary" href="/audit" target="_self">Start Audit →</a>
    <a class="btn-secondary" href="#">Read the docs</a>
</div>
</div>
""", unsafe_allow_html=True)

# Visualization separately
st.markdown("""
<div style="display:flex;justify-content:center;padding:0 2rem 5rem;background:#F7F6F0">
<div class="viz-container">
    <div class="viz-title">// live model vulnerability snapshot</div>
    <div class="viz-row">
        <span class="viz-label">FGSM</span>
        <div class="viz-bar-bg">
            <div class="viz-bar-fill" style="width:87%;background:#e53e3e;"></div>
        </div>
        <span class="viz-pct">87%</span>
    </div>
    <div class="viz-row">
        <span class="viz-label">BIM</span>
        <div class="viz-bar-bg">
            <div class="viz-bar-fill" style="width:92%;background:#e53e3e;"></div>
        </div>
        <span class="viz-pct">92%</span>
    </div>
    <div class="viz-row">
        <span class="viz-label">DeepFool</span>
        <div class="viz-bar-bg">
            <div class="viz-bar-fill" style="width:78%;background:#dd6b20;"></div>
        </div>
        <span class="viz-pct">78%</span>
    </div>
    <div class="viz-row">
        <span class="viz-label">Trojan</span>
        <div class="viz-bar-bg">
            <div class="viz-bar-fill" style="width:34%;background:#38a169;"></div>
        </div>
        <span class="viz-pct">34%</span>
    </div>
    <div class="viz-badges">
        <span class="viz-badge badge-red">✗ FGSM Vulnerable</span>
        <span class="viz-badge badge-red">✗ BIM Vulnerable</span>
        <span class="viz-badge badge-yellow">⚠ DeepFool Partial</span>
        <span class="viz-badge badge-green">✓ Trojan Clean</span>
    </div>
</div>
</div>

<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ── FEATURES SECTION ─────────────────────────────────────────────────────
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
                Hooks into neuron activations and uses clustering to detect 
                hidden backdoor functionality embedded during training.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Security Report</div>
            <div class="feature-desc">
                Generates a full report with robustness scores, visualizations, 
                and actionable recommendations you can act on immediately.
            </div>
        </div>
    </div>
</div>

<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-divider"></div>
<div class="footer">
    <div class="footer-logo">SENTINEL(ML)</div>
    <div class="footer-copy">Built for ML security research</div>
</div>
""", unsafe_allow_html=True)