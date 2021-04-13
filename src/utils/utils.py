import os


def path_from_root(*args):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..' ,*args)
