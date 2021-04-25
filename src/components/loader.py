"""
Loader component
"""

import json
from utils import path_from_root, random_name, detect_indentation, add_indentation
from exceptions import LoaderException
from .logger import logger


class Loader:
  """
  The responsibility of the loader is to
   - Parse the input JSON
   - Validate the input JSON
   - Prepare the unique module names for the user specified algorithm
   - Prepare the code specified by the user (add function definition, ...)
   - Create the module which holds the user specified algorithm
  """
  def create_module(self):
    """
    Creates the module which holds the user specified code

    raises:
     - LoaderException: if it is impossible to write to the designated file
    """
    try:
      with open(self.module_path, 'w') as f:
        f.write(self.code)

      logger.debug('Creating module {} -> success'.format(self.module_name))
    except OSError:
      logger.debug('Creating module {} -> error'.format(self.module_name))
      raise LoaderException()


  def validate_cfg(self):
    """
    Validates the input config JSON

    raises:
     - LoaderException: if the input config JSON is not valid

    todo:
     - uses JSON schema validation
    """
    try:
      if 'code' not in self.cfg:
        raise LoaderException('`code` property not in cfg')

      logger.debug('Validating cfg -> valid')
    except LoaderException as e:
      logger.debug('Validating cfg -> invalid')
      raise e


  def parse_cfg(self):
    """
    Parses the input config JSON

    raises:
     - LoaderException: if the JSON cannot be parsed
    """
    try:
      self.cfg = json.loads(self.raw)

      logger.debug('Parsing cfg -> success')
    except json.JSONDecodeError:
      logger.debug('Parsing cfg -> error')
      raise LoaderException('Error parsing cfg')


  def prepare_code(self):
    """
    Prepares the user specified code to be run be the runner component.
    Wraps the code inside of a unique method which receives these arguments:
     - engine: the engine component
     - print: the overloaded print function which dumps the output to a list
              stored in the engine

    raises:
     - LoaderException: if the indentation of the code is inconsistent
    """
    try:
      code = self.cfg['code']
      indentation = detect_indentation(code)

      self.code = 'def {}(engine, print):\n{}'.format(
        self.unique_id,
        add_indentation(code, indentation)
      )
    except IndentationError:
      raise LoaderException('Indentation error')


  def load(self):
    """
    Prepares the module which can be run by the runner component from the user
    provided JSON config
    """
    self.parse_cfg()
    self.validate_cfg()
    self.prepare_code()
    self.create_module()


  def __init__(self, cfg:str):
    """
    Creates a new instance of Loader

    parameters:
     - cfg (str): the JSON config input
    """
    self.raw = cfg
    self.unique_id = '_{}'.format(random_name())
    self.module_name = '{}.{}'.format('__algs', self.unique_id)
    self.module_path = '{}.py'.format(path_from_root('__algs', self.unique_id))

    self.cfg = None
    self.code = None
