"""Application logging configuration, completed in Task 3."""

import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logging."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if not root_logger.handlers:
        logging.basicConfig(
            level=level,
            format="%(levelname)s [%(name)s] %(message)s",
            stream=sys.stderr,
        )
