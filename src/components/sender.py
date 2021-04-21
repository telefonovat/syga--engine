import json
from .logger import logger


class Sender:
  def _send_response(self, res:bool, err:Exception, frames):
    """
    Sends the response to stdout

    parameters:
     - res (bool): Whether the run was successful
     - err (Exception): The exception thrown during preparation or execution
     - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    logger.debug('Sending {} response'.format(res))
    
    print(json.dumps({
      'res': res,
      'err': str(err),
      'frames': frames
    }))
  
  def send_error(self, e:Exception):
    """
    Sends an error response

    parameters:
     - e (Exception): The exception thrown during preparation or execution
    """
    self._send_response('error', e, None)

  def send_mixed(self, frames, e:Exception):
    """
    Sends a mixed response

    parameters:
     - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    self._send_response('mixed', e, frames)

  def send_success(self, frames):
    """
    Sends a success response
    
    parameters:
     - frames (list<Frame>): The list of generated frames (or an empty list)
    """
    self._send_response('success', None, frames)
