"""Alert system for ranking changes.

Supports email and webhook notifications when material rankings change significantly.

Configuration via .streamlit/secrets.toml or environment variables:

[alerts]
enabled = true
threshold_rank_change = 2  # Alert if rank changes by this much
threshold_score_change = 0.5  # Alert if score changes by this much

[alerts.email]
enabled = true
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "alerts@example.com"
sender_password = "app-password"
recipient_emails = ["user@example.com"]

[alerts.webhook]
enabled = true
url = "https://hooks.slack.com/services/..."
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib

import pandas as pd

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"
SNAPSHOT_FILE = DATA_DIR / ".rankings_snapshot.json"


def get_current_rankings() -> dict:
    """Get current rankings from processed data."""
    filepath = PROCESSED_DIR / "materials_master.csv"
    if not filepath.exists():
        return {}

    df = pd.read_csv(filepath)
    return {
        row["material"]: {
            "rank": int(row["rank"]),
            "score": round(row["composite_score"], 2),
            "criticality": row.get("criticality_category", "Unknown"),
        }
        for _, row in df.iterrows()
    }


def load_snapshot() -> dict:
    """Load previous rankings snapshot."""
    if SNAPSHOT_FILE.exists():
        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_snapshot(rankings: dict):
    """Save current rankings as snapshot."""
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "rankings": rankings,
    }
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshot, f, indent=2)


def detect_changes(
    current: dict,
    previous: dict,
    rank_threshold: int = 2,
    score_threshold: float = 0.5,
) -> list:
    """Detect significant ranking changes.

    Args:
        current: Current rankings dict
        previous: Previous rankings dict
        rank_threshold: Alert if rank changes by this much
        score_threshold: Alert if score changes by this much

    Returns:
        List of change dictionaries
    """
    if not previous.get("rankings"):
        return []

    changes = []
    prev_rankings = previous["rankings"]

    for material, data in current.items():
        if material not in prev_rankings:
            changes.append({
                "material": material,
                "type": "new",
                "message": f"New material added: {material} (Rank #{data['rank']})",
            })
            continue

        prev = prev_rankings[material]
        rank_change = prev["rank"] - data["rank"]
        score_change = data["score"] - prev["score"]

        if abs(rank_change) >= rank_threshold:
            direction = "improved" if rank_change > 0 else "dropped"
            changes.append({
                "material": material,
                "type": "rank_change",
                "old_rank": prev["rank"],
                "new_rank": data["rank"],
                "change": rank_change,
                "message": f"{material} {direction} from #{prev['rank']} to #{data['rank']}",
            })

        if abs(score_change) >= score_threshold:
            direction = "increased" if score_change > 0 else "decreased"
            changes.append({
                "material": material,
                "type": "score_change",
                "old_score": prev["score"],
                "new_score": data["score"],
                "change": round(score_change, 2),
                "message": f"{material} score {direction} from {prev['score']} to {data['score']}",
            })

    # Check for removed materials
    for material in prev_rankings:
        if material not in current:
            changes.append({
                "material": material,
                "type": "removed",
                "message": f"Material removed: {material}",
            })

    return changes


def format_alert_message(changes: list, format_type: str = "text") -> str:
    """Format changes into alert message.

    Args:
        changes: List of change dictionaries
        format_type: 'text', 'html', or 'markdown'
    """
    if not changes:
        return ""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if format_type == "html":
        lines = [
            "<h2>Materials Priority Tool - Ranking Changes</h2>",
            f"<p><em>Detected at {timestamp}</em></p>",
            "<ul>",
        ]
        for change in changes:
            lines.append(f"<li><strong>{change['material']}</strong>: {change['message']}</li>")
        lines.append("</ul>")
        lines.append("<p>View the dashboard for full details.</p>")
        return "\n".join(lines)

    elif format_type == "markdown":
        lines = [
            "## Materials Priority Tool - Ranking Changes",
            f"*Detected at {timestamp}*",
            "",
        ]
        for change in changes:
            lines.append(f"- **{change['material']}**: {change['message']}")
        lines.append("")
        lines.append("View the dashboard for full details.")
        return "\n".join(lines)

    else:  # text
        lines = [
            "Materials Priority Tool - Ranking Changes",
            f"Detected at {timestamp}",
            "-" * 40,
        ]
        for change in changes:
            lines.append(f"• {change['material']}: {change['message']}")
        lines.append("-" * 40)
        lines.append("View the dashboard for full details.")
        return "\n".join(lines)


def send_email_alert(
    changes: list,
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    recipient_emails: list,
) -> bool:
    """Send email alert for ranking changes.

    Returns:
        True if sent successfully, False otherwise
    """
    if not changes:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Materials Priority Alert: {len(changes)} ranking changes detected"
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipient_emails)

        text_content = format_alert_message(changes, "text")
        html_content = format_alert_message(changes, "html")

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())

        return True
    except Exception as e:
        print(f"Email alert failed: {e}")
        return False


def send_webhook_alert(changes: list, webhook_url: str) -> bool:
    """Send webhook alert (Slack, Teams, etc.).

    Returns:
        True if sent successfully, False otherwise
    """
    if not changes or not REQUESTS_AVAILABLE:
        return False

    try:
        message = format_alert_message(changes, "markdown")

        # Slack-compatible payload
        payload = {
            "text": f"Materials Priority Tool Alert: {len(changes)} changes detected",
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message},
                }
            ],
        }

        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Webhook alert failed: {e}")
        return False


def check_and_alert() -> dict:
    """Check for changes and send alerts if configured.

    Returns:
        Dict with check results
    """
    current = get_current_rankings()
    previous = load_snapshot()

    # Get config from Streamlit secrets or defaults
    config = {}
    if STREAMLIT_AVAILABLE:
        try:
            config = dict(st.secrets.get("alerts", {}))
        except Exception:
            pass

    enabled = config.get("enabled", False)
    rank_threshold = config.get("threshold_rank_change", 2)
    score_threshold = config.get("threshold_score_change", 0.5)

    changes = detect_changes(current, previous, rank_threshold, score_threshold)

    result = {
        "timestamp": datetime.now().isoformat(),
        "changes_detected": len(changes),
        "changes": changes,
        "alerts_sent": [],
    }

    if enabled and changes:
        # Email alerts
        email_config = config.get("email", {})
        if email_config.get("enabled"):
            success = send_email_alert(
                changes,
                email_config.get("smtp_server", ""),
                email_config.get("smtp_port", 587),
                email_config.get("sender_email", ""),
                email_config.get("sender_password", ""),
                email_config.get("recipient_emails", []),
            )
            if success:
                result["alerts_sent"].append("email")

        # Webhook alerts
        webhook_config = config.get("webhook", {})
        if webhook_config.get("enabled"):
            success = send_webhook_alert(changes, webhook_config.get("url", ""))
            if success:
                result["alerts_sent"].append("webhook")

    # Save new snapshot
    save_snapshot(current)

    return result


def render_alert_status():
    """Render alert status in Streamlit UI."""
    if not STREAMLIT_AVAILABLE:
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("Alert Status")

    try:
        config = dict(st.secrets.get("alerts", {}))
        if config.get("enabled"):
            st.sidebar.success("🔔 Alerts enabled")

            if config.get("email", {}).get("enabled"):
                st.sidebar.caption("📧 Email alerts active")
            if config.get("webhook", {}).get("enabled"):
                st.sidebar.caption("🔗 Webhook alerts active")
        else:
            st.sidebar.info("🔕 Alerts disabled")
    except Exception:
        st.sidebar.info("🔕 Alerts not configured")
