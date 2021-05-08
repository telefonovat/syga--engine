"""
The sender component
"""

import json
from engine.color import Color
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
      return obj.rgba

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
    frames = [dict(frame) for frame in self._runner.make_frames()]
    elapsed = self._runner.get_elapsed_time()

    self._parse_colors(frames)

    logger.debug('Sending {} response'.format(res))
    logger.debug('Algorithm run in {:.6f} seconds'.format(elapsed))

    print(json.dumps({
      'res': res,
      'err': None if err is None else str(err),
      'elapsed': elapsed,
      'frames': frames
    }))


  def send_error(self, err):
    """
    Sends an error response

    parameters:
      - err (Exception): The exception raised during preparation or execution
    """
    self._send_response('error', err)


  def send_mixed(self, err):
    """
    Sends a mixed response

    parameters:
      - err (Exception): The exception raised during preparation or execution
    """
    self._send_response('mixed', err)


  def send_success(self):
    """
    Sends a success response
    """
    self._send_response('success')


  def __init__(self, runner:Runner):
    """
    Creates a new instance of Sender
    """
    self._runner = runner
