import json
import os
import binascii
import re
import logging
from utils import path_from_root
from exceptions import LoaderException


class Loader:
  def create_module(self):
    try:
      logging.debug('Creating module {} -> '.format(self.module_name))

      with open(self.module_path, 'w') as f:
        f.write(self.code)

      logging.debug('success')
    except OSError as e:
      logging.debug('error')
      raise LoaderException(e)

  def validate_cfg(self):
    logging.debug('Validating cfg -> ')

    try:
      if 'code' not in self.cfg:
        raise LoaderException('`code` property not in cfg')

      logging.debug('valid')
    except LoaderException as e:
      logging.debug('invalid')
      raise e

  def parse_cfg(self):
    try:
      logging.debug('Parsing cfg -> ')
      
      self.cfg = json.loads(self.raw)

      logging.debug('success')
    except json.JSONDecodeError:
      logging.debug('error')
      raise LoaderException('Error parsing cfg')

  def prepare_code(self):
    self.code = 'def {}(engine, print):\n  {}'.format(
      self.unique_id,
      re.sub('\n', '\n  ', self.cfg['code'])
    )

  def load(self):
    self.parse_cfg()
    self.validate_cfg()
    self.prepare_code()
    self.create_module()
  
  def __init__(self, cfg:str):
    self.raw = cfg
    self.unique_id = '_{}'.format(binascii.b2a_hex(os.urandom(16)).decode('utf-8'))
    self.module_name = '{}.{}'.format('__algs', self.unique_id)
    self.module_path = '{}.py'.format(path_from_root('__algs', self.unique_id))
