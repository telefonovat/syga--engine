import json
import re
from .logger import logger
from utils import path_from_root, random_name, detect_indentation, add_indentation
from exceptions import LoaderException


class Loader:
  def create_module(self):
    try:
      logger.debug('Creating module {} -> '.format(self.module_name))

      with open(self.module_path, 'w') as f:
        f.write(self.code)

      logger.debug('success')
    except OSError as e:
      logger.debug('error')
      raise LoaderException(e)

  def validate_cfg(self):
    logger.debug('Validating cfg -> ')

    # todo: use JSON schema validation
    try:
      if 'code' not in self.cfg:
        raise LoaderException('`code` property not in cfg')

      logger.debug('valid')
    except LoaderException as e:
      logger.debug('invalid')
      raise e

  def parse_cfg(self):
    try:
      logger.debug('Parsing cfg -> ')
      
      self.cfg = json.loads(self.raw)

      logger.debug('success')
    except json.JSONDecodeError:
      logger.debug('error')
      raise LoaderException('Error parsing cfg')

  def prepare_code(self):
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
    self.parse_cfg()
    self.validate_cfg()
    self.prepare_code()
    self.create_module()
  
  def __init__(self, cfg:str):
    self.raw = cfg
    self.unique_id = '_{}'.format(random_name())
    self.module_name = '{}.{}'.format('__algs', self.unique_id)
    self.module_path = '{}.py'.format(path_from_root('__algs', self.unique_id))
