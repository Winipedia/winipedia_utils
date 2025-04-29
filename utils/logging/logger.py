from logging.config import dictConfig
import logging

from utils.logging.config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


def get_logger(name):
    return logging.getLogger(name)
