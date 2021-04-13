import networkx


class Graph(networkx.Graph):
  def __init__(self, incoming_graph_data=None, **attr):
    super().__init__(incoming_graph_data=incoming_graph_data, **attr)

  def color_nodes_by(self, *args, **kwargs):
    pass

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
