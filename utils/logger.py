"""
Logging configuration module.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
import atexit

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Name for the logger
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if the logger doesn't have handlers
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # File handler (always writes to file)
        log_file = os.path.join('logs', 'dkp_log.log')
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, delay=True)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Console handler (only shows in debug mode)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # Set console handler level based on debug flag
        if os.getenv('DEBUG_MODE') == 'true':
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.CRITICAL)  # Only show critical errors
            
        logger.addHandler(console_handler)
    
    return logger

# Ensure proper closure of handlers on application exit
@atexit.register
def shutdown_logging():
    logging.shutdown()
