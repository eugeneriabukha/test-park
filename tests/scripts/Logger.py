import logging
import logging.handlers
import logging.config
import sys

class cLogger:
    def __init__(self,logLevel=None):
        logging.config.fileConfig('/var/lib/stbt/test-pack/tests/scripts/logging.conf',disable_existing_loggers=False)
        self.note = logging.getLogger(__name__)
Logger = cLogger(logLevel=logging.DEBUG)