"""
The entrypoint
"""

import traceback
import sys
import json
from environment import DEBUG_MODE
from components import Loader, Runner, Sender, logger
from exceptions import AlgorithmException


def main():
  """
  Expects a config JSON in the POST body. The config JSON consists of:
    - code: the algorithm
    - secret (optional): the secret password to gain admin access
    - uid (optional): the uid of the module - ignored without admin access

  The loader validates the input JSON and prepares the module.
  The runner creates an engine and runs the algorithm.
  The sender prepares the response.
  """
  if DEBUG_MODE:
    logger.info('Running in debug mode')

  try:
    logger.info('start')

    # Initiate components
    loader = Loader()
    runner = Runner(loader)
    sender = Sender(runner)

    # Read config
    loader.set_input(json.load(sys.stdin))

    # Prepare the module
    loader.load()

    # Run the module
    runner.run()

    logger.info('result: OK')
    print(sender.send_success())

  except AlgorithmException as e:
    logger.error('result: AlgorithmException', { 'exception': traceback.format_exc() })
    print(sender.send_mixed(e))

  except Exception as e: # pylint: disable=broad-except
    logger.error('result: Exception', { 'exception': traceback.format_exc() })
    print(sender.send_error(e))


if __name__ == '__main__':
  main()
