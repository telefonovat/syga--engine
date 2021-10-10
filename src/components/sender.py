"""
The sender component
"""

import datetime
import traceback
import os
import json
from environment import DEBUG_MODE
from engine.color import Color
from engine.stopwatch import Stopwatch
from .logger import logger
from .runner import Runner


class Sender:
  """
  Sender is used to send the result of the algorithm run. Provided frames are
  parsed before to make sure they can be JSON encoded
  """

  def _parse_colors(self, obj):
    """
    Recursively turns all instances of Color into RGB tuples
    """
    if isinstance(obj, Color):
      return obj.to_hex()

    if isinstance(obj, list):
      for i in range(len(obj)): # pylint: disable=consider-using-enumerate
        obj[i] = self._parse_colors(obj[i])

    elif isinstance(obj, dict):
      for key, value in obj.items():
        obj[key] = self._parse_colors(value)

    return obj


  def _send_response(self, res, err=None):
    """
    Sends the response to stdout

    parameters:
     - res (bool): Whether the run was successful
     - err (Exception): The exception thrown during preparation or execution
     - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    try:
      stopwatch = Stopwatch().start()

      # Get ticks only in debug mode
      ticks = None
      if DEBUG_MODE:
        ticks = [dict(tick) for tick in self._runner.get_ticks()]

      # Get all frames as dicts
      frames = [dict(frame) for frame in self._runner.make_frames()]

      self._parse_colors(frames)

      # Get elapsed times
      alg_time = self._runner.get_elapsed_time()
      parse_time = stopwatch.stop().elapsed
      elapsed = alg_time + parse_time

      if frames:
        frames[0]['console_logs'] = '\n'.join([
          f'Algorithm ran in {round(alg_time * 1000)}ms',
          f'Response ready in {round(parse_time * 1000)}ms',
          frames[0]["console_logs"]
        ])

      logger.debug('Sending {} response'.format(res))
      logger.debug('Algorithm run in {:.6f} seconds'.format(alg_time))
      logger.debug('Response prepared in {:.6f} seconds'.format(parse_time))
      logger.debug('Everything took {:.6f} seconds'.format(elapsed))

      return json.dumps({
        'timestamp': datetime.datetime.now().isoformat(),
        'res': res,
        'err': None if err is None else str(err),
        'alg_time': alg_time,
        'parse_time': parse_time,
        'elapsed': elapsed,
        'frames': frames,
        'ticks': ticks
      })

    except Exception: # pylint: disable=broad-except
      logger.exception(traceback.format_exc())

      return {
        'timestamp': datetime.datetime.now().isoformat(),
        'res': 'error',
        'err': 'Error while processing response'
      }


  def send_error(self, err):
    """
    Sends an error response

    parameters:
      - err (Exception): The exception raised during preparation or execution
    """
    return self._send_response('error', err)


  def send_mixed(self, err):
    """
    Sends a mixed response

    parameters:
      - err (Exception): The exception raised during preparation or execution
    """
    return self._send_response('mixed', err)


  def send_success(self):
    """
    Sends a success response
    """
    return self._send_response('success')


  def __init__(self, runner:Runner):
    """
    Creates a new instance of Sender
    """
    self._runner = runner
