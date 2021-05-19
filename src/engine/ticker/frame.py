"""
The frame module
"""

class Frame:
  """
  A frame stores all data used to draw one step of the visualized algorithm.
  A frame is created from tick by computing the style of the components. After
  that, neighbouring frames, which are equal, are merged into one.
  Frame consists of:
    - lineno: taken from the tick which became a frame
    - console_logs: The current stdout output forwarded here, possible merged
    - components: The style of the components - see Visualizer.compute_style
  """

  def __iter__(self):
    """
    Iterator function which allows to turn this object into dict using the
    default dict() function.
    """
    yield ('lineno', self.lineno)
    yield ('console_logs', self.console_logs)
    yield ('components', self.components)


  def __bool__(self):
    """
    Defines the conversion to bool for a frame.

    The conditions for deciding the thruthyness of a Frame are:
      1. if there are console logs, the frame is truthy - never remove frames
         with console logs
      2. if there are no components (ie. self.components is empty) and there
         are no console logs, the frame is falsy - such frames are useless
      3. If there are components, but no console logs, the frame is truthy only
         if at least one of it's components has truthy style - this means that
         component['style'] is not None and is not an empty dict

      The third rule might be removed later on, because it prevents people from
      using no style, but observing the changes in a structure of a visualizer.
      For example changes in nodes and edges of a graph will be ignored if at
      least one style property has not been specified for the graph.
    """
    if self.console_logs:
      return True # 1.

    if not self.components:
      return False # 2.

    return any(component['style'] for component in self.components) # 3.


  def __eq__(self, value):
    """
    Used to compare two frames. Frames are equal when the styles of the
    components are equal.

    Frame defines the __eq__ method to compare the neighbouring frames. If two
    neighbouring frames are identical, they will be merged.
    """
    if not isinstance(value, Frame):
      return False

    # todo: think more about the comparison.

    return self.components == value.components


  def merge_with(self, frame):
    """
    Merges this frame with the specified frame.

    parameters:
      - frame (Frame): The frame to merge with

    returns:
      - self (Frame): Reference to this frame
    """
    if frame.console_logs:
      self.lineno += frame.lineno
      self.console_logs = f'{frame.console_logs}{self.console_logs}'

    return self


  def __init__(self, lineno, console_logs, components):
    """
    Creates a new instance of Frame.

    parameters:
      - lineno (list): The current lines - may be more than one if merged
      - console_logs (string): The text printed by the overloaded print method
      - components (list): The list of component's styles. Result of the
        compute_style method. See Tick.to_frame method.
    """
    self.lineno = lineno
    self.console_logs = console_logs
    self.components = components
