import json
from .logger import logger
from colour import Color


class Sender:
  def _parse_colors(self, obj):
    """
    Recursively turns all instances of Color into RGB tuples

    todo: consider using different library than colour
    """
    if isinstance(obj, Color):
      return obj.rgb
    
    if isinstance(obj, list):
      for i in range(len(obj)):
        obj[i] = self._parse_colors(obj[i])
    
    elif isinstance(obj, dict):
      for key, value in obj.items():
        obj[key] = self._parse_colors(value)

    return obj

      
  
  def _send_response(self, res:bool, frames, err:Exception):
    """
    Sends the response to stdout

    parameters:
     - res (bool): Whether the run was successful
     - err (Exception): The exception thrown during preparation or execution
     - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    logger.debug('Sending {} response'.format(res))
    
    self._parse_colors(frames)
    
    print(json.dumps({
      'res': res,
      'err': str(err),
      'frames': frames
    }))
  

  def send_error(self, err:Exception):
    """
    Sends an error response

    parameters:
      - err (Exception): The exception raised during preparation or execution
    """
    self._send_response('error', frames=None, err=err)


  def send_mixed(self, frames, err:Exception):
    """
    Sends a mixed response

    parameters:
      - frames (list<Frame>): The list of generated frames (or an empty list)
      - err (Exception): The exception raised during preparation or execution
    """
    self._send_response('mixed', frames=frames, err=err)


  def send_success(self, frames):
    """
    Sends a success response
    
    parameters:
      - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    self._send_response('success', frames=frames, err=None)
