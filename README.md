# Email Automation System

A Python-based application for sending emails using SMTP with support for bulk emails, attachments, validation, logging, and secure credential management.

## Features

* Single and bulk email sending
* Plain text and HTML emails
* Multiple file attachments
* SMTP authentication with TLS
* Email and attachment validation
* Logging and CSV reporting
* Environment variable configuration (`.env`)
* Error handling and user feedback

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Your Name
```

## Run

```bash
python main.py
```

## Logs

Generated automatically:

```text
logs/email_automation.log
logs/email_report.csv
```

## Security

* No hardcoded credentials
* TLS-encrypted connections
* Secure environment variable storage
* Input validation before sending

## Acceptance Criteria

✔ Send emails to single or multiple recipients

✔ SMTP authentication and secure delivery

✔ Attachment support

✔ Bulk email support

✔ Input validation

✔ Error handling and logging

✔ CSV reporting

✔ Success/failure notifications

## Version

**Email Automation System v1.0**

Developed by Neha P
