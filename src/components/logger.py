"""
The logger components
"""

import sys
import json
from datetime import datetime
from typing import TypeAlias


class Logger:
    """
    A simple logger which outputs to stderr.
    """

    Level: TypeAlias = str
    LEVEL_ERROR: Level = "error"
    LEVEL_WARNING: Level = "warning"
    LEVEL_INFO: Level = "info"
    LEVEL_DEBUG: Level = "debug"
    LEVEL_VERBOSE: Level = "verbose"
    LEVEL_SILLY: Level = "silly"

    def log(self, level: Level, msg: str, meta=None):
        """
        Logs the specified message.
        """
        obj = {
            "timestamp": datetime.now().isoformat(),
            "namespace": self.namespace,
            "level": level,
            "msg": msg,
            "meta": meta,
        }

        print(json.dumps(obj), file=sys.stderr)

    def error(self, msg: str, meta=None):
        """
        Logs an error message.
        """
        self.log(self.LEVEL_ERROR, msg, meta)

    def warning(self, msg: str, meta=None):
        """
        Logs a warning message.
        """
        self.log(self.LEVEL_WARNING, msg, meta)

    def info(self, msg, meta=None):
        """
        Logs an info message.
        """
        self.log(self.LEVEL_INFO, msg, meta)

    def debug(self, msg: str, meta=None):
        """
        Logs a debug message.
        """
        self.log(self.LEVEL_DEBUG, msg, meta)

    def verbose(self, msg: str, meta=None):
        """
        Logs a verbose message.
        """
        self.log(self.LEVEL_VERBOSE, msg, meta)

    def silly(self, msg: str, meta=None):
        """
        Logs a silly message.
        """
        self.log(self.LEVEL_SILLY, msg, meta)

    def __init__(self, namespace: str):
        """
        Creates a new instance of Logger.
        """
        self.namespace = namespace


logger = Logger("main")
logger.info("created")
