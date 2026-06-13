"""
Email Automation System - Test Suite
Tests all core functionality to ensure system is working correctly.
"""
import sys
import os
import unittest
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.validators import EmailValidator
from utils.exceptions import ConfigurationError
from config.settings import EmailConfig

class TestEmailValidator(unittest.TestCase):
    """Test email validation functionality."""
    
    def test_valid_emails(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            "user@example.com",
            "john.doe@company.co.uk",
            "test+tag@domain.org",
            "a@b.co",
        ]
        
        for email in valid_emails:
            self.assertTrue(
                EmailValidator.is_valid_email(email),
                f"Email {email} should be valid"
            )
    
    def test_invalid_emails(self):
        """Test rejection of invalid email addresses."""
        invalid_emails = [
            "invalid.email",           # No @
            "@example.com",            # No local part
            "user@",                   # No domain
            "user @example.com",       # Space in email
            "user@domain",             # No TLD
            "",                        # Empty
            "user..name@domain.com",   # Double dot
        ]
        
        for email in invalid_emails:
            self.assertFalse(
                EmailValidator.is_valid_email(email),
                f"Email {email} should be invalid"
            )
    
    def test_validate_recipients_list(self):
        """Test validation of recipient list."""
        recipients = [
            "user1@example.com",
            "user2@example.com",
            "invalid-email",
        ]
        
        valid, invalid = EmailValidator.validate_recipients(recipients)
        
        self.assertEqual(len(valid), 2)
        self.assertEqual(len(invalid), 1)
        self.assertIn("user1@example.com", valid)
        self.assertIn("user2@example.com", valid)
    
    def test_validate_email_structure(self):
        """Test email content validation."""
        # Valid email
        is_valid, errors = EmailValidator.validate_email_structure(
            subject="Test",
            body="Test body"
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Missing subject
        is_valid, errors = EmailValidator.validate_email_structure(
            subject="",
            body="Test body"
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Missing body
        is_valid, errors = EmailValidator.validate_email_structure(
            subject="Test",
            body=""
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_email_length_validation(self):
        """Test email address length constraints."""
        # Local part too long (> 64 chars)
        long_local = "a" * 65 + "@example.com"
        self.assertFalse(EmailValidator.is_valid_email(long_local))
        
        # Total length too long (> 254 chars)
        long_email = "a" * 250 + "@b.com"
        self.assertFalse(EmailValidator.is_valid_email(long_email))
    
    def test_subject_length_validation(self):
        """Test subject length validation."""
        # Valid subject
        is_valid, errors = EmailValidator.validate_email_structure(
            subject="Valid Subject",
            body="Test"
        )
        self.assertTrue(is_valid)
        
        # Subject too long (> 255 chars)
        long_subject = "a" * 256
        is_valid, errors = EmailValidator.validate_email_structure(
            subject=long_subject,
            body="Test"
        )
        self.assertFalse(is_valid)


class TestConfiguration(unittest.TestCase):
    """Test configuration loading."""
    
    def test_config_loaded(self):
        """Test that configuration is loaded."""
        self.assertIsNotNone(EmailConfig.SMTP_SERVER)
        self.assertIsNotNone(EmailConfig.SMTP_PORT)
        self.assertIsNotNone(EmailConfig.SENDER_EMAIL)
    
    def test_smtp_port_is_integer(self):
        """Test SMTP port is an integer."""
        self.assertIsInstance(EmailConfig.SMTP_PORT, int)
        self.assertGreater(EmailConfig.SMTP_PORT, 0)
        self.assertLess(EmailConfig.SMTP_PORT, 65536)
    
    def test_config_has_defaults(self):
        """Test that configuration has sensible defaults."""
        self.assertEqual(EmailConfig.SMTP_SERVER, "smtp.gmail.com")
        self.assertEqual(EmailConfig.SMTP_PORT, 587)
        self.assertEqual(EmailConfig.SENDER_NAME, "Your Name")


class TestExceptionHandling(unittest.TestCase):
    """Test custom exceptions."""
    
    def test_exception_hierarchy(self):
        """Test exception class hierarchy."""
        from utils.exceptions import (
            EmailAutomationException,
            SMTPConnectionError,
            AuthenticationError,
            InvalidEmailError
        )
        
        # Test inheritance
        self.assertTrue(issubclass(SMTPConnectionError, EmailAutomationException))
        self.assertTrue(issubclass(AuthenticationError, EmailAutomationException))
        self.assertTrue(issubclass(InvalidEmailError, EmailAutomationException))
    
    def test_exception_raising(self):
        """Test that exceptions can be raised and caught."""
        from utils.exceptions import InvalidEmailError
        
        with self.assertRaises(InvalidEmailError):
            raise InvalidEmailError("Test error")


def run_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Email Automation System - Test Suite".center(60))
    print("=" * 60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestEmailValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestExceptionHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary".center(60))
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
