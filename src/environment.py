"""
The environment variables
"""

import os
import binascii


# The secret password is required in order for some admin-level parameters to
# be considered (otherwise they are ignored).
SECRET_PASSWORD = (
  os.environ['SECRET_PASSWORD'] if
  'SECRET_PASSWORD' in os.environ else
  binascii.b2a_hex(os.urandom(128)).decode('utf-8').lower()
)

# The prefix shared by all the endpoints
API_BASE = os.environ['API_BASE'] if 'API_BASE' in os.environ else '/api'

# Whether to run in debug mode
DEBUG_MODE = 'DEBUG_MODE' in os.environ and os.environ['DEBUG_MODE'] == 'yes'
