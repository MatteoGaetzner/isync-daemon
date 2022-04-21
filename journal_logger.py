import logging

from systemd.journal import JournalHandler

from config import config

loglevelmap = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

# create logger
logger = logging.getLogger(config.logger_name)

logger.setLevel(loglevelmap[config.log_level])

# add handler
if config.debug != "true":
    logger.addHandler(JournalHandler())

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(loglevelmap[config.log_level])

# create formatter
formatter = logging.Formatter("[%(levelname)s]  %(name)s  %(asctime)s:  %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
