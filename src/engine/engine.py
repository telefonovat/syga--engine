"""
The engine module
"""

from io import StringIO
import logging
from utils.path import path_from_root
from engine.graph import Graph
from .ticker import Ticker
from .stopwatch import Stopwatch
from .color import Color


class Engine:
  """
  Engine is the main component which is responsible for
    - Initiation of visualizers
    - Tick sampling
    - Computation of frames

  A new instance of engine is created every time an algorithm is visualized.

  Engine defines a factory method for every visualizer which instantiates the
  visualizer and stores a reference to it in a property. The transformed state
  of every visualizer is then generated and saved for every tick.

  The transformed state of every visualizer is then passed as an argument for
  style computation method of the visualizer. After the style is computed,
  ticks can be merged into frames
  """

  TICK_SOURCE_LINE = 0
  TICK_SOURCE_VARS = 1
  TICK_SOURCE_USER = 2
  TICK_SOURCE_STYLIZER = 3


  Color = Color


  def print(self, *args, **kwargs):
    """
    Overloaded print method which is passed as an argument to the wrapper
    function of the visualized algorithm. Instead of printing to stdout,
    the printed contents are saved to a property of type StringIO.

    The printed text is then saved as a data member of a Tick.
    """
    self._logger.debug('{}:  --- print({}, {})'.format(self._lineno, list(args), dict(kwargs)))
    kwargs['file'] = self._console_log
    print(*args, **kwargs)


  def line_callback(self, src):
    """
    This method is called for every 'line' event of the Hunter library. The
    initiation of code tracking is a responsibility of the runner component.

    Engine will save the number of the current line and call the tick method

    parameters:
      - src (object): the source line
    """
    if not self._can_tick:
      return # Skip line callback if ticks are not enabled ATM

    self._lineno = src.lineno

    if self._logger is not None:
      self._logger.debug('{}: {}'.format(self._lineno, src.fullsource.replace('\n', '')))

    self.tick(self.TICK_SOURCE_LINE)


  def tick(self, source=None):
    """
    The tick method computes the transformed state for every visualizer
    (component), creates a new tick and saves it using the Ticker

    parameters:
      - source (int): The source of the tick. Valid values are defined as
        constans with prefix TICK_SOURCE_
    """
    if not self._can_tick:
      return # Stop if ticks are not enabled ATM

    if not self._components:
      return # Ignore tick with no components

    try:
      self._can_tick = False

      if source is None:
        source = self.TICK_SOURCE_USER

      console_logs = self._console_log.getvalue()
      components = [ (comp, comp.get_transformed_state()) for comp in self._components ]

      self._ticker.tick(
        source=source,
        lineno=self._lineno,
        console_logs=console_logs,
        components=components
      )

      self._console_log = StringIO() # Empty the contents

    finally:
      self._can_tick = True


  def make_frames(self):
    """
    This method is called by the runner component after execution of the
    visualized algorithm has ended. The first step in making frames is the
    interpretation of all visualizers (component).

    After that, style is computed for every frame and for every visualizer
    (component). Neighboring frames with the same style of the components
    are then merged into one. More detailed description of the merging
    algorithm can be found here:
      - https://gitlab.mff.cuni.cz/wikarskm/mw-nprg045-docs/-/blob/master/engine/engine.md#zlievanie

    returns:
      - frames (list): the frames used for visualization
    """
    for component in self._components:
      component.interpret_transformed_state()

    return self._ticker.to_frames()


  def Graph(self, incoming_graph_data=None, **attr): # pylint: disable=invalid-name
    """
    Creates a new instance of Graph visualizer
    """
    if 'visualize' not in attr:
      attr['visualize'] = True

    graph = Graph(incoming_graph_data=incoming_graph_data, _engine=self, **attr)

    if attr['visualize']:
      self._components.append(graph)

    return graph


  def init_logger(self, uid):
    """
    Initiates the engine's logger. A unique ID must be provided. This ID
    will be used to create a unique log file for debugging purposes

    parameters:
      - uid (str): The unique ID of this engine
    """
    self._logger = logging.getLogger(uid)
    self._logger.addHandler(logging.FileHandler(path_from_root('../logs/algs/{}.log'.format(uid))))
    self._logger.setLevel(logging.DEBUG)


  def __init__(self):
    """
    Creates a new instance of Engine.
    """
    self._can_tick = True
    self._console_log = StringIO()
    self._components = []
    self._lineno = 1

    self._logger = None
    self._ticker = Ticker()

    self.stopwatch = Stopwatch()
