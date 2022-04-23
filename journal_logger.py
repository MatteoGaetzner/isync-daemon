"""This module takes care of logging related things."""

import logging

from systemd import journal

from config import config

loglevelmap = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


def get_logger(name):
    # create logger
    logger = logging.getLogger(name)

    # Set minimum log level for output
    logger.setLevel(loglevelmap[config.log_level])

    # add handler
    if config.debug != "true":
        logger.addHandler(journal.JournalHandler())
        logger.debug("Systemd journal handler set.")

    return logger
