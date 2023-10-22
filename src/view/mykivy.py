from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

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

    def __init__(self, app, **kwargs):
        self.app = app
        Config.set('kivy', 'window_icon', self.app.conf.ICON_PNG)
        Window.clearcolor = (0, 0, 0, 1)
        super().__init__(**kwargs)
        self.container = TabbedPanel()
        self.app.options = Options(self.app)
        self.table = Table(app=self)
        self.catalog = Catalog(app=self)
        self.options = Options(app=self)

    def build(self):
        Window.bind(size=self.catalog.on_resize)
        self.icon = self.app.conf.ICON_ICO
        self.container.size_hint = (1, 1)
        self.container.do_default_tab = False
        self.container.add_widget(self.catalog)
        self.container.add_widget(self.table)
        self.container.add_widget(self.options)
        self.container.default_tab = self.table
        return self.container

    def on_start(self):
        self.catalog.on_resize()
