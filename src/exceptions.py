"""
All exceptions used by this app MUST be defined here
"""

class AppException(Exception):
  """
  The root which should be used as a base for all other exceptions used
  by this app. Every other exception should inherit from this one.
  """
  pass


class LoaderException(AppException):
  """
  A general loader exception. Whenever something goes wrong with the loader
  component, this exception should be raised.
  """
  pass


class RunnerException(AppException):
  """
  A general runner exception. Whenever something goes wrong with the runner
  component, this exception should be raised.
  """
  pass


class AlgorithmException(AppException):
  """
  A general algorithm exception. Whenever something goes wrong with the user
  provided algorithm, this exception should be raised.
  """
  pass
