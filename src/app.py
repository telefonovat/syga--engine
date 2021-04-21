import traceback
from utils import path_from_root
from components import Loader, Runner, Sender, logger
from exceptions import AlgorithmException


class App:
  """
  The main class
  """
  def init(self):
    """
    Initiates the app
    """
    pass

  def main_loop(self):
    """
    The main loop of the app. The app waits for an input on the stdint in JSON
    format. After receiving an input, it is loaded and run
    """
    try:
      logger.debug('{} main_loop START'.format('-' * 70))

      sender = Sender()

      cfg = input()
      logger.debug('Input read: {} chars'.format(len(cfg)))

      loader = Loader(cfg)
      runner = Runner(loader)

      loader.load()
      runner.run()

      sender.send_success(runner.engine.make_frames())
      
    except EOFError as e:
      logger.warn('EOF, exiting')
      exit()

    except AlgorithmException as e:
      logger.warn(traceback.format_exc())
      sender.send_mixed(e, runner.engine.make_frames())

    except Exception as e:
      logger.exception(traceback.format_exc())
      sender.send_error(e)

    finally:
      logger.debug('{} main_loop END\n'.format('-' * 70))

  def run(self):
    """
    Runs the app after initialization. This is the method alternative for
    main() function
    """
    while True:
      self.main_loop()

  def die(self, e:Exception):
    """
    This method MUST be called whenever there occurres an error which the app
    cannot recover from. In such case the app dies  
    """
    logger.error('The app is dead')
    logger.exception(traceback.format_exc())
    exit(1)
