import hunter
import importlib
import logging
from components.loader import Loader
from engine import Engine
from exceptions import RunnerException, AlgorithmException

class Runner:
  def import_module(self):
    module_name = self.loader.module_name
    
    logging.debug('Importing module {} -> '.format(module_name))

    try:
      self.module = importlib.import_module(module_name)
      logging.debug('success')
    except Exception as e:
      logging.debug('error')
      raise RunnerException(e)
  
  def run(self):
    module_name = self.loader.module_name
    fun_name = self.loader.unique_id

    self.import_module()

    hunter.trace(module=module_name, kind='line', action=self.engine.line_callback)

    fun = getattr(self.module, fun_name)

    logging.debug('Running {} -> '.format(module_name))

    args = {
      'fun': fun,
      'engine': self.engine,
      'print': self.engine.print
    }

    try:
      exec('fun(engine, print)', {}, args)
      logging.debug('success')
    except Exception as e:
      logging.debug('error')
      raise AlgorithmException(e)

  def __init__(self, loader:Loader):
    self.loader = loader
    self.engine = Engine(self.loader.unique_id)
