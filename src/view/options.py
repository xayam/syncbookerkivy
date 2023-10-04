from kivy.uix.tabbedpanel import TabbedPanelItem


class Options(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.container_item_options = TabbedPanelItem.__init__(self, text="Options")
