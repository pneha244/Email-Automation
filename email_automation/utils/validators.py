"""
Email validation utilities.
Validates email addresses before sending.
"""
import re
from typing import List, Tuple

class EmailValidator:
    """Validator for email addresses."""
    
    # RFC 5322 simplified email regex pattern
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate a single email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        if not isinstance(email, str):
            return False
        
        email = email.strip()
        
        # Check length
        if len(email) > 254:
            return False
        
        # Check pattern
        if not EmailValidator.EMAIL_PATTERN.match(email):
            return False
        
        # Check local part length
        local_part = email.split('@')[0]
        if len(local_part) > 64:
            return False
        
        return True
    
    @staticmethod
    def validate_recipients(recipients: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Validate a list of email addresses.
        
        Args:
            recipients: List of email addresses to validate
            
        Returns:
            Tuple containing:
                - List of valid email addresses
                - List of tuples (invalid_email, error_reason)
        """
        if not recipients:
            return [], [("", "Recipient list is empty")]
        
        if not isinstance(recipients, list):
            return [], [("", "Recipients must be a list")]
        
        valid_emails = []
        invalid_emails = []
        
        for email in recipients:
            if not isinstance(email, str):
                invalid_emails.append((str(email), "Email must be a string"))
            elif not EmailValidator.is_valid_email(email):
                invalid_emails.append((email, "Invalid email format"))
            else:
                valid_emails.append(email)
        
        return valid_emails, invalid_emails
    
    @staticmethod
    def validate_email_structure(subject: str, body: str) -> Tuple[bool, List[str]]:
        """
        Validate email subject and body.
        
        Args:
            subject: Email subject
            body: Email body
            
        Returns:
            Tuple containing:
                - bool: True if valid
                - List of error messages
        """
        errors = []
        
        if not subject or not isinstance(subject, str):
            errors.append("Subject is required and must be a string")
        elif len(subject.strip()) == 0:
            errors.append("Subject cannot be empty")
        elif len(subject) > 255:
            errors.append("Subject is too long (max 255 characters)")
        
        if not body or not isinstance(body, str):
            errors.append("Body is required and must be a string")
        elif len(body.strip()) == 0:
            errors.append("Body cannot be empty")
        
        return len(errors) == 0, errors
