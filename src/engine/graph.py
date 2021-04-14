import networkx
from .visualizer import Visualizer


class GraphNodeColorizerTransformer:
  def transform(self, G):
    return dict([ (v, self._transform(v, G)) for v in G.nodes ])
  
  def __init__(self, transform):
    self._transform = transform


class GraphNodeColorizerInterpreter:
  def interpret(self, transformed_state):
    if isinstance(self.color, int):
      pass

    elif isinstance(self.color, list):
      pass

    elif isinstance(self.color, dict):
      pass
  
  def __init__(self, **kwargs):
    self.color = None
    
    if 'color' in kwargs:
      self.color = kwargs['color']


class GraphNodeColorizer:
  @staticmethod
  def build(*args, **kwargs):
    if 'color' in kwargs and 'colors' in kwargs:
      raise Exception('color_nodes_by: color and colors argument are mutually exclusive')
    
    if len(args) >= 2:
      raise Exception('color_nodes_by: too many positional arguments') # todo: use proper exception

    if len(args) == 1:
      if not callable(args[0]):
        return GraphNodeColorizer.build(lambda v: v in args[0], **kwargs)
      transformer = GraphNodeColorizerTransformer(args[0])
      return GraphNodeColorizer(transformer, None)

    else:
      if 'prop' not in kwargs:
        raise Exception('color_nodes_by: source not specified') # todo: use proper exception
      prop = kwargs['prop']
      return GraphNodeColorizer.build(lambda v,G: None if prop not in G.nodes[v] else G.nodes[v][prop], **kwargs)

  def transform(self, G):
    return self._transformer.transform(G)

  def __init__(self, transformer, interpreter):
    self._transformer = transformer


class Graph(networkx.Graph, Visualizer):
  def get_transformed_state(self):
    return {
      'nodes': list(self.nodes),
      'edges': list(self.edges),
      'transformed': {
        'node_colors': None if self.node_colorizer is None else self.node_colorizer.transform(self)
      }
    }

  def color_nodes_by(self, *args, **kwargs):
    self.node_colorizer = GraphNodeColorizer.build(*args, **kwargs)

  def color_edges_by(self, *args, **kwargs):
    pass

  def shape_nodes_by(self, *args, **kwargs):
    pass

  def shape_edges_by(self, *args, **kwargs):
    pass

  def scale_nodes_by(self, *args, **kwargs):
    pass

  def scale_edges_by(self, *args, **kwargs):
    pass

  def label_nodes_by(self, *args, **kwargs):
    pass

  def label_edges_by(self, *args, **kwargs):
    pass

  def __init__(self, incoming_graph_data=None, **attr):
    super().__init__(incoming_graph_data=incoming_graph_data, **attr)

    self.node_colorizer = None
