"""
Configuration management for email automation system.
Loads settings from environment variables securely.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailConfig:
    """Email configuration settings loaded from environment variables."""
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    SENDER_NAME = os.getenv('SENDER_NAME', 'Sender')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/email_automation.log')
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present."""
        required_fields = ['SENDER_EMAIL', 'SENDER_PASSWORD']
        missing_fields = [field for field in required_fields if not getattr(EmailConfig, field)]
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}. "
                           f"Please set these in your .env file.")
        
        return True
