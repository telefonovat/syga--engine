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
from exceptions import GraphNodeColorizerException


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
    OPT_INT = 0   # pylint: disable=invalid-name
    OPT_COLOR = 1 # pylint: disable=invalid-name
    OPT_LIST = 2  # pylint: disable=invalid-name
    OPT_DICT = 3  # pylint: disable=invalid-name

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

    raise Exception('Invalid opt: {}'.format(opt))


  def _random_colors_argument_binary(self):
    """
    Generates a random valid argument for the color(s) parameter. Options are
      - int 1
      - a single color (str or Color instance)
      - a list of colors with just one item (str or Color instance)
      - a tuple of colors with just one item (str or Color instance)

    returns:
      - colors (int|str|Color|list|dict): valid argument for color kwarg
    """
    color = self._random_colors_argument()

    if isinstance(color, int):
      return 1

    if isinstance(color, (str, Color)):
      return color

    if isinstance(color, (list, tuple)):
      return color[:1]

    if isinstance(color, dict):
      return self._random_colors_argument_binary()

    raise Exception('Unknown color type: {}'.format(color))


  def _random_colors_argument_group(self):
    """
    Generates a random valid argument for the color(s) parameter. Options are
      - int greater than 1
      - a list of colors with more than one item (str or Color instance)
      - a tuple of colors with more than one item (str or Color instance)

    returns:
      - colors (int|str|Color|list|dict): valid argument for color kwarg
    """
    color = self._random_colors_argument()

    if isinstance(color, int):
      return max(2, color)

    if isinstance(color, (str, Color)):
      return self._random_colors_argument_group()

    if isinstance(color, (list, tuple, dict)):
      return self._random_colors_argument_group() if len(color) == 1 else color

    raise Exception('Unknown color type: {}'.format(color))


  #
  # Validation | ANCHOR
  #

  def test_validate_color_arg_valid(self):
    """
    Tests the validate_colors static function if the input is valid.

    conditions:
      - any valid color is invalid
    """
    for _ in range(200):
      colors = self._random_colors_argument()

      self.assertTrue(
        GraphNodeColorizer.validate_colors(colors),
        f'colors={colors} is valid'
      )


  def test_validate_color_arg_invalid(self):
    """
    Tests the validate_colors static function if the input is invalid. This is
    done by generating a random valid color and then malforming it.
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


  def test_validate_palette_arg_valid(self):
    """
    todo: implement this test
    """


  def test_validate_palette_arg_invalid(self):
    """
    todo: implement this test
    """


  def test_validate_range_arg(self):
    """
    Tests the validate_colors static function if the input is either valid of
    invalid.

    Conditions:
      - the lower bound must be a smaller number that the upper bound
      - integers and real numbers can be used - validity is unchanged
    """
    for _ in range(200):
      lower = random.randrange(-200, 200)
      upper = random.randrange(-200, 200)

      if random.random() > 0.5:
        lower += random.random()

      if random.random() > 0.5:
        upper += random.random()

      valid = lower < upper

      self.assertEqual(
        GraphNodeColorizer.validate_range((lower, upper)),
        valid,
        'Range {} is {}'.format((lower, upper), 'valid' if valid else 'invalid')
      )


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

    for key, value in props:
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

    transformed = {key for key, value in colorizer.transform(G).items() if value}

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
      - see _random_colors_argument_binary for valid binary colors - any valid
        binary color is a valid argument
    """
    props = ['color', 'colors']
    values = [self._random_colors_argument_binary() for _ in range(100)]

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
    values = [self._random_colors_argument_group() for _ in range(100)]

    for prop, value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()

      self.assertTrue(
        colorizer.has_group_interpretation(),
        'Group interpretation specified by {}={}'.format(prop, value)
      )


  def test_group_interpretation_specified_too_few_colors(self):
    """
    Tests the group interpretation when there are more distinct values than
    color specified by color(s) parameter. This can only happen if the type
    of color(s) parameter is an int or a list or a tuple.

    conditions:
      - too few colors should raise exception
    """
    props = ['color', 'colors']
    values = [self._random_colors_argument_group() for _ in range(100)]

    for prop, value in itertools.product(props, values):
      value = list(value.values()) if isinstance(value, dict) else value
      distinct = value if isinstance(value, int) else len(value)

      if distinct == 2:
        continue # 2 values will fall back to binary interpretation and not raise an exception

      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      G = Graph()

      # Add more unique values than colors
      distinct += random.randrange(1, 20)
      for v in range(distinct):
        G.add_node(v, lorem=random_name(50))

      colorizer.transform(G)

      msg = f'Should raise expection with colors={value} and {distinct} distinct values'

      with self.assertRaises(GraphNodeColorizerException, msg=msg):
        colorizer.interpret()


  def test_group_interpretation_two_colors_more_values(self):
    """
    Tests the fallback to binary interpretation when two colors specified and
    more than two unique values found. This can happen only if the color(s)
    parameter is an int, a list or a tuple.

    conditions:
      - binary interpretation should be used instead
      - no exception should be raised
    """
    props = ['color', 'colors']
    values = [self._random_colors_argument_group() for _ in range(100)]

    for prop, v in itertools.product(props, values):
      v = 2 if isinstance(v, int) else list(v.values())[:2] if isinstance(v, dict) else v[:2]
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: v })
      G = Graph()

      # Add more unique values than colors
      for w in range(random.randrange(3, 30)):
        G.add_node(w, lorem=random_name(50))

      colorizer.transform(G)
      colorizer.interpret() # This should not raise an exception

      self.assertTrue(
        colorizer.has_binary_interpretation(),
        f'Binary interpretation should be used when colors={v} and >2 distinct values'
      )


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
    binary interpretation automatically - no interpretation parameters used.

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
        G.nodes[i][prop] = random.random() > 0.5

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_binary_interpretation(),
      'Guess binary interpretation when True/False values'
    )


  def test_binary_interpretation_guess_lambda(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    binary interpretation automatically - no interpretation parameters used.

    Lambda transformation is used

    conditions:
      - only True and False transformed values cause binary interpretation
    """
    G = Graph()
    colorizer = GraphNodeColorizer.build(lambda v, G: bool(v % 2))

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_binary_interpretation(),
      'Guess binary interpretation when True/False values produced by lambda'
    )


  def test_group_interpretation_guess_meta(self):
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


  def test_group_interpreattion_guess_lambda(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    group interpretation automatically - no interpretation parameters used

    Lambda transformation is used

    conditions:
      - transformed values are from {0, ..., 9} - this should cause group
        interpretation to be chosen
    """
    transform = lambda v, G: v % 10
    G = Graph()
    colorizer = GraphNodeColorizer.build(transform)
    unique = set()

    for v in range(random.randrange(500, 1000)):
      if random.random() > 0.5:
        G.add_node(v)
        unique.add(transform(v, G))

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_group_interpretation(),
      f'Guess group interpretation when unique values are {unique}'
    )


  def test_identity_interpretation_guess_meta(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    identity interpretation automatically - no interpretation parameters used

    Meta transformation is used

    conditions:
      - transformed values are colors
    """
    G = Graph()
    prop = random_name()
    colors = [random_color() for _ in range(random.randint(5, 20))]
    colorizer = GraphNodeColorizer.build(prop=prop)

    for v in range(random.randint(500, 1000)):
      if random.random() > 0.5:
        G.add_node(v)
        G.nodes[v][prop] = colors[v % len(colors)]

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_identity_interpretation(),
      f'Guess identity interpretation when unique values are {set(colors)}'
    )


  def test_identity_interpretation_guess_lambda(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    identity interpretation automatically - no interpretation parameters used

    Lambda transformation is used

    conditions:
      - transformed values are colors
    """
    G = Graph()
    colors = [random_color() for _ in range(random.randint(5, 20))]
    colorizer = GraphNodeColorizer.build(lambda v, G: colors[v % len(colors)])

    for v in range(random.randint(500, 1000)):
      if random.random() > 0.5:
        G.add_node(v)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_identity_interpretation(),
      f'Guess identity interpretation when unique values are {set(colors)}'
    )


  def test_spectral_interpretation_guess_meta(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    spectral interpretation automatically - no interpretation parameters used

    Meta transformation is used

    conditions:
      - transformed values are of type int and float (at least one float)
    """
    G = Graph()
    prop = random_name()
    colorizer = GraphNodeColorizer.build(prop=prop)

    for v in range(random.randint(500, 1000)):
      if random.random() > 0.5:
        G.add_node(v)
        if random.random() > 0.5:
          G.nodes[v][prop] = random.randint(-99, 99)
          if random.random() > 0.5:
            G.nodes[v][prop] += random.random() * 2 - 1

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_spectral_interpretation(),
      'Guess spectral interpretation when values are of types int and float'
    )


  def test_spectral_interpretation_guess_lambda(self):
    """
    Tests the conditions which should cause the graph visualizer to choose the
    spectral interpretation automatically - no interpretation parameters used

    Lambda transformation is used

    conditions:
      - transformed values are of type int and float (at least one float)
    """
    G = Graph()
    scale = random.random()
    shift = random.random() * random.randint(50, 100)
    colorizer = GraphNodeColorizer.build(lambda v, G: v * scale + shift)

    for v in range(random.randint(500, 1000)):
      if random.random() > 0.5:
        G.add_node(v)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertTrue(
      colorizer.has_spectral_interpretation(),
      'Guess spectral interpretation when values are of types int and float'
    )

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
    values = [self._random_colors_argument_binary() for _ in range(100)]

    for prop, value in itertools.product(props, values):
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })

      colorizer.interpret()

      if value == 1:
        excepted = colorizer.DEFAULT_TRUE_COLOR
      elif isinstance(value, (list, tuple)):
        excepted = value[0]
      else:
        excepted = value

      self.assertEqual(
        colorizer.compute_single(True),
        Color(excepted),
        f'Binary interpretation specified by {prop}={value} --> True'
      )

      self.assertEqual(
        colorizer.compute_single(False),
        colorizer.DEFAULT_FALSE_COLOR,
        f'Binary interpretation specified by {prop}={value} --> False'
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

      for key,color in colors.items():
        index = list(colors.values()).index(color)

        self.assertEqual(
          colorizer.compute_single(key),
          Color(color) if value != len(colors) else Color(palette[index]),
          f'Group interpretation specified by {prop}={value} --> {key} = {color}'
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
