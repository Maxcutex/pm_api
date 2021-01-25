import sys
import logging
from typing import Optional


DEFAULT_LOG_LEVEL = logging.INFO
logging.basicConfig(stream=sys.stdout)


class Logs:
    """
    Standardizes the logging mechanism
    """

    @staticmethod
    def logger(
        category: str, log_level: Optional[int] = DEFAULT_LOG_LEVEL
    ) -> logging.Logger:
        """
        Creates and configures a new standard logger with the given category log level
        """
        logger = logging.getLogger(category)
        logger.setLevel(log_level)  # Must set log level on individual loggers
        return logger
