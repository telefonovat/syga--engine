class Ticker:
  def tick(self, source, lineno, console_logs, components):
    tick = Tick(
      tick_id=self.next_tick_id,
      source=source,
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )

    if len(self.ticks) > 0 and self.ticks[-1] == tick:
      return # Same data - skip this tick

    self.next_tick_id += 1
    self.ticks.append(tick)

  def get_ticks(self):
    return self.ticks
  
  def __init__(self):
    self.next_tick_id = 0
    self.ticks = []


class Tick:
  def __eq__(self, value):
    if not isinstance(value, Tick):
      return False

    return (
      self.data['source'] == value.data['source'] and
      self.data['console_logs'] == value.data['console_logs'] and
      self.data['components'] == value.data['components'] 
    )
  
  def __init__(self, tick_id, source, lineno, console_logs, components):
    self.data = dict(
      tick_id=tick_id,
      source=source,
      lineno=lineno,
      console_logs=console_logs,
      components=components
    )
