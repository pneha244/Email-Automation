"""
Email Automation System - Interactive CLI Application
Main entry point for sending emails through the command-line interface.
"""
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from email_sender import EmailSender
from utils.exceptions import ConfigurationError, AuthenticationError, SMTPConnectionError
from utils.validators import EmailValidator

def print_header():
    """Print application header."""
    print("\n" + "=" * 60)
    print("  EMAIL AUTOMATION SYSTEM".center(60))
    print("=" * 60 + "\n")

def print_menu():
    """Print main menu."""
    print("\nOptions:")
    print("1. Send single email (optional attachments)")
    print("2. Send bulk email (comma-separated, optional attachments)")
    print("3. Send bulk email with attachment(s)")
    print("4. View configuration")
    print("5. View help")
    print("6. Exit")
    print("-" * 40)

def choose_attachment_files():
    """Open a system dialog so the user can pick attachment files."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        file_paths = filedialog.askopenfilenames(
            title='Select attachment files',
            filetypes=[('All Files', '*.*')]
        )
        root.destroy()

        return list(file_paths)
    except Exception:
        return []


def send_single_email(sender):
    """Interactive single email sending."""
    print("\n--- Send Single Email ---")
    recipient = input("Recipient email: ").strip()
    subject = input("Subject: ").strip()
    body = input("Body (use \\n for line breaks): ").strip().replace('\\n', '\n')
    
    attachments = []
    attach_choice = input("Add attachment files? (y/n): ").strip().lower()
    if attach_choice == 'y':
        print("\nSelect attachment files from your system.")
        attachments = choose_attachment_files()
        if attachments:
            print(f"Selected {len(attachments)} attachment(s).")
        else:
            print("No files were selected. Sending without attachments.")
    
    print("\nSending email...")
    success, message = sender.send_email(recipient, subject, body, attachments)
    
    if success:
        print(f"✓ Success: {message}")
    else:
        print(f"✗ Failed: {message}")

def send_bulk_email(sender):
    """Interactive bulk email sending."""
    print("\n--- Send Bulk Email ---")
    recipients_input = input("Recipients (comma-separated): ").strip()
    recipients = [r.strip() for r in recipients_input.split(',') if r.strip()]
    subject = input("Subject: ").strip()
    body = input("Body (use \\n for line breaks): ").strip().replace('\\n', '\n')
    
    attachments = []
    attach_choice = input("Add attachment files? (y/n): ").strip().lower()
    if attach_choice == 'y':
        print("\nSelect attachment files from your system.")
        attachments = choose_attachment_files()
        if attachments:
            print(f"Selected {len(attachments)} attachment(s).")
        else:
            print("No files were selected. Sending without attachments.")
    
    print(f"\nSending emails to {len(recipients)} recipients...")
    result = sender.send_bulk_emails(recipients, subject, body, attachments)
    
    print(f"\nResults:")
    print(f"  Total: {result['total']}")
    print(f"  ✓ Successful: {result['success_count']}")
    print(f"  ✗ Failed: {result['failure_count']}")
    
    if result['successful']:
        print(f"\n  Sent to: {', '.join(result['successful'])}")
    
    if result['failed']:
        print(f"\n  Failed:")
        for email, error in result['failed']:
            print(f"    - {email}: {error}")

def send_email_with_attachment(sender):
    """Interactive bulk email sending with attachment support."""
    print("\n--- Send Bulk Email with Attachment(s) ---")
    recipients_input = input("Recipients (comma-separated): ").strip()
    recipients = [r.strip() for r in recipients_input.split(',') if r.strip()]
    subject = input("Subject: ").strip()
    body = input("Body (use \\n for line breaks): ").strip().replace('\\n', '\n')
    
    print("\nSelect attachment files from your system.")
    attachments = choose_attachment_files()
    
    if not attachments:
        print("\nNo files selected using dialog.")
        attachments_input = input("Enter file paths manually (comma-separated), or leave empty: ").strip()
        if attachments_input:
            attachments = [f.strip().strip('"') for f in attachments_input.split(',') if f.strip()]
    
    print("\nSending email with attachment(s)...")
    result = sender.send_bulk_emails(recipients, subject, body, attachments)
    
    print(f"\nResults:")
    print(f"  Total: {result['total']}")
    print(f"  ✓ Successful: {result['success_count']}")
    print(f"  ✗ Failed: {result['failure_count']}")
    
    if result['successful']:
        print(f"\n  Sent to: {', '.join(result['successful'])}")
    
    if result['failed']:
        print(f"\n  Failed:")
        for email, error in result['failed']:
            print(f"    - {email}: {error}")

def view_configuration():
    """Display current configuration."""
    from config.settings import EmailConfig
    print("\n--- Configuration ---")
    print(f"SMTP Server: {EmailConfig.SMTP_SERVER}:{EmailConfig.SMTP_PORT}")
    print(f"Sender Email: {EmailConfig.SENDER_EMAIL}")
    print(f"Sender Name: {EmailConfig.SENDER_NAME}")
    print(f"Log Level: {EmailConfig.LOG_LEVEL}")
    print(f"Log File: {EmailConfig.LOG_FILE}")

def print_help():
    """Print help information."""
    help_text = """
