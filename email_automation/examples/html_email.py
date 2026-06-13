"""
Example: Send HTML-formatted email.
Demonstrates sending emails with HTML content.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from email_sender import EmailSender
from utils.exceptions import ConfigurationError

def main():
    """Send HTML email example."""
    try:
        # Initialize sender
        sender = EmailSender()
        
        # Email details
        recipient = "recipient@example.com"
        subject = "HTML Formatted Email"
        
        # HTML body
        body = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h1 style="color: #333;">Welcome!</h1>
                <p>This is an <strong>HTML-formatted</strong> email.</p>
                
                <h2>Features:</h2>
                <ul>
                    <li>Rich formatting</li>
                    <li>Styled content</li>
                    <li>Professional appearance</li>
                </ul>
                
                <p style="color: #666;">
                    Sent by Email Automation System
                </p>
            </body>
        </html>
        """
        
        # Send email with HTML flag
        print(f"Sending HTML email to {recipient}...")
        success, message = sender.send_email(recipient, subject, body, is_html=True)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ Failed: {message}")
    
    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
