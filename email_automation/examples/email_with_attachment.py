"""
Example: Send email with attachments.
Demonstrates email sending with file attachments.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import EmailSender
from utils.exceptions import ConfigurationError, AttachmentError

def main():
    """Send email with attachment example."""
    try:
        # Initialize sender
        sender = EmailSender()
        
        # Email details
        recipient = "recipient@example.com"
        subject = "Email with Attachment"
        body = """Hello,

Please find the attached file.

Best regards,
Email Automation"""
        
        # Attachments (create a sample file for testing)
        attachments = []
        
        # Example: Create a sample text file
        sample_file = "examples/sample_attachment.txt"
        os.makedirs(os.path.dirname(sample_file), exist_ok=True)
        
        if not os.path.exists(sample_file):
            with open(sample_file, 'w') as f:
                f.write("This is a sample attachment file.\n")
                f.write("It contains test content.\n")
            print(f"Created sample file: {sample_file}")
        
        attachments.append(sample_file)
        
        # Send email
        print(f"Sending email to {recipient} with {len(attachments)} attachment(s)...")
        success, message = sender.send_email(recipient, subject, body, attachments)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ Failed: {message}")
    
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
    
    except AttachmentError as e:
        print(f"Attachment Error: {e}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
