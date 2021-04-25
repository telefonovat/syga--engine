"""
The entrypoint
"""

from app import App


def main():
  """
  The main function
  """
  app = App()

  try:
    app.init()
    app.run()
  except Exception as err: # pylint: disable=broad-except
    app.die(err)


if __name__ == '__main__':
  main()
