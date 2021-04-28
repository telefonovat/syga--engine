"""
The runner component
"""

import importlib
import hunter
from engine import Engine
from exceptions import RunnerException, AlgorithmException
from .logger import logger
from .loader import Loader


class Runner:
  """
  Runner component receives the module which was prepared by the loader
  component, imports it and prepares the code trackers (Hunter). A new instance
  of engine is then created and passed to the algorithm as an argument of the
  wrapper function
  """

  def import_module(self):
    """
    Imports the module created by the loader component using importlib

    raises:
     - RunnerException: if an error occurres while importing the module
    """
    module_name = self._loader.module_name

    try:
      self._module = importlib.import_module(module_name)
      logger.debug('Importing module {} -> success'.format(module_name))

    except Exception as e:
      logger.debug('Importing module {} -> error'.format(module_name))
      raise RunnerException(e)


  def run(self):
    """
    Runs the user provided algorithm by running the module created by the
    loader component and initiates line tracing by the hunter library

    raises:
     - RunnerException: if an error occurres while importing the module
     - AlgorithmException: if an error is raised while running the algorithm
    """
    self._engine.init_logger(self._loader.unique_id)

    module_name = self._loader.module_name
    fun_name = self._loader.unique_id

    self.import_module()

    hunter.trace(module=module_name, kind='line', action=self._engine.line_callback)

    fun = getattr(self._module, fun_name)

    logger.debug('Running {} <<<'.format(module_name))

    args = {
      'fun': fun,
      'engine': self._engine,
      'print': self._engine.print
    }

    self._engine.stopwatch.start()

    try:
      exec('fun(engine, print)', {}, args) # pylint: disable=exec-used
      logger.debug('>>> success')

    except Exception as e:
      logger.debug('>>> error')
      raise AlgorithmException(e)

    finally:
      self._engine.stopwatch.stop()


  def make_frames(self):
    """
    Engine computes the visualization frames. These frames are then returned
    """
    return self._engine.make_frames()


  def get_elapsed_time(self):
    """
    Returns the amount of time elapsed during the execution of the visualized
    algorithm in seconds.

    returns:
      time (float): elapsed time in seconds
    """
    return self._engine.stopwatch.elapsed


  def __init__(self, loader:Loader):
    """
    Creates a new instance of Runner

    parameters:
     - loader (Loader): the loader which already loaded the config
    """
    self._loader = loader
    self._module = None
    self._engine = Engine()
