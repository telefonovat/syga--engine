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
  def is_color(*args, **kwargs):
    """
    Returns True if the arguments are valid for the Color constructor, ie. they
    will product a valid color. This is tested using very simple try/except

    returns:
      - is_color (bool): True if valid False otherwise
    """
    try:
      Color(*args, **kwargs)
      return True
    except:
      return False


  @staticmethod
  def are_colors(iterable):
    """
    Returns True if all items in the iterable are colors; False otherwise
    """
    return all([ GraphNodeColorizer.is_color(color) for color in iterable ])


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
      if transformed is not None:
        self._unique_values.add(transformed)
      
    return res


  def _binary_interpretation(self, t=None, f=None):
    """
    States that this graph node colorizer will use binary interpretation.
    The colors for true and false values can be specified. If omitted, default
    value are used

    parameters:
      - t (color): the color of true values (must be a valid argument of Color)
      - f (color): the color of false values (must be a valid argument of Color)
    """
    true_color = Color(t) if t is not None else self.DEFAULT_TRUE_COLOR
    false_color = Color(f) if f is not None else self.DEFAULT_FALSE_COLOR
    
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
      self._colors = [ Color(rgb=color) for color in sns.color_palette(self.DEFAULT_DISCRETE_PALETTE, colors) ]

    elif isinstance(colors, list):
      self._colors = [ Color(color) for color in colors ]

    elif isinstance(colors, dict):
      self._colors = dict([ (key, Color(color)) for key,color in colors.items() ])
    
    # If _colors is a list, it will be turned into a dict if possible. It may
    # not be possible if there are more unique items than the number of colors
    # In such case an Exception is raised
    if isinstance(self._colors, list):
      if len(self._colors) < len(self._unique_values):
        if len(self._colors) == 2:
          # Two colors with more unique values will turn into binary
          # interpretation with the specified colors as true/false colors
          self._binary_interpretation(*self._colors)
        else:
          raise Exception('Too few colors: found {} unique values'.format(len(self._unique_values))) # todo: use proper exception
      else:
        self._colors = dict(zip(sorted(self._unique_values), self._colors[:len(self._unique_values)]))


  def _identity_interpretation(self):
    """
    States that this graph node colorizer will use identity interpretation.
    """
    self._interpretation = self.IDENTITY_INTERPRETATION


  def _spectral_interpretation(self):
    """
    Stats that this graph node colorizer will use spectral interpretation.
    The upper and lower boundaries of the unique values will be computed. If
    there are no unique values -inf and +inf is used.
    """
    self._interpretation = self.SPECTRAL_INTERPRETATION

    if self._range is None:
      uv = self._unique_values
      lower = float('-inf') if len(uv) == 0 else min(uv)
      upper = float('+inf') if len(uv) == 0 else max(uv)

    self._range = (lower, upper)


  def interpret(self):
    """
    If the interpretation was specified by a parameter, the type of the
    interpretation is computed. During this process, the value of _colors is
    normalized, the type of _colors will depend on the interpretation type

    If the interpretation was NOT specified, it is guessed from the contents
    of _unique_values. The options are:
      - a subset of {True, False} (inc. an empty set) --> BINARY_INTERPRETATION
      - a set of colors --> IDENTITY_INTERPRETATION
      - everything else --> GROUP_INTERPRETATION

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

      elif isinstance(self._colors, str):
        self._binary_interpretation(self._colors)

      elif isinstance(self._colors, (list, tuple)):
        if len(self._colors) == 1:
          self._binary_interpretation(self._colors[0])
        elif len(self._colors) > 1:
          self._group_interpretation(self._colors)

      elif isinstance(self._colors, dict):
        self._group_interpretation(self._colors)

      # Unable to determine the interpretation type
      if self._interpretation is None:
        raise Exception('Invalid value of color(s) parameter') # todo: use proper exception

    # todo: consider _palette parameter

    else:
      uv = self._unique_values
      
      if uv == {True, False} or uv == {True} or uv == {False} or uv == {}:
        self._binary_interpretation()
        
      elif all([ isinstance(x, (float, int)) for x in uv ]) and any([ isinstance(x, float) for x in uv ]):
        self._spectral_interpretation()

      elif GraphNodeColorizer.are_colors(uv):
        self._identity_interpretation()

      else:
        self._group_interpretation(len(self._unique_values))


  def compute_single(self, value):
    """
    Computes the color for the single specified value. The process depends on
    the type of the interpretation.
    """
    if value is None:
      return None
    
    if self._interpretation == self.BINARY_INTERPRETATION:
      return self._colors[int(bool(value))]

    elif self._interpretation == self.GROUP_INTERPRETATION:
      return self._colors[value] if value in self._colors else self.DEFAULT_FALSE_COLOR

    elif self._interpretation == self.SPECTRAL_INTERPRETATION:
      if not isinstance(value, (int, float)):
        # Do not raise an exception here, instead the node will have no color
        # Todo: maybe add warning
        return self.DEFAULT_FALSE_COLOR
      lower,upper = self._range
      x = min(1, max(0, (value - lower) / (upper - lower)))
      return 'color-' + str(x) # todo: use actual palette
      
    elif self._interpretation == self.IDENTITY_INTERPRETATION:
      return value

    raise Exception('Unknown interpretation type') # todo: use proper exception


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


  def _validate_colors(self):
    """
    Validates the value of _colors. The validity criteria is based on the type
      - None: always valid (color(s) parameter was omitted)
      - int: valid if greater than 0
      - str: valid if is color
      - list: valid if not empty and consists only of colors
      - tuple: same as list
      - dict: valid if not empty and the values are colors

    All other types are considered invalid

    returns:
      - validity (bool): True if valid False otherwise
    """
    if self._colors is None:
      return True
    
    if isinstance(self._colors, int):
      return self._colors > 0

    elif isinstance(self._colors, str):
      return GraphNodeColorizer.is_color(self._colors)

    elif isinstance(self._colors, (list, tuple)):
      return len(self._colors) > 0 and GraphNodeColorizer.are_colors(self._colors)

    elif isinstance(self._colors, dict):
      return len(self._colors) > 0 and GraphNodeColorizer.are_colors(self._colors.values())

    return False


  def _validate_palette(self):
    """
    Validates the value of _palette.

    returns
      - validity (bool): True if valid False otherwise 
    """
    if self._palette is None:
      return True
    
    # todo: implement this
    return True


  def _validate_range(self):
    """
    Validates the value of _range. Following rules must be met:
      - type is list or tuple
      - length is two
      - both items are of type int or float
      - first item is lower than the second item

    If the type of _range is list, it is cast to tuple

    returns
      - validity (bool): True if valid False otherwise
    """
    if self._range is None:
      return True

    if isinstance(self._range, list):
      self._range = tuple(self._range)

    if not isinstance(self._range, tuple):
      return False

    if len(self._range) != 2:
      return False

    lower,upper = self._range

    return (
      isinstance(lower, (int, float)) and
      isinstance(upper, (int, float)) and
      lower < upper
    )


  def __init__(self, transform, **kwargs):
    """
    Creates a new instance of GraphNodeColorizer

    GraphNodeColorizer.build MUST be used instead of this constructor. This
    constructore can be considered private
    """
    if 'color' in kwargs and 'colors' in kwargs:
      raise Exception('color_nodes_by: color and colors arguments are mutually exclusive') # todo: use proper exception
    
    self._interpretation = None
    self._transform = transform
    self._unique_values = set()
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
      raise Exception('color(s) and palette parameters are mutually exclusive') # todo: use proper exception

    if not self._validate_colors():
      raise Exception('Invalid value for color(s) parameter: {}'.format(self._colors))

    if not self._validate_palette():
      raise Exception('Invalid value for palette parameter: {}'.format(self._palette))

    if not self._validate_range():
      raise Exception('Invalid value for range parameter: {}'.format(self._range))
