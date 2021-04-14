import unittest
import re
from utils import random_name


class TestUtils(unittest.TestCase):
  def test_random_name(self):
    [ self.assertEqual(len(random_name(x)), x * 2, 'len = 2x bytes') for x in [10, 15, 20] ]
