import streamlit as st

st.set_page_config(
    page_title="SentinelML — Documentation",
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
.page-wrap { max-width: 760px; margin: 0 auto; padding: 5rem 1.5rem 6rem; }
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
.step-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    margin: 1rem 0;
}
.step-item {
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    padding: 1.1rem 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.step-item:last-child { border-bottom: none; }
.step-num {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    color: #bbb;
    min-width: 24px;
    padding-top: 2px;
}
.step-content-title {
    font-family: 'Geist', sans-serif;
    font-size: 0.875rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.2rem;
}
.step-content-desc {
    font-family: 'Geist', sans-serif;
    font-size: 0.825rem;
    color: #888;
    line-height: 1.5;
}
.info-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.info-row:last-child { border-bottom: none; }
.info-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #888;
    min-width: 160px;
}
.info-value {
    font-family: 'Geist', sans-serif;
    font-size: 0.825rem;
    color: #0a0a0a;
    line-height: 1.5;
    text-align: right;
}
.badge-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.75rem 0; }
.badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    white-space: nowrap;
}
.badge-green { background: #f0fff4; color: #276749; }
.badge-blue  { background: #ebf4ff; color: #1a56db; }
.badge-red   { background: #fef0ef; color: #c0392b; }
.badge-grey  { background: #f5f5f5; color: #555; }
.code-block {
    background: #0a0a0a;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-family: 'Geist Mono', monospace;
    font-size: 0.78rem;
    color: #a8b5c8;
    line-height: 1.6;
    overflow-x: auto;
}
.tier-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
}
.tier-title {
    font-family: 'Geist', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #0a0a0a;
    margin-bottom: 0.3rem;
}
.tier-desc {
    font-family: 'Geist', sans-serif;
    font-size: 0.825rem;
    color: #888;
    line-height: 1.5;
}
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
[data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }
div[data-testid="stVerticalBlockSeparator"] { display: none !important; }
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
    <div class="eyebrow">Documentation</div>
    <div class="page-title">How SentinelML works</div>
    <div class="page-subtitle">
        A complete guide to auditing your PyTorch models for adversarial
        vulnerabilities and neural Trojan backdoors.
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── QUICK START ───────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Quick Start</div>
    <div class="section-title">Run your first audit in 3 steps</div>
    <div class="step-box">
        <div class="step-item">
            <div class="step-num">01</div>
            <div>
                <div class="step-content-title">Save your model</div>
                <div class="step-content-desc">
                    Export your PyTorch model as a full model file using
                    torch.save(model, "model.pth") — not just the state dict.
                    SentinelML needs the full model object to run inference.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">02</div>
            <div>
                <div class="step-content-title">Upload and analyze</div>
                <div class="step-content-desc">
                    Go to the Audit page, upload your .pt or .pth file.
                    SentinelML will automatically detect the architecture,
                    parameter count, input size, and number of output classes.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">03</div>
            <div>
                <div class="step-content-title">Run security tests</div>
                <div class="step-content-desc">
                    Click Adversarial Test and/or Trojan Detection.
                    Results appear with a robustness score, per-attack breakdown,
                    and a downloadable PDF report.
                </div>
            </div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── MODEL UPLOAD ──────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Step 01</div>
    <div class="section-title">Model upload</div>
    <p class="body-text">
        SentinelML accepts PyTorch model files saved with torch.save().
        The model must be saved as a complete object — not just the state dict —
        so that SentinelML can run forward passes without needing your original
        class definition.
    </p>
    <div class="badge-row">
        <span class="badge badge-green">✓ .pt files</span>
        <span class="badge badge-green">✓ .pth files</span>
        <span class="badge badge-red">✗ state dicts only</span>
        <span class="badge badge-grey">Max 200MB</span>
    </div>
    <div class="code-block">
        # Correct — save full model<br>
        torch.save(model, "my_model.pth")<br>
        <br>
        # Wrong — state dict only (SentinelML cannot use this)<br>
        torch.save(model.state_dict(), "weights_only.pth")
    </div>
    <p class="body-text">
        After upload, SentinelML detects: total parameters, number of layers,
        output classes, and input image size by probing with dummy inputs at
        common sizes (32, 64, 128, 224px).
    </p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── ADVERSARIAL ATTACKS ───────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Step 02</div>
    <div class="section-title">Adversarial attack testing</div>
    <p class="body-text">
        SentinelML runs three adversarial attacks of increasing difficulty
        against your model using a random test image. Each attack attempts
        to find a small perturbation that causes misclassification.
    </p>
    <div class="step-box">
        <div class="step-item">
            <div class="step-num" style="color:#c0392b">01</div>
            <div>
                <div class="step-content-title">FGSM — Fast Gradient Sign Method</div>
                <div class="step-content-desc">
                    One-step attack. Computes the gradient of the loss with
                    respect to the input and adds a small perturbation in the
                    direction that maximises the loss. Epsilon = 0.1.
                    The easiest attack to defend against — if your model fails
                    this, it is highly vulnerable.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num" style="color:#c0392b">02</div>
            <div>
                <div class="step-content-title">BIM — Basic Iterative Method</div>
                <div class="step-content-desc">
                    Iterative version of FGSM. Applies 10 small FGSM steps
                    with clipping to stay within an epsilon-ball around the
                    original image. Alpha = 0.01, Epsilon = 0.1.
                    Stronger than FGSM — a model resisting BIM is meaningfully robust.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num" style="color:#c0392b">03</div>
            <div>
                <div class="step-content-title">DeepFool</div>
                <div class="step-content-desc">
                    Finds the minimum perturbation needed to cross the nearest
                    decision boundary. Runs up to 20 iterations.
                    The hardest attack — resisting DeepFool indicates strong
                    inherent robustness. Worth 40 of the 100 robustness points.
                </div>
            </div>
        </div>
    </div>
    <div class="info-box">
        <div class="info-row">
            <div class="info-label">FGSM weight</div>
            <div class="info-value">25 / 100 points</div>
        </div>
        <div class="info-row">
            <div class="info-label">BIM weight</div>
            <div class="info-value">35 / 100 points</div>
        </div>
        <div class="info-row">
            <div class="info-label">DeepFool weight</div>
            <div class="info-value">40 / 100 points</div>
        </div>
        <div class="info-row">
            <div class="info-label">Score interpretation</div>
            <div class="info-value">0-39 Vulnerable · 40-69 Moderate · 70-100 Robust</div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── TROJAN DETECTION ──────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Step 03</div>
    <div class="section-title">Neural Trojan detection</div>
    <p class="body-text">
        SentinelML implements Neural Cleanse — the leading backdoor detection
        method from the 2019 IEEE S&P paper. The key insight: if a model has
        a backdoor trigger, there exists an unusually small perturbation that
        forces any input to be classified as the target class.
    </p>
    <p class="body-text">
        For each candidate class, SentinelML optimises a trigger mask and
        pattern that causes misclassification. The L1 norm of the resulting
        mask measures how small the trigger needs to be. A class with a
        suspiciously small norm is flagged as a likely backdoor target using
        MAD (Median Absolute Deviation) anomaly scoring.
    </p>
    <div class="info-box">
        <div class="info-row">
            <div class="info-label">Detection method</div>
            <div class="info-value">Neural Cleanse (Wang et al. 2019)</div>
        </div>
        <div class="info-row">
            <div class="info-label">Scoring method</div>
            <div class="info-value">MAD anomaly index</div>
        </div>
        <div class="info-row">
            <div class="info-label">Anomaly threshold</div>
            <div class="info-value">2.0 (from original paper)</div>
        </div>
        <div class="info-row">
            <div class="info-label">Classes scanned</div>
            <div class="info-value">Up to 10 (capped for speed)</div>
        </div>
        <div class="info-row">
            <div class="info-label">Steps per class</div>
            <div class="info-value">100 optimisation steps</div>
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── AI ANALYSIS ───────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Step 04</div>
    <div class="section-title">AI security analysis</div>
    <p class="body-text">
        After running security tests, SentinelML can generate a personalised
        AI analysis of your results using Llama 3.3 70B via Groq.
        The analysis is tailored to your experience level — choose the tier
        that matches your background.
    </p>
    <div class="tier-card">
        <div class="tier-title">Student / Researcher</div>
        <div class="tier-desc">
            Plain English explanation of vulnerabilities, real-world impact,
            and 3 beginner-friendly suggestions. No jargon.
        </div>
    </div>
    <div class="tier-card">
        <div class="tier-title">ML Engineer</div>
        <div class="tier-desc">
            Technical breakdown of each vulnerability, exact code changes needed,
            specific defense strategies with parameters, and priority-ordered fixes.
        </div>
    </div>
    <div class="tier-card">
        <div class="tier-title">Red Team Analyst</div>
        <div class="tier-desc">
            Full threat model, complete rewritten source code with all security
            fixes applied and inline comments, CVE-style vulnerability descriptions,
            and deployment monitoring strategy. Requires source code upload.
        </div>
    </div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── PDF REPORT ────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem">
    <div class="section-sub">Export</div>
    <div class="section-title">PDF report</div>
    <p class="body-text">
        After running at least one test, a Download PDF Report button appears.
        The report includes: model overview, layer architecture, adversarial
        attack results with robustness score, trojan detection verdict with
        trigger norm visualisation per class, and a timestamped footer.
    </p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── FAQ ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:760px;margin:0 auto;padding:0 1.5rem 4rem">
    <div class="section-sub">FAQ</div>
    <div class="section-title">Common questions</div>
    <div class="step-box">
        <div class="step-item">
            <div class="step-num">?</div>
            <div>
                <div class="step-content-title">Why does my model score 0/100?</div>
                <div class="step-content-desc">
                    Most standard pretrained models score 0 because they were
                    not adversarially trained. This is expected and correct —
                    it means your model is vulnerable to adversarial attacks,
                    which is true of most ImageNet models out of the box.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">?</div>
            <div>
                <div class="step-content-title">My model fails to load — state dict error</div>
                <div class="step-content-desc">
                    You saved only the weights, not the full model.
                    Re-save with torch.save(model, path) instead of
                    torch.save(model.state_dict(), path).
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">?</div>
            <div>
                <div class="step-content-title">How long does the trojan scan take?</div>
                <div class="step-content-desc">
                    Approximately 1-3 minutes depending on model size.
                    It runs 100 optimisation steps per class across up to
                    10 classes. Larger models with more parameters will take longer.
                </div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">?</div>
            <div>
                <div class="step-content-title">Is my model data kept private?</div>
                <div class="step-content-desc">
                    Yes. Models are processed in memory and never stored on disk
                    or sent to any external service. The AI analysis sends only
                    the audit results and your source code text to Groq —
                    never the model weights.
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)