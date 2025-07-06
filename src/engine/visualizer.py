"""
The Visualizer class
"""


class Visualizer:
    """
    Visualizer is a data structure which can be visualized. This class is used
    as an abstract base for all visualizers. Is simply defines the interface
    which must be implemented by every visualizer.
    """

    def get_transformed_state(self):
        """
        Returns the transformed state of the visualizer
        """
        raise NotImplementedError()

    def interpret_transformed_state(self):
        """
        Interprets the transformed state. This method is called AFTER the execution
        of the visualized algorithm has ended
        """
        raise NotImplementedError()

    def compute_style(self, state):
        """
        Computes the style from the transformed state
        """
        raise NotImplementedError()
