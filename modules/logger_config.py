"""
logger_config.py
-----------------
Sets up a single, shared logger for the whole application.

Having centralized logging satisfies the "Logging / Monitoring"
non-functional requirement: every module reports what it is doing and
any errors it hits, both to the console and to a log file on disk.
"""

import logging
import sys

import config


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance for the given module name."""
    logger = logging.getLogger(name)

    # Avoid attaching duplicate handlers if this is called more than once
    # (e.g. once per module import).
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
