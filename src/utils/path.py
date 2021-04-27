"""
Utility functions dealing with paths and URLs
"""

import os
from urllib.parse import urlsplit, urlunsplit


def resolve_url(url):
  """
  Resolve the specified URL - replacing all ./ ../ URL parts with the
  corresponding directories-

  Taken from https://stackoverflow.com/a/40537179

  Parameters:
   - url (str): The URL to resolve

  Returns:
   - resolved_url (str): The resolved URL
  """
  parts = list(urlsplit(url))
  segments = parts[2].split('/')
  segments = [segment + '/' for segment in segments[:-1]] + [segments[-1]]
  resolved = []
  for segment in segments:
    if segment in ('../', '..'):
      if resolved[1:]:
        resolved.pop()
    elif segment not in ('./', '.'):
      resolved.append(segment)
  parts[2] = ''.join(resolved)
  return urlunsplit(parts)


def path_from_root(*args):
  """
  Returns the path from root the root directory

  parameters:
   - *args: Parts of the path (this path will then start from the root dir)

  returns:
   - absolute_path (str): Absolute path from the root project directory
  """
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../' ,*args)
