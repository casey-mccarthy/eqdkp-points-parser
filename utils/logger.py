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
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(level)
    
    # Create formatters and handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, f"{name}.log"),
        when="midnight",
        interval=1,
        backupCount=7
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
