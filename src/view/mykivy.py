from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

from kivy.app import App as KivyApp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.tabbedpanel import TabbedPanel

from src.model.mysound import MySound

from .catalog import Catalog
from .table import Table


class MyKivy(KivyApp):

    def __init__(self, app, **kwargs):
        self.app = app
        Config.set('kivy', 'window_icon', self.app.conf.ICON_PNG)
        super().__init__(**kwargs)
        self.container = TabbedPanel()
        # self.app.options = Options(self.app)
        self.table = Table(app=self)
        self.catalog = Catalog(app=self)

    def build(self):
        Window.bind(size=self.catalog.on_resize)
        self.icon = self.app.conf.ICON_ICO
        self.container.size_hint = (1, 1)
        self.container.do_default_tab = False
        self.container.add_widget(self.catalog)
        self.container.add_widget(self.table)
        # self.app.container.add_widget(self.app.options)
        self.container.default_tab = self.table
        with self.table.table_gridlayout.canvas.before:
            Color(0, 0, 0, mode="rgb")
            Rectangle(size=(10 ** 6, Window.height - self.container.tab_height - 6),
                      pos=(0, 0))
        return self.container
