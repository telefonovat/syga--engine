"""
The ticker module
"""

from .tick import Tick


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
    has_console_logs = bool(console_logs)

    if not has_console_logs and all(component[1] is None for component in components):
      return # All transformed states are None - this tick is useless

    tick = Tick(
      tick_id=self.next_tick_id,
      source=source,
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )

    if not has_console_logs and len(self.ticks) > 0 and self.ticks[-1] == tick:
      return # Same data - skip this tick

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

    # Phase 1 - assume the first frame is important. Use this frame for
    # comparison. Keep iterating until a frame differs or has some console
    # logs. When this happens, store this frame for comparison and continue
    # the process until the end of the iterator.
    merged_frames = []

    try:
      iterator = iter(frames)
      curr = next(iterator)

      merged_frames.append(curr)

      while True:
        frame = next(iterator)
        if curr != frame or bool(frame.console_logs):
          merged_frames.append(frame)
        curr = frame

    except StopIteration:
      pass # This is ok

    except Exception as e:
      raise e # Anything else is not okay

    # Phase 2
    if len(merged_frames) >= 2:
      for left, right in zip(range(len(merged_frames) - 1), range(1, len(merged_frames))):
        l_frame = merged_frames[left]
        r_frame = merged_frames[right]

        if l_frame == r_frame and bool(l_frame.console_logs) and bool(r_frame.console_logs):
          r_frame.merge_with(l_frame)
          merged_frames[left] = None

      merged_frames = list(filter(lambda frame: frame is not None, merged_frames))

    return merged_frames


  def set_logger(self, logger):
    """
    Sets the debug logger used by the ticker. This allows ticker to make debug
    logs when the program runs in debug mode.

    parameters:
      - logger (Logger): The logger used by the engine
    """
    self._logger = logger


  def __init__(self):
    """
    Creates a new instance of Ticker
    """
    self._logger = None

    self.next_tick_id = 0
    self.ticks = []
