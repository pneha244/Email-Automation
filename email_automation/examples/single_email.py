"""
Example: Send a single email.
Demonstrates basic email sending with subject and body.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import EmailSender
from utils.exceptions import ConfigurationError, SMTPConnectionError, AuthenticationError

def main():
    """Send a single email example."""
    try:
        # Initialize sender
        sender = EmailSender()
        
        # Email details
        recipient = "recipient@example.com"
        subject = "Test Email"
        body = """Hello,

This is a test email sent from the Email Automation system.

Best regards,
Email Automation"""
        
        # Send email
        print(f"Sending email to {recipient}...")
        success, message = sender.send_email(recipient, subject, body)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ Failed: {message}")
    
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure .env file is properly configured.")
    
    except AuthenticationError as e:
        print(f"Authentication Error: {e}")
        print("Please check your SMTP credentials in .env file.")
    
    except SMTPConnectionError as e:
        print(f"Connection Error: {e}")
        print("Please check your SMTP settings.")
    
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
