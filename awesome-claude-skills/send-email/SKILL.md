---
name: send-email
description: Send emails via SMTP directly from Claude. This skill should be used when the user asks Claude to send an email, test email delivery, or automate email sending via Gmail, Outlook, or any SMTP server.
---

# Send Email

## Overview

To send emails programmatically using Python's `smtplib` via any SMTP provider (Gmail, Outlook, SendGrid, or custom servers), use the `scripts/send_email.py` script included in this skill.

## Setup

### Gmail (recommended for testing)

1. Enable 2-factor authentication on the Google account
2. Generate an App Password: Google Account → Security → App Passwords
3. Set environment variables:

```bash
export EMAIL_FROM="you@gmail.com"
export EMAIL_PASSWORD="your-16-char-app-password"
```

### Other providers

```bash
export EMAIL_FROM="you@example.com"
export EMAIL_USERNAME="you@example.com"   # if different from EMAIL_FROM
export EMAIL_PASSWORD="your-password"
export SMTP_HOST="smtp.example.com"       # default: smtp.gmail.com
export SMTP_PORT="587"                    # default: 587
```

## Sending an Email

### Basic usage

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Test Email" \
  --body "Hello, this is a test email."
```

### With explicit credentials (overrides env vars)

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Hello" \
  --body "Message body here" \
  --from sender@gmail.com \
  --password "app-password-here"
```

### HTML email

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "HTML Email" \
  --body "<h1>Hello</h1><p>This is an <b>HTML</b> email.</p>" \
  --html
```

### Outlook / Office 365

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Test" \
  --body "Message" \
  --smtp-host smtp.office365.com \
  --smtp-port 587
```

## Workflow

To send an email:

1. Check whether `EMAIL_FROM` and `EMAIL_PASSWORD` are set in the environment
2. If credentials are missing, prompt the user to set them or pass via `--from` and `--password`
3. Run `scripts/send_email.py` with the appropriate flags
4. Confirm success or report the error message

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `SMTPAuthenticationError` | Wrong credentials | Use App Password for Gmail, not account password |
| `Connection refused` | Wrong host/port | Verify SMTP_HOST and SMTP_PORT |
| `Sender address required` | Missing EMAIL_FROM | Set `--from` flag or `EMAIL_FROM` env var |

## Keywords

send email, test email, SMTP, Gmail, Outlook, email automation, transactional email
