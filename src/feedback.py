"""Feedback widget for Materials Priority Tool.

Allows users to submit feedback directly from the app.
Feedback is stored locally in a JSON file for review.
"""

import json
import streamlit as st
from datetime import datetime
from pathlib import Path

# Feedback storage
FEEDBACK_FILE = Path(__file__).parent.parent / "data" / ".feedback.json"


def load_feedback() -> list:
    """Load existing feedback from file."""
    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_feedback(feedback: dict):
    """Save feedback to file."""
    existing = load_feedback()
    existing.append(feedback)

    # Ensure directory exists
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(existing, f, indent=2)


def render_feedback_widget():
    """Render feedback widget in sidebar."""
    st.sidebar.markdown("---")

    with st.sidebar.expander("💬 Send Feedback", expanded=False):
        st.markdown("Help us improve this tool!")

        # Feedback type
        feedback_type = st.selectbox(
            "Type",
            ["General Feedback", "Bug Report", "Feature Request", "Data Issue", "Other"],
            key="feedback_type"
        )

        # Rating
        rating = st.slider(
            "How useful is this tool?",
            min_value=1,
            max_value=5,
            value=4,
            key="feedback_rating",
            help="1 = Not useful, 5 = Very useful"
        )

        # Stars display
        stars = "⭐" * rating + "☆" * (5 - rating)
        st.caption(stars)

        # Message
        message = st.text_area(
            "Your feedback",
            placeholder="Tell us what you think, report a bug, or suggest a feature...",
            key="feedback_message",
            height=100
        )

        # Email (optional)
        email = st.text_input(
            "Email (optional)",
            placeholder="your@email.com",
            key="feedback_email",
            help="If you'd like us to follow up"
        )

        # Submit button
        if st.button("Submit Feedback", key="submit_feedback", type="primary"):
            if message.strip():
                feedback = {
                    "timestamp": datetime.now().isoformat(),
                    "type": feedback_type,
                    "rating": rating,
                    "message": message.strip(),
                    "email": email.strip() if email else None,
                    "page": st.session_state.get("current_page", "Unknown"),
                }

                save_feedback(feedback)
                st.success("✓ Thank you for your feedback!")
                st.balloons()
            else:
                st.warning("Please enter a message")

        # GitHub issues link
        st.markdown("---")
        st.markdown(
            "🐛 Found a bug? [Open an issue on GitHub]"
            "(https://github.com/deepakdeo/materials-priority-tool/issues)"
        )


def render_feedback_badge():
    """Render a small feedback prompt at the bottom of pages."""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style="text-align: center; padding: 10px; background: #f0f2f6; border-radius: 10px;">
                <p style="margin: 0;">💬 <strong>Have feedback?</strong> Use the feedback form in the sidebar!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
