class Visualizer:
  def get_transformed_state(self):
    raise NotImplementedError()

  def interpret_transformed_state(self):
    raise NotImplementedError()

  def compute_style(self, transformed_state):
    raise NotImplementedError()
