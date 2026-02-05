"""Theme management for Materials Priority Tool.

Provides dark/light mode toggle functionality.
"""

import streamlit as st

# Theme configurations
LIGHT_THEME = {
    "name": "light",
    "background": "#ffffff",
    "secondary_background": "#f0f2f6",
    "text": "#262730",
    "primary": "#1f77b4",
}

DARK_THEME = {
    "name": "dark",
    "background": "#0e1117",
    "secondary_background": "#262730",
    "text": "#fafafa",
    "primary": "#4da6ff",
}


def init_theme():
    """Initialize theme in session state."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"


def get_current_theme() -> dict:
    """Get current theme configuration."""
    init_theme()
    return DARK_THEME if st.session_state.theme == "dark" else LIGHT_THEME


def toggle_theme():
    """Toggle between light and dark theme."""
    init_theme()
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


def render_theme_toggle():
    """Render theme toggle in sidebar."""
    init_theme()

    current = st.session_state.theme
    icon = "🌙" if current == "light" else "☀️"
    label = "Dark Mode" if current == "light" else "Light Mode"

    if st.sidebar.button(f"{icon} {label}", key="theme_toggle"):
        toggle_theme()
        st.rerun()


def apply_theme_css():
    """Apply current theme as custom CSS."""
    init_theme()
    theme = get_current_theme()

    if st.session_state.theme == "dark":
        st.markdown(f"""
        <style>
            /* Dark mode overrides */
            .stApp {{
                background-color: {theme['background']};
            }}

            .stMarkdown, .stText, p, span, label, .stMetricValue, .stMetricLabel {{
                color: {theme['text']} !important;
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: {theme['text']} !important;
            }}

            .stDataFrame {{
                background-color: {theme['secondary_background']};
            }}

            .stExpander {{
                background-color: {theme['secondary_background']};
                border-color: #444;
            }}

            .stSelectbox > div > div,
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input {{
                background-color: {theme['secondary_background']} !important;
                color: {theme['text']} !important;
            }}

            .stSlider > div > div > div {{
                background-color: {theme['primary']} !important;
            }}

            .feature-card {{
                background: {theme['secondary_background']} !important;
                border-left-color: {theme['primary']} !important;
            }}

            .feature-card h4, .feature-card p {{
                color: {theme['text']} !important;
            }}

            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {theme['secondary_background']};
            }}

            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] label {{
                color: {theme['text']} !important;
            }}

            /* Tables */
            .stDataFrame td, .stDataFrame th {{
                color: {theme['text']} !important;
            }}

            /* Metrics */
            [data-testid="stMetricValue"] {{
                color: {theme['text']} !important;
            }}

            [data-testid="stMetricDelta"] {{
                color: #888 !important;
            }}

            /* Expander header */
            .streamlit-expanderHeader {{
                color: {theme['text']} !important;
                background-color: {theme['secondary_background']} !important;
            }}

            /* Caption */
            .stCaption {{
                color: #888 !important;
            }}

            /* Buttons - fix white text on white background */
            .stButton > button {{
                background-color: {theme['secondary_background']} !important;
                color: {theme['text']} !important;
                border: 1px solid #444 !important;
            }}

            .stButton > button:hover {{
                background-color: #3a3a4a !important;
                color: {theme['text']} !important;
                border-color: {theme['primary']} !important;
            }}

            /* Primary buttons */
            .stButton > button[kind="primary"],
            .stButton > button[data-testid="baseButton-primary"] {{
                background-color: {theme['primary']} !important;
                color: white !important;
                border: none !important;
            }}

            /* Download buttons */
            .stDownloadButton > button {{
                background-color: {theme['secondary_background']} !important;
                color: {theme['text']} !important;
                border: 1px solid #444 !important;
            }}

            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: {theme['secondary_background']};
            }}

            .stTabs [data-baseweb="tab"] {{
                color: {theme['text']} !important;
                background-color: transparent !important;
            }}

            .stTabs [aria-selected="true"] {{
                background-color: {theme['background']} !important;
                color: {theme['primary']} !important;
            }}

            /* Radio buttons and checkboxes */
            .stRadio > div,
            .stCheckbox > div {{
                color: {theme['text']} !important;
            }}

            /* Multiselect */
            .stMultiSelect > div > div {{
                background-color: {theme['secondary_background']} !important;
                color: {theme['text']} !important;
            }}

            /* Links */
            a {{
                color: {theme['primary']} !important;
            }}

            /* Sidebar navigation links */
            section[data-testid="stSidebar"] a {{
                color: {theme['text']} !important;
            }}

            section[data-testid="stSidebar"] a:hover {{
                color: {theme['primary']} !important;
            }}
        </style>
        """, unsafe_allow_html=True)

    # Mobile responsive CSS (applied for both themes)
    st.markdown("""
    <style>
        /* Mobile responsive styles */
        @media (max-width: 768px) {
            /* Reduce padding on mobile */
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1rem;
            }

            /* Stack columns on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }

            /* Smaller headings on mobile */
            h1 {
                font-size: 1.75rem !important;
            }

            h2 {
                font-size: 1.4rem !important;
            }

            h3 {
                font-size: 1.2rem !important;
            }

            /* Better metric display on mobile */
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }

            [data-testid="stMetricLabel"] {
                font-size: 0.85rem !important;
            }

            /* Touch-friendly buttons */
            .stButton > button {
                min-height: 44px;
                padding: 0.5rem 1rem;
            }

            /* Better table scrolling */
            .stDataFrame {
                overflow-x: auto;
            }

            /* Responsive feature cards */
            .feature-card {
                margin-bottom: 1rem;
                padding: 15px !important;
            }

            /* Sidebar adjustments */
            section[data-testid="stSidebar"] {
                width: 100% !important;
            }

            /* Better chart container */
            .stPlotlyChart {
                overflow-x: auto;
            }
        }

        /* Tablet responsive styles */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }

            h1 {
                font-size: 2rem !important;
            }
        }

        /* General improvements for all screen sizes */
        .stDataFrame {
            width: 100%;
        }

        /* Smooth transitions */
        .stButton > button,
        .stSelectbox,
        .stSlider {
            transition: all 0.2s ease;
        }

        /* Better focus states for accessibility */
        .stButton > button:focus,
        .stSelectbox:focus-within,
        input:focus {
            outline: 2px solid #667eea;
            outline-offset: 2px;
        }

        /* Improve readability of long tables */
        .stDataFrame td {
            white-space: nowrap;
        }
    </style>
    """, unsafe_allow_html=True)
