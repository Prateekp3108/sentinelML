import streamlit as st

st.set_page_config(
    page_title="SentinelML — About",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
div[data-testid="stVerticalBlockSeparator"] { display: none !important; }

.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: rgba(247, 246, 240, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.08);
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
}
.navbar-logo {
    font-family: 'Geist Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #0a0a0a !important;
    text-decoration: none !important;
}
.navbar-links { display: flex; align-items: center; gap: 1.8rem; }
.navbar-link {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    color: #555 !important;
    text-decoration: none !important;
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
}
.eyebrow {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.page-title {
    font-family: 'Geist', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #0a0a0a;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 0.5rem;
}
.page-subtitle {
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    color: #888;
    line-height: 1.6;
    margin-bottom: 2.5rem;
}
.divider { width: 100%; height: 1px; background: rgba(0,0,0,0.07); margin: 2.5rem 0; }
.section-title {
    font-family: 'Geist', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #0a0a0a;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}
.section-sub {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.body-text {
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    color: #555;
    line-height: 1.75;
    margin-bottom: 1rem;
}
.card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 0.75rem 0;
}
.card-title {
    font-family: 'Geist', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.3rem;
}
.card-sub {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #bbb;
    letter-spacing: 1px;
    margin-bottom: 0.75rem;
}
.card-body {
    font-family: 'Geist', sans-serif;
    font-size: 0.85rem;
    color: #666;
    line-height: 1.65;
}
.paper-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin: 1rem 0;
}
.paper-item {
    display: flex;
    gap: 1.25rem;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    align-items: flex-start;
}
.paper-item:last-child { border-bottom: none; }
.paper-num {
    font-family: 'Geist Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    min-width: 20px;
    padding-top: 3px;
}
.paper-title {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.2rem;
}
.paper-authors {
    font-family: 'Geist', sans-serif;
    font-size: 0.78rem;
    color: #888;
    margin-bottom: 0.3rem;
}
.paper-desc {
    font-family: 'Geist', sans-serif;
    font-size: 0.8rem;
    color: #aaa;
    line-height: 1.5;
}
.stack-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: rgba(0,0,0,0.07);
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin: 1rem 0;
}
.stack-card { background: #fff; padding: 1.1rem 1.25rem; }
.stack-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.62rem;
    color: #bbb;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.stack-value {
    font-family: 'Geist', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: #0a0a0a;
}
.dev-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 1.75rem;
    margin: 1rem 0;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
}
.dev-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: #0a0a0a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Geist Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #F7F6F0;
    flex-shrink: 0;
}
.dev-name {
    font-family: 'Geist', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.2rem;
}
.dev-role {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #bbb;
    letter-spacing: 1px;
    margin-bottom: 0.6rem;
}
.dev-bio {
    font-family: 'Geist', sans-serif;
    font-size: 0.85rem;
    color: #666;
    line-height: 1.6;
}
.link-row { display: flex; gap: 0.75rem; margin-top: 0.75rem; flex-wrap: wrap; }
.link-btn {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #0a0a0a !important;
    text-decoration: none !important;
    padding: 0.3rem 0.8rem;
    border: 1px solid rgba(0,0,0,0.15);
    border-radius: 6px;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div style="display:flex;align-items:center;gap:2.5rem">
        <a class="navbar-logo" href="/" target="_self">SENTINEL(ML)</a>
        <div class="navbar-links">
            <a class="navbar-link" href="/documentation" target="_self">Documentation</a>
            <a class="navbar-link" href="/about" target="_self">About</a>
        </div>
    </div>
    <a class="navbar-back" href="/" target="_self">← Home</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:4.5rem 1.5rem 0">
    <div class="eyebrow">About</div>
    <div class="page-title">Built to make ML security accessible</div>
    <div class="page-subtitle">
        SentinelML started as a research project exploring how adversarial
        attacks and neural Trojans affect real-world PyTorch models —
        and grew into a full security auditing tool.
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── THE PROJECT ───────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">The Project</div>
    <div class="section-title">What is SentinelML?</div>
    <p class="body-text">
        SentinelML is an ML model security auditor that automatically tests
        PyTorch models for adversarial vulnerabilities and neural Trojan backdoors.
        It combines research-grade attack implementations with an accessible UI
        so that anyone — from students to security researchers — can understand
        the risks in their models.
    </p>
    <p class="body-text">
        Most ML practitioners focus entirely on accuracy and never think about
        security. A model that achieves 95% test accuracy can still be trivially
        fooled by a one-pixel perturbation, or secretly backdoored to misclassify
        any image with a specific trigger pattern. SentinelML makes these risks visible.
    </p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── TECH STACK ────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Built With</div>
    <div class="section-title">Tech stack</div>
    <div class="stack-grid">
        <div class="stack-card">
            <div class="stack-label">Framework</div>
            <div class="stack-value">Streamlit</div>
        </div>
        <div class="stack-card">
            <div class="stack-label">ML</div>
            <div class="stack-value">PyTorch</div>
        </div>
        <div class="stack-card">
            <div class="stack-label">AI Analysis</div>
            <div class="stack-value">Llama 3.3 70B</div>
        </div>
        <div class="stack-card">
            <div class="stack-label">AI Provider</div>
            <div class="stack-value">Groq</div>
        </div>
        <div class="stack-card">
            <div class="stack-label">Reports</div>
            <div class="stack-value">ReportLab</div>
        </div>
        <div class="stack-card">
            <div class="stack-label">Deployment</div>
            <div class="stack-value">Streamlit Cloud</div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── RESEARCH PAPERS ───────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Research Foundation</div>
    <div class="section-title">Papers this project is based on</div>
    <p class="body-text">
        SentinelML's attack and defense implementations are grounded in
        peer-reviewed security research. The two core papers:
    </p>
    <div class="paper-box">
        <div class="paper-item">
            <div class="paper-num">01</div>
            <div>
                <div class="paper-title">
                    Safe Machine Learning and Defeating Adversarial Attacks
                </div>
                <div class="paper-authors">
                    UC San Diego — introduces MRR (Modular Robust Redundancy)
                </div>
                <div class="paper-desc">
                    Proposes a countermeasure where multiple independent modules
                    vote on predictions, making it statistically unlikely that an
                    adversarial example crafted for one module fools all of them.
                    Forms the basis of SentinelML's MRR defense implementation.
                </div>
            </div>
        </div>
        <div class="paper-item">
            <div class="paper-num">02</div>
            <div>
                <div class="paper-title">
                    A Survey on Neural Trojans
                </div>
                <div class="paper-authors">
                    University of Maryland — comprehensive backdoor attack survey
                </div>
                <div class="paper-desc">
                    Surveys the landscape of neural Trojan attacks and defenses,
                    including the Neural Cleanse detection method that SentinelML
                    uses for backdoor detection. Covers trigger generation,
                    MAD anomaly scoring, and practical detection thresholds.
                </div>
            </div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── DEVELOPER ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Developers</div>
    <div class="section-title">Who built this</div>
    <div class="dev-card">
        <div class="dev-avatar">P</div>
        <div>
            <div class="dev-name">Prateek Pandey</div>
            <div class="dev-role">DEVELOPER · RESEARCHER</div>
            <div class="dev-bio">
                Studying at Manipal University, Jaipur. Co-developed SentinelML as a
                research and portfolio project exploring the intersection of
                machine learning and security. Interested in adversarial
                robustness, model interpretability, and making security tooling
                accessible to the broader ML community.
            </div>
            <div class="link-row">
                <a class="link-btn" href="https://github.com/Prateekp3108" target="_blank">
                    GitHub →
                </a>
                <a class="link-btn" href="https://github.com/Prateekp3108/sentinelML" target="_blank">
                    Repository →
                </a>
            </div>
        </div>
    </div>
    <div class="dev-card">
        <div class="dev-avatar">S</div>
        <div>
            <div class="dev-name">Suhani Sharma</div>
            <div class="dev-role">DEVELOPER · RESEARCHER</div>
            <div class="dev-bio">
                Studying at Manipal University, Jaipur. Co-developer of
                SentinelML, contributing to the research, design, and
                implementation of the security auditing pipeline.
            </div>
            <div class="link-row">
                <a class="link-btn" href="https://github.com/tsunamiuwu" target="_blank">
                    GitHub →
                </a>
                <a class="link-btn" href="https://github.com/Prateekp3108/sentinelML" target="_blank">
                    Repository →
                </a>
            </div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── ROADMAP ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem 5rem">
    <div class="section-sub">Roadmap</div>
    <div class="section-title">Where SentinelML is headed</div>
    <div class="card">
        <div class="card-title">Enterprise Model Registry Integration</div>
        <div class="card-sub">Scaling</div>
        <div class="card-body">
            Connect directly to MLflow, Weights & Biases, and Hugging Face
            Model Hub to audit models at scale — scanning entire registries
            for vulnerabilities rather than one model at a time.
        </div>
    </div>
    <div class="card">
        <div class="card-title">CI/CD Security Pipeline</div>
        <div class="card-sub">DevSecOps</div>
        <div class="card-body">
            GitHub Actions and GitLab CI integration so security audits run
            automatically on every model push — blocking deployment if a model
            fails adversarial thresholds or trojan detection.
        </div>
    </div>
    <div class="card">
        <div class="card-title">Multi-Framework Support</div>
        <div class="card-sub">Compatibility</div>
        <div class="card-body">
            Extend beyond PyTorch to support TensorFlow, JAX, and ONNX models —
            covering the full spectrum of production ML frameworks used across
            the industry.
        </div>
    </div>
    <div class="card">
        <div class="card-title">Compliance Reporting</div>
        <div class="card-sub">Governance</div>
        <div class="card-body">
            Audit reports aligned with emerging AI security standards including
            NIST AI RMF, EU AI Act requirements, and ISO 42001 —
            giving enterprises audit-ready documentation for regulatory compliance.
        </div>
    </div>
    <div class="card">
        <div class="card-title">Real-Time Production Monitoring</div>
        <div class="card-sub">Observability</div>
        <div class="card-body">
            Monitor deployed models in production for adversarial input patterns,
            distribution shift, and anomalous prediction confidence —
            alerting security teams before attacks cause damage.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)