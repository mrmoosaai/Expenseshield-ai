"""Central logging configuration for the expense agent."""

import logging
import os
import sys
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("ExpenseShield_AI")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(
    f"logs/agent_{datetime.now().strftime('%Y%m%d')}.log",
    encoding="utf-8",
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def info(message: str):
    """Write an info-level log entry."""
    logger.info(message)


def warning(message: str):
    """Write a warning-level log entry."""
    logger.warning(message)


def error(message: str):
    """Write an error-level log entry."""
    logger.error(message)


def debug(message: str):
    """Write a debug-level log entry."""
    logger.debug(message)


def critical(message: str):
    """Write a critical-level log entry."""
    logger.critical(message)
