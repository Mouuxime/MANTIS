"""
MANTIS - Logger
"""

import logging
import sys


def setup_logger():
    logger = logging.getLogger("mantis")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # évite les doublons

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(asctime)s] [MANTIS] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
