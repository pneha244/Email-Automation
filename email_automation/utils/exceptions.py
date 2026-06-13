"""
Custom exceptions for email automation system.
"""

class EmailAutomationException(Exception):
    """Base exception for email automation."""
    pass

class SMTPConnectionError(EmailAutomationException):
    """Raised when SMTP connection fails."""
    pass

class AuthenticationError(EmailAutomationException):
    """Raised when authentication with SMTP server fails."""
    pass

class InvalidEmailError(EmailAutomationException):
    """Raised when email address is invalid."""
    pass

class AttachmentError(EmailAutomationException):
    """Raised when attachment handling fails."""
    pass

class EmailSendError(EmailAutomationException):
    """Raised when email sending fails."""
    pass

class ConfigurationError(EmailAutomationException):
    """Raised when configuration is invalid."""
    pass
