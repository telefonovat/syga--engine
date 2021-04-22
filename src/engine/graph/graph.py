import networkx
from engine.visualizer import Visualizer
from components.logger import logger
from .node_colorizer import GraphNodeColorizer


class Graph(networkx.Graph, Visualizer):
  def get_transformed_state(self):
    return {
      'nodes': list(self.nodes),
      'edges': list(self.edges),
      'transformed': {
        'node_colors': None if self.node_colorizer is None else self.node_colorizer.transform(self)
      }
    }

  def interpret_transformed_state(self):
    if self.node_colorizer is not None: self.node_colorizer.interpret()

  def compute_style(self, transformed_state):
    return {
      'nodes': transformed_state['nodes'],
      'edges': transformed_state['edges'],
      'style': {
        'node_colors': None if self.node_colorizer is None else self.node_colorizer.compute(transformed_state['transformed']['node_colors'])
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
