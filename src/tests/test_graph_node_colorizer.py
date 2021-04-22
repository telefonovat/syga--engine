import unittest
from engine.graph import Graph
from engine.graph.node_colorizer import GraphNodeColorizer
from utils import random_name
from colour import Color
import seaborn as sns
import itertools
import random


class TestGraphNodeColorizer(unittest.TestCase):
  #
  # Transformation
  #

  def test_meta_transformation(self):
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
    G = Graph()
    s = set()
    colorizer = GraphNodeColorizer.build(s)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      if random.random() > 0.75:
        s.add(i)

    self.assertEqual(
      set([ key for key,value in colorizer.transform(G).items() if value ]),
      s,
      'Set transformation from the specified set'
    )

  def test_lambda_transformation(self):
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
  # Interpretation specified
  #

  def test_binary_interpretation_specified(self):
    props = ['color', 'colors']
    values = [1, 'blue', ['red'], '#333', '#123456']
    # todo: implement random_color function

    for prop,value in itertools.product(props, values):
      G = Graph()
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()
      self.assertEqual(
        colorizer._interpretation,
        colorizer.BINARY_INTERPRETATION,
        'Binary interpretation specified by {}={}'.format(prop, ''' + value + ''' if isinstance(value, str) else str(value))
      )

  def test_group_interpretation_specified(self):
    props = ['color', 'colors']
    values = [2, 3, 4, ['red', 'blue'], { 'foo': 'red', 'bar': 'blue' }]

    for prop,value in itertools.product(props, values):
      G = Graph()
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()
      self.assertEqual(
        colorizer._interpretation,
        colorizer.GROUP_INTERPRETATION,
        'Group interpretation specified by {}={}'.format(prop, ''' + value + ''' if isinstance(value, str) else str(value))
      )

  def test_group_interpretation_specified_too_few_colors(self):
    # todo: implement this test
    pass

  def test_group_interpretation_two_colors_more_values(self):
    # todo: implement this test
    pass

  def test_spectral_interpretation_specified(self):
    # todo: implement this test
    pass

  #
  # Interpretation guess
  #

  def test_binary_interpretation_guess(self):
    G = Graph()
    s = set()
    colorizer = GraphNodeColorizer.build(s)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      if random.random() > 0.75:
        s.add(i)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertEqual(
      colorizer._interpretation,
      colorizer.BINARY_INTERPRETATION,
      'Guess binary interpretation when True/False values'
    )

  def test_group_interpretation_guess(self):
    G = Graph()
    colorizer = GraphNodeColorizer.build(prop='component')
    components = range(10)

    for i in range(random.randrange(500, 1000)):
      G.add_node(i)
      G.nodes[i]['component'] = random.choice(components)

    colorizer.transform(G)
    colorizer.interpret()

    self.assertEqual(
      colorizer._interpretation,
      colorizer.GROUP_INTERPRETATION,
      'Guess group interpretation when 10 different int values'
    )

  def test_group_interpretation_guess_random(self):
    # todo: implement this test
    pass
  
  def test_identity_interpretation_guess(self):
    # todo: implement this test
    pass

  def test_spectral_interpretation_guess(self):
    # todo: implement this test
    pass

  #
  # Compute single - interpretation specified
  #

  def test_compute_single_binary_interpretation_specified(self):
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
        self.assertEqual(
          colorizer.compute_single(key),
          Color(color) if value != len(colors) else Color(rgb=palette[list(colors.values()).index(color)]),
          'Group interpretation specified by {} --> {} = {}'.format(comment, key, color)
        )

      self.assertEqual(
        colorizer.compute_single('this_key_is_not_in_dict'),
        colorizer.DEFAULT_FALSE_COLOR,
        'Default if not in dict'
      )

  def test_compute_single_group_interpretation_two_colors_more_values_specified(self):
    # todo: implement this test
    pass

  def test_compute_single_spectral_interpretation_specified(self):
    # todo: implement this test
    pass

  #
  # Compute single - interpretation guessed
  #

  def test_compute_single_binary_interpretation_guess(self):
    # todo: implement this test
    pass

  def test_compute_single_group_interpretation_guess(self):
    # todo: implement this test
    pass

  def test_compute_single_identity_interpretation_guess(self):
    # todo: implement this test
    pass

  def test_compute_single_spectral_interpretation_guess(self):
    # todo: implement this test
    pass
  
  #
  # Compute
  #

  def test_compute_binary_interpretation(self):
    # todo: implement this test
    pass

  def test_compute_group_interpretation(self):
    # todo: implement this test
    pass

  def test_compute_identity_interpretation(self):
    # todo: implement this test
    pass

  def test_compute_spectral_interpretation(self):
    # todo: implement this test
    pass
