from kivy.uix.tabbedpanel import TabbedPanelItem


class Options(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        TabbedPanelItem.__init__(self, text="Options")
