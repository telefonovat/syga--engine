"""
The DiGraph Visualizer module
"""

import networkx
from .base_graph import BaseGraph


class DiGraph(networkx.DiGraph, BaseGraph):
    """
    DiGraph Visualizer is simply a wrapper for the networkx.DiGraph class which
    implements all visualization methods. The more precise description can be
    found in the following document:
      - https://syga.kam.mff.cuni.cz/docs/graphs/graphs
    """

    def get_type(self):
        """
        Returns the graph type.
        """
        return "DiGraph"

    def __init__(self, incoming_graph_data=None, **attr):
        """
        Creates a new instance of DiGraph. A new instance MUST be creating by calling
        engine.DiGraph(), which calls this constructor and forwards the arguments
        """
        super().__init__(incoming_graph_data=incoming_graph_data, **attr)

        self._engine = attr["_engine"] if "_engine" in attr else None
        self._default_stylizers()
