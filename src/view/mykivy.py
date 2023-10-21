from kivy.app import App as KivyApp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.config import Config

from src.model.mysound import MySound

from .catalog import Catalog
from .table import Table


class MyKivy(KivyApp):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        Config.set('kivy', 'window_icon', self.app.conf.ICON_PNG)
        self.container = TabbedPanel()
        # self.app.options = Options(self.app)
        self.table = Table(self)
        self.catalog = Catalog(self)

    def build(self):
        self.icon = self.app.conf.ICON_ICO
        self.app.container.size_hint = (1, 1)
        self.app.container.do_default_tab = False
        self.app.container.add_widget(self.app.catalog)
        self.app.container.add_widget(self.app.table)
        # self.app.container.add_widget(self.app.options)
        self.app.container.default_tab = self.app.table
        with self.app.table.table_gridlayout.canvas.before:
            Color(0, 0, 0, mode="rgb")
            Rectangle(size=(10 ** 6, Window.height - self.app.container.tab_height - 6),
                      pos=(0, 0))
        return self.app.container
