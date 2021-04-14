import binascii
import os


def path_from_root(*args):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../' ,*args)


def random_name(n_bytes=16):
  return binascii.b2a_hex(os.urandom(n_bytes)).decode('utf-8').lower()
