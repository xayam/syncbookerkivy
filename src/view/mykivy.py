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
        print(str(self.model))
        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)
        Window.clearcolor = (0, 0, 0, 1)
        self.model.container = TabbedPanel()
        self.model.table = Table(model=self.model)
        self.model.catalog = Catalog(model=self.model)
        self.model.options = Options(model=self.model)
        Window.bind(size=self.model.catalog.on_resize)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.model.container.size_hint = (1, 1)
        self.model.container.do_default_tab = False
        self.model.container.add_widget(self.model.catalog)
        self.model.container.add_widget(self.model.table)
        self.model.container.add_widget(self.model.options)
        self.model.container.default_tab = self.model.table
        return self.model.container

    def on_start(self):
        self.model.catalog.on_resize()
