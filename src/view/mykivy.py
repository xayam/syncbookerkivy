from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel

from src.model.mysound import MySound

from .catalog import Catalog
from .table import Table
from .options import Options

Window.minimum_width = 480
Window.minimum_height = 360


class MyKivy(KivyApp):

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app
        
        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)
        Window.clearcolor = (0, 0, 0, 1)
        self.controller.container = TabbedPanel()
        self.controller.table = Table(model=self.model)
        self.controller.catalog = Catalog(model=self.model)
        self.controller.options = Options(model=self.model)
        Window.bind(size=self.controller.catalog.on_resize)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.controller.container.size_hint = (1, 1)
        self.controller.container.do_default_tab = False
        self.controller.container.add_widget(self.controller.catalog)
        self.controller.container.add_widget(self.controller.table)
        self.controller.container.add_widget(self.controller.options)
        self.controller.container.default_tab = self.controller.table
        return self.controller.container

    def on_start(self):
        self.controller.catalog.on_resize()
