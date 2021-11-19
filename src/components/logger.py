"""
The logger components
"""

import sys
import json
from datetime import datetime

class Logger:
  """
  A simple logger which outputs to stderr.
  """

  LEVEL_ERROR = 'error'
  LEVEL_WARNING = 'warning'
  LEVEL_INFO = 'info'
  LEVEL_DEBUG = 'debug'
  LEVEL_VERBOSE = 'verbose'
  LEVEL_SILLY = 'silly'


  def log(self, level, msg, meta=None):
    """
    Logs the specified message.
    """
    obj = {
      'timestamp': datetime.now().isoformat(),
      'namespace': self.namespace,
      'level': level,
      'msg': msg,
      'meta': meta,
    }

    print(json.dumps(obj), file=sys.stderr)


  def error(self, msg, meta=None):
    """
    Logs an error message.
    """
    self.log(self.LEVEL_ERROR, msg, meta)


  def warning(self, msg, meta=None):
    """
    Logs a warning message.
    """
    self.log(self.LEVEL_WARNING, msg, meta)


  def info(self, msg, meta=None):
    """
    Logs an info message.
    """
    self.log(self.LEVEL_INFO, msg, meta)


  def debug(self, msg, meta=None):
    """
    Logs a debug message.
    """
    self.log(self.LEVEL_DEBUG, msg, meta)


  def verbose(self, msg, meta=None):
    """
    Logs a verbose message.
    """
    self.log(self.LEVEL_VERBOSE, msg, meta)


  def silly(self, msg, meta=None):
    """
    Logs a silly message.
    """
    self.log(self.LEVEL_SILLY, msg, meta)


  def __init__(self, namespace):
    """
    Creates a new instance of Logger.
    """
    self.namespace = namespace


logger = Logger('main')
logger.info('created')
