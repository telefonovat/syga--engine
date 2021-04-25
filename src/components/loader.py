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

  def parse_cfg(self):
    """
    Parses the input config JSON

    raises:
     - LoaderException: if the JSON cannot be parsed
    """
    try:
      self.cfg = json.loads(self.raw)

      if 'code' not in self.cfg:
        raise LoaderException('`code` property not in cfg')

      if 'secret' in self.cfg:
        if self.cfg['secret'] == 'super-secret-password': # todo: use .env
          self.admin_access = True
        else:
          raise LoaderException('Invalid value of `secret` property')

      logger.debug('Parsing cfg -> success')

    except LoaderException as e:
      logger.debug('Parsing cfg -> error')
      raise e
      
    except json.JSONDecodeError:
      logger.debug('Parsing cfg -> error')
      raise LoaderException('Error parsing cfg')


  def generate_name(self):
    """
    Generates the unique name of the module. If running in admin mode (by
    providing correct secret in the config JSON, an uid can be specified.
    Otherwise a random 32 bytes [0-9a-f] will be generated and prefixed with
    an underscore (_) and used as the unique name.
    """
    if self.admin_access and 'uid' in self.cfg:
      self.unique_id = self.cfg['uid']
    else:
      self.unique_id = '_{}'.format(random_name())

    self.module_name = '{}.{}'.format('__algs', self.unique_id)
    self.module_path = '{}.py'.format(path_from_root('__algs', self.unique_id))


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


  def load(self):
    """
    Prepares the module which can be run by the runner component from the user
    provided JSON config
    """
    self.parse_cfg()
    self.generate_name()
    self.prepare_code()
    self.create_module()


  def __init__(self, cfg:str):
    """
    Creates a new instance of Loader

    parameters:
     - cfg (str): the JSON config input
    """
    self.raw = cfg
    self.unique_id = None
    self.module_name = None
    self.module_path = None

    self.cfg = None
    self.code = None

    self.admin_access = False
