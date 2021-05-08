"""
Helper module for colors

todo:
  - consider rounding error
"""

import re
from colour import COLOR_NAME_TO_RGB
from webcolors import CSS3_NAMES_TO_HEX
from exceptions import ColorException


# Normalized rgba format is tuple of floats - float error must be considered
FLOAT_ERROR = 0.000005


# Matches color in hex format
HEX_REGEX_STR = r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$'

# Matches a part of an rgb(a) color if in integer format
RGBA_INT_REGEX_STR = r'(?:0*(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2}))'

# Matches a part of an rgb(a) color if in float format
RGBA_FLOAT_REGEX_STR = r'(?:0*(?:0+|1|1\.0*|0?\.[0-9]*))'

# Matches a part of an rgb(a) color if in percent format
RGBA_PERCENT_REGEX_STR = r'(?:0*(?:100(?:\.0*)?|[0-9]{1,2}(?:\.[0-9]*)?)%)'

# Matches the comma separator of an rgb(a) color
COMMA_SEPARATOR_REGEX_STR = r'(?:\s*,\s*)'

# Matches a whole rgb(a) color
RGBA_REGEX_STR = (
  r'rgba?\(\s*(?:(?:{i}{s}{i}{s}{i})|(?:{p}{s}{p}{s}{p}))(?:{s}(?:{f}|{p}))?\s*\)'.format(
    i=RGBA_INT_REGEX_STR,
    s=COMMA_SEPARATOR_REGEX_STR,
    p=RGBA_PERCENT_REGEX_STR,
    f=RGBA_FLOAT_REGEX_STR
  )
)


# The actual regexes
HEX_REGEX = re.compile(HEX_REGEX_STR)
RGBA_REGEX = re.compile(RGBA_REGEX_STR)


# Map from color name to normalized rgba tuple
# Initialized at the end of the script after Color class definition
COLOR_NAME_TO_RGBA = {}


