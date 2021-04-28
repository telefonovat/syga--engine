"""
Tests for src/engine/graph/node_colorizer.py
"""

import unittest
import itertools
import random
import seaborn as sns
from engine.color import Color
from engine.graph import Graph
from engine.graph.node_colorizer import GraphNodeColorizer
from utils.random import random_name, random_color


class TestGraphNodeColorizer(unittest.TestCase):
  """
  Tests for src/engine/graph/node_colorizer.py
  """

  def _random_colors_argument(self):
    """
    Generates a random valid argument for the color(s) parameter. Options are
      - int greater than 0
      - a single color (str or Color instance)
      - a list of colors (str or Color instance, can be mixed)
      - a tuple of colors (str or Color instance, can be mixed)
      - a dict where values are colors (str or Color instance, can be mixed)

    returns:
      - colors (int|str|Color|list|dict): valid argument for color kwarg
    """
    OPT_INT = 0 # pylint: disable=invalid-name
    OPT_COLOR = 1 # pylint: disable=invalid-name
    OPT_LIST = 2 # pylint: disable=invalid-name
    OPT_DICT = 3 # pylint: disable=invalid-name

    opt = random.choice([OPT_INT, OPT_COLOR, OPT_LIST, OPT_DICT])

    if opt == OPT_INT:
      return random.randint(1, 20)

    if opt == OPT_COLOR:
      return random_color()

    if opt == OPT_LIST:
      l = [random_color() for _ in range(random.randint(1, 20))]
      return l if random.random() > 0.5 else tuple(l)

    if opt == OPT_DICT:
      return { random_name(4): random_color() for _ in range(random.randint(1, 20)) }

    raise Exception('Invalid opt')

  #
  # Validation | ANCHOR
  #

  def test_validate_color_arg_valid(self):
    """
    Tests the validate_colors static function if the input is valid.
    """
    for _ in range(200):
      colors = self._random_colors_argument()

      self.assertTrue(
        GraphNodeColorizer.validate_colors(colors),
        f'colors={colors} is valid'
      )


  def test_validate_palette_arg_valid(self):
    """
    todo: implement this test
    """


  def test_validate_range_arg_valid(self):
    """
    todo: implement this test
    """


  def test_validate_color_arg_invalid(self):
    """
    Tests the validate_colors static function if the input is invalid.
    """
    for _ in range(200):
      colors = self._random_colors_argument()

      if isinstance(colors, int):
        colors = 1 - colors # will be 0 or less

      if isinstance(colors, (str, Color)):
        colors = random_name(5) # not a color

      if isinstance(colors, (list, tuple)):
        was_tuple = isinstance(colors, tuple)
        colors = list(colors)
        colors.append(random_name(5)) # not a color
        random.shuffle(colors)
        if was_tuple:
          colors = tuple(colors)

      if isinstance(colors, dict):
        keys = list(colors.keys())
        values = list(colors.values())

        keys.append(random_name(5))
        values.append(random_name(5)) # not a color

        random.shuffle(keys)
        random.shuffle(values)

        colors = dict(zip(keys, values))

      self.assertFalse(
        GraphNodeColorizer.validate_colors(colors),
        f'colors={colors} is NOT valid'
      )


  def test_validate_palette_arg_invalid(self):
    """
    todo: implement this test
    """


  def test_validate_range_arg_invalid(self):
    """
    todo: implement this test
    """

  #
  # Transformation | ANCHOR
  #

  def test_meta_transformation(self):
    """
    Tests the meta transformation specified by parameter `prop`

    conditions:
      - the result of transformation must be a dict from node to value
    """
    G = Graph()
    prop = random_name()
    colorizer = GraphNodeColorizer.build(prop=prop)

    props = []
    for i in range(random.randrange(500, 1000)):
      if random.random() > 0.75:
        props.append((i, random.randint(1, 100)))

    for key,value in props:
      G.add_node(key)
      G.nodes[key][prop] = value

    self.assertEqual(
      colorizer.transform(G),
      dict(props),
      'Meta transformation of the specified property'
    )


  def test_set_transformation(self):
    """
    Tests the set transformation specified by a set reference

    conditions:
      - True transformed values should be the same as in set `s`
    """
    G = Graph()
    nodes = set()
    colorizer = GraphNodeColorizer.build(nodes)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      if random.random() > 0.75:
        nodes.add(i)

    transformed = {key for key,value in colorizer.transform(G).items() if value}

    self.assertEqual(transformed, nodes, 'Set transformation from the specified set')


  def test_lambda_transformation(self):
    """
    Tests the lambda transformation

    conditions:
      - lambda should be used correctly
    """
    G = Graph()
    colorizer = GraphNodeColorizer.build(lambda v,G: v ** 2)
    expected = dict()

    for i in range(random.randrange(500, 1000)):
      if random.random() > 0.75:
        G.add_node(i)
        expected[i] = i ** 2

    self.assertEqual(
      colorizer.transform(G),
      expected,
      'Lambda transformation using node ids'
    )

  #
  # Interpretation specified | ANCHOR
  #

  def test_binary_interpretation_specified(self):
    """
    Tests ways to specified usage of the binary transformation

    conditions:
      - 1 is valid
      - color name is valid
      - color hex of length 3 and 6 is valid
      - instance of Color is valid
      - list with exactly one item which is a valid parameter is valid
    """
    props = ['color', 'colors']
    values = [1, 'blue', ['red'], '#333', ['#123456'], Color((0.5, 0.1, 0.2)), [Color('pink')]]

    for prop, value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()

      self.assertTrue(
        colorizer.has_binary_interpretation(),
        'Binary interpretation specified by {}={}'.format(prop, str(value))
      )


  def test_group_interpretation_specified(self):
    """
    Tests ways to specify usage of the group interpretation

    conditions:
      - int greater than 1 is valid
      - list of multiple valid colors is valid
      - dict of valid colors is valid
      - different representations of colors can be mixed
    """
    props = ['color', 'colors']
    values = [
      2,
      3,
      4,
      ['red', 'blue'],
      { 'foo': 'red', 'bar': 'blue' },
      [Color('pink'), Color('grey')],
      { 'lorem': Color((0.1, 0.2, 0.3)), 'ipsum': 'red', 'dolor': '#123' }
    ]

    for prop,value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()

      self.assertTrue(
        colorizer.has_group_interpretation(),
        'Group interpretation specified by {}={}'.format(prop, value)
      )


  def test_group_interpretation_specified_too_few_colors(self):
    """
    todo: implement this test

    conditions:
      - too few colors should raise exception
    """


  def test_group_interpretation_two_colors_more_values(self):
    """
    todo: implement this test

    conditions:
      - binary interpretation should be used instead
      - no exception should be raised
    """


  def test_spectral_interpretation_specified(self):
    """
    todo: implement this test

    conditions:
      - continuous palette is valid
      - discrete palette is valid
    """

  #
  # Interpretation guess | ANCHOR
  #

  def test_binary_interpretation_guess_set(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    binary interpretation automatically - no interpretation parameters used

    Set transformation is used

    conditions:
      - only True and False transformed values cause binary interpretation
    """
    G = Graph()
    nodes = set()
    colorizer = GraphNodeColorizer.build(nodes)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      if random.random() > 0.75:
        nodes.add(i)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_binary_interpretation(),
      'Guess binary interpretation when True/False values'
    )


  def test_binary_interpretation_guess_meta(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    binary interpretation automatically - no interpretation parameters used

    Meta transformation is used

    conditions:
      - only True and False transformed values cause binary interpretation
    """
    G = Graph()
    prop = random_name()
    colorizer = GraphNodeColorizer.build(prop=prop)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      if random.random() > 0.75:
        G.nodes[i]['prop'] = random.random() > 0.5

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_binary_interpretation(),
      'Guess binary interpretation when True/False values'
    )


  def test_group_interpretation_guess(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    group interpretation automatically - no interpretation parameters used

    Meta transformation is used

    conditions:
      - transformed values are from {0, ..., 9} - this should cause group
        interpretation to be chosen
    """
    G = Graph()
    colorizer = GraphNodeColorizer.build(prop='component')
    components = range(10)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      G.nodes[i]['component'] = random.choice(components)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_group_interpretation(),
      'Guess group interpretation when 10 different int values'
    )


  def test_group_interpretation_guess_random(self):
    """
    todo: implement this test
    """


  def test_identity_interpretation_guess(self):
    """
    todo: implement this test
    """


  def test_spectral_interpretation_guess(self):
    """
    todo: implement this test
    """

  #
  # Compute single - interpretation specified | ANCHOR
  #

  def test_compute_single_binary_interpretation_specified(self):
    """
    Tests compute_single method when binary interpretation is used.

    Conditions:
      - an instance of Color, equal to the specified color, is returned
      - if an int=1 was specified, the default true color should be returned
    """
    props = ['color', 'colors']
    values = [1, 'blue', ['red'], '#333', '#123456']

    for prop,value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })

      colorizer.interpret()

      if value == 1:
        excepted = colorizer.DEFAULT_TRUE_COLOR
      elif isinstance(value, list):
        excepted = value[0]
      else:
        excepted = value

      comment = '{}={}'.format(prop, ''' + value + ''' if isinstance(value, str) else str(value))

      self.assertEqual(
        colorizer.compute_single(True),
        Color(excepted),
        'Binary interpretation specified by {} --> True'.format(comment)
      )

      self.assertEqual(
        colorizer.compute_single(False),
        colorizer.DEFAULT_FALSE_COLOR,
        'Binary interpretation specified by {} --> False'.format(comment)
      )


  def test_compute_single_group_interpretation_specified(self):
    """
    Tests compute_single method when binary interpretation is used.

    Conditions:
      - The correct Color is returned
      - When an int>1 was used, a color from the default palette should be
        returned
    """
    props = ['color', 'colors']
    colors = { 'a': 'red', 'b': 'blue', 'c': 'green' }
    values = [len(colors), list(colors.values()), colors]
    palette = sns.color_palette(GraphNodeColorizer.DEFAULT_DISCRETE_PALETTE, len(colors))

    for prop,value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='foo', **{ prop: value })
      G = Graph()

      G.add_nodes_from([1, 2, 3])
      G.nodes[1]['foo'] = 'a'
      G.nodes[2]['foo'] = 'b'
      G.nodes[3]['foo'] = 'c'

      colorizer.transform(G)
      colorizer.interpret()

      comment = '{}={}'.format(prop, ''' + value + ''' if isinstance(value, str) else str(value))

      for key,color in colors.items():
        index = list(colors.values()).index(color)

        self.assertEqual(
          colorizer.compute_single(key),
          Color(color) if value != len(colors) else Color(palette[index]),
          'Group interpretation specified by {} --> {} = {}'.format(comment, key, color)
        )

      self.assertEqual(
        colorizer.compute_single('this_key_is_not_in_dict'),
        colorizer.DEFAULT_FALSE_COLOR,
        'Default if not in dict'
      )


  def test_compute_single_group_interpretation_two_colors_more_values_specified(self):
    """
    todo: implement this test
    """


  def test_compute_single_spectral_interpretation_specified(self):
    """
    todo: implement this test
    """

  #
  # Compute single - interpretation guessed | ANCHOR
  #

  def test_compute_single_binary_interpretation_guess(self):
    """
    todo: implement this test
    """


  def test_compute_single_group_interpretation_guess(self):
    """
    todo: implement this test
    """


  def test_compute_single_identity_interpretation_guess(self):
    """
    todo: implement this test
    """


  def test_compute_single_spectral_interpretation_guess(self):
    """
    todo: implement this test
    """

  #
  # Compute | ANCHOR
  #

  def test_compute_binary_interpretation(self):
    """
    todo: implement this test
    """


  def test_compute_group_interpretation(self):
    """
    todo: implement this test
    """


  def test_compute_identity_interpretation(self):
    """
    todo: implement this test
    """


  def test_compute_spectral_interpretation(self):
    """
    todo: implement this test
    """
