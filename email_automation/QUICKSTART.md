# Email Automation System - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Configure SMTP Settings (2 minutes)

Edit the `.env` file with your email provider settings:

#### Gmail Setup
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Your Name
```
** Important**: Use [App Password](https://myaccount.google.com/apppasswords), not your regular password

#### Outlook/Microsoft 365
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your_email@outlook.com
SENDER_PASSWORD=your_password
SENDER_NAME=Your Name
```

### Step 3: Verify Setup (2 minutes)
```bash
python setup_validation.py
```

## Getting Started

### Option A: Interactive CLI (Easiest)
```bash
python main.py
```
Follow the menu to send emails, view config, or access help. When prompted, you can optionally select attachments using the file dialog for both single and bulk email sends.

### Option B: Run Examples
```bash
# Send single email
python examples/single_email.py

# Send bulk email
python examples/bulk_email.py

# Send with attachment
python examples/email_with_attachment.py

# Send HTML email
python examples/html_email.py
```

### Option C: Use in Your Code
```python
from email_sender import EmailSender

sender = EmailSender()
success, msg = sender.send_email(
 recipient="user@example.com",
 subject="Hello",
 body="Test email"
)
print(msg)
```

## Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'dotenv'` | Run: `pip install -r requirements.txt` |
| `AuthenticationError: Invalid credentials` | Check SENDER_EMAIL and SENDER_PASSWORD in .env |
| `SMTPConnectionError` | Verify SMTP_SERVER and SMTP_PORT in .env |
| `Validation error: Invalid email` | Check recipient email format (user@domain.com) |

## Project Features Implemented

 **Email Sending** - Single and bulk recipient support 
 **SMTP Integration** - Secure TLS connection and authentication 
 **Input Validation** - RFC 5322 email validation 
 **Attachments** - File attachment support 
 **Bulk Sending** - Send to multiple recipients 
 **Error Handling** - Meaningful error messages 
 **Logging** - Automatic CSV report generation 
 **Security** - Environment variables, no hardcoded credentials 
 **Performance** - < 10 seconds per email 
 **User Feedback** - Success/failure confirmation 

## File Overview

```
email_automation/
├── main.py # Interactive CLI app (START HERE)
├── email_sender.py # Core email sending module
├── requirements.txt # Python dependencies
├── .env # Your SMTP configuration
├── .env.example # Configuration template
├── README.md # Full documentation
├── setup_validation.py # Setup verification script
│
├── config/
│ └── settings.py # Configuration loader
│
├── utils/
│ ├── validators.py # Email validation
│ ├── logger.py # Logging system
│ └── exceptions.py # Custom exceptions
│
├── examples/
│ ├── single_email.py # Send 1 email
│ ├── bulk_email.py # Send multiple
│ ├── email_with_attachment.py
│ └── html_email.py
│
└── logs/
 ├── email_automation.log # Activity logs
 └── email_report.csv # Delivery report
```

## Next Steps

1. **Configure**: Edit `.env` with your email settings
2. **Verify**: Run `python setup_validation.py`
3. **Test**: Run `python examples/single_email.py`
4. **Use**: Run `python main.py` or integrate into your code

## Key Features Explained

### Email Validation
- Validates email format before sending
- Catches typos and invalid addresses
- Prevents sending to invalid recipients

### Logging & Reporting
- Automatic `email_report.csv` created in `logs/` folder
- Tracks all sent emails with timestamp, recipient, status
- Useful for auditing and tracking deliveries

### Error Handling
- Clear error messages for configuration issues
- Connection errors reported with details
- Failed emails logged with reasons

### Security
- No credentials hardcoded in code
- All sensitive data in `.env` file
- `.env` excluded from git repository
- TLS encryption for SMTP connections

## Support Resources

- **Full Documentation**: See `README.md`
- **Examples**: Check `examples/` folder
- **Logs**: Check `logs/email_automation.log` for debugging
- **Configuration**: Review `.env.example` for all options

---

**Ready to send emails?** Run: `python main.py`

Developed by Neha P