class Color:
  """
  Used to represent a RGBA color
  """

  @staticmethod
  def is_keyword(color):
    """
    Return True if the specified color is a known color keyword (name)

    parameters:
      - color (any): anything

    returns:
      - is_keyword (bool)
    """
    return isinstance(color, str) and color in COLOR_NAME_TO_RGBA


  @staticmethod
  def is_hex(color):
    """
    Returns True if the specified color is in hex format

    parameters:
      - color (any): anything

    returns:
      - is_hex (bool)
    """
    return isinstance(color, str) and bool(HEX_REGEX.match(color.strip()))


  @staticmethod
  def is_rgba(color):
    """
    Returns True if the specified color is in rgba format

    parameters:
      - color (any): anything

    returns:
      - is_rgba (bool)
    """
    if isinstance(color, str):
      return bool(RGBA_REGEX.match(color.strip()))

    if isinstance(color, (list, tuple)):
      if len(color) not in (3, 4):
        return False

      if not all(isinstance(part, (int, float)) for part in color):
        return False

      if len(color) == 4 and (color[3] < -FLOAT_ERROR or color[3] > 1 + FLOAT_ERROR):
        return False

      rgb = color[:3]

      if any(isinstance(c, float) for c in rgb):
        return all(-FLOAT_ERROR <= c <= 1 + FLOAT_ERROR for c in rgb)

      if all(isinstance(c, int) for c in rgb):
        return all(0 <= c <= 255 for c in rgb)

    return False


  @staticmethod
  def is_color(color):
    """
    Returns True if the specified color is in any recognized format or is
    None or is equal to string `default` (which is the same as None).

    parameters:
      - color (any): anything

    returns:
      - is_color (bool)
    """
    return (
      isinstance(color, Color) or
      color is None or
      color == 'default' or
      Color.is_keyword(color) or
      Color.is_hex(color) or
      Color.is_rgba(color)
    )


  @staticmethod
  def are_colors(iterable):
    """
    Returns True if all items in the iterable are colors; False otherwise

    parameters:
      - iterable (iterable): any iterable collection of data

    returns:
      - are_colors (bool)
    """
    return all(Color.is_color(color) for color in iterable)


  @staticmethod
  def from_keyword(color):
    """
    Returns the normalized rgba tuple saved under the specified keyword

    parameters:
      - color (str): color name

    returns:
      - rgba (tuple): normalized rgba tuple (r, g, b, a)
    """
    return COLOR_NAME_TO_RGBA[color]


  @staticmethod
  def normalize_hex(color):
    """
    Converts color from hex format to normalized rgba format. This method
    assumes the color is in fact in HEX format - no checks are done. In case
    of invalid input any exception might be raised.

    parameters:
      - color (str): color in HEX format

    returns:
      - rgba (tuple): normalized rgba tuple (r, g, b, a)
    """
    col = color.strip()[1:]

    if len(col) == 3:
      col += 'f'

    if len(col) == 6:
      col += 'ff'

    if len(col) == 4:
      rgba = [ch * 2 for ch in col]

    if len(col) == 8:
      rgba = [col[0:2], col[2:4], col[4:6], col[6:8]]

    return tuple(int(v, 16) / 255 for v in rgba)


  @staticmethod
  def normalize_rgba(color):
    """
    Normalizes the specified color in rgba format. The color can either be a
    string or a list or a tuple. This method assumes the color is in fact in
    rgb(a) format - no checks are done. In case of invalid input any exception
    might be raised.

    parameters:
      - color (str|tuple): color in rgb(a) format

    returns:
      - rgba (tuple): normalized rgba tuple (r, g, b, a)
    """
    parse_int = lambda i: int(i) / 255
    parse_perc = lambda p: float(p.replace('%', '')) / 100

    if isinstance(color, str):
      parts = [p.strip() for p in color.strip()[(4 + int('rgba' in color)):-1].split(',')]
      rgba = parts[:3]

      if all('%' in c for c in rgba):
        rgba = [parse_perc(c) for c in rgba]
      else:
        rgba = [parse_int(c) for c in rgba]

      if len(parts) == 4:
        rgba.append(parse_perc(parts[3]) if '%' in parts[3] else float(parts[3]))

    if isinstance(color, (list, tuple)):
      perc = any(isinstance(c, float) for c in color)
      rgba = [c if perc else c / 255 for c in color]

    if len(rgba) == 3:
      rgba.append(1)

    return tuple(rgba)


  @staticmethod
  def normalize_color(color):
    """
    Normalizes the specified color in any format. If the format cannot be
    determined or is not implemented (for example CMYK) an ColorException is
    raised

    raises:
      - ColorException when no format matched

    paramaters:
      - color (any): color in any recognized format

    returns:
      - rgba (tuple): normalized rgba tuple (r, g, b, a)
    """
    if color is None or color == 'default':
      return None # None is a valid color

    if isinstance(color, Color):
      # This does NOT create an object clone, but tuples are immutable, so it
      # does not really matter and saves a little bit of time
      return color.rgba

    if Color.is_keyword(color):
      return Color.from_keyword(color)

    if Color.is_hex(color):
      return Color.normalize_hex(color)

    if Color.is_rgba(color):
      return Color.normalize_rgba(color)

    raise ColorException('Invalid color: {}'.format(color))


  def __eq__(self, color):
    """
    Defines equality of two colors
    """
    if not Color.is_color(color):
      return False

    color = Color(color)

    if self.rgba is None or color.rgba is None:
      return self.rgba is None and color.rgba is None

    return all(abs(x - y) <= FLOAT_ERROR for x, y in zip(self.rgba, color.rgba))


  def __hash__(self):
    """
    Defines the hash function - hash the normalized rgba tuple
    """
    return hash(self.rgba)


  def __str__(self):
    """
    Defines conversion to string
    """
    r, g, b, a = self.rgba
    return f'<Color r={r} g={g} b={b} a={a}>'


  def __repr__(self):
    """
    Defines the string representation
    """
    return str(self)


  def __init__(self, color):
    """
    Creates a new instance of Color.

    parameters:
      - color (any): color in any known format, will be normalized to rgba
    """
    self.rgba = Color.normalize_color(color)


for _key, _rgb in COLOR_NAME_TO_RGB.items():
  _r, _g, _b = _rgb
  COLOR_NAME_TO_RGBA[_key] = (_r / 255, _g / 255, _b / 255, 1)

for _key, _hex in CSS3_NAMES_TO_HEX.items():
  if _key not in COLOR_NAME_TO_RGBA:
    COLOR_NAME_TO_RGBA[_key] = Color.normalize_hex(_hex)

COLOR_NAMES = list(COLOR_NAME_TO_RGBA.keys())
