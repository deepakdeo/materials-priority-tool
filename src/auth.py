"""Simple password authentication for Materials Priority Tool.

To enable authentication:
1. Create .streamlit/secrets.toml with:
   [auth]
   enabled = true
   password = "your-secure-password"

2. For Streamlit Cloud, add these secrets in the dashboard.

If auth is not configured, the app runs without password protection.
"""

import streamlit as st


def check_password() -> bool:
    """Check if user has entered correct password.

    Returns:
        True if authenticated or auth disabled, False if authentication failed.
    """
    # Check if auth is enabled in secrets
    try:
        auth_enabled = st.secrets.get("auth", {}).get("enabled", False)
        if not auth_enabled:
            return True  # Auth disabled, allow access
    except Exception:
        return True  # No secrets configured, allow access

    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Already authenticated
    if st.session_state.authenticated:
        return True

    # Show login form
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 🔐 Materials Priority Tool")
        st.markdown("Please enter the password to access the dashboard.")

        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login", type="primary", use_container_width=True):
            try:
                correct_password = st.secrets["auth"]["password"]
                if password == correct_password:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
            except Exception as e:
                st.error(f"Authentication error: {e}")

        st.markdown("---")
        st.caption("Contact your administrator if you need access.")

    return False


def logout():
    """Log out the current user."""
    st.session_state.authenticated = False
    st.rerun()


def render_logout_button():
    """Render logout button in sidebar if authenticated."""
    try:
        auth_enabled = st.secrets.get("auth", {}).get("enabled", False)
        if not auth_enabled:
            return
    except Exception:
        return

    if st.session_state.get("authenticated", False):
        if st.sidebar.button("🚪 Logout"):
            logout()
