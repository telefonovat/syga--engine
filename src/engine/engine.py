from watchpoints import watch, unwatch
from io import StringIO
import inspect
import logging
from utils import path_from_root
from engine.graph import Graph


class Engine:
  def print(self, *args, **kwargs):
    print('[{}] '.format(self.line), file=self.console_log, end='')
    print(*args, **kwargs, file=self.console_log)
  
  # def init(self, alg_locals):
  #   watch(alg_locals, deepcopy=False, callback=self.watch_locals)

  # def watch_locals(self, frame, elem, exec_info):
  #   for key in frame.f_locals:
  #     if not inspect.isclass(frame.f_locals[key]) and not inspect.ismodule(frame.f_locals[key]) and not inspect.ismethod(frame.f_locals[key]):
  #       unwatch(frame.f_locals[key])
  #       watch(frame.f_locals[key], deepcopy=True, callback=self.local_change)
  #   self.local_change(frame, elem, exec_info)
  
  # def local_change(self, frame, elem, exec_info):
  #   self.logger.debug(exec_info)
  #   self.line = exec_info[0]
  #   self.tick(Engine.TICK_SOURCE_VARS)

  def line_callback(self, src):
    self.line = src.lineno - 1
    self.logger.debug('{}: {}'.format(self.line, src.fullsource.replace('\n', '')))
    self.tick(Engine.TICK_SOURCE_LINE)

  def tick(self, source=None):
    if len(self.components) == 0:
      return # Ignore tick with no components
    
    if source is None:
      source = Engine.TICK_SOURCE_USER
  
  def make_frames(self):
    return []

  def Graph(self, incoming_graph_data=None, **attr):
    if 'visualize' not in attr:
      attr['visualize'] = True

    graph = Graph(incoming_graph_data=None, **attr)

    if attr['visualize']:
      self.components.append(graph)

    return graph

  # def __del__(self):
    # if hasattr(self, 'alg_locals') and self.alg_locals is not None:
    #   unwatch(self.alg_locals)
    # pass

  def __init__(self, unique_id:str):
    self.console_log = StringIO()
    self.ticks = []
    self.components = []
    self.line = 1

    self.alg_locals = None

    self.logger = logging.getLogger(unique_id)
    self.logger.addHandler(logging.FileHandler(path_from_root('../logs/algs/{}.log'.format(unique_id))))
    self.logger.setLevel(logging.DEBUG)


Engine.TICK_SOURCE_LINE = 0
Engine.TICK_SOURCE_VARS = 1
Engine.TICK_SOURCE_USER = 2
