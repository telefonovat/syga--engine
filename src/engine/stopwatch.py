"""
A simple stopwatch module
"""

import time


_STOPWATCHES = {}


class Stopwatch:
  """
  A simple stopwatch which supports
    - only single stopwatch
    - start and stop without reset
    - reset on demand
    - getting elapsed time without the need to stop
  """

  @staticmethod
  def get_stopwatch(name):
    """
    Returns the stopwatch saved under the specified name from the global
    stopwatch storage. If stopwatch with such name does not exist a new one is
    created.

    returns:
      - stopwatch (Stopwatch)
    """
    if name not in _STOPWATCHES:
      _STOPWATCHES[name] = Stopwatch()

    return _STOPWATCHES[name]


  def _diff(self):
    """
    Returns the difference in seconds between start and the current moment.
    If the stopwatch is not running 0 is returned.

    returns:
      - diff (float)
    """
    return time.perf_counter() - self._started if self._running else 0


  def start(self):
    """
    Starts the stopwatch.

    returns:
      - self (Stopwatch)
    """
    if not self._running:
      self._started = time.perf_counter()
      self._running = True

    return self


  def stop(self):
    """
    Stops the stopwatch.

    returns:
      - self (Stopwatch)
    """
    if self._running:
      self._elapsed += self._diff()
      self._running = False

    return self


  def reset(self):
    """
    Resets the stopwatch - sets the elapsed time to 0.

    returns:
      - self (Stopwatch)
    """
    self._elapsed = 0

    return self


  @property
  def elapsed(self):
    """
    Returns elapsed time in seconds. If the stopwatch is running, diff is
    computed and added to the storage elapsed time.

    returns:
      - elapsed (float): elapsed time in seconds
    """
    return self._elapsed + self._diff()


  @property
  def running(self):
    """
    Returns True if the stopwatch is running; False otherwise

    returns:
      - is_running (bool)
    """
    return self._running


  def __str__(self):
    """
    The string representation of the stopwatch
    """
    return f'<Stopwatch running={self.running} elapsed={self.elapsed}>'


  def __repr__(self):
    """
    The string representation of the stopwatch
    """
    return str(self)


  def __init__(self):
    """
    Creates a new instance of Stopwatch
    """
    self._elapsed = 0
    self._running = False
    self._started = None
