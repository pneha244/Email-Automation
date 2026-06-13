"""
Example: Send emails to multiple recipients.
Demonstrates bulk email sending with logging.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import EmailSender
from utils.exceptions import ConfigurationError

def main():
    """Send bulk emails example."""
    try:
        # Initialize sender
        sender = EmailSender()
        
        # Email details
        recipients = [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com",
            "invalid-email",  # This will be rejected
        ]
        
        subject = "Bulk Email Test"
        body = """Hello,

This email was sent to you as part of a bulk email campaign.

Best regards,
Email Automation System"""
        
        # Send bulk emails
        print(f"Sending emails to {len(recipients)} recipients...")
        print("-" * 50)
        
        result = sender.send_bulk_emails(recipients, subject, body)
        
        # Display results
        print("\nResults:")
        print(f"Total Recipients: {result['total']}")
        print(f"Successful: {result['success_count']}")
        print(f"Failed: {result['failure_count']}")
        
        if result['successful']:
            print("\n✓ Successfully sent to:")
            for email in result['successful']:
                print(f"  - {email}")
        
        if result['failed']:
            print("\n✗ Failed to send to:")
            for email, error in result['failed']:
                print(f"  - {email}: {error}")
    
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        print("Please ensure .env file is properly configured.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
