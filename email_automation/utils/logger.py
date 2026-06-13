"""
Logging system for email automation.
Logs all email sending activities with status and timestamps.
"""
import logging
import os
from datetime import datetime
from config.settings import EmailConfig

class EmailLogger:
    """Logger for email automation system."""
    
    _logger = None
    _file_handler = None
    
    @classmethod
    def get_logger(cls):
        """
        Get or create the logger instance.
        
        Returns:
            logging.Logger: Configured logger instance
        """
        if cls._logger is None:
            cls._logger = logging.getLogger('email_automation')
            cls._logger.setLevel(EmailConfig.LOG_LEVEL)
            
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(EmailConfig.LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # File handler
            cls._file_handler = logging.FileHandler(EmailConfig.LOG_FILE)
            cls._file_handler.setLevel(EmailConfig.LOG_LEVEL)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(EmailConfig.LOG_LEVEL)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            cls._file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            cls._logger.addHandler(cls._file_handler)
            cls._logger.addHandler(console_handler)
        
        return cls._logger
    
    @classmethod
    def log_email_sent(cls, recipient: str, subject: str, status: str, details: str = ""):
        """
        Log a sent email.
        
        Args:
            recipient: Recipient email address
            subject: Email subject
            status: 'Success' or 'Failed'
            details: Additional details/error message
        """
        logger = cls.get_logger()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"Email to {recipient} | Subject: {subject} | Status: {status}"
        if details:
            message += f" | Details: {details}"
        
        if status.lower() == 'success':
            logger.info(message)
        else:
            logger.error(message)
        
        # Write to CSV-like format for reporting
        cls._write_to_report(recipient, subject, status, timestamp, details)
    
    @staticmethod
    def _write_to_report(recipient: str, subject: str, status: str, timestamp: str, details: str):
        """Write email sending details to a report file."""
        report_file = 'logs/email_report.csv'
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(report_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create header if file doesn't exist
        if not os.path.exists(report_file):
            with open(report_file, 'w') as f:
                f.write("Timestamp,Recipient,Subject,Status,Details\n")
        
        # Append report entry
        with open(report_file, 'a') as f:
            # Escape details for CSV
            details_escaped = details.replace('"', '""') if details else ""
            f.write(f"{timestamp},\"{recipient}\",\"{subject}\",{status},\"{details_escaped}\"\n")
