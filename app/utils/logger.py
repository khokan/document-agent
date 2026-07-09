"""
📊 Logging configuration for the PDF Knowledge Assistant.

Sets up structured logging with file and console handlers.
"""

import logging
import logging.handlers
from pathlib import Path

from app.utils.config import config


def setup_logging():
    """Setup application-wide logging."""
    # Create logs directory if it doesn't exist
    log_dir = Path(config.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger("pdf_assistant")
    logger.setLevel(getattr(logging, config.log_level))

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        config.log_file,
        maxBytes=config.get("logging.max_size_mb", 100) * 1024 * 1024,
        backupCount=config.get("logging.backup_count", 5),
    )
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()
