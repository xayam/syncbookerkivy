import os
# from plyer.facades.orientation import Orientation
# from kivy.utils import platform

os.environ["KIVY_AUDIO"] = "ffpyplayer"

# if platform == "android":
#     orientation = Orientation()
#     orientation.set_sensor(mode='landscape')

from src.app import App

application = App()
application.run()
