import os
import threading
import time

from kivy import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup

from p4a import VERSION
from src.controller.downloader import Downloader
from src.model.utils import *
from src.controller.proxy import Proxy


class Catalog(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.dir_books = {}
        self.app.downloader = Downloader(self.app)
        TabbedPanelItem.__init__(self, text="Catalog")
        self.app.catalog_input = TextInput(size_hint_y=None,
                                           font_size='16sp',
                                           multiline=False,
                                           hint_text=f"v{VERSION}",
                                           text="")
        self.app.catalog_input.size = ('32sp', '32sp')
        self.catalog_buttons = GridLayout(rows=1,
                                          size_hint_x=None,
                                          padding=[140, 15],
                                          spacing=[140])
        self.catalog_buttons.bind(minimum_width=self.catalog_buttons.setter('width'))
        self.catalog_scrollview = ScrollView(do_scroll_x=True, do_scroll_y=False)

        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET
                                 # Permission.READ_EXTERNAL_STORAGE,
                                 # Permission.WRITE_EXTERNAL_STORAGE,
                                 # Permission.MEDIA_CONTENT_CONTROL,
                                 # Permission.GLOBAL_SEARCH,
                                 # Permission.READ_MEDIA_AUDIO
                                 ])

        self.app.downloader.update_list()

        for i in os.listdir("data"):
            if os.path.isfile("data/" + i) and (i[-4:] == ".jpg"):
                cover = f"data/{i}"
                self.dir_books[cover] = f"data/{i[:-4]}/"
                button = Button(size_hint=(None, 1),
                                width=(Window.size[0] - 3 * 140) // 2,
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
        if not (self.app.table.clock_action is None):
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
        self.valid = value.background_normal[:-4] + "/valid"
        path = value.background_normal[5:-4]
        self.zip = path + ".zip"
        self.app.container.switch_to(self.app.table)
        self.app.log("self.show_popup()")
        self.show_popup()
        Clock.schedule_once(self.delay_start, timeout=1)

    def delay_start(self, event=None):
        self.app.log("thread_download create")
        thread_download = threading.Thread(target=self.download_zip)
        self.app.log("thread_download start()")
        thread_download.start()
        self.app.log("thread_download join()")
        thread_download.join()
        self.app.pre_load()
        Proxy.load_text_book(self,
                             self.app.table_label_left,
                             self.app.eng_chunks[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.rus_chunks[self.app.chunk_current])
    def show_popup(self):
        self.content = GridLayout(cols=1)
        self.content.add_widget(Label(text=f"Download book '{self.zip}'"))
        self.popup = Popup(title="Downloading...",
                           size_hint=(None, None), size=(512, 256),
                           content=self.content, disabled=True)
        self.popup.open()

    def download_zip(self):
        if not os.path.exists(self.valid):
            self.app.downloader.download_book(self.zip)
        self.popup.dismiss()
