"""
The GraphNodeColorizer module
"""

import types
import seaborn as sns
from engine.color import Color


class GraphNodeColorizer:
  """
  GraphNodeColorizer computes the colors of the nodes in a graph. The process
  is described in the following document:
    - todo: add link
  """

  BINARY_INTERPRETATION = 0
  GROUP_INTERPRETATION = 1
  IDENTITY_INTERPRETATION = 2
  SPECTRAL_INTERPRETATION = 3

  DEFAULT_FALSE_COLOR = None
  DEFAULT_TRUE_COLOR = Color('blue')

  DEFAULT_DISCRETE_PALETTE = 'hls' # sns.color_palette("hls", 8)
  DEFAULT_CONTINUOUS_PALETTE = 'Spectral' # sns.color_palette("Spectral", as_cmap=True)


  @staticmethod
  def build(*args, **kwargs):
    """
    Creates the GraphNodeColorizer
    """
    if len(args) >= 2:
      raise Exception('Too many positional arguments')

    if len(args) == 1:
      if not isinstance(args[0], types.FunctionType):
        # todo: validate the used of in operator
        return GraphNodeColorizer.build(lambda v, graph: v in args[0], **kwargs)
      return GraphNodeColorizer(args[0], **kwargs)

    if 'prop' not in kwargs:
      raise Exception('Source not specified')

    prop = kwargs['prop']
    transform = lambda v, graph: None if prop not in graph.nodes[v] else graph.nodes[v][prop]
    return GraphNodeColorizer.build(transform, **kwargs)


  def transform(self, graph):
    """
    Runs the _transform method for every node in the graph, thus creating the
    transformed structure state for the specified Graph component

    parameters:
      - graph (networkx.Graph): the graph to transform

    returns:
      - transformed_state (dict): node to transformed information
    """
    res = {}

    for node in graph.nodes:
      transformed = self._transform(node, graph)
      res[node] = transformed
      if transformed is not None:
        self._unique_values.add(transformed)

    return res


  def _binary_interpretation(self, true=None, false=None):
    """
    States that this graph node colorizer will use binary interpretation.
    The colors for true and false values can be specified. If omitted, default
    value are used.

    After this method runs, the value of _colors will be a tuple of two colors:
      - first color is the false color
      - second color is the true color

    This enable for writing `_colors[int(bool(value))]`

    parameters:
      - true (color): the color of true values (must be a valid argument of Color)
      - false (color): the color of false values (must be a valid argument of Color)
    """
    true_color = Color(true) if true is not None else self.DEFAULT_TRUE_COLOR
    false_color = Color(false) if false is not None else self.DEFAULT_FALSE_COLOR

    self._colors = (false_color, true_color)
    self._interpretation = self.BINARY_INTERPRETATION


  def _group_interpretation(self, colors):
    """
    States that this graph node colorizer will use group interpretation.
    The colors of the groups can be specified by one of the following:

     - int: the number of groups; default discrete palette will be used to
       generate the colors of the groups

     - list: the colors to be used, one for every group, association will be
       determined at the end of the method

     - dict: value to color; each group gets a color; groups with no colors will
       have the DEFAULT_FALSE_COLOR

    After this method runs, the value of _colors will be a dict which for every
    known value specified a color. Values which are missing from this dict will
    have the DEFAULT_FALSE_COLOR

    parameters:
      - colors (int|list|dict): the colors of the groups
    """
    self._interpretation = self.GROUP_INTERPRETATION

    if isinstance(colors, int):
      palette = sns.color_palette(self.DEFAULT_DISCRETE_PALETTE, colors)
      self._colors = [Color(color) for color in palette]

    elif isinstance(colors, list):
      self._colors = [Color(color) for color in colors]

    elif isinstance(colors, dict):
      self._colors = {key: Color(color) for key, color in colors.items()}

    # If _colors is a list, it will be turned into a dict if possible. It may
    # not be possible if there are more unique items than the number of colors
    # In such case an Exception is raised
    if isinstance(self._colors, list):
      uniq = self._unique_values

      if len(self._colors) < len(uniq):
        if len(self._colors) == 2:
          # Two colors with more unique values will turn into binary
          # interpretation with the specified colors as true/false colors
          self._binary_interpretation(*self._colors)
        else:
          raise Exception('Too few colors: found {} unique values'.format(len(uniq)))
      else:
        self._colors = dict(zip(sorted(uniq), self._colors[:len(uniq)]))


  def _identity_interpretation(self):
    """
    States that this graph node colorizer will use identity interpretation.
    """
    self._interpretation = self.IDENTITY_INTERPRETATION


  def _spectral_interpretation(self):
    """
    States that this graph node colorizer will use spectral interpretation.
    The upper and lower boundaries of the unique values will be computed. If
    there are no unique values -inf and +inf is used.

    After this method runs the value of _range will a tuple of two items:
      - The first item is the lower bound of the range
      - The second item is the upper bound of the range
    """
    self._interpretation = self.SPECTRAL_INTERPRETATION

    if self._range is None:
      uniq = self._unique_values
      lower = float('-inf') if uniq else min(uniq)
      upper = float('+inf') if uniq else max(uniq)

    self._range = (lower, upper)


  def _guess_interpretation(self):
    """
    Used to guess the correct interpretation if no interpretation parameters
    were specified. The contents of _unique_values are used. The options are:
      - a subset of {True, False} (inc. an empty set) --> BINARY_INTERPRETATION
      - a set of colors --> IDENTITY_INTERPRETATION
      - everything else --> GROUP_INTERPRETATION
    """
    uniq = self._unique_values

    if uniq in ({True, False}, {True}, {False}, set()):
      self._binary_interpretation()

    elif {type(x) for x in uniq} == {int, float}:
      self._spectral_interpretation()

    elif Color.are_colors(uniq):
      self._identity_interpretation()

    else:
      self._group_interpretation(len(self._unique_values))


  def interpret(self):
    """
    If the interpretation was specified by a parameter, the type of the
    interpretation is computed.

    If the interpretation was NOT specified, it is guessed using the
    _guess_interpretation method. See this method for more info

    After interpretation the type of _colors, _range and _palette may change.
    Each interpretation type defines the requested type of the props.

    The type of _colors depends on the type of interpretation:
      - BINARY_INTERPRETATION   --> tuple ("true color", "false color")
      - GROUP_INTERPRETATION    --> dict value to color
      - IDENTITY_INTERPRETATION --> None
      - SPECTRAL_INTERPRETATION --> None

    The type of _range depends on the type of interpretation:
      - BINARY_INTERPRETATION   --> None
      - GROUP_INTERPRETATION    --> None
      - IDENTITY_INTERPRETATION --> None
      - SPECTRAL_INTERPRETATION --> tuple (lower, upper)
    """
    if self._colors is not None:
      if isinstance(self._colors, int):
        if self._colors == 1:
          self._binary_interpretation()
        elif self._colors > 1:
          self._group_interpretation(self._colors)

      elif Color.is_color(self._colors):
        self._binary_interpretation(self._colors)

      elif isinstance(self._colors, list):
        if len(self._colors) == 1:
          self._binary_interpretation(self._colors[0])
        elif len(self._colors) > 1:
          self._group_interpretation(self._colors)

      elif isinstance(self._colors, dict):
        self._group_interpretation(self._colors)

      # Unable to determine the interpretation type - if this happends, it is
      # an implementation error - the arguments MUST be validated properly
      if self._interpretation is None:
        raise Exception('Error during the colorization process')

    # todo: consider the _palette

    else:
      self._guess_interpretation()


  def compute_single(self, value):
    """
    Computes the color for the single specified value. The process depends on
    the type of the interpretation.
    """
    if value is None:
      return None

    if self._interpretation == self.BINARY_INTERPRETATION:
      return self._colors[int(bool(value))]

    if self._interpretation == self.GROUP_INTERPRETATION:
      return self._colors[value] if value in self._colors else self.DEFAULT_FALSE_COLOR

    if self._interpretation == self.SPECTRAL_INTERPRETATION:
      if not isinstance(value, (int, float)):
        # Do not raise an exception here, instead the node will have no color
        # Todo: maybe add warning
        return self.DEFAULT_FALSE_COLOR
      lower, upper = self._range
      point = min(1, max(0, (value - lower) / (upper - lower)))
      return 'color-' + str(point) # todo: use actual palette

    if self._interpretation == self.IDENTITY_INTERPRETATION:
      return value

    raise Exception('Unknown interpretation type')


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


  def has_spectral_interpretation(self):
    """
    Returns True if spectral interpretation is used
    """
    return self._interpretation == self.SPECTRAL_INTERPRETATION


  @staticmethod
  def validate_colors(colors):
    """
    Validates the value of colors. The validity criteria is based on the type
      - None: always valid (color(s) parameter was omitted)
      - int: valid if greater than 0
      - str: valid if is color
      - list: valid if not empty and consists only of colors
      - tuple: same as list
      - dict: valid if not empty and the values are colors

    All other types are considered invalid.

    parameters:
      - colors (any): The color(s) argument

    returns:
      - validity (bool): True if valid False otherwise
    """
    if colors is None:
      return True

    if isinstance(colors, int):
      return colors > 0

    if isinstance(colors, (list, tuple)):
      return colors and Color.are_colors(colors)

    if isinstance(colors, dict):
      return colors and Color.are_colors(colors.values())

    return Color.is_color(colors)


  @staticmethod
  def validate_palette(palette):
    """
    Validates the value of _palette.

    parameters:
      - palette (any): The palette argument

    returns:
      - validity (bool): True if valid False otherwise
    """
    if palette is None:
      return True

    # todo: implement this
    return True


  @staticmethod
  def validate_range(ran):
    """
    Validates the value of _range. Following rules must be met:
      - type is list or tuple
      - length is two
      - both items are of type int or float
      - first item is lower than the second item

    If the type of _range is list, it is cast to tuple.

    parameters:
      - ran (any): The range argument

    returns
      - validity (bool): True if valid False otherwise
    """
    if ran is None:
      return True

    if not isinstance(ran, (tuple, list)) or len(ran) != 2:
      return False

    low, upp = ran

    return isinstance(low, (int, float)) and isinstance(upp, (int, float)) and low < upp


  def _prepare_colors(self):
    """
    Prepares the _colors property after retrieving it as an argument
    """
    if isinstance(self._colors, tuple):
      self._colors = list(self._colors)


  def _prepare_palette(self):
    """
    Prepares the _palette property after retrieving it as an argument
    """


  def _prepare_range(self):
    """
    Prepares the _range property after retrieving it as an argument
    """
    if isinstance(self._range, list):
      self._range = tuple(self._range)


  def __init__(self, transform, **kwargs):
    """
    Creates a new instance of GraphNodeColorizer

    GraphNodeColorizer.build MUST be used instead of this constructor. This
    constructore can be considered private
    """
    if 'color' in kwargs and 'colors' in kwargs:
      raise Exception('Color and colors arguments are mutually exclusive')

    self._transform = transform

    self._unique_values = set()
    self._interpretation = None

    self._colors = None
    self._palette = None
    self._range = None

    if 'color' in kwargs:
      self._colors = kwargs['color']

    if 'colors' in kwargs:
      self._colors = kwargs['colors']

    if 'palette' in kwargs:
      self._palette = kwargs['palette']

    if 'range' in kwargs:
      self._range = kwargs['range']

    if self._palette is not None and self._colors is not None:
      raise Exception('Parameters color(s) and palette are mutually exclusive')

    if not GraphNodeColorizer.validate_colors(self._colors):
      raise Exception('Invalid value for parameter color(s): {}'.format(self._colors))

    if not GraphNodeColorizer.validate_palette(self._palette):
      raise Exception('Invalid value for parameter palette: {}'.format(self._palette))

    if not GraphNodeColorizer.validate_range(self._range):
      raise Exception('Invalid value for parameter range: {}'.format(self._range))

    self._prepare_colors()
    self._prepare_palette()
    self._prepare_range()
