"""
The entrypoint
"""

import os
import traceback
import datetime
from argparse import ArgumentParser
from flask import Flask, request
from dotenv import load_dotenv
from components import Loader, Runner, Sender, logger
from exceptions import AlgorithmException


load_dotenv()
app = Flask(__name__)


parser = ArgumentParser()

parser.add_argument('--port',
  type=int, default=5000, required=False, help='The port to open')

parser.add_argument('--debug',
  action='store_true', dest='debug', required=False, help='Run in debug mode')

arguments = parser.parse_args()


@app.route('{}/ping'.format(os.environ['API_BASE']), methods=['GET'])
def ping():
  """
  Tests whether the REST API works
  """
  return {
    'time': datetime.datetime.now().isoformat()
  }


@app.route('{}/alg'.format(os.environ['API_BASE']), methods=['POST'])
def entrypoint():
  """
  Expects a config JSON in the POST body. The config JSON consists of:
    - code: the algorithm
    - secret (optional): the secret password to gain admin access
    - uid (optional): the uid of the module - ignored without admin access

  The loader validates the input JSON and prepares the module.
  The runner creates an engine and runs the algorithm.
  The sender prepares the response.
  """
  try:
    logger.debug('{} main START'.format('-' * 70))

    # Initiate components
    loader = Loader()
    runner = Runner(loader)
    sender = Sender(runner)

    # Read config
    cfg = request.get_json(silent=True) or ''
    logger.debug('Input received: {}'.format(cfg))
    loader.set_input(cfg)

    # Prepare the module
    loader.load()

    # Run the module
    runner.run()

    return sender.send_success()

  except AlgorithmException as e:
    logger.debug(traceback.format_exc())
    return sender.send_mixed(e)

  except Exception as e: # pylint: disable=broad-except
    logger.exception(traceback.format_exc())
    return sender.send_error(e)

  finally:
    logger.debug('{} main END\n'.format('-' * 70))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=arguments.port)
