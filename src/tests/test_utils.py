import unittest
import re
from utils import random_name, path_from_root, detect_indentation, add_indentation, resolve_url
import random
import os


class TestUtils(unittest.TestCase):
  def _get_code(self, indentation):
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
  
  def test_random_name(self):
    for x in random.choices(range(5, 100), k=10):
      self.assertRegex(
        random_name(x),
        '^[0-9a-f]{{{}}}$'.format(x * 2),
        'Random name should be composed of [0-9a-f] and have corrent length'
      )

  def test_path_from_root(self):
    self.assertEqual(
      resolve_url(os.path.join(os.path.dirname(__file__), '..')),
      resolve_url(path_from_root()),
      'Path from root should be ../ from this file'
    )

  def test_detect_indentation(self):
    for indentation in random.choices(range(1, 11), k=10):
      code = self._get_code(indentation)
      
      self.assertEqual(
        detect_indentation(code),
        indentation,
        'Correctly detect indentation'
      )

  def test_add_indentation(self):
    for indentation in random.choices(range(1, 11), k=10):
      code_before = self._get_code(indentation)
      indentations_before = [ len(line) - len(line.lstrip()) for line in code_before.splitlines() ]

      code_after = add_indentation(code_before, indentation)
      indentations_after = [ len(line) - len(line.lstrip()) for line in code_after.splitlines() ]

      diff = [ after - before for after,before in zip(indentations_after, indentations_before) ]

      self.assertEqual(
        diff,
        [indentation] * len(indentations_after),
        'Indentation should be added correctly'
      )
