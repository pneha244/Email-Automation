# Email Automation System

A comprehensive Python-based email automation solution with SMTP integration, bulk sending capabilities, attachment support, and professional logging.

## Features

### Email Sending
- Send emails to single or multiple recipients
- Support for plain text and HTML content
- Configurable sender name and email

### SMTP Integration
- Secure SMTP connection with TLS encryption
- Automatic authentication with configured credentials
- Support for multiple SMTP servers (Gmail, Outlook, etc.)
- Connection timeout handling

### Input Validation
- RFC 5322 compliant email address validation
- Email subject and body validation
- File attachment existence verification
- Recipient list validation with detailed error reporting

### Attachment Support
- Attach single or multiple files
- Optional file picker selection for attachments in the CLI
- Automatic MIME type detection
- Base64 encoding for secure transmission
- File existence and accessibility checks

### Bulk Email Support
- Send to multiple recipients efficiently
- Individual email delivery to each recipient
- Optional attachments for bulk sends via CLI file picker
- Detailed success/failure reporting
- Summary statistics

### Error Handling
- Meaningful error messages for all failure scenarios
- Specific exceptions for different error types
- Failed delivery logging
- Connection and authentication error handling

### Logging and Reporting
- Timestamp-based logging of all sent emails
- CSV report file generation (`logs/email_report.csv`)
- Success/failure status tracking
- Detailed error information in logs

### Security
- No hardcoded credentials
- Environment variable configuration via `.env` file
- TLS encryption for all SMTP connections
- Sensitive information protection

### Performance
- Email delivery typically completes in < 5 seconds
- Connection pooling support
- Timeout management for network issues

### User Feedback
- Success confirmation messages
- Detailed error notifications
- Real-time sending progress
- Delivery time reporting

## Project Structure

```
email_automation/
├── config/
│ ├── __init__.py
│ └── settings.py # Configuration management
├── utils/
│ ├── __init__.py
│ ├── validators.py # Email validation
│ ├── logger.py # Logging system
│ └── exceptions.py # Custom exceptions
├── examples/
│ ├── single_email.py # Single email example
│ ├── bulk_email.py # Bulk email example
│ ├── email_with_attachment.py # Attachment example
│ └── html_email.py # HTML email example
├── logs/ # Auto-generated logs
├── email_sender.py # Main email sending module
├── main.py # Interactive CLI application
├── requirements.txt # Python dependencies
├── .env # Configuration (create from .env.example)
├── .env.example # Configuration template
└── README.md # This file
```

## Installation

### 1. Clone/Download Project
```bash
cd email_automation
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your SMTP credentials
# Edit with your preferred text editor
```

#### Configuration Details

Edit `.env` file with your email provider's settings:

**For Gmail:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SENDER_NAME=Your Name
```

*Note: For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.*

**For Outlook:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your_email@outlook.com
SENDER_PASSWORD=your_password
SENDER_NAME=Your Name
```

**For Custom SMTP:**
```env
SMTP_SERVER=your.smtp.server
SMTP_PORT=587
SENDER_EMAIL=your_email@domain.com
SENDER_PASSWORD=your_password
SENDER_NAME=Your Name
```

## Usage

### Interactive CLI Application
```bash
python main.py
```

Follow the on-screen menu to:
- Send single emails
- Send bulk emails
- Add attachments
- View configuration
- Access help

### Send Single Email (Programmatically)
```python
from email_sender import EmailSender

# Initialize
sender = EmailSender()

# Send email
success, message = sender.send_email(
 recipient="user@example.com",
 subject="Hello",
 body="This is a test email."
)

if success:
 print(f"Email sent: {message}")
else:
 print(f"Error: {message}")
```

### Send Bulk Email
```python
from email_sender import EmailSender

sender = EmailSender()

recipients = [
 "user1@example.com",
 "user2@example.com",
 "user3@example.com"
]

result = sender.send_bulk_emails(
 recipients=recipients,
 subject="Announcement",
 body="Important announcement for all users."
)

print(f"Sent: {result['success_count']}")
print(f"Failed: {result['failure_count']}")
```

### Send Email with Attachment
```python
from email_sender import EmailSender

sender = EmailSender()

success, message = sender.send_email(
 recipient="user@example.com",
 subject="Document",
 body="Please find the attached document.",
 attachments=["path/to/file.pdf", "path/to/image.png"]
)

print(message)
```

### Send HTML Email
```python
from email_sender import EmailSender

sender = EmailSender()

html_body = """
<html>
 <body>
 <h1>Welcome!</h1>
 <p>This is an <strong>HTML</strong> email.</p>
 </body>
</html>
"""

success, message = sender.send_email(
 recipient="user@example.com",
 subject="HTML Email",
 body=html_body,
 is_html=True
)

print(message)
```

## Examples

Located in the `examples/` directory:

### 1. Single Email (examples/single_email.py)
```bash
python examples/single_email.py
```
Basic example of sending a single email.

### 2. Bulk Email (examples/bulk_email.py)
```bash
python examples/bulk_email.py
```
Example of sending emails to multiple recipients with results summary.

### 3. Email with Attachment (examples/email_with_attachment.py)
```bash
python examples/email_with_attachment.py
```
Example of sending email with file attachments.

