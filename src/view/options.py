from kivy.uix.tabbedpanel import TabbedPanelItem


class Options(TabbedPanelItem):
    def __init__(self, model):
        self.model = model
        TabbedPanelItem.__init__(self,
                                 background_normal=self.model.conf.ICON_OPTIONS,
                                 background_down=self.model.conf.ICON_OPTIONS_PRESSED)
