import logging
import os
from logging.handlers import TimedRotatingFileHandler

def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name.
    
    :param name: The name of the logger.
    :param level: The logging level.
    :return: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(name)
    
    # Prevent duplicate log entries
    if logger.hasHandlers():
        return logger
    
    # Set the logging level
    logger.setLevel(level)
    
    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create a file handler (rotates every day and keeps 7 backups)
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        os.path.join(log_directory, f"{name}.log"),
        when="midnight",
        interval=1,
        backupCount=7
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
