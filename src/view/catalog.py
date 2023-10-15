import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from src.model.utils import *
from src.controller.proxy import Proxy


class Catalog(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.dir_books = {}
        self.app.pre_load()
        TabbedPanelItem.__init__(self, text="Catalog")
        self.app.catalog_input = TextInput(size_hint_y=None,
                                           font_size='16sp',
                                           multiline=False,
                                           text="")
        self.app.catalog_input.size = ('32sp', '32sp')
        self.catalog_buttons = GridLayout(rows=1,
                                          size_hint_x=None,
                                          padding=[70, 15],
                                          spacing=[70])
        self.catalog_buttons.bind(minimum_width=self.catalog_buttons.setter('width'))
        self.catalog_scrollview = ScrollView(do_scroll_x=True, do_scroll_y=False)

        # button = Button(size_hint=(None, 1),
        #                 width=Window.size[0] // 2,
        #                 background_normal=self.app.FRAGMENT_BOOK_DIR + 'cover.jpg',
        #                 on_release=self.catalog_button_click)
        # self.catalog_buttons.add_widget(button)
        for i in os.listdir("data"):
            if not os.path.isdir("data/" + i):
                continue
            cover = f"data/{i}/{self.app.COVER}"
            self.dir_books[cover] = f"data/{i}/"
            button = Button(size_hint=(None, 1),
                            width=(Window.size[0] - 3*70) // 2,
                            background_normal=cover,
                            on_release=self.catalog_button_click)
            self.catalog_buttons.add_widget(button)
        self.catalog_scrollview.add_widget(self.catalog_buttons)

        self.item_catalog_boxlayout = BoxLayout(orientation="vertical")
        self.item_catalog_boxlayout.add_widget(self.app.catalog_input)
        self.item_catalog_boxlayout.add_widget(self.catalog_scrollview)
        self.add_widget(self.item_catalog_boxlayout)

    def catalog_button_click(self, value=None):
        current = self.dir_books[value.background_normal]
        self.app.log(f"Selected book - '{current}'")
        if not(self.app.table.clock_action is None):
            self.app.table.clock_action.cancel()
        self.app.current_select = current
        try:
            self.app.sound.stop()
        except AttributeError:
            self.app.log("Warning: AttributeError (ignored this)")
        try:
            self.app.set_sound_pos(float(self.app.option[POSITIONS][self.app.current_select][POSI]))
        except KeyError:
            self.app.set_sound_pos(0.0)
            self.app.option[POSITIONS][self.app.current_select] = {POSI: "0", AUDIO: EN}
        self.app.container.switch_to(self.app.table)
        self.app.pre_load()
        Proxy.load_text_book(self, self.app.table_label_left, self.app.eng_book)
        Proxy.load_text_book(self, self.app.table_label_right, self.app.rus_book)
