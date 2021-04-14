import json
from .logger import logger


class Sender:
  def _send_response(self, res, err:Exception, frames):
    logger.debug('Sending {} response'.format(res))
    
    print(json.dumps({
      'res': res,
      'err': str(err),
      'frames': frames
    }))
  
  def send_error(self, e):
    self._send_response('error', e, None)

  def send_mixed(self, frames, e):
    self._send_response('mixed', e, frames)

  def send_success(self, frames):
    self._send_response('success', None, frames)
