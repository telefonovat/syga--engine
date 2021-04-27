"""
Utils for code analysis and transformation
"""

def detect_indentation(code):
  """
  A trivial function for detecting indentation of the specified code.

  raises:
   - IndentationError: if the indentation is inconsistent

  parameters:
   - code (str): The code

  returns:
   - indentation (int): The size of the indentation used
  """
  indentations = [ len(line) - len(line.lstrip()) for line in code.splitlines() ]
  min_indentation = min(indentations)

  indentations = [ x - min_indentation for x in indentations if x > min_indentation ]

  if len(indentations) == 0:
    return min_indentation

  min_indentation = min(indentations)

  for indentation in indentations:
    if indentation % min_indentation != 0:
      raise IndentationError()

  return min_indentation


def add_indentation(code, indentation):
  """
  Adds the specified amount of indentation to the beginning of each line.
  The indentation MUST be done using space (not tabulator). It is not the
  responsibility of this function to detect whether tabulation was used.

  parameters:
   - code (str): The code
   - indentation (int): The number of spaces

  returns:
   - transformed_code (str): The code after adding indentations
  """
  prefix = ' ' * indentation
  return '\n'.join([ prefix + line for line in code.splitlines() ])


def get_sample_code(indentation):
  """
  Returns a sample code for testing.

  parameters:
    - indentation (int): The size of the indentation

  returns:
    - code (string): Sample code with the specified indentation size
  """
  lines = [
    'print("lorem")',
    'print("ipsum")',
    'for i in range(10):',
    '{}x = i ** 2',
    '{}for j in range(x):',
    '{}{}print(j)',
    'print("all done")'
  ]

  lines = [ line.replace('{}', ' ' * indentation) for line in lines ]

  return '\n'.join(lines)
