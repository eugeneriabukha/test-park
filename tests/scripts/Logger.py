import logging
import logging.handlers
import logging.config
import sys
import os

RESULT = 25

class cLogger:
    def __init__(self,logLevel=None):
		logging.addLevelName(RESULT_LEVEL,"RESULT_LEVEL")
		logging.config.fileConfig('/var/lib/stbt/test-pack/tests/scripts/logging.conf',disable_existing_loggers=False)
		self.note = logging.getLogger(__name__)
		self.note1 = logging.getLogger("resultLogger")

Logger = cLogger(logLevel=logging.DEBUG)