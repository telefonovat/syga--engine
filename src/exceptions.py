"""
All exceptions used by this app MUST be defined here
"""

class AppException(Exception):
  """
  The root which should be used as a base for all other exceptions used
  by this app. Every other exception should inherit from this one.
  """


class LoaderException(AppException):
  """
  A general loader exception. Whenever something goes wrong with the loader
  component, this exception should be raised.
  """


class RunnerException(AppException):
  """
  A general runner exception. Whenever something goes wrong with the runner
  component, this exception should be raised.
  """


class AlgorithmException(AppException):
  """
  A general algorithm exception. Whenever something goes wrong with the user
  provided algorithm, this exception should be raised.
  """


class ColorException(AlgorithmException):
  """
  An exception which should be raised when there is a color problem
  """


class NodeShapeException(AlgorithmException):
  """
  An exception which should be raised when there is a node shape problem
  """


class EdgeShapeException(AlgorithmException):
  """
  An exception which should be raised when there is an edge shape problem
  """


class GraphColorizerException(AlgorithmException):
  """
  The base for the following exceptions:
    - GraphNodeColorizerException
    - GraphEdgeColorizerException
  """


class GraphNodeColorizerException(GraphColorizerException):
  """
  An exception which should be raised when there is a problem with a graph
  node colorizer - eg. invalid parameters, problem with interpretation ...
  """


class GraphEdgeColorizerException(GraphColorizerException):
  """
  An exception which should be raised when there is a problem with a graph
  edge colorizer - eg. invalid parameters, problem with interpretation ...
  """


class GraphShaperException(AlgorithmException):
  """
  The base for the following exceptions:
    - GraphNodeShaperException
    - GraphEdgeShaperException
  """


class GraphNodeShaperException(GraphShaperException):
  """
  An exception which should be raised when there is a problem with a graph
  node shaper - eg. invalid parameters, problem with interpretation ...
  """


class GraphEdgeShaperException(GraphShaperException):
  """
  An exception which should be raised when there is a problem with a graph
  edge shaper - eg. invalid parameters, problem with interpretation ...
  """


class GraphLabelerException(AlgorithmException):
  """
  The base for the following exceptions:
    - GraphNodeLabelerException
    - GraphEdgeLabelerException
  """


class GraphNodeLabelerException(GraphLabelerException):
  """
  An exception which should be raised when there is a problem with a graph
  node labeler - eg. invalid parameters, problem with interpretation ...
  """


class GraphEdgeLabelerException(GraphLabelerException):
  """
  An exception which should be raised when there is a problem with a graph
  edge labeler - eg. invalid parameters, problem with interpretation ...
  """
