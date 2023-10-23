from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.core.window import Window
from kivy.uix.label import Label

Window.minimum_width = 480
Window.minimum_height = 360


class MyKivySync(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)
        Window.clearcolor = (0, 0, 0, 1)
        self.controller.container = Label(text="In development")

    def build(self):
        self.icon = self.model.conf.ICON_ICO

        return self.controller.container

    def on_start(self):
        pass
