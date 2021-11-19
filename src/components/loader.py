"""
Loader component
"""

import json
from environment import SECRET_PASSWORD
from utils.path import path_from_root
from utils.code import detect_indentation, add_indentation
from utils.random_utils import random_name
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

  def set_input(self, cfg):
    """
    Sets the raw user JSON config input
    """
    self._cfg = cfg

    return self


  def parse_cfg(self):
    """
    Parses the input config JSON

    raises:
     - LoaderException: if the JSON cannot be parsed
    """
    try:
      if 'code' not in self._cfg:
        raise LoaderException('Code is missing')

      if not isinstance(self._cfg['code'], str):
        raise LoaderException('Code is invalid - must be a string')

      if not self._cfg['code']:
        raise LoaderException('Code is empty')

      if 'secret' in self._cfg:
        if self._cfg['secret'] == SECRET_PASSWORD:
          self._admin_access = True
        else:
          raise LoaderException('Invalid value of `secret` property')

      logger.info('Parsing cfg: success')

      return self

    except LoaderException as error:
      logger.error('Parsing cfg: error')
      raise error

    except json.JSONDecodeError as error:
      logger.error('Parsing cfg: error')
      raise LoaderException('Error parsing cfg')


  def generate_name(self):
    """
    Generates the unique name of the module. If running in admin mode (by
    providing correct secret in the config JSON, an uid can be specified.
    Otherwise a random 32 bytes [0-9a-f] will be generated and prefixed with
    an underscore (_) and used as the unique name.
    """
    if self._admin_access and 'uid' in self._cfg:
      self.unique_id = self._cfg['uid']
    else:
      self.unique_id = '_{}'.format(random_name())

    self.module_name = '{}.{}'.format('__algs', self.unique_id)
    self.module_path = '{}.py'.format(path_from_root('__algs', self.unique_id))

    return self


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
      code = self._cfg['code']
      indentation = detect_indentation(code)

      # If there is no indentation (no if, for, while blocks), use 2
      if indentation == 0:
        indentation = 2

      code += '\nprint("That\'s all, folks!")'

      self._code = 'def {}(engine, print):\n{}'.format(
        self.unique_id,
        add_indentation(code, indentation)
      )

      return self

    except IndentationError:
      raise LoaderException('Indentation error')


  def create_module(self):
    """
    Creates the module which holds the user specified code

    raises:
     - LoaderException: if it is impossible to write to the designated file
    """
    try:
      with open(self.module_path, 'w', encoding='utf8') as f:
        f.write(self._code)

      logger.info('Creating module: success', { 'module': self.module_name })

      return self

    except OSError as e:
      logger.error('Creating module: error', { 'module': self.module_name })
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

    return self


  def __init__(self):
    """
    Creates a new instance of Loader

    parameters:
     - cfg (str): the JSON config input
    """
    self.unique_id = None
    self.module_name = None
    self.module_path = None

    self._cfg = None
    self._code = None

    self._admin_access = False
