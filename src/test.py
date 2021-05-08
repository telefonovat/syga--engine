"""
The tests entrypoint
"""

import unittest
from dotenv import load_dotenv
from tests.test_utils import TestUtils # pylint: disable=unused-import
from tests.test_color import TestColor # pylint: disable=unused-import
from tests.test_loader import TestLoader # pylint: disable=unused-import
from tests.test_graph_node_colorizer import TestGraphNodeColorizer # pylint: disable=unused-import

if __name__ == '__main__':
  load_dotenv()
  unittest.main()
