from app import App


def main():
  app = App()
  
  try:
    app.init()
    app.run()
  except Exception as e:
    app.die(e)


if __name__ == '__main__':
  main()