--- HELP ---

Email Automation System - Comprehensive email sending solution

FEATURES:
1. Single Email Sending
   - Send formatted emails to individual recipients
   - Support for plain text and HTML content

2. Bulk Email Sending
   - Send to multiple recipients simultaneously
   - Each email is sent individually
   - Detailed success/failure reporting

3. Email Attachments
   - Attach files to emails
   - Support for multiple file types
   - Automatic MIME type handling

4. Security
   - Credentials loaded from .env file
   - No hardcoded sensitive information
   - TLS encryption for SMTP connection

5. Logging & Reporting
   - All sent emails logged with timestamp
   - CSV report file generated automatically
   - Detailed error messages for debugging

CONFIGURATION:
- Edit the .env file with your SMTP settings
- Required fields: SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
- Optional: SENDER_NAME, LOG_LEVEL, LOG_FILE

VALIDATION:
- Email addresses validated before sending
- Invalid emails rejected with error messages
- File attachments checked for existence

ERROR HANDLING:
- Meaningful error messages for all failures
- Connection errors reported immediately
- Authentication failures clearly indicated

EXAMPLES:
See the 'examples' directory for sample code:
- single_email.py: Basic email sending
- bulk_email.py: Multiple recipients
- email_with_attachment.py: Attachments
- html_email.py: HTML formatting

For more information, check the README.md file.
"""
    print(help_text)

def main():
    """Main application loop."""
    print_header()
    
    try:
        # Initialize sender
        print("Initializing Email Automation System...")
        sender = EmailSender()
        print("✓ System initialized successfully\n")
    
    except ConfigurationError as e:
        print(f"✗ Configuration Error: {e}")
        print("\nPlease ensure:")
        print("1. .env file exists in the project directory")
        print("2. SENDER_EMAIL and SENDER_PASSWORD are configured")
        print("3. SMTP_SERVER and SMTP_PORT are set correctly")
        return
    
    # Main loop
    while True:
        print_menu()
        choice = input("Select option (1-6): ").strip()
        
        try:
            if choice == '1':
                send_single_email(sender)
            elif choice == '2':
                send_bulk_email(sender)
            elif choice == '3':
                send_email_with_attachment(sender)
            elif choice == '4':
                view_configuration()
            elif choice == '5':
                print_help()
            elif choice == '6':
                print("\n✓ Goodbye!")
                break
            else:
                print("✗ Invalid option. Please select 1-6.")
        
        except AuthenticationError as e:
            print(f"✗ Authentication Error: {e}")
            print("Please check your SMTP credentials in .env file.")
        
        except SMTPConnectionError as e:
            print(f"✗ Connection Error: {e}")
            print("Please check your SMTP server settings.")
        
        except KeyboardInterrupt:
            print("\n\n✓ Interrupted by user. Goodbye!")
            break
        
        except Exception as e:
            print(f"✗ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