### 4. HTML Email (examples/html_email.py)
```bash
python examples/html_email.py
```
Example of sending formatted HTML emails.

## Logging and Reporting

### Log Files
- **Email Log**: `logs/email_automation.log`
 - Contains all sending activities with timestamps
 - Shows success and failure messages
 - Includes connection and authentication details

- **CSV Report**: `logs/email_report.csv`
 - Machine-readable format for analysis
 - Columns: Timestamp, Recipient, Subject, Status, Details
 - Useful for tracking delivery history

### Log Example
```
2024-06-07 10:30:45 - email_automation - INFO - Connecting to SMTP server: smtp.gmail.com:587
2024-06-07 10:30:47 - email_automation - INFO - Successfully authenticated with SMTP server
2024-06-07 10:30:48 - email_automation - INFO - Email to user@example.com | Subject: Test | Status: Success | Details: Sent in 0.89s
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ConfigurationError` | Missing .env file or credentials | Create `.env` from `.env.example` and fill in credentials |
| `AuthenticationError` | Invalid SMTP credentials | Verify username/password in `.env` file |
| `SMTPConnectionError` | Cannot connect to SMTP server | Check SMTP_SERVER and SMTP_PORT settings |
| `InvalidEmailError` | Invalid recipient email format | Verify email address format (user@domain.com) |
| `AttachmentError` | File not found or not readable | Check file path and permissions |

### Exception Types
```python
from utils.exceptions import (
 EmailAutomationException, # Base exception
 SMTPConnectionError, # Connection failures
 AuthenticationError, # Auth failures
 InvalidEmailError, # Invalid email addresses
 AttachmentError, # Attachment issues
 EmailSendError, # Sending failures
 ConfigurationError # Configuration issues
)
```

## Validation

### Email Address Validation
- RFC 5322 compliant pattern matching
- Maximum length checks (254 characters total, 64 local part)
- Format verification (user@domain.com)
- Rejection of obviously invalid addresses

### Content Validation
- Subject: Required, 1-255 characters
- Body: Required, non-empty string
- Recipients: Required, must be list of valid emails

### Attachment Validation
- File existence check
- File accessibility verification
- MIME type detection
- Size handling (no arbitrary limits)

## Performance

- **Email Sending**: < 10 seconds typical (depends on network and SMTP server)
- **Bulk Sending**: Scales based on recipient count and network latency
- **Validation**: < 100ms per email address
- **Connection**: TLS handshake typically completes in < 2 seconds

## Security Considerations

 **No Hardcoded Credentials**: All sensitive info in `.env` file (not in repository)
 **TLS Encryption**: All SMTP connections use TLS 1.2+
 **Secure Authentication**: Credentials never logged or displayed
 **Input Validation**: All inputs validated before processing
 **Error Handling**: Errors don't expose sensitive information
 **File Permissions**: Log files created with appropriate permissions

## Dependencies

- **python-dotenv**: For secure environment variable management
- **Python 3.6+**: Standard library (smtplib, email, logging, os)

## Testing

### Run Examples
```bash
python examples/single_email.py
python examples/bulk_email.py
python examples/email_with_attachment.py
python examples/html_email.py
```

### Interactive Testing
```bash
python main.py
```

## Troubleshooting

### Email not sending?
1. Verify `.env` file exists and is properly configured
2. Check that SENDER_EMAIL and SENDER_PASSWORD are correct
3. For Gmail, ensure using App Password (not regular password)
4. Check firewall/proxy settings
5. Review logs in `logs/email_automation.log`

### Authentication failing?
1. Verify credentials in `.env` file
2. Check that SMTP_SERVER and SMTP_PORT are correct
3. Ensure TLS is enabled on SMTP server
4. Try disabling 2FA on email account (if temporary)
5. Use App Passwords for Gmail accounts

### Validation errors?
1. Check email format (should be: user@domain.com)
2. Ensure subject and body are non-empty
3. Verify attachment file paths exist

## Best Practices

1. **Use Environment Variables**: Never hardcode credentials
2. **Error Handling**: Always catch and handle exceptions
3. **Logging**: Monitor `email_automation.log` for issues
4. **Testing**: Test with valid credentials before production use
5. **Rate Limiting**: Implement delays between bulk emails if needed
6. **Validation**: Always validate input before sending
7. **Backups**: Keep copies of logs for audit trails

## Acceptance Criteria Met

- Email Sending: Send emails to one or more valid recipients
- Email Content: Subject and message body included
- SMTP Integration: Connect to SMTP with authentication
- Input Validation: Validate email addresses before sending
- Attachment Support: Attach files to emails with optional CLI file picker
- Bulk Email Support: Send to multiple recipients with optional attachments
- Error Handling: Meaningful error messages and logging
- Logging & Reporting: CSV report with delivery status
- Security: No hardcoded credentials, environment variables
- Performance: Emails sent within < 10 seconds
- User Confirmation: Success/failure messages displayed

## Support

For issues or questions:
1. Check the logs in `logs/email_automation.log`
2. Review the examples in `examples/` directory
3. Verify your `.env` configuration
4. Check the troubleshooting section above

## License

This project is provided as-is for educational and production use.

## Version

**Email Automation System v1.0**
Created: June 2024

Developed by Neha P
