"""
Logging Module for PhotoDedup.

This module configures the standard Python logging system to write logs
to a centralized file within the application's data directory.
It ensures that the log file is cleared upon every application startup,
providing a clean trace for the current session.
"""

import logging
from pathlib import Path

from src.modules.config.state import app_data_dir


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

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info(f"Logger initialized. Writing logs to: {log_file}")

    return logger
