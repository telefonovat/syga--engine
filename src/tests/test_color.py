"""
Tests for src/engine/color.py
"""

import unittest
from random import random, randrange, randint, choice, shuffle
from engine.color import Color, COLOR_NAMES
from utils.random import random_name, random_chunk, random_whitespace_pad


class TestColor(unittest.TestCase):
  """
  Tests for src/engine/color.py
  """

  def test_is_keyword(self):
    """
    Test is_keyword

    conditions:
      - any key from COLOR_NAMES is valid
      - anything else is invalid
    """
    random_valid = lambda: choice(COLOR_NAMES)
    random_invalid = lambda: random_name(5)

    for _ in range(500):
      is_valid = random() > 0.5
      keyword = random_valid() if is_valid else random_invalid()

      self.assertEqual(
        Color.is_keyword(keyword),
        is_valid,
        '{} is{} valid'.format(keyword, '' if is_valid else ' not')
      )


  def test_is_hex(self):
    """
    Test is_hex by generating a random string of length 1-10.

    conditions:
      - length with # prefix in (4, 5, 7, 9)
      - only [1-9a-fA-F] symbols are valid
      - whitespace padding does not affect validity
    """
    for chunk in random_chunk(random_name(5000), max_chunk=10):
      color = '#{}'.format(''.join(chunk))
      valid = len(color) in (4, 5, 7, 9)

      # 25% probability to lose # prefix | not valid
      if valid and random() > 0.25:
        color = color[1:]
        valid = False

      # 50% probability to use upper case | valid
      if valid and random() > 0.5:
        color = color.upper()

      # 25% probability to use one invalid symbol | not valid
      if valid and random() > 0.25:
        parts = ''.split(color)
        parts[randrange(len(parts))] = chr(randint(103, 122))
        color = ''.join(parts)
        valid = False

      # 50% probability of adding random whitespace pad | valid
      if random() > 0.5:
        color = random_whitespace_pad(color)

      self.assertEqual(
        Color.is_hex(color),
        valid,
        '{} is{} valid'.format(color, '' if valid else ' not')
      )


  def test_is_rgba_int_valid(self):
    """
    Tests is_rgba by generating a random tuple in int format. The tests are
    done for both string and tuple/list representation.

    conditions:
      - alpha channel may or may not be specified
      - rgba and rgb are interchangable even when specifing alpha channel
      - whitespace padding does not affect validity
      - whitespace before and after symbols (), does not affect validity
      - tuple or list are both valid
    """
    for _ in range(500):
      color_rgba = [randint(0, 255) for _ in range(3)]

      # 50% probability of adding transparency | valid
      if random() > 0.5:
        color_rgba.append(random())

      # 50% probability to exclude 'a' even when using transparency | valid
      color_rgba_str = 'rgb{}({})'.format(
        'a' if len(color_rgba) == 4 and random() > 0.5 else '',
        ','.join([ random_whitespace_pad(c) for c in color_rgba ])
      )

      # 50% probability of adding random whitespace pad | valid
      if random() > 0.5:
        color_rgba_str = random_whitespace_pad(color_rgba_str)

      # 50% probability of using tuple | valid
      if random() > 0.5:
        color_rgba = tuple(color_rgba)

      self.assertTrue(Color.is_rgba(color_rgba), '{} is valid'.format(color_rgba))
      self.assertTrue(Color.is_rgba(color_rgba_str), '{} is valid'.format(color_rgba_str))


  def test_is_rgba_percent_valid(self):
    """
    Tests is_rgba by generating a random tuple in percent format. The tests are
    done for both string and tuple/list representation.

    Conditions are same as in test_is_rgba_int_valid.
    """
    for _ in range(500):
      color_rgba = [random() for _ in range(3)]

      # 50% probability of adding transparency | valid
      if random() > 0.5:
        color_rgba.append(random())

      # 50% probability to exclude 'a' even when using transparency | valid
      color_rgba_str = 'rgb{}({})'.format(
        'a' if len(color_rgba) == 4 and random() > 0.5 else '',
        ','.join([ random_whitespace_pad(f'{c * 100}%') for c in color_rgba ])
      )

      # 50% probability of adding random whitespace pad | valid
      if random() > 0.5:
        color_rgba_str = random_whitespace_pad(color_rgba_str)

      # 50% probability of using tuple | valid
      if random() > 0.5:
        color_rgba = tuple(color_rgba)

      self.assertTrue(Color.is_rgba(color_rgba), '{} is valid'.format(color_rgba))
      self.assertTrue(Color.is_rgba(color_rgba_str), '{} is valid'.format(color_rgba_str))


  def test_is_rgba_invalid(self):
    """
    Tests is_rgba by generating a random tuple in percent format. The tests are
    done for both string and tuple/list representation.

    This tests tests various forms of invalid input. False positives (input is
    actually invalid, but considered valid) are much less problematic. For this
    reason, less attention is payed to testing invalid input.
    """
    # Too high values, too many values, too few values
    for _ in range(500):
      color_rgba = [randint(256, 1000) for _ in range(randint(1, 7))]

      color_rgba_str = 'rgb{}({})'.format(
        'a' if random() > 0.5 else '',
        ','.join([ random_whitespace_pad(c) for c in color_rgba ])
      )

      self.assertFalse(Color.is_rgba(color_rgba), f'{color_rgba} is invalid')
      self.assertFalse(Color.is_rgba(color_rgba_str), f'{color_rgba_str} is invalid')

    # Too low values, too many values, too few values
    for _ in range(500):
      color_rgba = [randint(-400, -1) for _ in range(randint(1, 7))]

      color_rgba_str = 'rgb{}({})'.format(
        'a' if random() > 0.5 else '',
        ','.join([ random_whitespace_pad(c) for c in color_rgba ])
      )

      self.assertFalse(Color.is_rgba(color_rgba), f'{color_rgba} is invalid')
      self.assertFalse(Color.is_rgba(color_rgba_str), f'{color_rgba_str} is invalid')

    # Mixing floats and integers
    for _ in range(500):
      color_rgba = [random(), randint(2, 255), randint(2, 255)]
      shuffle(color_rgba)
      self.assertFalse(Color.is_rgba(color_rgba), f'{color_rgba} is invalid')


  def test_normalize_hex_long(self):
    """
    Test normalize_hex by generating a random tuple of 4 numbers from interval
    (0, 1) and converting it to hex color. Then the hex color is converted back
    to rgba using normalize_hex. The values are expected to be the same minus
    rounding error.

    conditions:
      - almost equal values (at least 2 decimal points) of all rgba parts
      - transparency does not have to be specified - default value if ff = 1.0
      - whitespace padding does not affect validity
    """
    for _ in range(500):
      color_rgba = [randint(0, 255) / 255 for _ in range(4)]
      color_hex = '#{}'.format(''.join(["%02x" % round(c * 255) for c in color_rgba]))

      # 50% probability of not specifing transparency | valid
      if random() > 0.5:
        color_hex = color_hex[:7]
        color_rgba[3] = 1

      # 50% probability of adding random whitespace pad | valid
      if random() > 0.5:
        color_hex = random_whitespace_pad(color_hex)

      normalized = Color.normalize_hex(color_hex)

      for expected, actual in zip(color_rgba, normalized):
        self.assertAlmostEqual(expected, actual)


  def test_normalize_hex_short(self):
    """
    Same as test_normalize_hex_long, but in short format
    """
    for _ in range(500):
      color_rgba = [randrange(1, 16) for _ in range(4)]
      color_hex = '#{}'.format(''.join(["%01x" % c for c in color_rgba]))
      color_rgba = [(c * 16 + c) / 255 for c in color_rgba]

      # 50% probability of not specifing transparency | valid
      if random() > 0.5:
        color_hex = color_hex[:4]
        color_rgba[3] = 1

      # 50% probability of adding random whitespace pad | valid
      if random() > 0.5:
        color_hex = random_whitespace_pad(color_hex)

      normalized = Color.normalize_hex(color_hex)

      for expected, actual in zip(color_rgba, normalized):
        self.assertAlmostEqual(expected, actual)


  def test_normalize_rgba_int(self):
    """
    Test normalize_rgb using int format by generating a random tuple

    conditions:
      - normalized rgba tuple should be equal to the original one minus
        rounding error
    """
    for _ in range(500):
      color_rgba = [randint(0, 255) for _ in range(3)]

      if random() > 0.5:
        color_rgba.append(random())

      color_rgba_str = 'rgb{}({})'.format(
        'a' if random() > 0.5 else '',
        ','.join([ random_whitespace_pad(c) for c in color_rgba ])
      )

      # Normalize the colors before comparing them
      for i, c in enumerate(color_rgba[:3]):
        color_rgba[i] = c / 255

      for actual, expected in zip(Color.normalize_color(color_rgba_str), color_rgba):
        self.assertAlmostEqual(actual, expected, 7, color_rgba_str)

      for actual, expected in zip(Color.normalize_color(color_rgba), color_rgba):
        self.assertAlmostEqual(actual, expected, 7, color_rgba)


  def test_normalize_rgba_perc(self):
    """
    Same as test_normalize_rgba_int but with perc format
    """
    for _ in range(500):
      color_rgba = [random() for _ in range(3)]

      if random() > 0.5:
        color_rgba.append(random())

      color_rgba_str = 'rgb{}({})'.format(
        'a' if random() > 0.5 else '',
        ','.join([ random_whitespace_pad(f'{c * 100}%') for c in color_rgba ])
      )

      for actual, expected in zip(Color.normalize_color(color_rgba_str), color_rgba):
        self.assertAlmostEqual(actual, expected, 7, color_rgba_str)

      for actual, expected in zip(Color.normalize_color(color_rgba), color_rgba):
        self.assertAlmostEqual(actual, expected, 7, color_rgba)
