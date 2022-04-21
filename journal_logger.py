import logging
import os

from systemd.journal import JournalHandler

DEBUG = os.getenv("DEBUG_MAILSYNC") == "true"

# TODO Add to (future) settings file
APP_NAME = "mailsync-daemon"

# create logger
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)

# add handler
if DEBUG != "true":
    logger.addHandler(JournalHandler())

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO if not DEBUG else logging.DEBUG)

# create formatter
formatter = logging.Formatter("[%(levelname)s]  %(name)s  %(asctime)s:  %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
