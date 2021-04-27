"""
The utility functions used across the app and tests
"""

import binascii
import os
import random
from itertools import islice
from urllib.parse import urlsplit, urlunsplit


def resolve_url(url) :
  """
  Resolve the specified URL - replacing all ./ ../ URL parts with the
  corresponding directories-

  Taken from ttps://stackoverflow.com/a/40537179

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


def random_name(n_bytes=16) :
  """
  Generates and returns a random name consisting of symbols 0-9a-f of the
  specified length. One byte is two chars (ie. 16 bytes = 32 symbols in
  the generated name)

  parameters:
   - n_bytes (int): The length of the random name in bytes. Defaults to 16

  returns:
   - random_name (str): A random name
  """
  return binascii.b2a_hex(os.urandom(n_bytes)).decode('utf-8').lower()


def detect_indentation(code) :
  """
  A trivial function for detecting indentation of the specified code.

  raises:
   - IndentationError: if the indentation is inconsistent

  parameters:
   - code (str): The code

  returns:
   - indentation (int): The size of the indentation used
  """
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


def add_indentation(code, indentation) :
  """
  Adds the specified amount of indentation to the beginning of each line.
  The indentation MUST be done using space (not tabulator). It is not the
  responsibility of this function to detect whether tabulation was used.

  parameters:
   - code (str): The code
   - indentation (int): The number of spaces

  returns:
   - transformed_code (str): The code after adding indentations
  """
  prefix = ' ' * indentation
  return '\n'.join([ prefix + line for line in code.splitlines() ])


def get_sample_code(indentation):
  """
  Returns a sample code for testing.

  parameters:
    - indentation (int): The size of the indentation

  returns:
    - code (string): Sample code with the specified indentation size
  """
  lines = [
    'print("lorem")',
    'print("ipsum")',
    'for i in range(10):',
    '{}x = i ** 2',
    '{}for j in range(x):',
    '{}{}print(j)',
    'print("all done")'
  ]

  lines = [ line.replace('{}', ' ' * indentation) for line in lines ]

  return '\n'.join(lines)


def random_chunk(lis, min_chunk=1, max_chunk=3):
  """
  Splits iterable into into chunks of random size. Returns a generator

  Taken from https://stackoverflow.com/a/21439176

  paramters:
    - li (iterable): The iterable to split into chunks
    - min_chunk (int): The lower bound on chunk size
    - max_chunk (int): The upper bound on chunk size

  returns:
    - chunk_generator (generator)
  """
  iterator = iter(lis)
  while True:
    nxt = list(islice(iterator, random.randint(min_chunk, max_chunk)))
    if nxt:
      yield nxt
    else:
      break


def random_whitespace_pad(word, min_pad=0, max_pad=10):
  """
  Pads the specified word with a random amount of whitespace from both sides

  parameters:
    - word (any): The word to pad
    - min_pad (int): The lower bound on pad size
    - max_pad (int): The upper bound on pad size

  returns:
    - padded_word (str)
  """
  left_pad = ' ' * random.randint(min_pad, max_pad)
  right_pad = ' ' * random.randint(min_pad, max_pad)

  return '{}{}{}'.format(left_pad, str(word), right_pad)
