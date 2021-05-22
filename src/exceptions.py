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


class GraphNodeColorizerException(AlgorithmException):
  """
  An exception which should be raised when there is a problem with a graph
  node colorizer - eg. invalid parameters, problem with interpretation ...
  """


class GraphEdgeColorizerException(AlgorithmException):
  """
  An exception which should be raised when there is a problem with a graph
  edge colorizer - eg. invalid parameters, problem with interpretation ...
  """
