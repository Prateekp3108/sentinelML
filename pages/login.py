import streamlit as st
from streamlit_oauth import OAuth2Component
from modules.auth import fetch_github_user, is_logged_in, has_selected_tier

st.set_page_config(
    page_title="SentinelML — Login",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── If already logged in, redirect ───────────────────────────────────────
if is_logged_in():
    if not has_selected_tier():
        st.switch_page("pages/tier_select.py")
    else:
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
    transition: opacity 0.15s !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "user_tier" not in st.session_state:
    st.session_state.user_tier = None

# ── OAUTH SETUP ───────────────────────────────────────────────────────────
client_id     = st.secrets.get("GITHUB_CLIENT_ID", "")
client_secret = st.secrets.get("GITHUB_CLIENT_SECRET", "")
redirect_uri  = st.secrets.get("REDIRECT_URI", "https://sentinelml.streamlit.app")

oauth2 = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://github.com/login/oauth/authorize",
    token_endpoint="https://github.com/login/oauth/access_token",
    refresh_token_endpoint=None,
    revoke_token_endpoint=None,
)

# ── LOGIN PAGE ────────────────────────────────────────────────────────────
_, col, _ = st.columns([2, 3, 2])

with col:
    # ── Top of card ───────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:4rem 0 1rem;display:flex;flex-direction:column;
    align-items:center">
        <div style="font-family:'Geist Mono',monospace;font-size:1.1rem;
        font-weight:700;color:#0a0a0a;letter-spacing:-0.5px;
        margin-bottom:2.5rem">SENTINEL(ML)</div>
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);
        border-radius:14px;padding:2.5rem;width:100%">
            <div style="font-family:'Geist',sans-serif;font-size:1.3rem;
            font-weight:700;color:#0a0a0a;letter-spacing:-0.5px;
            margin-bottom:0.4rem">Sign in</div>
            <div style="font-family:'Geist',sans-serif;font-size:0.875rem;
            color:#888;line-height:1.5;margin-bottom:1.5rem">
                Sign in with GitHub to access the ML security auditor.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── OAuth button ───────────────────────────────────────────────────
    result = oauth2.authorize_button(
        name="Continue with GitHub",
        icon="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        redirect_uri=redirect_uri,
        scope="read:user",
        key="github_oauth",
        use_container_width=True,
    )

    if result and "token" in result:
        token     = result["token"].get("access_token", "")
        user_data = fetch_github_user(token)

        if user_data:
            st.session_state.user = user_data
            st.rerun()
        else:
            st.markdown("""
            <div style="font-family:'Geist Mono',monospace;font-size:0.78rem;
            color:#c0392b;padding:0.75rem 1rem;background:#fef0ef;
            border-radius:8px;border:1px solid #f5c6c2;margin-top:1rem">
            ✗ Login failed — could not fetch GitHub profile. Please try again.
            </div>
            """, unsafe_allow_html=True)
