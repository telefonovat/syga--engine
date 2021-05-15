"""
The Graph Visualizer module
"""

import networkx
from engine.visualizer import Visualizer
from .node_colorizer import GraphNodeColorizer


class Graph(networkx.Graph, Visualizer):
  """
  Graph Visualizer is simply a wrapper for the networkx.Graph class which
  implements all visualization methods. The more precise description can be
  found in the following document:
    - https://gitlab.mff.cuni.cz/wikarskm/mw-nprg045-docs/-/blob/master/graphs/graphs.md

  The style properties are as follows:
    - node color
    - node shape
    - node scale
    - node label
    - edge color
    - edge shape
    - edge scale
    - edge label

  The stylization of every property can be specified by a designated method.
  This method simply passes all arguments to the builder of the designated
  Stylizer
  """

  def _engine_tick(self):
    """
    If a reference to the engine is stored in this graph component, a tick is
    created. The type of the tick is TICK_SOURCE_STYLIZER
    """
    if self._engine is not None:
      self._engine.tick(self._engine.TICK_SOURCE_STYLIZER)


  def get_transformed_state(self):
    """
    Returns the transformed state of the Graph which is composed of
      - list of nodes
      - list of edges
      - dict (element to transformed information) for every style property

    If the graph is empty, None is returned. If all components in a tick are
    None, the tick can be skipped - it is useless.

    Only the properties which have stylizers specified are included in the
    transformed dict.

    This method MUST be called every time a tick is being generated.

    returns:
      - transformed_information (dict): The information used for stylization
    """
    if not self.nodes and not self.nodes:
      return None

    transformed = {}

    for name, stylizer in self._stylizers.items():
      if stylizer is not None:
        transformed[name] = stylizer.transform(self)

    return {
      'nodes': list(self.nodes),
      'edges': list(self.edges),
      'transformed': transformed
    }


  def interpret_transformed_state(self):
    """
    Calls the interpret method for every Stylizer. This method MUST be called
    after all ticks were generated.
    """
    for stylizer in self._stylizers.values():
      if stylizer is not None:
        stylizer.interpret()


  def compute_style(self, state):
    """
    Computes the style of the graph elements using the transformed information.
    The only parameter of this method is the dict returned by the method
    `get_transformed_state`. The engine is responsible for keeping the
    transformed information and calling this method with it as the argument.

    The transformed state for a property might not be present in the state
    dict. This happends when ticks are generated BEFORE a stylizer has been
    specified by the user. In such case the style of the property will NOT be
    included in the style dict.

    The style dict can also be empty if no stylizers were specified when
    computing the transformed state. In such case the style dict is empty. If
    all style dicts in a frame are empty - the frame will be ignored.

    parameters:
      - state (dict): The dict returned by the `get_transformed_state` method

    returns:
      - style (dict): The final information used to draw the graph
    """
    if state is None:
      return None

    style = {}

    for name, stylizer in self._stylizers.items():
      if stylizer is not None and name in state['transformed']:
        style[name] = stylizer.compute(state['transformed'][name])

    return {
      'nodes': state['nodes'],
      'edges': state['edges'],
      'style': style
    }


  def color_nodes_by(self, *args, **kwargs):
    """
    Creates an instance of GraphNodeColorizer used by this graph
    """
    self._stylizers['node_colors'] = GraphNodeColorizer.build(*args, **kwargs)

    self._engine_tick()


  def shape_nodes_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def scale_nodes_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def label_nodes_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def color_edges_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def shape_edges_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def scale_edges_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def label_edges_by(self, *args, **kwargs):
    """
    todo: implement this
    """


  def __init__(self, incoming_graph_data=None, **attr):
    """
    Creates a new instance of Graph. A new instance MUST be creating by calling
    engine.Graph(), which calls this constructor and forwards the arguments
    """
    super().__init__(incoming_graph_data=incoming_graph_data, **attr)

    self._engine = attr['_engine'] if '_engine' in attr else None

    self._stylizers = {
      'node_colors': None,
      'node_shapes': None,
      'node_scales': None,
      'node_labels': None,

      'edge_colors': None,
      'edge_shapes': None,
      'edge_scales': None,
      'edge_labels': None
    }
