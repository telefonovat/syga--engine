"""
Utility functions dealing with randomness
"""

import binascii
import os
import itertools
from random import randint


def random_name(n_bytes=16):
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


def random_chunk(lis, min_chunk=1, max_chunk=3):
  """
  Splits iterable into into chunks of random size. Returns a generator

  Taken from https://stackoverflow.com/a/21439176

  paramters:
    - lis (iterable): The iterable to split into chunks
    - min_chunk (int): The lower bound on chunk size
    - max_chunk (int): The upper bound on chunk size

  returns:
    - chunk_generator (generator)
  """
  iterator = iter(lis)
  while True:
    nxt = list(itertools.islice(iterator, randint(min_chunk, max_chunk)))
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
  left_pad = ' ' * randint(min_pad, max_pad)
  right_pad = ' ' * randint(min_pad, max_pad)

  return '{}{}{}'.format(left_pad, str(word), right_pad)
