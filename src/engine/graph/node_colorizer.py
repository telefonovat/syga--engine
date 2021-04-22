from colour import Color
import seaborn as sns


class GraphNodeColorizer:
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
      raise Exception('color_nodes_by: too many positional arguments') # todo: use proper exception

    if len(args) == 1:
      if not callable(args[0]):
        return GraphNodeColorizer.build(lambda v,G: v in args[0], **kwargs)
      return GraphNodeColorizer(args[0], **kwargs)

    else:
      if 'prop' not in kwargs:
        raise Exception('color_nodes_by: source not specified') # todo: use proper exception
      prop = kwargs['prop']
      return GraphNodeColorizer.build(lambda v,G: None if prop not in G.nodes[v] else G.nodes[v][prop], **kwargs)

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
      transformed = self._transform(v, G)
      res[v] = transformed
      self._unique_values.add(transformed)
      
    return res

  def _make_binary_interpretation(self, true_color=None, false_color=None):
    # todo: use this method in the interpret method
    pass

  def _make_group_interpretation(self, colors):
    # todo: use this method in the interpret method
    pass

  def _make_identity_interpretation(self):
    # todo: use this method in the interpret method
    pass

  def _make_spectral_interpretation(self):
    # todo: use this method in the interpret method
    pass

  def interpret(self):
    """
    If the interpretation was specified by a parameter, the type of the
    interpretation is computed. During this process, the value of _colors is
    normalized, meaning any scalar value is wrapped inside of a list.

    If the interpretation was NOT specified, it is guessed from the contents
    of _unique_values. The options are:
      - a subset of {True, False} (inc. an empty set) --> BINARY_INTERPRETATION
      - a set of colors --> IDENTITY_INTERPRETATION
      - everything else --> GROUP_INTERPRETATION

    The type of _colors depends on the type of interpretation:
      - BINARY_INTERPRETATION   --> tuple ("true color", "false color")
      - GROUP_INTERPRETATION    --> dict value to color
      - IDENTITY_INTERPRETATION --> undefined (does not matter)
      - SPECTRAL_INTERPRETATION --> tuple of (lower, upper)
    """
    if self._colors is not None:
      if isinstance(self._colors, int):
        if self._colors == 1:
          self._colors = (self.DEFAULT_FALSE_COLOR, self.DEFAULT_TRUE_COLOR)
          self._interpretation = self.BINARY_INTERPRETATION
        elif self._colors > 1:
          self._colors = [ Color(rgb=color) for color in sns.color_palette(self.DEFAULT_DISCRETE_PALETTE, self._colors) ]
          self._interpretation = self.GROUP_INTERPRETATION

      elif isinstance(self._colors, str):
        self._colors = (self.DEFAULT_FALSE_COLOR, Color(self._colors))
        self._interpretation = self.BINARY_INTERPRETATION

      elif isinstance(self._colors, (list, tuple)):
        if len(self._colors) == 1:
          self._colors = (self.DEFAULT_FALSE_COLOR, Color(self._colors[0]))
          self._interpretation = self.BINARY_INTERPRETATION
        elif len(self._colors) > 1:
          self._colors = [ Color(color) for color in self._colors ]
          self._interpretation = self.GROUP_INTERPRETATION

      elif isinstance(self._colors, dict):
        self._colors = dict([ (key, Color(color)) for key,color in self._colors.items() ])
        self._interpretation = self.GROUP_INTERPRETATION

      # Unable to determine the interpretation type
      if self._interpretation is None:
        raise Exception('Invalid value of color(s) parameter') # todo: use proper exception

      # At this point we know the type of the interpretation. If it is GROUP and
      # if the type is a list, it will be turned into a dict if possible. It may
      # not be possible if there are more unique items than the number of colors
      # In such case an Exception is thrown
      if self._interpretation == self.GROUP_INTERPRETATION and isinstance(self._colors, list):
        if len(self._colors) < len(self._unique_values):
          # todo: group interpretation based on True/False when two groups
          raise Exception('Too few colors: found {} unique values'.format(len(self._unique_values)))
        self._colors = dict(zip(sorted(self._unique_values), self._colors[:len(self._unique_values)]))

    else:
      if self._unique_values == {True, False} or self._unique_values == {True} or self._unique_values == {False} or self._unique_values == {}:
        self._interpretation = self.BINARY_INTERPRETATION
        self._colors = (self.DEFAULT_FALSE_COLOR, self.DEFAULT_TRUE_COLOR)
      elif all([ isinstance(x, (float, int)) for x in self._unique_values ]) and any([ isinstance(x, float) for x in self._unique_values ]):
        self._interpretation = self.SPECTRAL_INTERPRETATION
        self._colors = (min(self._unique_values), max(self._unique_values))
      # todo: implement IDENTITY_INTERPRETATION guess
      else:
        self._interpretation = self.GROUP_INTERPRETATION
        self._colors = [ 'color-' + str(i) for i in range(len(self._unique_values)) ] # todo: use actual palette

  def compute_single(self, value):
    """
    Computes the color for the single specified value. The process depends on
    the type of the interpretation.
    """
    if self._interpretation == self.BINARY_INTERPRETATION:
      return self._colors[int(bool(value))]

    elif self._interpretation == self.GROUP_INTERPRETATION:
      return self._colors[value] if value in self._colors else self.DEFAULT_FALSE_COLOR

    elif self._interpretation == self.SPECTRAL_INTERPRETATION:
      lower,upper = self._colors
      return 'color-' + str((value - lower) / (upper - lower)) # todo: use actual palette
      
    elif self._interpretation == self.IDENTITY_INTERPRETATION:
      return value

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

    return dict([ (key, self.compute_single(value)) for key,value in transformed_state.items() ])    

  def __init__(self, transform, **kwargs):
    """
    Creates a new instance of GraphNodeColorizer

    GraphNodeColorizer.build MUST be used instead of this constructor
    """
    if 'color' in kwargs and 'colors' in kwargs:
      raise Exception('color_nodes_by: color and colors arguments are mutually exclusive') # todo: use proper exception
    
    self._transform = transform
    self._unique_values = set()
    self._colors = None
    self._palette = None

    if 'color' in kwargs:
      self._colors = kwargs['color']

    if 'colors' in kwargs:
      self._colors = kwargs['colors']

    if 'palette' in kwargs:
      self._palette = kwargs['palette']

    self._interpretation = None
