"""
Helper module for shapes.
"""

from exceptions import EdgeShapeException


EDGE_SHAPES = {
    "solid": "solid",
    "dash": "dashed",
    "dashed": "dashed",
    "dot": "dotted",
    "dotted": "dotted",
    "comb": "combined",
    "combined": "combined",
    "no": "hidden",
    "hidden": "hidden",
}

# The edge shapes available when picking at random
AVAILABLE_EDGE_SHAPES = [
    "solid",
    "dashed",
    "dotted",
    "combined",
]


class EdgeShape:
    """
    Used to represent the shape of a edge.
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
        return isinstance(shape, str) and shape in EDGE_SHAPES

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
            isinstance(shape, EdgeShape)
            or shape is None
            or shape == "default"
            or EdgeShape.is_keyword(shape)
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
        return all(EdgeShape.is_shape(shape) for shape in iterable)

    @staticmethod
    def from_keyword(shape):
        """
        Returns the normalized shape slug saved under the specified keyword

        parameters:
          - shape (str): shape name

        returns:
          - shape_slug (str): normalized shape slug
        """
        return EDGE_SHAPES[shape]

    @staticmethod
    def normalize_shape(shape):
        """
        Normalizes the specified shape in any format. If the format cannot be
        determined or is not implemented a EdgeShapeException is raised

        raises:
          - EdgeShapeException when no format matched

        paramaters:
          - shape (any): shape in any recognized format

        returns:
          - shape_slug (str): normalized slug of the shape
        """
        if shape is None or shape == "default":
            return None  # None is a valid shape

        if isinstance(shape, EdgeShape):
            # This does NOT create an object clone, but tuples are immutable, so it
            # does not really matter and saves a little bit of time
            return shape.shape

        if EdgeShape.is_keyword(shape):
            return EdgeShape.from_keyword(shape)

        raise EdgeShapeException("Invalid edge shape: {}".format(shape))

    @staticmethod
    def create(shape):
        """
        Creates a new instance of EdgeShape and returns it.

        parameters:
          - shape (any): shape in any known format, will be normalized
        """
        return EdgeShape(shape)

    def __init__(self, shape):
        """
        Creates a new instance of EdgeShape.

        parameters:
          - shape (any): shape in any known format, will be normalized
        """
        self.shape = EdgeShape.normalize_shape(shape)
