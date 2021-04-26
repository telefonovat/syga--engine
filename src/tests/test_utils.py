"""
Tests for src/utils/utils.py
"""

import unittest
import random
import os
from utils import (
  random_name,
  path_from_root,
  detect_indentation,
  add_indentation,
  resolve_url,
  get_sample_code
)


class TestUtils(unittest.TestCase):
  """
  Tests for src/utils/utils.py
  """
  def test_random_name(self):
    """
    Test whether the random_name function generates a random name in the
    correct format and of the correct length

    conditions:
      - correct symbols
      - correct length
    """
    for x in random.choices(range(5, 100), k=10):
      self.assertRegex(
        random_name(x),
        '^[0-9a-f]{{{}}}$'.format(x * 2),
        'Random name should be composed of [0-9a-f] and have corrent length'
      )


  def test_path_from_root(self):
    """
    Test whether the path_from_root function returns the correct path, ie. the
    same path as this file plus ..

    conditions:
      - correct path
    """
    self.assertEqual(
      resolve_url(os.path.join(os.path.dirname(__file__), '..')),
      resolve_url(path_from_root()),
      'Path from root should be ../ from this file'
    )


  def test_detect_indentation(self):
    """
    Test whether indentation is detected correctly using the detect_indentation
    function. Helper function _get_code is used here.

    conditions:
      - correct indentation
    """
    for indentation in random.choices(range(1, 11), k=10):
      code = get_sample_code(indentation)

      self.assertEqual(
        detect_indentation(code),
        indentation,
        'Correctly detect indentation'
      )


  def test_add_indentation(self):
    """
    Test whether the add_indentation function behaves correctly by adding
    measuring the indentation size before and after and computing the diff for
    every line. The diff should be equal to the size of the added indentation.
    The size of the indentation is measured WITHOUT the use of the
    detect_indentation function because an IndentationError might be raised.

    conditions:
      - the indentation of every line was increased as specified
    """
    for indentation in random.choices(range(1, 11), k=10):
      code_before = get_sample_code(indentation)
      indentations_before = [ len(line) - len(line.lstrip()) for line in code_before.splitlines() ]

      code_after = add_indentation(code_before, indentation)
      indentations_after = [ len(line) - len(line.lstrip()) for line in code_after.splitlines() ]

      diff = [ after - before for after,before in zip(indentations_after, indentations_before) ]

      self.assertEqual(
        diff,
        [indentation] * len(indentations_after),
        'Indentation should be added correctly'
      )
