"""
The ticker module
"""

class Ticker:
  """
  Used to store the ticks an keep track of their IDs
  """

  def tick(self, source, lineno, console_logs, components):
    """
    Creates and saves a new tick

    parameters:
      - source (int): The code of the tick source (see Engine)
      - lineno (int): The number of the current line
      - console_logs (string): The text printed by the overloaded print method
      - components (list): A list of tuples (component, transformed state)
    """
    tick = Tick(
      tick_id=self.next_tick_id,
      source=source,
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )

    if len(self.ticks) > 0 and self.ticks[-1] == tick:
      return # Same data - skip this tick

    if all(component[1] is None for component in components):
      return # All transformed states are None - this tick is useless

    self.next_tick_id += 1
    self.ticks.append(tick)


  def to_frames(self):
    """
    Turns the ticks into frames and returns them. The megring algorithm is
    executed here.

    returns:
      - frames (list<Frame>): The frames
    """
    # Create frames from the ticks and take only the truthy ones. See
    # Frame.__bool__ for more information about the definition of truthyness.
    frames = filter(None, [tick.to_frame() for tick in self.ticks])

    # Merge the frames
    merged_frames = []
    curr = None

    try:
      iterator = iter(frames)
      curr = next(iterator)

      while True:
        frame = next(iterator)
        if curr == frame:
          curr.merge_with(frame)
        else:
          merged_frames.append(curr)
          curr = frame

    except StopIteration:
      if curr is not None:
        merged_frames.append(curr)

    return merged_frames


  def __init__(self):
    """
    Creates a new instance of Ticker
    """
    self.next_tick_id = 0
    self.ticks = []


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
    Defines the conversion to bool for a frame. A frame is truthy if at least
    one component has a truthy style - this happends when the style dict has at
    least one property specified.
    """
    if not self.components:
      return False

    return any(component['style'] for component in self.components) or bool(self.console_logs)


  def __eq__(self, value):
    """
    Used to compare two frames. Frames are equal when the styles of the
    components are equal.

    Frame defines the __eq__ method to compare the neighbouring frames. If two
    neighbouring frames are identical, they will be merged
    """
    if not isinstance(value, Frame):
      return False

    # todo: think more about the comparison.

    return self.components == value.components


  def merge_with(self, frame):
    """
    Merges this frame with the specified frame

    parameters:
      - frame (Frame): The frame to merge with

    returns:
      - self (Frame): Reference to this frame
    """
    # self.lineno = frame.lineno
    self.console_logs = f'{self.console_logs}{frame.console_logs}'
    return self


  def __init__(self, lineno, console_logs, components):
    """
    Creates a new instance of Frame.

    parameters:
      - lineno (int): The current line
      - console_logs (string): The text printed by the overloaded print method
      - components (list): The list of component's styles. Result of the
        compute_style method. See Tick.to_frame method.
    """
    self.lineno = lineno
    self.console_logs = console_logs
    self.components = components


class Tick:
  """
  A tick is a snapshot of the current state of the visualized algorithm.
  Tick consists of:
    - tick id: A unique ID of the tick
    - source: Identifies the source of the tick
    - lineno: The number of the currently interpreted line during tick creation
    - console_logs: The current stdout output forwarded here
    - components: A list of tuple (component object, transformed state)

  Tick defines the __eq__ method for comparing two ticks. If two neighbouring
  ticks are equal, the latter will be ignored by the Ticker - there is no need
  to store identical ticks in a row.
  """

  def to_frame(self):
    """
    Turns this Tick into a Frame by computing the style of all components

    returns:
      - frame (Frame): The frame created from this Tick
    """
    lineno = self.lineno
    console_logs = self.console_logs
    components = list(filter(None, [comp.compute_style(state) for comp, state in self.components]))

    return Frame(
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )


  def __iter__(self):
    """
    Iterator function which allows to turn this object into dict using the
    default dict() function.
    """
    yield ('tick_id', self.tick_id)
    yield ('source', self.source)
    yield ('lineno', self.lineno)
    yield ('console_logs', self.console_logs)
    yield ('components', [state for _, state in self.components])


  def __eq__(self, value):
    """
    Used to compare two ticks. Two ticks are considered equal if the following
    properties are equal:
      - source
      - console_logs
      - transformed state of the components

    parameters:
      - value (Tick): another tick
    """
    if not isinstance(value, Tick):
      return False

    return (
      self.source == value.source and
      self.console_logs == value.console_logs == '' and
      all([x[1] == y[1] for x, y in zip(self.components, value.components)])
    )


  def __init__(self, tick_id, source, lineno, console_logs, components):
    """
    Creates a new instance of Tick

    parameters:
      - tick_id (int): The unique ID of the tick
      - source (int): The code of the tick source (see Engine)
      - lineno (int): The number of the current line
      - console_logs (string): The text printed by the overloaded print method
      - components (list): A list of tuples (component, transformed state)
    """
    self.tick_id = tick_id
    self.source = source
    self.lineno = lineno
    self.console_logs = console_logs
    self.components = components
