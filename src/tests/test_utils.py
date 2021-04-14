import unittest
import re
from utils import random_name, path_from_root
import random
import os
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


class TestUtils(unittest.TestCase):
  def test_random_name(self):
    for x in random.choices(range(5, 100), k=10):
      self.assertTrue(
        re.match('^[0-9a-f]{{{}}}$'.format(x * 2), random_name(x)),
        'Random name should be composed of [0-9a-f] and have corrent length'
      )

  def test_path_from_root(self):
    self.assertEqual(
      resolve_url(os.path.join(os.path.dirname(__file__), '..')),
      resolve_url(path_from_root()),
      'Path from root should be ../ from this file'
    )
