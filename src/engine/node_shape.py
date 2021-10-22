"""
Helper module for shapes.
"""

from exceptions import NodeShapeException


NODE_SHAPES = {
  'circle': 'circle',
  'square': 'square',
  'hidden': 'hidden',
}


class NodeShape:
  """
  Used to represent the shape of a node.
  """

  @staticmethod
  def is_keyword(shape):
    """
    Return True if the specified shape is a known shape keyword (name)

    parameters:
      - shape (any): anything

    returns:
      - is_keyword (bool)
    """
    return isinstance(shape, str) and shape in NODE_SHAPES


  @staticmethod
  def is_shape(shape):
    """
    Returns True if the specified shape is in any recognized format or is
    None or is equal to string `default` (which is the same as None).

    parameters:
      - shape (any): anything

    returns:
      - is_shape (bool)
    """
    return (
      isinstance(shape, NodeShape) or
      shape is None or
      shape == 'default' or
      NodeShape.is_keyword(shape)
    )


  @staticmethod
  def are_shapes(iterable):
    """
    Returns True if all items in the iterable are shapes; False otherwise

    parameters:
      - iterable (iterable): any iterable collection of data

    returns:
      - are_shapes (bool)
    """
    return all(NodeShape.is_shape(shape) for shape in iterable)


  @staticmethod
  def from_keyword(shape):
    """
    Returns the normalized shape slug saved under the specified keyword

    parameters:
      - shape (str): shape name

    returns:
      - shape_slug (str): normalized shape slug
    """
    return NODE_SHAPES[shape]


  @staticmethod
  def normalize_shape(shape):
    """
    Normalizes the specified shape in any format. If the format cannot be
    determined or is not implemented a NodeShapeException is raised

    raises:
      - NodeShapeException when no format matched

    paramaters:
      - shape (any): shape in any recognized format

    returns:
      - shape_slug (str): normalized slug of the shape
    """
    if shape is None or shape == 'default':
      return None # None is a valid shape

    if isinstance(shape, NodeShape):
      # This does NOT create an object clone, but tuples are immutable, so it
      # does not really matter and saves a little bit of time
      return shape.shape

    if NodeShape.is_keyword(shape):
      return NodeShape.from_keyword(shape)

    raise NodeShapeException('Invalid shape: {}'.format(shape))


  def __init__(self, shape):
    """
    Creates a new instance of NodeShape.

    parameters:
      - shape (any): shape in any known format, will be normalized to rgba
    """
    self.shape = NodeShape.normalize_shape(shape)
