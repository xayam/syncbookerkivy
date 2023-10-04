from kivy.app import App as KivyApp
from kivy.uix.tabbedpanel import TabbedPanel
from .catalog import Catalog
from .table import Table
# from .options import Options


class View(KivyApp):

    def __init__(self, app):
        KivyApp.__init__(self)
        self.app = app
        self.app.container = TabbedPanel()
        # self.app.options = Options(self.app)
        self.app.catalog = Catalog(self.app)
        self.app.table = Table(self.app)

    def build(self):
        self.app.container.size_hint = (1, 1)
        self.app.container.do_default_tab = False
        self.app.container.add_widget(self.app.catalog)
        self.app.container.add_widget(self.app.table)
        # self.app.container.add_widget(self.app.options)
        self.app.container.default_tab = self.app.table
        return self.app.container
