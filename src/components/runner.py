import hunter
import importlib
from .logger import logger
from .loader import Loader
from engine import Engine
from exceptions import RunnerException, AlgorithmException


class Runner:
  def import_module(self):
    module_name = self.loader.module_name

    try:
      self.module = importlib.import_module(module_name)
      logger.debug('Importing module {} -> success'.format(module_name))
    except Exception as e:
      logger.debug('Importing module {} -> error'.format(module_name))
      raise RunnerException(e)
  
  def run(self):
    module_name = self.loader.module_name
    fun_name = self.loader.unique_id

    self.import_module()

    hunter.trace(module=module_name, kind='line', action=self.engine.line_callback)

    fun = getattr(self.module, fun_name)

    logger.debug('Running {} <<<'.format(module_name))

    args = {
      'fun': fun,
      'engine': self.engine,
      'print': self.engine.print
    }

    try:
      exec('fun(engine, print)', {}, args)
      logger.debug('>>> success')
    except Exception as e:
      logger.debug('>>> error')
      raise AlgorithmException(e)

  def __init__(self, loader:Loader):
    self.loader = loader
    self.engine = Engine(self.loader.unique_id)
