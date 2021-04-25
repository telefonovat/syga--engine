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

    self.next_tick_id += 1
    self.ticks.append(tick)


  def get_ticks(self):
    """
    Returns all ticks
    """
    return self.ticks
  

  def __init__(self):
    """
    Creates a new instance of Ticker
    """
    self.next_tick_id = 0
    self.ticks = []


class Tick:
  """
  The tick class is just a wrapper for a dict, which stores the tick properties
  which implements the __eq__ method.
  """
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
      self.data['source'] == value.data['source'] and
      self.data['console_logs'] == value.data['console_logs'] and
      all([x[1] == y[1] for x, y in zip(self.data['components'], value.data['components'])])
    )
  

  def __init__(self, tick_id:int, source:int, lineno:int, console_logs:str, components):
    """
    Creates a new instance of Tick

    parameters:
      - tick_id (int): The unique ID of the tick
      - source (int): The code of the tick source (see Engine)
      - lineno (int): The number of the current line
      - console_logs (string): The text printed by the overloaded print method
      - components (list): A list of tuples (component, transformed state)
    """
    self.data = dict(
      tick_id=tick_id,
      source=source,
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )
