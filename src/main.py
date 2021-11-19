"""
The entrypoint
"""

import traceback
import sys
import json
from environment import DEBUG_MODE
from components import Loader, Runner, Sender
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
    print('Running in debug mode', file=sys.stderr)

  try:
    print('{} main START'.format('-' * 70), file=sys.stderr)

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

    print(sender.send_success())

  except AlgorithmException as e:
    print(traceback.format_exc(), file=sys.stderr)
    print(sender.send_mixed(e))

  except Exception as e: # pylint: disable=broad-except
    print(traceback.format_exc(), file=sys.stderr)
    print(sender.send_error(e))

  finally:
    print('{} main END\n'.format('-' * 70), file=sys.stderr)


if __name__ == '__main__':
  main()
