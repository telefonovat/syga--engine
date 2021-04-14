import binascii
import os
import re
from urllib.parse import urlsplit, urlunsplit


# https://stackoverflow.com/a/40537179
def resolve_url(url):
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
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../' ,*args)


def random_name(n_bytes=16):
  return binascii.b2a_hex(os.urandom(n_bytes)).decode('utf-8').lower()


def detect_indentation(code):
  indentations = [ len(line) - len(line.lstrip()) for line in code.splitlines() ]
  min_indentation = min(indentations)

  indentations = [ x - min_indentation for x in indentations if x > min_indentation ]

  if len(indentations) == 0:
    return min_indentation

  min_indentation = min(indentations)

  for indentation in indentations:
    if indentation % min_indentation != 0:
      raise IndentationError()

  return min_indentation


def add_indentation(code:str, indentation:int):
  prefix = ' ' * indentation
  return '\n'.join([ prefix + line for line in code.splitlines() ])
