"""
The tick module
"""

from .frame import Frame


class Tick:
    """
    A tick is a snapshot of the current state of the visualized algorithm.
    Tick consists of:
      - tick id: A unique ID of the tick
      - source: Identifies the source of the tick
      - lineno: The number of the currently interpreted line during tick creation
      - console_logs: The current stdout output forwarded here
      - components: A list of tuple (component object, transformed state)

    Tick defines the __eq__ method for comparing two ticks. If two neighbouring
    ticks are equal, the latter will be ignored by the Ticker - there is no need
    to store identical ticks in a row.
    """

    def to_frame(self):
        """
        Turns this Tick into a Frame by computing the style of all components.

        returns:
          - frame (Frame): The frame created from this Tick
        """
        lineno = [self.lineno]
        console_logs = self.console_logs
        components = list(
            filter(None, [comp.compute_style(state) for comp, state in self.components])
        )

        return Frame(lineno=lineno, console_logs=console_logs, components=components)

    def __iter__(self):
        """
        Iterator function which allows to turn this object into dict using the
        default dict() function.
        """
        yield ("tick_id", self.tick_id)
        yield ("source", self.source)
        yield ("lineno", self.lineno)
        yield ("console_logs", self.console_logs)
        yield ("components", [state for _, state in self.components])

    def __eq__(self, value):
        """
        Used to compare two ticks. Two ticks are considered equal if the following
        properties are equal:
          - source
          - console_logs
          - transformed state of the components

        parameters:
          - value (Tick): another tick
        """
        if not isinstance(value, Tick):
            return False

        return self.source == value.source and all(
            [x[1] == y[1] for x, y in zip(self.components, value.components)]
        )

    def __init__(self, tick_id, source, lineno, console_logs, components):
        """
        Creates a new instance of Tick

        parameters:
          - tick_id (int): The unique ID of the tick
          - source (int): The code of the tick source (see Engine)
          - lineno (int): The number of the current line
          - console_logs (string): The text printed by the overloaded print method
          - components (list): A list of tuples (component, transformed state)
        """
        self.tick_id = tick_id
        self.source = source
        self.lineno = lineno
        self.console_logs = console_logs
        self.components = components
