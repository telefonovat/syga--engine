from watchpoints import watch, unwatch
from io import StringIO
import inspect
import logging
from utils import path_from_root
from engine.graph import Graph
from .ticker import Ticker

class Engine:
  TICK_SOURCE_LINE = 0
  TICK_SOURCE_VARS = 1
  TICK_SOURCE_USER = 2
  
  def print(self, *args, **kwargs):
    print(*args, **kwargs, file=self.console_log)

  def line_callback(self, src):
    self.lineno = src.lineno - 1
    self.logger.debug('{}: {}'.format(self.lineno, src.fullsource.replace('\n', '')))
    self.tick(self.TICK_SOURCE_LINE)

  def tick(self, source:int=None):
    if len(self.components) == 0:
      return # Ignore tick with no components
    
    if source is None:
      source = self.TICK_SOURCE_USER

    console_logs = self.console_log.getvalue()
    components = [ (component, component.get_transformed_state()) for component in self.components ]

    self.ticker.tick(
      source=source,
      lineno=self.lineno,
      console_logs=console_logs,
      components=components
    )

    self.console_log.flush()
  
  def make_frames(self):
    for component in self.components:
      component.interpret_transformed_state()
    
    all_ticks = self.ticker.get_ticks()

    for tick in all_ticks:
      tick.data['components'] = [ component.compute_style(transformed_state) for component, transformed_state in tick.data['components'] ]
  
    return [ tick.data for tick in all_ticks ]

  def Graph(self, incoming_graph_data=None, **attr):
    if 'visualize' not in attr:
      attr['visualize'] = True

    graph = Graph(incoming_graph_data=None, **attr)

    if attr['visualize']:
      self.components.append(graph)

    return graph

  def __init__(self, unique_id:str):
    self.console_log = StringIO()
    self.components = []
    self.lineno = 1

    self.alg_locals = None

    self.logger = logging.getLogger(unique_id)
    self.logger.addHandler(logging.FileHandler(path_from_root('../logs/algs/{}.log'.format(unique_id))))
    self.logger.setLevel(logging.DEBUG)

    self.ticker = Ticker()
