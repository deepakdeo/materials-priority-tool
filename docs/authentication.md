# Authentication Setup

The Materials Priority Tool supports optional password protection. When enabled, users must enter a password to access the dashboard.

## Enabling Password Protection

### For Local Development

1. Create a secrets file at `.streamlit/secrets.toml`:

```toml
[auth]
enabled = true
password = "your-secure-password"
```

2. The `.streamlit/secrets.toml` file is gitignored by default for security.

3. Restart the Streamlit app.

### For Streamlit Cloud

1. Go to your app dashboard at [share.streamlit.io](https://share.streamlit.io)

2. Click on your app → **Settings** → **Secrets**

3. Add the following secrets:

```toml
[auth]
enabled = true
password = "your-secure-password"
```

4. Click **Save**. The app will automatically restart.

## Disabling Password Protection

To run the app without authentication:

1. Set `enabled = false` in secrets, OR
2. Remove the `[auth]` section entirely, OR
3. Don't create a secrets file at all

## Security Notes

- **Never commit passwords** to version control
- Use a strong, unique password
- For production, consider using Streamlit's native authentication or an identity provider
- The password is transmitted securely over HTTPS on Streamlit Cloud
- Sessions are stored in browser memory and cleared on tab close

## Logout

When authentication is enabled, a "Logout" button appears in the sidebar. Clicking it clears the session and returns to the login screen.

## Troubleshooting

### "Authentication error" message
- Check that secrets are properly formatted (TOML syntax)
- Verify the `[auth]` section exists with both `enabled` and `password` keys

### Can't access after setting password
- Clear browser cache and cookies
- Try incognito/private browsing mode
- Verify the password matches exactly (case-sensitive)

### Password not working on Streamlit Cloud
- Go to app Settings → Secrets and verify the format
- Check for trailing spaces in the password
- Redeploy the app after changing secrets
