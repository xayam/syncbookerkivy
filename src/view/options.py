from kivy.uix.tabbedpanel import TabbedPanelItem


class Options(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        TabbedPanelItem.__init__(self,
                                 background_normal=self.app.conf.ICON_OPTIONS,
                                 background_down=self.app.conf.ICON_OPTIONS_PRESSED)
