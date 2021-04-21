class GraphNodeColorizer:
  BINARY_INTERPRETATION = 0
  GROUP_INTERPRETATION = 1
  IDENTITY_INTERPRETATION = 2
  
  @staticmethod
  def build(*args, **kwargs):
    if len(args) >= 2:
      raise Exception('color_nodes_by: too many positional arguments') # todo: use proper exception

    if len(args) == 1:
      if not callable(args[0]):
        return GraphNodeColorizer.build(lambda v: v in args[0], **kwargs)
      return GraphNodeColorizer(args[0], **kwargs)

    else:
      if 'prop' not in kwargs:
        raise Exception('color_nodes_by: source not specified') # todo: use proper exception
      prop = kwargs['prop']
      return GraphNodeColorizer.build(lambda v,G: None if prop not in G.nodes[v] else G.nodes[v][prop], **kwargs)

  def transform(self, G):
    res = {}

    for v in G.nodes:
      transformed = self._transform(v, G) 
      res[v] = transformed
      self._unique_values.add(transformed)
      
    return res

  def interpret(self):
    if self._has_interpretation:
      if isinstance(self._colors, int):
        if self._colors == 1:
          self._interpretation = self.BINARY_INTERPRETATION
        elif self._colors > 1:
          self._interpretation = self.GROUP_INTERPRETATION

      elif isinstance(self._colors, list):
        if len(self._colors) == 1:
          self._interpretation = self.BINARY_INTERPRETATION
        elif len(self._colors) > 1:
          self._interpretation = self.GROUP_INTERPRETATION

      elif isinstance(self._colors, dict):
        self._interpretation = self.GROUP_INTERPRETATION

      if self._interpretation is None:
        raise Exception('Unknown coloring')
    else:
      pass # todo : implement this

  def compute_single(self, value):
    if self._interpretation == self.BINARY_INTERPRETATION:
      return self._colors[0] if bool(value) else 'default'

    elif self._interpretation == self.GROUP_INTERPRETATION:
      return self._colors[value]
      
    elif self._interpretation == self.IDENTITY_INTERPRETATION:
      return value

  def compute(self, transformed_state):
    if transformed_state is None:
      return None

    return dict([ (key, self.compute_single(value)) for key,value in transformed_state.items() ])    

  def __init__(self, transform, **kwargs):
    if 'color' in kwargs and 'colors' in kwargs:
      raise Exception('color_nodes_by: color and colors argument are mutually exclusive') # todo: use proper exception
    
    self._unique_values = set()
    self._transform = transform
    self._colors = None

    if 'color' in kwargs:
      self._colors = kwargs['color']

    if 'colors' in kwargs:
      self._colors = kwargs['colors']

    self._has_interpretation = self._colors is not None
    self._interpretation = None
