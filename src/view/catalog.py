import threading

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup

from src.model.utils import *


class Catalog(TabbedPanelItem):
    def __init__(self, app):
        self.popup = None
        self.app = app
        self.zip = None
        self.valid = None
        TabbedPanelItem.__init__(self,
                                 background_normal=self.app.conf.ICON_CATALOG,
                                 background_down=self.app.conf.ICON_CATALOG_PRESSED)
        self.app.catalog_input = TextInput(size_hint_y=None,
                                           font_size='16sp',
                                           multiline=False,
                                           hint_text=f"v{VERSION}_{ARCH}",
                                           text="")
        self.app.catalog_input.size = ('32sp', '32sp')
        self.catalog_buttons = GridLayout(rows=1,
                                          size_hint_x=None,
                                          padding=[140, 15],
                                          spacing=[140])
        self.catalog_buttons.bind(minimum_width=self.catalog_buttons.setter('width'))
        self.catalog_scrollview = ScrollView(do_scroll_x=True, do_scroll_y=False)

        for cover in self.app.stor.storage_books:
            c = cover[5:-4]
            title = c.split("_-_")
            author = title[0].replace("_", " ")
            book = title[1].replace("_", " ")
            button_box_layout = BoxLayout(size_hint=(None, 1),
                                          padding=(0, 0),
                                          width=(Window.size[0] - 3 * 140) // 2,
                                          orientation="vertical")
            button_up = Label(text=author,
                              font_size='32px',
                              bold=True,
                              size_hint=(1, 0.1),
                              padding=(0, 0),
                              color="white")
            button = Button(size_hint=(1, 0.5),
                            padding=(0,0),
                            width=(Window.size[0] - 3 * 140) // 2,
                            background_normal=cover,
                            on_release=self.catalog_button_click)
            button_down = Label(text=book,
                                font_size='32px',
                                bold=True,
                                size_hint=(1, 0.1),
                                padding=(0, 0),
                                color="white")
            button_box_layout.add_widget(button_up)
            button_box_layout.add_widget(button)
            button_box_layout.add_widget(button_down)
            self.catalog_buttons.add_widget(button_box_layout)
            button.bind(on_double_tap=self.catalog_double_tap)
        self.catalog_scrollview.add_widget(self.catalog_buttons)

        self.item_catalog_boxlayout = BoxLayout(orientation="vertical")
        self.item_catalog_boxlayout.add_widget(self.app.catalog_input)
        self.item_catalog_boxlayout.add_widget(self.catalog_scrollview)
        self.add_widget(self.item_catalog_boxlayout)
        with self.catalog_buttons.canvas.before:
            Color(0, 0, 0, mode="rgb")
            Rectangle(size=(10 ** 6, 10 ** 6), pos=(-10 ** 3, 0))

    def on_press(self):
        self.on_resize()

    def on_resize(self, _=None, __=None):
        Clock.schedule_once(self.resize_widgets, timeout=0.5)

    def resize_widgets(self, _=None):
        with self.app.table.table_gridlayout.canvas.before:
            Color(0, 0, 0, mode="rgb")
            Rectangle(size=(10 ** 6, Window.height - self.app.container.tab_height - 6),
                      pos=(0, 0))
        for layout in self.catalog_buttons.children:
            if layout.width >= Window.width:
                layout.width = Window.width
                layout.children[0].size_hint = (1, None)
                layout.children[1].size_hint = (1, None)
                layout.children[2].size_hint = (1, None)
                layout.children[0].height = (layout.height - layout.width) // 2
                layout.children[1].height = layout.width
                layout.children[2].height = (layout.height - layout.width) // 2
            else:
                layout.children[0].size_hint = (1, 0.25)
                layout.children[1].size_hint = (1, 0.5)
                layout.children[2].size_hint = (1, 0.25)
                layout.width = layout.children[1].height
            layout.children[0].font_size = str(layout.width // 16) + 'px'
            layout.children[2].font_size = str(layout.width // 16) + 'px'

    def catalog_button_click(self, value=None):
        self.app.log.debug("Enter to function 'catalog_button_click()'")
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()

        current = self.app.stor.storage_books[value.background_normal]
        self.app.log.debug(f"Selected book - '{current}'")
        self.app.conf.load_options()

        try:
            self.app.sound.stop()
        except AttributeError:
            self.app.log.debug("WARNING: AttributeError self.app.sound.stop()")
        try:
            self.app.current_select = current
            self.app.set_sound_pos(float(self.app.opt[POSITIONS][self.app.current_select][POSI]))
            self.app.chunk_current = \
                self.app.opt[POSITIONS][self.app.current_select][CHUNK]
        except KeyError:
            self.app.set_sound_pos(0.0)
            self.app.opt[POSITIONS][self.app.current_select] = {
                POSI: "0", AUDIO: EN, CHUNK: 0}
            self.app.chunk_current = 0
            self.app.conf.save_options()
        self.valid = value.background_normal[:-4] + "/" + self.app.conf.VALID
        self.zip = self.app.current_select[5:-1] + ".zip"
        self.app.container.switch_to(self.app.table)
        self.show_popup()
        Clock.schedule_once(self.start_thread, timeout=1)

    def start_thread(self, _):
        self.app.log.debug("Enter to function 'start_thread()'")
        thread_download = threading.Thread(target=self.download_zip)
        thread_download.start()
        thread_download.join()
        self.app.log.debug("self.app.syncs[self.app.current_select].loads()")
        self.app.syncs[self.app.current_select].loads()
        self.app.log.debug("Create Clock.schedule_once(self.app.player.delay_run, timeout=0)")
        Clock.schedule_once(self.app.player.delay_run, timeout=0)

    def catalog_double_tap(self, _=None, __=None, ___=None):
        self.app.log.debug("Fired function catalog_double_tap() for Button widget")

    def show_popup(self):
        self.app.log.debug("Enter to function 'show_popup()'")
        self.app.popup_content = GridLayout(cols=1)
        self.app.popup_label = Label(text=f"Load file '{self.zip}'")
        self.app.popup_content.add_widget(self.app.popup_label)
        self.app.popup = Popup(title="Loading...",
                               size_hint=(0.8, 0.5),
                               content=self.app.popup_content, disabled=True)
        self.app.popup.open()

    def download_zip(self):
        self.app.log.debug("Enter to function 'download_zip()'")
        if not os.path.exists(self.valid):
            self.app.stor.storage_book(self.zip)
        self.app.popup.dismiss()
