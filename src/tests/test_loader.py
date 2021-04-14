import unittest
from components import Loader
import json
from utils import random_name, resolve_url, path_from_root
import random
import os
from exceptions import LoaderException
from random_dict import random_string_dict


class TestLoader(unittest.TestCase):
  def _get_cfg(self):
    return json.dumps({
      'code': '\n'.join([
        'print("lorem")',
        'print("ipsum")',
        'for i in range(10):',
        '  print(i ** 2)'
      ])
    })

  def _get_loader(self):
    return Loader(self._get_cfg())
  
  def test_unique_id(self):
    loader = self._get_loader()

    self.assertRegex(
      loader.unique_id,
      '^_[0-9a-f]{32}$',
      'The unique ID should be 33 chars long and start with _'
    )

  def test_parse_cfg(self):
    not_json = random_name(random.randint(100, 200))
    loader = Loader(not_json)
    
    with self.assertRaises(LoaderException):
      loader.parse_cfg()

    # This should NOT raise an exception
    self._get_loader().parse_cfg()

  def test_validate_cfg(self):
    for _ in range(20):
      random_cfg = json.dumps(random_string_dict(random.randint(1, 5), random.randint(1, 5)))
      loader = Loader(random_cfg)

      # This should NOT raise an exception
      loader.parse_cfg()

      with self.assertRaises(LoaderException):
        loader.validate_cfg()

  def test_prepare_code(self):
    loader = self._get_loader()

    loader.parse_cfg()
    loader.validate_cfg()
    loader.prepare_code()

    lines = loader.code.splitlines()

    self.assertEqual(
      lines[0],
      'def {}(engine, print):'.format(loader.unique_id),
      'The first line of the file should be a function definition'
    )

  def test_create_module(self):
    loader = self._get_loader()

    loader.parse_cfg()
    loader.validate_cfg()
    loader.prepare_code()
    loader.create_module()

    self.assertTrue(
      resolve_url(path_from_root()) in resolve_url(loader.module_path),
      'Module should be somewhere inside root'
    )

    self.assertTrue(
      os.path.isfile(loader.module_path),
      'Python file should be created'
    )
