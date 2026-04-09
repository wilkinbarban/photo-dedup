"""
Logging Module for PhotoDedup.

This module configures the standard Python logging system to write logs
to a centralized file within the application's data directory.
It ensures that the log file is cleared upon every application startup,
providing a clean trace for the current session.
"""

import logging
from pathlib import Path

# We import the application data directory from the state module to ensure
# all application files (config, cache, logs) are kept in the same place.
from core.state import app_data_dir

def setup_logger() -> logging.Logger:
    """
    Configures the global logging system for the application.
    
    The log file is created in the application's configuration directory
    (e.g., ~/.photo_dedup/app.log or %APPDATA%/PhotoDedup/app.log).
    The file mode is 'w', which means the log file will be overwritten
    every time the application starts. This makes it easier to debug
    the current session without wading through historical logs.
    
    Returns:
        logging.Logger: The configured root logger instance.
    """
    log_file: Path = app_data_dir / 'app.log'
    
    # Create the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture everything from DEBUG and above
    
    # Clear any existing handlers to avoid duplicate logs if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # Create a File Handler to write logs to the file
    # mode='w' ensures the log file is wiped clean on every fresh startup
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Create a Console Handler to output logs to the terminal/console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Keep console cleaner with only INFO and above
    
    # Define the format for log messages
    # Example: 2026-04-05 10:20:30 - INFO - Application started successfully
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add both handlers to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info(f"Logger initialized. Writing logs to: {log_file}")
    
    return logger
