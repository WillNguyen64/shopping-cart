import os
import logging
import logging.config

from functools import lru_cache
from pathlib import Path

from ..common.settings import get_settings


def get_logging_conf():
    return Path(__file__).parent.parent / "config" / "logging.conf"


@lru_cache
def get_logger(logger_name, settings=get_settings()):
    logging.config.fileConfig(get_logging_conf(), disable_existing_loggers=False)
    logger = logging.getLogger(logger_name)
    logger.setLevel(settings.log_level)
    return logger
