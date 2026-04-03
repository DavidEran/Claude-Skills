#!/usr/bin/env python3
"""
Send Email Script
Sends an email via SMTP. Supports Gmail, Outlook, and generic SMTP servers.

Usage:
    python3 send_email.py --to recipient@example.com \
                          --subject "Subject" \
                          --body "Message body" \
                          [--from sender@example.com] \
                          [--smtp-host smtp.gmail.com] \
                          [--smtp-port 587] \
                          [--username user@gmail.com] \
                          [--password "app_password"] \
                          [--html]

Environment variables (alternative to flags):
    EMAIL_FROM      - Sender email address
    EMAIL_USERNAME  - SMTP username (often same as EMAIL_FROM)
    EMAIL_PASSWORD  - SMTP password or app password
    SMTP_HOST       - SMTP server hostname (default: smtp.gmail.com)
    SMTP_PORT       - SMTP server port (default: 587)
"""

import argparse
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(
    to: str,
    subject: str,
    body: str,
    from_addr: str = None,
    smtp_host: str = None,
    smtp_port: int = None,
    username: str = None,
    password: str = None,
    is_html: bool = False,
) -> bool:
    """Send an email via SMTP. Returns True on success."""
    from_addr = from_addr or os.environ.get("EMAIL_FROM")
    username = username or os.environ.get("EMAIL_USERNAME") or from_addr
    password = password or os.environ.get("EMAIL_PASSWORD")
    smtp_host = smtp_host or os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = smtp_port or int(os.environ.get("SMTP_PORT", "587"))

    if not from_addr:
        print("Error: Sender address required (--from or EMAIL_FROM env var)", file=sys.stderr)
        return False
    if not password:
        print("Error: SMTP password required (--password or EMAIL_PASSWORD env var)", file=sys.stderr)
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to

    content_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body, content_type))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(from_addr, [to], msg.as_string())
        print(f"Email sent successfully to {to}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP authentication failed. Check username/password.", file=sys.stderr)
        return False
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Send an email via SMTP")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body")
    parser.add_argument("--from", dest="from_addr", help="Sender email address")
    parser.add_argument("--smtp-host", help="SMTP server hostname (default: smtp.gmail.com)")
    parser.add_argument("--smtp-port", type=int, help="SMTP server port (default: 587)")
    parser.add_argument("--username", help="SMTP username")
    parser.add_argument("--password", help="SMTP password or app password")
    parser.add_argument("--html", action="store_true", help="Treat body as HTML")
    args = parser.parse_args()

    success = send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        from_addr=args.from_addr,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        username=args.username,
        password=args.password,
        is_html=args.html,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
