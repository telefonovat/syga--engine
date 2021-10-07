"""
Tests for src/components/loader.py
"""

import unittest
import random
import os
from components import Loader
from utils.path import resolve_url, path_from_root
from utils.code import detect_indentation, get_sample_code
from utils.random import random_name


class TestLoader(unittest.TestCase):
  """
  Tests for src/components/loader.py

  Every tests is performed 20 times because some Loader methods and some parts
  of the tests rely on chance
  """

  def _get_cfg(self, uid):
    """
    Returns a sample valid config

    parameters:
      - uid (str): the unique ID of the module
    """
    cfg = {
      'code': get_sample_code(random.randint(1, 5) * 2)
    }

    if uid is not None:
      cfg['uid'] = uid

    return cfg


  def _get_admin_cfg(self, uid=None):
    """
    Returns a sample valid config with admin password
    """
    cfg = {
      'code': get_sample_code(random.randint(1, 5) * 2),
      'secret': 'super-secret-password'
    }

    if uid is not None:
      cfg['uid'] = uid

    return cfg


  def _get_loader(self, uid=None):
    """
    Returns a loader with valid config. A unique ID can be specified but will
    be ignored by the Loader, because the secret was not specified

    parameters:
      - uid (str): the unique ID of the module
    """
    return Loader().set_input(self._get_cfg(uid))


  def _get_admin_loader(self, uid=None):
    """
    Returns a loader with valid config and admin access. A unique ID can be
    specified. The unique ID will be the name of the module which runs the
    visualized algorithm

    parameters:
      - uid (str): the unique ID of the module
    """
    return Loader().set_input(self._get_admin_cfg(uid))


  def test_unique_id_random(self):
    """
    Tests whether the format of the random ID is correct when generated
    randomly.

    conditions:
      - prefixed with _
      - only symbols [_0-9a-f]
      - exactly 33 characters
      - uid can be specified but will be ignored with no admin access
    """
    for _ in range(20):
      loader = self._get_loader(random_name(random.randint(20, 30)))

      loader.generate_name()

      self.assertRegex(
        loader.unique_id,
        '^_[0-9a-f]{32}$',
        'The unique ID should be 33 chars long and start with _'
      )


  def test_unique_id_specified(self):
    """
    Tests whether unique ID can be specified with admin access.

    conditions:
      - the specified unique is used by the module
    """
    for _ in range(20):
      name = '_{}'.format(random_name(random.randint(10, 20)))
      loader = self._get_admin_loader(name)

      loader.parse_cfg()
      loader.generate_name()

      self.assertEqual(loader.unique_id, name, "Unique ID should equal the specified one")


  def test_parse_cfg_valid(self):
    """
    Tests a valid

    conditions:
      - valid input does not raise LoaderException
      - unique id is not checked before calling generate_name
    """
    for _ in range(20):
      self._get_loader(random_name(random.randint(10, 20))).parse_cfg()
      self._get_admin_loader(random_name(random.randint(10, 20))).parse_cfg()


  def test_prepare_code(self):
    """
    Tests whether the first line of the code is a wrapper functions definition

    conditions:
      - first line must be a function definition with correct parameters
      - indentation cannot be modified
    """
    for _ in range(20):
      loader = self._get_loader()

      loader.parse_cfg()

      # pylint: disable=protected-access
      indentation_before = detect_indentation(loader._cfg['code'])

      loader.generate_name()
      loader.prepare_code()

      lines = loader._code.splitlines()  # pylint: disable=protected-access
      indentation_after = detect_indentation(loader._code) # pylint: disable=protected-access

      self.assertEqual(
        lines[0],
        'def {}(engine, print):'.format(loader.unique_id),
        'The first line of the file should be a function definition'
      )

      self.assertEqual(
        indentation_before,
        indentation_after,
        'Indentation cannot be modified'
      )


  def test_create_module(self):
    """
    Tests whether the crete_module method creates the module

    conditions:
      - module is in project root directory
      - module file exists
      - contents of the module file are correct
    """
    for _ in range(20):
      loader = self._get_loader()

      loader.parse_cfg()
      loader.generate_name()
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

      with open(loader.module_path, 'r', encoding='utf8') as f:
        code = loader._code # pylint: disable=protected-access
        self.assertEqual(f.read(), code, "File contents should be correct")
