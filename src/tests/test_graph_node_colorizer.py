import unittest
from engine.graph import Graph
from engine.graph.node_colorizer import GraphNodeColorizer
from utils import random_name
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
    values = [1, 'blue', ['red'], '#333', '#123456', 'rgb(123, 12, 32)', 'rgba(12, 12, 12, 0.5)']
    # todo: implement random_color function

    for prop,value in itertools.product(props, values):
      G = Graph()
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })
      colorizer.interpret()
      self.assertEqual(
        colorizer._interpretation,
        colorizer.BINARY_INTERPRETATION,
        'Binary interpretation specified by {}={}'.format(prop, "'" + value + "'" if isinstance(value, str) else str(value))
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
        'Group interpretation specified by {}={}'.format(prop, "'" + value + "'" if isinstance(value, str) else str(value))
      )

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
      "Guess binary interpretation when True/False values"
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
      "Guess group interpretation when 10 different int values"
    )

  # todo: IDENTITY_INTERPRETATION guess
  # todo: random values tests --> they should yield GROUP_INTERPRETATION

  def test_compute_single_binary_interpretation(self):
    props = ['color', 'colors']
    values = [1, 'blue', ['red'], '#333', '#123456', 'rgb(123, 12, 32)', 'rgba(12, 12, 12, 0.5)']

    for prop,value in itertools.product(props, values):  
      colorizer = GraphNodeColorizer.build(prop='lorem', **{ prop: value })

      colorizer.interpret()

      if value == 1:
        excepted = colorizer.DEFAULT_TRUE_COLOR
      elif isinstance(value, list):
        excepted = value[0]
      else:
        excepted = value

      comment = '{}={}'.format(prop, "'" + value + "'" if isinstance(value, str) else str(value))

      self.assertEqual(
        colorizer.compute_single(True),
        excepted,
        "Binary interpretation specified by {} --> True".format(comment)
      )

      self.assertEqual(
        colorizer.compute_single(False),
        colorizer.DEFAULT_FALSE_COLOR,
        "Binary interpretation specified by {} --> False".format(comment)
      )
