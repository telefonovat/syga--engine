"""
Utility functions dealing with randomness
"""

import binascii
import os
from random import random, randint, randrange, choice
import itertools
from engine.color import COLOR_NAMES


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
    - li (iterable): The iterable to split into chunks
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


def random_color_name():
  """
  Returns a random valid color name

  Returns:
    - color_name (str)
  """
  return choice(COLOR_NAMES)


def random_color_hex():
  """
  Returns a random valid color in hex format. There are 4 valid lengths:
    - 3: short, no alpha channel
    - 4: short, with alpha channel
    - 6: long, no alpha channel
    - 8: long, with alpha channel

  Upper or lower case are both valid.
  Whitespace padding is valid.

  returns:
    - color (str)
  """
  color = '#' + random_name(choice([3, 4, 6, 8]))

  if random() > 0.5:
    color = color.upper()

  if random() > 0.5:
    color = random_whitespace_pad(color)

  return color


def random_color_rgba():
  """
  a
  """
  use_perc = random() > 0.5
  use_alpha = random() > 0.5
  use_alpha_perc = use_alpha and random() > 0.5

  random_int = lambda: str(randint(0, 255))
  random_perc = lambda: f'{random() * 100}%'
  random_float = lambda: str(random())

  rgba = [random_perc() if use_perc else random_int() for _ in range(3)]

  if use_alpha:
    rgba.append(random_perc() if use_alpha_perc else random_float())

  for i, c in enumerate(rgba):
    if random() > 0.25:
      rgba[i] = random_whitespace_pad(c)

  rgba = 'rgb{}({})'.format(choice(['a', '']), ','.join(rgba))

  if random() > 0.5:
    rgba = random_whitespace_pad(rgba)

  return rgba
