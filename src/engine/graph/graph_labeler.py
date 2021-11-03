"""
The GraphLabeler module
"""

import types
from collections.abc import Iterable
from exceptions import GraphLabelerException, GraphEdgeLabelerException, GraphNodeLabelerException
from components.logger import logger # pylint: disable=unused-import


class GraphLabeler:
  """
  An abstract class which is the base for the following classes:
    - GraphNodeLabeler
    - GraphEdgeLabeler

  GraphLabeler computes the labels of the items of a graph. The process
  is described in the following document:
    - https://syga.kam.mff.cuni.cz/docs/graphs/labels/labels
  """
  def transform_single(self, *args):
    """
    Transforms a single value
    """
    transformed = self._transform(*args)

    if transformed is None:
      return None

    if isinstance(transformed, Iterable):
      return [str(part) for part in transformed]

    return [str(transformed)]


  def transform(self, G):
    """
    Runs the _transform method for every item in the graph, thus creating the
    transformed structure state for the specified Graph component.

    This method MUST be overridden.

    parameters:
      - G (networkx.Graph): the graph to transform

    returns:
      - transformed_state (dict): item to transformed information
    """
    raise NotImplementedError()


  def interpret(self):
    """
    Interpretation determines the formatting of the text. The possible choices
    are:
      - Plain
      - HTML
      - Markdown
      - Latex

    Filters are currently not implemented. The only filter used is Plain,
    therefore this method is empty.
    """


  def compute_single(self, value):
    """
    Computes the label for the single specified value.

    parameters:
      - value (list of string): The transformed value
    """
    if value is None:
      return None

    if self._separator is not None:
      return self._separator.join(value)

    return format(value, self._format)


  def compute(self, transformed_state):
    """
    Computes the styles for every item in the transformed_style dict

    This method MUST be overridden

    parameters:
      - transformed_state: item to transformed value (by transform())

    returns:
      - style: item to its style
    """
    raise NotImplementedError()


  def __init__(self, transform, **kwargs):
    """
    Creates a new instance of GraphLabeler.

    One of the following two methods must be used instead of the constructor:
      - GraphNodeLabeler.build
      - GraphEdgeLabeler.build
    """
    if 'format' in kwargs and 'separator' in kwargs:
      raise GraphLabelerException('Format and separator arguments are mutually exclusive')

    self._transform = transform

    self._format = None
    self._separator = None

    if 'format' in kwargs:
      self._format = kwargs['format']

    if 'separator' in kwargs:
      self._separator = kwargs['separator']

    if self._format is None and self._separator is None:
      self._separator = ', '

    # todo: implement
    # if not GraphLabeler.validate_format(self._format):
    #   raise GraphLabelerException(f'Invalid value for parameter format: {self._format}')

    # todo: implement
    # if not GraphLabeler.validate_separator(self._separator):
    #   raise GraphLabelerException(f'Invalid value for parameter separator: {self._separator}')


class GraphNodeLabeler(GraphLabeler):
  """
  GraphNodeLabeler computes the labels of the nodes of a graph. The process
  is described in the following document:
    - https://syga.kam.mff.cuni.cz/docs/graphs/labels/labels

  todo: implement filters
  """

  def transform(self, G):
    """
    Runs the _transform method for every node in the graph, thus creating the
    transformed structure state for the specified Graph component

    parameters:
      - G (networkx.Graph): the graph to transform

    returns:
      - transformed_state (dict): node to transformed information
    """
    res = {}

    for v in G.nodes:
      res[v] = self.transform_single(v, G)

    return res


  def compute(self, transformed_state):
    """
    Computes the styles for every node in the transformed_style dict

    parameters:
      - transformed_state (dict): node to transformed value (by transform())

    returns:
      - style (dict): node to its style
    """
    if transformed_state is None:
      return None

    return {key: self.compute_single(value) for key, value in transformed_state.items()}


  @staticmethod
  def build(*args, **kwargs):
    """
    Creates a GraphNodeLabeler
    """
    if len(args) >= 2:
      raise GraphNodeLabelerException('Too many positional arguments')

    if len(args) == 1:
      if isinstance(args[0], types.FunctionType):
        return GraphNodeLabeler(args[0], **kwargs)

      raise GraphNodeLabelerException(f'Cannot use object of type {type(args[0])} as source')

    if 'prop' in kwargs and 'props' in kwargs:
      raise GraphLabelerException('Prop and props arguments are mutually exclusive')

    props = dict.get(kwargs, 'prop', None) or dict.get(kwargs, 'props', None)

    if props is None:
      raise GraphNodeLabelerException('Source not specified')

    props = list(props) if isinstance(props, Iterable) else [props]

    transform = lambda v, G: \
      ('' if prop not in G.nodes[v] else G.nodes[v][prop] for prop in props)

    return GraphNodeLabeler.build(transform, **kwargs)


class GraphEdgeLabeler(GraphLabeler):
  """
  GraphEdgeLabeler computes the labels of the edges of a graph. The process
  is described in the following document:
    - https://syga.kam.mff.cuni.cz/docs/graphs/labels/labels

  todo: implement filters
  """

  def transform(self, G):
    """
    Runs the _transform method for every edge in the graph, thus creating the
    transformed structure state for the specified Graph component

    parameters:
      - G (networkx.Graph): the graph to transform

    returns:
      - transformed_state (double dict): edge to transformed information
    """
    res = {}

    for u, v in G.edges:
      if u not in res:
        res[u] = {}

      res[u][v] = self.transform_single(u, v, G)

    return res


  def compute(self, transformed_state):
    """
    Computes the styles for every edge in the transformed_style dict

    parameters:
      - transformed_state (double dict): edge to transformed value (by transform())

    returns:
      - style (double dict): edge to its style
    """
    if transformed_state is None:
      return None

    res = {}

    for u in transformed_state.keys():
      if u not in res:
        res[u] = {}

      for v in transformed_state[u].keys():
        res[u][v] = self.compute_single(transformed_state[u][v])

    return res


  @staticmethod
  def build(*args, **kwargs):
    """
    Creates a GraphEdgeLabeler
    """
    if len(args) >= 2:
      raise GraphEdgeLabelerException('Too many positional arguments')

    if len(args) == 1:
      if isinstance(args[0], types.FunctionType):
        return GraphEdgeLabeler(args[0], **kwargs)

      raise GraphEdgeLabelerException(f'Cannot use object of type {type(args[0])} as source')

    if 'prop' in kwargs and 'props' in kwargs:
      raise GraphLabelerException('Prop and props arguments are mutually exclusive')

    props = dict.get(kwargs, 'prop', None) or dict.get(kwargs, 'props', None)

    if props is None:
      raise GraphEdgeLabelerException('Source not specified')

    props = list(props) if isinstance(props, Iterable) else [props]

    transform = lambda u, v, G: \
      ('' if prop not in G.edges[u, v] else G.edges[u, v][prop] for prop in props)

    return GraphEdgeLabeler.build(transform, **kwargs)
