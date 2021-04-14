import logging
from utils import path_from_root
from components import Loader, Runner, Sender
from exceptions import AlgorithmException
import traceback


class App:
  def init(self):
    logging.basicConfig(
      filename=path_from_root('../logs/debug.log'),
      format='[%(asctime)s] %(levelname)s: %(message)s',
      level=logging.DEBUG
    )

  def main_loop(self):
    try:
      sender = Sender()

      cfg = input()

      loader = Loader(cfg)
      runner = Runner(loader)

      loader.load()
      runner.run()

      sender.send_success(runner.engine.make_frames())
      
    except EOFError as e:
      logging.warn('EOF, exiting')
      exit()

    except AlgorithmException as e:
      logging.warn(traceback.format_exc())
      sender.send_mixed(e, runner.engine.make_frames())

    except Exception as e:
      logging.exception(traceback.format_exc())
      sender.send_error(e)

  def run(self):
    while True:
      self.main_loop()

  def die(self, e:Exception):
    logging.error('The app is dead')
    logging.exception(traceback.format_exc())
    exit()
