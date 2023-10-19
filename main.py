import os

from src.app import App

os.environ["KIVY_AUDIO"] = "ffpyplayer"

application = App()

try:
    application.run()
except Exception as e:
    application.app.log.debug("SystemError: " + type(e).__name__ + ", " + e.__str__())
