"""
The GraphShaper module
"""

import types
from collections.abc import Iterable
from engine.node_shape import NodeShape, AVAILABLE_NODE_SHAPES
from exceptions import GraphShaperException, GraphNodeShaperException


class GraphShaper:
  """
  An abstract class which is the base for the following classes:
    - GraphNodeShaper
    - GraphEdgeShaper

  GraphShaper computes the shapes of the items of a graph. The process
  is described in the following document:
    - https://syga.kam.mff.cuni.cz/docs/graphs/shapes/shapes
  """

  BINARY_INTERPRETATION = 0
  GROUP_INTERPRETATION = 1
  IDENTITY_INTERPRETATION = 2

  DEFAULT_FALSE_SHAPE = None
  DEFAULT_TRUE_SHAPE = None

  Shape = None


  def _binary_interpretation(self, true=None, false=None):
    """
    States that this graph shaper will use binary interpretation.
    The shapes for true and false values can be specified. If omitted, default
    value are used.

    After this method runs, the value of _shapes will be a tuple of two shapes:
      - first shape is the false shape
      - second shape is the true shape

    This enable for writing `_shapes[int(bool(value))]`

    parameters:
      - true (shape): the shape of true values (must be a valid argument of self.Shape)
      - false (shape): the shape of false values (must be a valid argument of self.Shape)
    """
    true_shape = self.Shape.create(true) if true is not None else self.DEFAULT_TRUE_SHAPE
    false_shape = self.Shape.create(false) if false is not None else self.DEFAULT_FALSE_SHAPE

    self._shapes = (false_shape, true_shape)
    self._interpretation = self.BINARY_INTERPRETATION


  def _group_interpretation(self, shapes):
    """
    States that this graph shaper will use group interpretation.
    The shapes of the groups can be specified by one of the following:

     - int: the number of groups; default discrete palette will be used to
       generate the shapes of the groups

     - list: the shapes to be used, one for every group, association will be
       determined at the end of the method

     - dict: value to shape; each group gets a shape; groups with no shapes will
       have the DEFAULT_FALSE_SHAPE

    After this method runs, the value of _shapes will be a dict which for every
    known value specified a shape. Values which are missing from this dict will
    have the DEFAULT_FALSE_SHAPE

    parameters:
      - shapes (int|list|dict): the shapes of the groups
    """
    self._interpretation = self.GROUP_INTERPRETATION

    if isinstance(shapes, int):
      max_shapes = len(AVAILABLE_NODE_SHAPES) - 1

      if shapes > max_shapes:
        raise GraphShaperException(f'Too many groups: {shapes}. There are only {max_shapes} shapes')

      # Consider edges
      self._shapes = [self.Shape.create(shape) for shape in AVAILABLE_NODE_SHAPES[:shapes]]

    if isinstance(shapes, list): # todo: turn this into elif
      self._shapes = [self.Shape.create(shape) for shape in shapes]

    elif isinstance(shapes, dict):
      self._shapes = {key: self.Shape.create(shape) for key, shape in shapes.items()}

    # If _shapes is a list, it will be turned into a dict if possible. It may
    # not be possible if there are more unique items than the number of shapes
    # In such case an Exception is raised
    if isinstance(self._shapes, list):
      uniq = self._unique_values

      if len(self._shapes) < len(uniq):
        if len(self._shapes) == 2:
          # Two shapes with more unique values will turn into binary
          # interpretation with the specified shapes as true/false shapes
          self._binary_interpretation(*self._shapes)
        else:
          raise GraphShaperException(f'Too few shapes: found {len(uniq)} unique values')
      else:
        self._shapes = dict(zip(sorted(uniq), self._shapes[:len(uniq)]))


  def _identity_interpretation(self):
    """
    States that this graph shaper will use identity interpretation.
    """
    self._interpretation = self.IDENTITY_INTERPRETATION


  def _guess_interpretation(self):
    """
    Used to guess the correct interpretation if no interpretation parameters
    were specified. The contents of _unique_values are used. The options are:
      - a subset of {True, False} (inc. an empty set) --> BINARY_INTERPRETATION
      - a set of shapes --> IDENTITY_INTERPRETATION
      - everything else --> GROUP_INTERPRETATION
    """
    uniq = self._unique_values

    if uniq in ({True, False}, {True}, {False}, set()):
      self._binary_interpretation()

    elif self.Shape.are_shapes(uniq):
      self._identity_interpretation()

    else:
      self._group_interpretation(len(self._unique_values))


  def transform_single(self, *args):
    """
    Transforms a single value
    """
    transformed = self._transform(*args)

    if isinstance(transformed, (dict, list)):
      raise GraphShaperException(f'Invalid value for graph shape: {transformed}')

    if transformed is not None:
      self._unique_values.add(transformed)

    return transformed


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
    If the interpretation was specified by a parameter, the type of the
    interpretation is computed.

    If the interpretation was NOT specified, it is guessed using the
    _guess_interpretation method. See this method for more info

    After interpretation the type of _shapes may change.
    Each interpretation type defines the requested type of the props.

    The type of _shapes depends on the type of interpretation:
      - BINARY_INTERPRETATION   --> tuple ("true shape", "false shape")
      - GROUP_INTERPRETATION    --> dict value to shape
      - IDENTITY_INTERPRETATION --> None
    """
    if self._shapes is not None:
      if isinstance(self._shapes, int):
        if self._shapes == 1:
          self._binary_interpretation()
        elif self._shapes > 1:
          self._group_interpretation(self._shapes)

      elif self.Shape.is_shape(self._shapes):
        self._binary_interpretation(self._shapes)

      elif isinstance(self._shapes, list):
        if len(self._shapes) == 1:
          self._binary_interpretation(self._shapes[0])
        elif len(self._shapes) > 1:
          self._group_interpretation(self._shapes)

      elif isinstance(self._shapes, dict):
        self._group_interpretation(self._shapes)

      # Unable to determine the interpretation type - if this happends, it is
      # an implementation error - the arguments MUST be validated properly
      if self._interpretation is None:
        raise GraphShaperException('Error during the shaping process')

    else:
      self._guess_interpretation()


  def compute_single(self, value):
    """
    Computes the shape for the single specified value. The process depends on
    the type of the interpretation.
    """
    if value is None:
      return None

    if self._interpretation == self.BINARY_INTERPRETATION:
      return self._shapes[int(bool(value))]

    if self._interpretation == self.GROUP_INTERPRETATION:
      return self._shapes[value] if value in self._shapes else self.DEFAULT_FALSE_SHAPE

    if self._interpretation == self.IDENTITY_INTERPRETATION:
      return value

    raise GraphShaperException('Unknown interpretation type')


  def compute(self, transformed_state):
    """
    Computes the styles for every item in the transformed_style dict.

    This method MUST be overridden

    parameters:
      - transformed_state (dict): item to transformed value (by transform())

    returns:
      - style (dict): item to its style
    """
    raise NotImplementedError()


  def has_interpretation(self):
    """
    Returns True if an interpretation has been specified
    """
    return self._interpretation is not None


  def has_binary_interpretation(self):
    """
    Returns True if binary interpretation is used
    """
    return self._interpretation == self.BINARY_INTERPRETATION


  def has_group_interpretation(self):
    """
    Returns True if group interpretation if used
    """
    return self._interpretation == self.GROUP_INTERPRETATION


  def has_identity_interpretation(self):
    """
    Returns True if identity interpretation is used
    """
    return self._interpretation == self.IDENTITY_INTERPRETATION


  def _validate_shapes(self, shapes):
    """
    Validates the value of shapes. The validity criteria is based on the type
      - None:  always valid (shape(s) parameter was omitted)
      - int:   valid if greater than 0
      - str:   valid if is shape
      - list:  valid if not empty and consists only of shapes
      - tuple: same as list
      - dict:  valid if not empty and the values are shapes
    All other types are considered invalid.

    returns:
      - validity (bool): True if valid False otherwise
    """
    if shapes is None:
      return True

    if isinstance(shapes, int):
      return shapes > 0

    if isinstance(shapes, (list, tuple)):
      return shapes and self.Shape.are_shapes(shapes)

    if isinstance(shapes, dict):
      return shapes and self.Shape.are_shapes(shapes.values())

    return self.Shape.is_shape(shapes)


  def _prepare_shapes(self):
    """
    Prepares the _shapes property after retrieving it as an argument
    """
    if isinstance(self._shapes, tuple):
      self._shapes = list(self._shapes)


  def __init__(self, transform, **kwargs):
    """
    Creates a new instance of GraphShaper

    GraphShaper.build MUST be used instead of this constructor. This
    constructore can be considered private.
    """
    if 'shape' in kwargs and 'shapes' in kwargs:
      raise GraphShaperException('Shape and shapes arguments are mutually exclusive')

    self._transform = transform

    self._unique_values = set()
    self._interpretation = None

    self._shapes = None

    if 'shape' in kwargs:
      self._shapes = kwargs['shape']

    if 'shapes' in kwargs:
      self._shapes = kwargs['shapes']

    if not self._validate_shapes(self._shapes):
      raise GraphShaperException(f'Invalid value for parameter shape(s): {self._shapes}')

    self._prepare_shapes()


class GraphNodeShaper(GraphShaper):
  """
  GraphNodeShaper computes the shapes of the items of a graph. The process
  is described in the following document:
    - https://syga.kam.mff.cuni.cz/docs/graphs/shapes/shapes
  """

  Shape = NodeShape

  DEFAULT_FALSE_SHAPE = None
  DEFAULT_TRUE_SHAPE = NodeShape('square')

  def transform(self, G):
    """
    Runs the _transform method for every node in the graph, thus creating the
    transformed structure state for the specified Graph component

    parameters:
      - G (networkx.Graph): the graph to transform

    returns:
      - transformed_state (dict): item to transformed information
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
    Creates a GraphNodeShaper
    """
    if len(args) >= 2:
      raise GraphNodeShaperException('Too many positional arguments')

    if len(args) == 1:
      if isinstance(args[0], Iterable):
        return GraphNodeShaper.build(lambda v, g: v in args[0], **kwargs)

      if isinstance(args[0], types.FunctionType):
        return GraphNodeShaper(args[0], **kwargs)

      raise GraphNodeShaperException(f'Cannot use object of type {type(args[0])} as source')

    if 'prop' not in kwargs:
      raise GraphNodeShaperException('Source not specified')

    prop = kwargs['prop']
    transform = lambda v, G: None if prop not in G.nodes[v] else G.nodes[v][prop]
    return GraphNodeShaper.build(transform, **kwargs)
