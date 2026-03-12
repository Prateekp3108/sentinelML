import streamlit as st
from modules.model_loader import load_model, format_param_count

st.set_page_config(
    page_title="SentinelML — Audit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────
if "model_result" not in st.session_state:
    st.session_state.model_result = None
if "attack_results" not in st.session_state:
    st.session_state.attack_results = None

# ── NAVBAR (once only) ────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div style="display:flex;align-items:center;gap:2.5rem">
        <a class="navbar-logo" href="/" target="_self">SENTINEL(ML)</a>
        <div class="navbar-links">
            <span class="navbar-link">Documentation</span>
            <span class="navbar-link">About</span>
        </div>
    </div>
    <a class="navbar-back" href="/" target="_self">← Home</a>
</div>
""", unsafe_allow_html=True)

# navbar height spacer
st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ── SINGLE CENTERED COLUMN ────────────────────────────────────────────────
_, main, _ = st.columns([2, 6, 2])

with main:

    # ── PAGE HEADER ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:2.5rem 0 0">
        <a class="back-link" href="/" target="_self">← Home</a>
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
    """, unsafe_allow_html=True)

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
        
        # ── LOADING UI ────────────────────────────────────────────────────
        progress_container = st.empty()
        
        stages = [
            (0.15, "Reading file..."),
            (0.35, "Deserializing model..."),
            (0.55, "Detecting architecture..."),
            (0.75, "Counting parameters..."),
            (0.90, "Probing input size..."),
            (1.00, "Done"),
        ]
        
        def render_progress(pct, label):
            bar_filled = int(pct * 28)
            bar_empty = 28 - bar_filled
            bar = "█" * bar_filled + "░" * bar_empty
            percent = int(pct * 100)
            progress_container.markdown(f"""
            <div style="padding:1.5rem 0 0.5rem">
                <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                color:#aaa;letter-spacing:1px;margin-bottom:0.6rem">
                    ANALYZING MODEL
                </div>
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

        # Animate through stages while load_model runs
        # Show first 5 stages as visual feedback, then do the real load
        for pct, label in stages[:-1]:
            render_progress(pct, label)
            time.sleep(0.3)

        # Do the actual load
        render_progress(0.95, "Finalizing...")
        st.session_state.model_result = load_model(uploaded_file)
        st.session_state.attack_results = None

        # Flash done
        render_progress(1.0, "Done")
        time.sleep(0.4)
        progress_container.empty()

    if uploaded_file is None:
        st.session_state.model_result = None
        st.session_state.attack_results = None

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

            # ── LAYER LIST (built separately to avoid f-string issues) ────
            layer_rows_html = ""
            for i, name in enumerate(result["layer_names"]):
                layer_rows_html += (
                    f'<div class="layer-row">{i+1:02d}. {name}</div>'
                )

            st.markdown(f"""
            <div style="margin-top:1.25rem">
                <div class="step-label" style="margin-bottom:0.6rem">
                    Layer Architecture
                </div>
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
                run_adv = st.button("⚔️  Adversarial Test")
            with b2:
                run_troj = st.button("🔍  Trojan Detection")

            if run_adv:
                if result["input_size"] and result["num_classes"]:
                    
                    atk_container = st.empty()

                    def render_attack_progress(pct, label):
                        bar_filled = int(pct * 28)
                        bar_empty = 28 - bar_filled
                        bar = "█" * bar_filled + "░" * bar_empty
                        percent = int(pct * 100)
                        atk_container.markdown(f"""
                        <div style="padding:1rem 0 0.5rem">
                            <div style="font-family:'Geist Mono',monospace;font-size:0.7rem;
                            color:#aaa;letter-spacing:1px;margin-bottom:0.6rem">
                                RUNNING SECURITY TESTS
                            </div>
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

                    # Each attack updates the bar via the status_callback
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

                    def update_status(msg):
                        pct = attack_stages.get(msg, 0.5)
                        render_attack_progress(pct, msg)

                    render_attack_progress(0.05, "Initializing...")

                    st.session_state.attack_results = run_adversarial_tests(
                        model=result["model"],
                        input_size=result["input_size"],
                        num_classes=result["num_classes"],
                        status_callback=update_status
                    )

                    render_attack_progress(1.0, "All tests complete")
                    import time
                    time.sleep(0.5)
                    atk_container.empty()

            if run_troj:
                st.markdown(
                    '<div class="status-line">↳ Coming soon...</div>',
                    unsafe_allow_html=True)

            # ── RESULTS ───────────────────────────────────────────────────
            if st.session_state.attack_results is not None:
                ar = st.session_state.attack_results
                score = ar["robustness_score"]
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
                        conf = (f"{r.get('original_conf','?')}% → "
                                f"{r.get('adversarial_conf','?')}%")
                        badge = (f'<span class="badge badge-fail">'
                                 f'✗ Fooled &nbsp;{conf}</span>')
                    else:
                        badge = '<span class="badge badge-pass">✓ Resisted</span>'

                    rows_html += (
                        f'<div class="attack-row">'
                        f'<div>'
                        f'<div class="attack-name">{atk_name}</div>'
                        f'<div class="attack-detail">{detail}</div>'
                        f'</div>{badge}</div>'
                    )

                st.markdown(f"""
                <div class="step-divider"></div>
                <div class="step-label">Results</div>
                <div class="step-title">Security report</div>
                <div class="score-block">
                    <div class="score-num" style="color:{score_color}">{score}</div>
                    <div class="score-sub">out of 100</div>
                    <div class="score-lbl">Robustness Score</div>
                </div>
                <div class="results-box">{rows_html}</div>
                """, unsafe_allow_html=True)

        else:
            st.markdown(
                f'<div class="error-box">✗ {result["error"]}</div>',
                unsafe_allow_html=True)

    # bottom breathing room
    st.markdown("<div style='height:5rem'></div>", unsafe_allow_html=True)