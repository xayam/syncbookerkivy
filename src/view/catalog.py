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
    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller

        self.popup = None
        self.zip = None
        self.valid = None

        TabbedPanelItem.__init__(self,
                                 background_normal=self.model.conf.ICON_CATALOG,
                                 background_down=self.model.conf.ICON_CATALOG_PRESSED)

        self.controller.catalog_input = TextInput(size_hint_y=None,
                                                  font_size='16sp',
                                                  multiline=False,
                                                  hint_text=f"v{VERSION}_{ARCH}",
                                                  text="")
        self.controller.catalog_input.size = ('32sp', '32sp')
        self.catalog_buttons = GridLayout(rows=1,
                                          size_hint=(None, 1),
                                          padding=[140, 15],
                                          spacing=[140])
        self.catalog_buttons.bind(minimum_width=self.catalog_buttons.setter('width'))
        self.catalog_scrollview = ScrollView(do_scroll_x=True, do_scroll_y=False)

        for cover in self.model.stor.storage_books:
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
                              size_hint=(1, 0.25),
                              padding=(0, 0),
                              color="white")
            button = Button(size_hint=(1, 0.5),
                            padding=(0, 0),
                            width=(Window.size[0] - 3 * 140) // 2,
                            background_normal=cover,
                            on_release=self.catalog_button_click)
            button_down = Label(text=book,
                                font_size='32px',
                                bold=True,
                                size_hint=(1, 0.25),
                                padding=(0, 0),
                                color="white")
            button_box_layout.add_widget(button_up)
            button_box_layout.add_widget(button)
            button_box_layout.add_widget(button_down)
            self.catalog_buttons.add_widget(button_box_layout)
            button.bind(on_double_tap=self.catalog_double_tap)
        self.catalog_scrollview.add_widget(self.catalog_buttons)

        self.item_catalog_boxlayout = BoxLayout(orientation="vertical")
        self.item_catalog_boxlayout.add_widget(self.controller.catalog_input)
        self.item_catalog_boxlayout.add_widget(self.catalog_scrollview)
        self.add_widget(self.item_catalog_boxlayout)
        with self.catalog_buttons.canvas.before:
            Color(0, 0, 0, mode="rgb")
            Rectangle(size=(10 ** 6, 10 ** 6), pos=(-10 ** 3, 0))

    def on_press(self):
        self.on_resize(timeout_catalog=0)

    def on_resize(self, _=None, __=None, timeout_table=0, timeout_catalog=1):
        Clock.schedule_once(self.redraw_table, timeout=timeout_table)
        Clock.schedule_once(self.resize_catalog, timeout=timeout_catalog)

    def redraw_table(self, _=None):
        self.model.log.debug("Enter to function 'redraw_table()'")
        self.controller.table.table_gridlayout.canvas.before.clear()
        with self.controller.table.table_gridlayout.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(Window.width, Window.height - self.controller.container.tab_height - 6),
                      pos=(0, 0))

    def resize_catalog(self, _=None):
        self.model.log.debug("Enter to function 'resize_catalog()'")
        self.controller.table.table_navigator.size_hint_x = None
        self.controller.table.table_navigator.width = \
            min([
                (Window.height - self.controller.container.tab_height - 6) // 5,
                self.controller.container.tab_width
            ])
        self.controller.table.table_navigator.padding = [0,
            (Window.height - self.controller.container.tab_height - 6 -
             5 * self.controller.table.table_navigator.width) // 2
        ]
        for button in self.controller.table.table_navigator.children:
            button.size_hint = (1, None)
            button.height = self.controller.table.table_navigator.width

        for layout in self.catalog_buttons.children:
            layout.width = min([
                Window.width - 40,
                int(0.5 * (Window.height - self.controller.container.tab_height - 6))])
            layout.children[0].size_hint = (1, None)
            layout.children[1].size_hint = (1, None)
            layout.children[2].size_hint = (1, None)
            layout.children[1].height = layout.width
            layout.children[0].height = (layout.height - layout.width) // 2
            layout.children[2].height = (layout.height - layout.width) // 2
            layout.children[0].font_size = str(layout.width // 16) + 'px'
            layout.children[2].font_size = str(layout.width // 16) + 'px'


    def catalog_button_click(self, value=None):
        self.model.log.debug("Enter to function 'catalog_button_click()'")
        if not (self.model.clock_action is None):
            self.model.clock_action.cancel()

        current = self.model.stor.storage_books[value.background_normal]
        self.model.log.debug(f"Selected book - '{current}'")
        self.model.conf.load_options()

        try:
            self.model.sound.stop()
        except AttributeError:
            self.model.log.debug("WARNING: AttributeError self.app.sound.stop()")
        try:
            self.model.current_select = current
            self.model.set_sound_pos(float(self.model.opt[POSITIONS][self.model.current_select][POSI]))
            self.model.chunk_current = \
                self.model.opt[POSITIONS][self.model.current_select][CHUNK]
        except KeyError:
            self.model.set_sound_pos(0.0)
            self.model.opt[POSITIONS][self.model.current_select] = {
                POSI: "0", AUDIO: EN, CHUNK: 0}
            self.model.chunk_current = 0
            self.model.conf.save_options()
        self.valid = value.background_normal[:-4] + "/" + self.model.conf.VALID
        self.zip = self.model.current_select[5:-1] + ".zip"
        self.controller.container.switch_to(self.controller.table)
        self.show_popup()
        Clock.schedule_once(self.start_thread, timeout=1)

    def start_thread(self, _):
        self.model.log.debug("Enter to function 'start_thread()'")
        thread_download = threading.Thread(target=self.download_zip)
        thread_download.start()
        thread_download.join()
        self.model.log.debug("self.app.syncs[self.app.current_select].loads()")
        self.model.syncs[self.model.current_select].loads()
        self.model.log.debug("Create Clock.schedule_once(self.app.player.delay_run, timeout=0)")
        Clock.schedule_once(self.controller.player.delay_run, timeout=0)

    def catalog_double_tap(self, _=None, __=None, ___=None):
        self.model.log.debug("Fired function catalog_double_tap() for Button widget")

    def show_popup(self):
        self.model.log.debug("Enter to function 'show_popup()'")
        self.controller.popup_content = GridLayout(cols=1)
        self.controller.popup_label = Label(text=f"Load file '{self.zip}'")
        self.controller.popup_content.add_widget(self.controller.popup_label)
        self.controller.popup = Popup(title="Loading...",
                                 size_hint=(0.8, 0.5),
                                 content=self.controller.popup_content, disabled=True)
        self.controller.popup.open()

    def download_zip(self):
        self.model.log.debug("Enter to function 'download_zip()'")
        if not os.path.exists(self.valid):
            self.model.stor.storage_book(self.zip)
        self.controller.popup.dismiss()
