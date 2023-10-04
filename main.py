import os
os.environ["KIVY_AUDIO"] = "ffpyplayer"
# from kivy.core.audio.audio_ffpyplayer import *
# from src.controller.mysound import MySound

from src.app import App

application = App()
application.run()
