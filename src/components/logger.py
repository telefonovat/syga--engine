"""
The main logger
"""

import logging
from utils import path_from_root


logger = logging.getLogger('main') # pylint: disable=invalid-name
logger.addHandler(logging.FileHandler(path_from_root('../logs/debug.log')))
logger.setLevel(logging.DEBUG)
