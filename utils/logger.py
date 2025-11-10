"""
Logging utilities
"""

import logging
from pathlib import Path
from core.config import get_config


def setup_logger(name: str) -> logging.Logger:
    """Setup logger with configuration"""
    config = get_config()

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.logging.level))

    # Create logs directory
    log_dir = Path(config.logging.file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # File handler
    fh = logging.FileHandler(config.logging.file)
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(config.logging.format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
