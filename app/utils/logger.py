"""
Logging configuration for the PDF Knowledge Assistant.

Sets up structured logging with file and console handlers.
Handles Unicode/emoji characters properly on all platforms.
"""

import logging
import logging.handlers
import sys
from pathlib import Path

from app.utils.config import config


def setup_logging():
    """Setup application-wide logging with Unicode support."""
    # Create logs directory if it doesn't exist
    log_dir = Path(config.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger("pdf_assistant")
    logger.setLevel(getattr(logging, config.log_level))

    # Create formatters with UTF-8 encoding
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler with rotation and UTF-8 encoding
    file_handler = logging.handlers.RotatingFileHandler(
        config.log_file,
        maxBytes=config.get("logging.max_size_mb", 100) * 1024 * 1024,
        backupCount=config.get("logging.backup_count", 5),
        encoding="utf-8",  # Force UTF-8 encoding for Unicode support
    )
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Console handler with UTF-8 encoding support
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Force UTF-8 encoding on Windows too
    if hasattr(console_handler.stream, 'reconfigure'):
        console_handler.stream.reconfigure(encoding='utf-8')
    
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()
