import streamlit as st
import requests
import hashlib
import json
import base64

def _encode_token(data: dict) -> str:
    """Simple base64 encoding of user data for URL storage."""
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def _decode_token(token: str) -> dict:
    try:
        return json.loads(base64.urlsafe_b64decode(token.encode()).decode())
    except:
        return {}

def is_logged_in() -> bool:
    # Check session state first
    if "user" in st.session_state and st.session_state["user"]:
        return True
    # Fall back to query param
    _restore_from_query()
    return "user" in st.session_state and bool(st.session_state["user"])

def has_selected_tier() -> bool:
    if not is_logged_in():
        return False
    return "user_tier" in st.session_state and bool(st.session_state["user_tier"])

def get_user() -> dict:
    is_logged_in()  # ensures restore attempt
    return st.session_state.get("user", {})

def get_tier() -> str:
    return st.session_state.get("user_tier", "student")

def logout():
    st.session_state.user = None
    st.session_state.user_tier = None
    st.query_params.clear()

def require_auth():
    if not is_logged_in():
        st.switch_page("pages/login.py")
        st.stop()
    if not has_selected_tier():
        st.switch_page("pages/tier_select.py")
        st.stop()

def _restore_from_query():
    """Try to restore session from URL query params."""
    params = st.query_params
    if "auth" in params:
        data = _decode_token(params["auth"])
        if data.get("user"):
            st.session_state.user = data["user"]
        if data.get("tier"):
            st.session_state.user_tier = data["tier"]

def persist_to_query():
    """Save current auth state to URL query params so it survives navigation."""
    user = st.session_state.get("user")
    tier = st.session_state.get("user_tier")
    if user:
        token = _encode_token({"user": user, "tier": tier})
        st.query_params["auth"] = token

def fetch_github_user(access_token: str) -> dict:
    resp = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"},
        timeout=10
    )
    if resp.status_code == 200:
        return resp.json()
    return {}