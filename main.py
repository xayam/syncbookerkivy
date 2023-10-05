import os
from plyer.facades.orientation import Orientation
from kivy.utils import platform

from src.app import App

os.environ["KIVY_AUDIO"] = "ffpyplayer"

if platform == "android":
    orientation = Orientation()
    orientation.set_sensor(mode='landscape')

application = App()
application.run()
