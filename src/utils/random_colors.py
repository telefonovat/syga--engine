"""
Utility function for generating random colors
"""

from engine.color import Color, COLOR_NAMES
from random import choice, random, randint
from utils.random_utils import random_name, random_whitespace_pad


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

  Other validity conditions are:
    - upper or lower case are both valid
    - whitespace padding is valid

  The probabilities are:
    1. 25%: for each of the specified lengths
    2. 50%: use upper case instead of lower case
    3. 50%: pad the color with random amount of whitespace

  returns:
    - color (str): color in hex format
  """
  color = '#' + random_name(4)[:choice([3, 4, 6, 8])] # 1.

  if random() > 0.5: # 2.
    color = color.upper()

  if random() > 0.5: # 3.
    color = random_whitespace_pad(color)

  return color


def random_color_rgba():
  """
  Returns a random valid color in rgba format. This means:
    - both rgb and rgba prefixes are valid
    - whitespace before and after brackets, commas and whole color is valid
    - int {0, ..., 255} or percents [0%, 100%] can be used, but not mixed
    - alpha channel may or may not be specified (default alpha is 1)

  The probabilities are:
    1. 50%: percentage notation will be used
    2. 50%: alpha chanell will be specified
    3. 50%: percentage will be used to specify the alpha channel (given 2.)
    4. 25%: color part will be padded with random whitespace (for every part)
    5. 50%: rgba will be used instead of rgb
    6. 50%: color will be padded with random whitespace

  returns:
    - color (str): color in rgba format
  """
  use_perc = random() > 0.5 # 1.
  use_alpha = random() > 0.5 # 2.
  use_alpha_perc = use_alpha and random() > 0.5 # 3.

  random_int = lambda: str(randint(0, 255))
  random_perc = lambda: f'{randint(0, 255) / 255 * 100}%'
  random_float = lambda: str(random())

  rgba = [random_perc() if use_perc else random_int() for _ in range(3)]

  if use_alpha:
    rgba.append(random_perc() if use_alpha_perc else random_float())

  for i, c in enumerate(rgba):
    if random() > 0.25: # 4.
      rgba[i] = random_whitespace_pad(c)

  rgba = 'rgb{}({})'.format(choice(['a', '']), ','.join(rgba)) # 5.

  if 'e-' in rgba:
    # If a part of the color is in format 9.594183194205907e-05, try again
    return random_color_rgba()

  if random() > 0.5: # 6.
    rgba = random_whitespace_pad(rgba)

  return rgba


def random_color():
  """
  Returns a random valid color in any format. There is also a 50% probability
  that an instance of Color will be returned instead of string.

  The probabilities are:
    1. 1/n: choice of color format
    2. 50%: color will be used to construct an instance of Color

  returns:
    - color (str|Color): random color
  """
  method = choice([random_color_name, random_color_hex, random_color_rgba])
  use_class = random() > 0.5

  color = method()

  if use_class:
    color = Color(color)

  return color
