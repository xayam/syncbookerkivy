import os

os.environ["KIVY_AUDIO"] = "ffpyplayer"

from src.app import App

application = App()
application.run()
