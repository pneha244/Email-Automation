"""
Main email sending module.
Handles SMTP connection, email composition, and sending.
"""
import smtplib
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from email import encoders
from typing import List, Optional, Tuple

from config.settings import EmailConfig
from utils.validators import EmailValidator
from utils.logger import EmailLogger
from utils.exceptions import (
    SMTPConnectionError, 
    AuthenticationError, 
    InvalidEmailError,
    AttachmentError,
    EmailSendError,
    ConfigurationError
)

class EmailSender:
    """Main email sender class with SMTP integration."""

    # Set a safe maximum total attachment size to avoid SMTP server disconnects.
    MAX_TOTAL_ATTACHMENT_SIZE = 24 * 1024 * 1024  # 24 MB
    MAX_SINGLE_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB
    
    def __init__(self):
        """Initialize EmailSender with configuration validation."""
        try:
            EmailConfig.validate_config()
            self.logger = EmailLogger.get_logger()
        except ValueError as e:
            raise ConfigurationError(str(e))
    
    def _connect_to_smtp(self) -> smtplib.SMTP:
        """
        Connect to SMTP server.
        
        Returns:
            smtplib.SMTP: Connected SMTP server instance
            
        Raises:
            SMTPConnectionError: If connection fails
            AuthenticationError: If authentication fails
        """
        try:
            self.logger.info(f"Connecting to SMTP server: {EmailConfig.SMTP_SERVER}:{EmailConfig.SMTP_PORT}")
            
            server = smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()
            
            self.logger.info("Starting TLS encryption")
            
            server.login(EmailConfig.SENDER_EMAIL, EmailConfig.SENDER_PASSWORD)
            self.logger.info("Successfully authenticated with SMTP server")
            
            return server
        
        except smtplib.SMTPServerDisconnected as e:
            msg = f"SMTP server disconnected: {str(e)}"
            self.logger.error(msg)
            raise SMTPConnectionError(msg)
        
        except smtplib.SMTPAuthenticationError as e:
            msg = f"SMTP authentication failed. Check your credentials: {str(e)}"
            self.logger.error(msg)
            raise AuthenticationError(msg)
        
        except smtplib.SMTPException as e:
            msg = f"SMTP error occurred: {str(e)}"
            self.logger.error(msg)
            raise SMTPConnectionError(msg)
        
        except Exception as e:
            msg = f"Failed to connect to SMTP server: {str(e)}"
            self.logger.error(msg)
            raise SMTPConnectionError(msg)
    
    def _validate_attachments(self, attachments: Optional[List[str]]) -> Tuple[List[str], List[str]]:
        """
        Validate attachment file paths.
        
        Args:
            attachments: List of file paths to attach
            
        Returns:
            Tuple containing:
                - List of valid file paths
                - List of error messages for invalid files
        """
        if not attachments:
            return [], []
        
        valid_files = []
        errors = []
        total_size = 0
        
        for filepath in attachments:
            if not isinstance(filepath, str):
                errors.append(f"Attachment path must be string: {filepath}")
                continue
            
            filepath = filepath.strip().strip('"')
            
            if not os.path.exists(filepath):
                errors.append(f"Attachment file not found: {filepath}")
                continue
            
            if not os.path.isfile(filepath):
                errors.append(f"Attachment path is not a file: {filepath}")
                continue
            
            size = os.path.getsize(filepath)
            total_size += size
            
            if size > self.MAX_SINGLE_ATTACHMENT_SIZE:
                errors.append(
                    f"Attachment '{os.path.basename(filepath)}' is too large ({size // (1024*1024)} MB). "
                    f"Max single attachment size is {self.MAX_SINGLE_ATTACHMENT_SIZE // (1024*1024)} MB."
                )
                continue
            
            valid_files.append(filepath)
        
        if valid_files and total_size > self.MAX_TOTAL_ATTACHMENT_SIZE:
            errors.append(
                f"Total attachment size is too large ({total_size // (1024*1024)} MB). "
                f"Keep combined attachments under {self.MAX_TOTAL_ATTACHMENT_SIZE // (1024*1024)} MB."
            )
        
        return valid_files, errors
    
    def _attach_files(self, message: MIMEMultipart, attachments: List[str]) -> None:
        """
        Attach files to email message.
        
        Args:
            message: MIMEMultipart message object
            attachments: List of file paths to attach
            
        Raises:
            AttachmentError: If attachment fails
        """
        for filepath in attachments:
            try:
                filename = os.path.basename(filepath)
                
                with open(filepath, 'rb') as attachment:
                    part = MIMEApplication(attachment.read(), Name=filename)
                
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                message.attach(part)
                
                self.logger.info(f"Attached file: {filename}")
            
            except Exception as e:
                msg = f"Failed to attach file {filepath}: {str(e)}"
                self.logger.error(msg)
                raise AttachmentError(msg)

    def _create_message(self, body: str, is_html: bool) -> MIMEMultipart:
        """
        Create a multipart email message with body content.
        """
        message = MIMEMultipart('mixed')
        message['Date'] = formatdate(localtime=True)
        message['Message-ID'] = make_msgid()

        alternative = MIMEMultipart('alternative')
        body_part = MIMEText(body, 'html' if is_html else 'plain')
        alternative.attach(body_part)
        message.attach(alternative)

        return message
    
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        is_html: bool = False
    ) -> Tuple[bool, str]:
        """
        Send email to a single recipient.
        
        Args:
            recipient: Recipient email address
            subject: Email subject
            body: Email body
            attachments: List of file paths to attach (optional)
            is_html: Whether body is HTML content (default: False)
            
        Returns:
            Tuple containing:
                - bool: True if successful, False otherwise
                - str: Success/error message
        """
        start_time = time.time()
        
        # Validate recipient
        if not EmailValidator.is_valid_email(recipient):
            error_msg = f"Invalid recipient email address: {recipient}"
            self.logger.error(error_msg)
            EmailLogger.log_email_sent(recipient, subject, "Failed", error_msg)
            return False, error_msg
        
        # Validate email content
        content_valid, content_errors = EmailValidator.validate_email_structure(subject, body)
        if not content_valid:
            error_msg = "; ".join(content_errors)
            self.logger.error(f"Email content validation failed: {error_msg}")
            EmailLogger.log_email_sent(recipient, subject, "Failed", error_msg)
            return False, error_msg
        
        # Validate attachments
        valid_attachments, attachment_errors = self._validate_attachments(attachments)
        if attachment_errors:
            error_msg = "; ".join(attachment_errors)
            self.logger.error(f"Attachment validation failed: {error_msg}")
            EmailLogger.log_email_sent(recipient, subject, "Failed", error_msg)
            return False, error_msg
        
        server = None
        try:
            # Connect to SMTP
            server = self._connect_to_smtp()
            
            # Create message
            if valid_attachments:
                message = self._create_message(body, is_html)
            else:
                message = MIMEText(body, 'html' if is_html else 'plain')
            
            message['From'] = f"{EmailConfig.SENDER_NAME} <{EmailConfig.SENDER_EMAIL}>"
            message['To'] = recipient
            message['Subject'] = subject
            
            # Attach files if any
            if valid_attachments:
                self._attach_files(message, valid_attachments)
            
            # Send email
            self.logger.info(f"Sending email to {recipient}")
            server.sendmail(EmailConfig.SENDER_EMAIL, recipient, message.as_string())
            
            elapsed_time = time.time() - start_time
            success_msg = f"Email sent successfully in {elapsed_time:.2f}s"
            self.logger.info(success_msg)
            EmailLogger.log_email_sent(recipient, subject, "Success", f"Sent in {elapsed_time:.2f}s")
            
            return True, success_msg
        
        except AuthenticationError as e:
            EmailLogger.log_email_sent(recipient, subject, "Failed", str(e))
            return False, str(e)
        
        except SMTPConnectionError as e:
            EmailLogger.log_email_sent(recipient, subject, "Failed", str(e))
            return False, str(e)
        
        except AttachmentError as e:
            EmailLogger.log_email_sent(recipient, subject, "Failed", str(e))
            return False, str(e)
        
        except smtplib.SMTPServerDisconnected as e:
            error_msg = (
                f"SMTP server disconnected while sending email. "
                f"This often happens when attachments are too large or the server closes the connection: {str(e)}"
            )
            self.logger.error(error_msg)
            EmailLogger.log_email_sent(recipient, subject, "Failed", error_msg)
            return False, error_msg
        
        except Exception as e:
            error_msg = f"Unexpected error while sending email: {str(e)}"
            self.logger.error(error_msg)
            EmailLogger.log_email_sent(recipient, subject, "Failed", error_msg)
            return False, error_msg
        
        finally:
            if server:
                try:
                    server.quit()
                    self.logger.info("Closed SMTP connection")
                except Exception as e:
                    self.logger.warning(f"Error closing SMTP connection: {str(e)}")
    
    def send_bulk_emails(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        is_html: bool = False
    ) -> dict:
        """
        Send email to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body
            attachments: List of file paths to attach (optional)
            is_html: Whether body is HTML content (default: False)
            
        Returns:
            dict: Summary with keys:
                - 'successful': List of successfully sent emails
                - 'failed': List of tuples (email, error_message)
                - 'total': Total recipients
                - 'success_count': Number of successful sends
                - 'failure_count': Number of failed sends
        """
        self.logger.info(f"Starting bulk email sending to {len(recipients)} recipients")
        
        # Validate recipients
        valid_recipients, invalid_emails = EmailValidator.validate_recipients(recipients)
        
        if invalid_emails:
            for email, error in invalid_emails:
                self.logger.warning(f"Skipping invalid email {email}: {error}")
        
        if not valid_recipients:
            error_msg = "No valid recipients after validation"
            self.logger.error(error_msg)
            return {
                'successful': [],
                'failed': invalid_emails,
                'total': len(recipients),
                'success_count': 0,
                'failure_count': len(recipients)
            }
        
        successful = []
        failed = []
        
        for idx, recipient in enumerate(valid_recipients, 1):
            self.logger.info(f"Sending email {idx}/{len(valid_recipients)} to {recipient}")
            success, message = self.send_email(recipient, subject, body, attachments, is_html)
            
            if success:
                successful.append(recipient)
            else:
                failed.append((recipient, message))
        
        # Final summary
        summary = {
            'successful': successful,
            'failed': failed + invalid_emails,
            'total': len(recipients),
            'success_count': len(successful),
            'failure_count': len(failed) + len(invalid_emails)
        }
        
        self.logger.info(
            f"Bulk email sending completed. "
            f"Successful: {summary['success_count']}, Failed: {summary['failure_count']}"
        )
        
        return summary
