"""
Logging configuration module.
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

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
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join('logs', 'dkp_log.log'),
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(file_handler)
        
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
