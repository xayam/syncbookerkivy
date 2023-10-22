from kivy.utils import platform

from src.controller.controller import Controller


class App(Controller):
    def __init__(self):
        self.android = platform == "android"
        self.controller = Controller.__init__(self, app=self)
