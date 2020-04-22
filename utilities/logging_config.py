import logging
import os
from logging import handlers

from url_shortener.settings import LOG_ROOT_DIR, LOGGING_TIME_ROTATING_WHEN, LOGGING_TIME_ROTATING_INTERVAL, BASE_LOG_FILE


def get_logger():
    """
    Get custom short url time rotating logger
    :return:
    """

    # Create a custom logger
    logger = logging.getLogger("short_url")

    # Create logger directory if it does not exists
    if not os.path.isdir(LOG_ROOT_DIR):
        os.mkdir(LOG_ROOT_DIR)

    if not logger.handlers:
        # Create time rotating file handler
        f_handler = logging.handlers.TimedRotatingFileHandler(
            LOG_ROOT_DIR + BASE_LOG_FILE,
            when=LOGGING_TIME_ROTATING_WHEN,
            interval=LOGGING_TIME_ROTATING_INTERVAL
        )
        f_handler.suffix = "%Y-%m-%d_%H-%M-%S"
        f_handler.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"
        f_handler.setLevel(logging.ERROR)

        # Add handler to the logger
        logger.addHandler(f_handler)

    return logger
