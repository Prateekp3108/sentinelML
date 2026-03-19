import streamlit as st
from modules.model_loader import load_model, format_param_count
import streamlit.components.v1 as components

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
    color: #0a0a0a !important;
    text-decoration: none !important;
    letter-spacing: -0.5px;
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

a.navbar-cta, a.navbar-cta:visited, a.navbar-cta:hover {
    color: #F7F6F0 !important;
    text-decoration: none !important;
}

.navbar-cta:hover { opacity: 0.85; }

.navbar-link {
    color: #555 !important;
    text-decoration: none !important;
}

.navbar-github {
    color: #444 !important;
    text-decoration: none !important;
}

.navbar-cta {
    color: #F7F6F0 !important;
    text-decoration: none !important;
}

a.navbar-link, a.navbar-github, a.navbar-cta {
    color: inherit !important;
    text-decoration: none !important;
}            

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
            <a class="navbar-link" href="/documentation" target="_self">Documentation</a>
            <a class="navbar-link" href="/about" target="_self">About</a>
        </div>
    </div>
    <div class="navbar-right">
        <a class="navbar-github" href="https://github.com/Prateekp3108/sentinelML" target="_blank">
            <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
                <path d="M16 2.667C8.636 2.667 2.667 8.636 2.667 16c0 5.893 3.827 10.893 9.12 12.667.667.107.88-.307.88-.667v-2.253c-3.693.8-4.48-1.587-4.48-1.587-.613-1.547-1.48-1.96-1.48-1.96-1.213-.827.093-.8.093-.8 1.333.093 2.04 1.373 2.04 1.373 1.16 2.027 3.12 1.427 3.88 1.107.12-.867.467-1.453.84-1.787-2.96-.333-6.067-1.48-6.067-6.56 0-1.48.507-2.667 1.373-3.613-.133-.333-.6-1.72.133-3.52 0 0 1.12-.36 3.667 1.36 1.053-.293 2.2-.44 3.333-.44 1.133 0 2.28.147 3.333.44 2.547-1.72 3.667-1.36 3.667-1.36.733 1.8.267 3.187.133 3.52.867.947 1.373 2.133 1.373 3.613 0 5.093-3.107 6.213-6.067 6.547.48.413.92 1.227.92 2.467v3.653c0 .36.213.787.893.667C25.52 26.88 29.333 21.893 29.333 16 29.333 8.636 23.364 2.667 16 2.667Z" fill="#444"/>
            </svg>
            GitHub
        </a>
        <a class="navbar-cta" href="/audit" target="_self">Run Audit →</a>
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
        a full security report.
    </p>
    <div class="hero-buttons">
        <a class="btn-primary" href="/audit" target="_self">Start Audit →</a>
        <a class="btn-secondary" href="/documentation" target="_self">Read the docs →</a>
    </div>
</div>
""", unsafe_allow_html=True)

#visualisation
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