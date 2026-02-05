# Alerts Setup Guide

The Materials Priority Tool can send notifications when rankings change significantly. This is useful for ongoing monitoring.

## Supported Alert Channels

1. **Email** - SMTP-based email notifications
2. **Webhooks** - Slack, Microsoft Teams, or custom endpoints

## Configuration

### Via Streamlit Secrets

Add to `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets:

```toml
[alerts]
enabled = true
threshold_rank_change = 2      # Alert if rank changes by 2+ positions
threshold_score_change = 0.5   # Alert if score changes by 0.5+ points

[alerts.email]
enabled = true
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"
recipient_emails = ["recipient1@example.com", "recipient2@example.com"]

[alerts.webhook]
enabled = true
url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

## Email Setup

### Gmail Setup

1. Go to Google Account → Security → 2-Step Verification (enable it)
2. Go to App Passwords → Generate new app password
3. Use that password in `sender_password`

### Other SMTP Providers

| Provider | Server | Port |
|----------|--------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| SendGrid | smtp.sendgrid.net | 587 |

## Webhook Setup

### Slack

1. Go to your Slack workspace → Apps → Incoming Webhooks
2. Create new webhook for your channel
3. Copy the webhook URL

### Microsoft Teams

1. In Teams channel → Connectors → Incoming Webhook
2. Configure and copy the webhook URL

### Custom Webhooks

The system sends JSON payloads compatible with Slack's format:

```json
{
  "text": "Materials Priority Tool Alert: 2 changes detected",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "## Materials Priority Tool - Ranking Changes\n..."
      }
    }
  ]
}
```

## Alert Triggers

Alerts are triggered when:

1. **Rank changes** by configured threshold (default: 2 positions)
   - Example: Lithium moves from #1 to #3

2. **Score changes** by configured threshold (default: 0.5 points)
   - Example: Graphite score goes from 6.76 to 7.30

3. **Materials added or removed**
   - Example: New material "Copper" added at rank #10

## Manual Alert Check

To manually check for changes and send alerts:

```python
from src.alerts import check_and_alert

result = check_and_alert()
print(f"Changes detected: {result['changes_detected']}")
print(f"Alerts sent: {result['alerts_sent']}")
```

## How It Works

1. System saves a snapshot of current rankings
2. On next check, compares current vs. snapshot
3. If changes exceed thresholds, sends alerts
4. Saves new snapshot

Snapshots are stored in `data/.rankings_snapshot.json` (gitignored).

## Testing

To test your configuration:

1. Make a small change to `data/reference/materials_baseline.csv`
2. Run `python -m src.data_processor` to regenerate scores
3. Run the alert check: `python -c "from src.alerts import check_and_alert; print(check_and_alert())"`
4. Check your email/Slack for the alert

## Troubleshooting

### Email not sending
- Check SMTP credentials
- For Gmail, ensure "Less secure apps" is enabled OR use App Password
- Check firewall allows outbound SMTP (port 587)

### Webhook not working
- Verify URL is correct
- Check webhook is active in Slack/Teams
- Look for error messages in console output

### No alerts despite changes
- Check `enabled = true` in config
- Verify changes exceed thresholds
- Check that snapshot file exists after first run
