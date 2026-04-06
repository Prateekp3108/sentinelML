import streamlit as st
import requests


def is_logged_in():
    return st.session_state.get("user") is not None


def get_user():
    return st.session_state.get("user")


def get_tier():
    return st.session_state.get("user_tier")


def has_selected_tier():
    return st.session_state.get("user_tier") is not None


def logout():
    st.session_state.user      = None
    st.session_state.user_tier = None
    st.session_state.pop("model_result",   None)
    st.session_state.pop("attack_results", None)
    st.session_state.pop("trojan_results", None)
    st.session_state.pop("ai_response",    None)
    st.session_state.pop("ai_tier",        None)


def fetch_github_user(token):
    """
    Fetches GitHub user profile using the OAuth access token.
    Returns dict with login, name, avatar_url or None on failure.
    """
    try:
        r = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            },
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "login":      data.get("login", ""),
                "name":       data.get("name") or data.get("login", ""),
                "avatar_url": data.get("avatar_url", ""),
                "token":      token
            }
    except Exception:
        pass
    return None


def require_auth():
    """
    Call at the top of any page that requires authentication.
    Redirects to login if not logged in.
    Redirects to tier selection if tier not yet chosen.
    """
    if not is_logged_in():
        st.switch_page("pages/login.py")
    if not has_selected_tier():
        st.switch_page("pages/tier_select.py")


def navbar_auth_block():
    """
    Returns HTML for the auth portion of the navbar —
    shows avatar + username + logout button when logged in.
    """
    user = get_user()
    if not user:
        return ""

    login  = user.get("login", "")
    avatar = user.get("avatar_url", "")

    return f"""
    <div style="display:flex;align-items:center;gap:0.75rem">
        <img src="{avatar}" width="26" height="26"
             style="border-radius:50%;border:1px solid rgba(0,0,0,0.1)"/>
        <span style="font-family:'Geist',sans-serif;font-size:0.825rem;
        color:#444">{login}</span>
    </div>
    """