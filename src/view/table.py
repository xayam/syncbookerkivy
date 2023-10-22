from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanelItem

from src.model.utils import *
from src.view.mytextinput import MyTextInput


class Table(TabbedPanelItem):
    def __init__(self, model):
        self.model = model
        TabbedPanelItem.__init__(self,
                                 background_normal=self.model.conf.ICON_TABLE,
                                 background_down=self.model.conf.ICON_TABLE_PRESSED)
        self.table_gridlayout = GridLayout(cols=3)
        self.table_navigator = GridLayout(rows=5,
                                          size_hint_x=0.3)
        self.table_prev = Button(background_normal=self.model.conf.ICON_PREV,
                                 background_down=self.model.conf.ICON_PREV_PRESSED,
                                 on_release=self.model.player.prev_button_click)
        self.table_navigator.add_widget(self.table_prev)
        self.table_play = Button(background_normal=self.model.conf.ICON_PLAY,
                                 background_down=self.model.conf.ICON_PLAY_PRESSED,
                                 on_release=self.model.player.play_button_click)
        self.table_navigator.add_widget(self.table_play)
        self.table_pause = Button(background_normal=self.model.conf.ICON_PAUSE,
                                  background_down=self.model.conf.ICON_PAUSE_PRESSED,
                                  on_release=self.model.player.pause_button_click)
        self.table_navigator.add_widget(self.table_pause)
        self.table_stop = Button(background_normal=self.model.conf.ICON_STOP,
                                 background_down=self.model.conf.ICON_STOP_PRESSED,
                                 on_release=self.model.player.stop_button_click)
        self.table_navigator.add_widget(self.table_stop)
        self.table_next = Button(background_normal=self.model.conf.ICON_NEXT,
                                 background_down=self.model.conf.ICON_NEXT_PRESSED,
                                 on_release=self.model.player.next_button_click)
        self.table_navigator.add_widget(self.table_next)
        self.table_gridlayout.add_widget(self.table_navigator)
        self.model.table_book_left = ScrollView(do_scroll_x=False,
                                                do_scroll_y=True,
                                                bar_width=15)
        self.model.table_label_left = MyTextInput(size_hint=(1, None),
                                                  focus=False,
                                                  selection_color=self.model.opt[SEL],
                                                  background_color=self.model.opt[BG],
                                                  foreground_color=self.model.opt[FG],
                                                  handle_image_left=self.model.conf.DISABLE_MARKER,
                                                  handle_image_right=self.model.conf.DISABLE_MARKER,
                                                  text="Select a book in the 'Catalog' section")
        self.model.table_label_left.is_focusable = False
        self.model.table_label_left.bind(text=self.on_text_table_label_left)
        self.model.table_label_left.bind(on_touch_up=self.model.action.touch_up_click)
        self.model.table_label_left.bind(on_double_tap=self.model.action.double_tap)
        self.model.table_label_left.height = max(self.model.table_label_left.minimum_height,
                                                 self.model.table_book_left.height)
        self.model.table_book_left.add_widget(self.model.table_label_left)
        self.table_gridlayout.add_widget(self.model.table_book_left)
        self.model.table_book_right = ScrollView(do_scroll_x=False,
                                                 do_scroll_y=True,
                                                 bar_width=15)
        self.model.table_label_right = MyTextInput(size_hint=(1, None),
                                                   focus=False,
                                                   selection_color=self.model.opt[SEL],
                                                   background_color=self.model.opt[BG],
                                                   foreground_color=self.model.opt[FG],
                                                   handle_image_left=self.model.conf.DISABLE_MARKER,
                                                   handle_image_right=self.model.conf.DISABLE_MARKER,
                                                   text="Выберите книгу в разделе 'Catalog'")
        self.model.table_label_right.is_focusable = False
        self.model.table_label_right.bind(text=self.on_text_table_label_right)
        self.model.table_label_right.bind(on_touch_up=self.model.action.touch_up_click)
        self.model.table_label_right.bind(on_double_tap=self.model.action.double_tap)
        self.model.table_label_right.height = max(self.model.table_label_right.minimum_height,
                                                  self.model.table_book_right.height)
        self.model.table_book_right.add_widget(self.model.table_label_right)
        self.table_gridlayout.add_widget(self.model.table_book_right)
        self.add_widget(self.table_gridlayout)

    def on_text_table_label_left(self, _=None, __=None):
        Clock.schedule_once(self.update_table_label_left, 0)

    def update_table_label_left(self, _=None):
        self.model.log.debug("Enter to function 'update_table_label_left()'")
        self.model.table_label_left.height = (len(self.model.table_label_left.lines) + 1) * \
                                             (self.model.table_label_left.line_height +
                                              self.model.table_label_left.line_spacing)
        if self.model.table_label_left.text == "\n" * 100:
            self.model.log.debug("True is self.app.table_label_left.text == '\n'*50")
            return
        self.model.log.debug("MySound().load_seek")
        if self.model.opt[POSITIONS][self.model.current_select][AUDIO] == EN:
            try:
                self.model.sound.stop()
                self.model.clock_action.cancel()
            except AttributeError:
                self.model.log.debug("WARNING: AttributeError self.app.sound.stop()")
            self.model.log.debug(f"self.app.chunk_current={self.model.chunk_current}")
            self.model.log.debug("self.app.opt[POSITIONS][self.app.current_select][CHUNK]=" +
                                 str(self.model.opt[POSITIONS][self.model.current_select][CHUNK]))

            self.model.sound = SoundLoader.load(
                self.model.current_select + self.model.conf.ENG_MP3). \
                load_seek(self.model.get_sound_pos())
            self.model.log.debug("Create Clock.schedule_interval(self.app.action.clock_action_time, 0.5)")
            self.model.clock_action = Clock.schedule_interval(self.model.action.clock_action_time, 0.5)

    def on_text_table_label_right(self, _=None, __=None):
        Clock.schedule_once(self.update_table_label_right, 0)

    def update_table_label_right(self, _=None):
        self.model.log.debug("Enter to function 'update_table_label_right()'")
        self.model.table_label_right.height = (len(self.model.table_label_right.lines) + 1) * \
                                              (self.model.table_label_right.line_height +
                                               self.model.table_label_right.line_spacing)
        if self.model.table_label_left.text == "\n" * 100:
            self.model.log.debug("True is self.app.table_label_right.text == '\n'*50")
            return
        self.model.log.debug("MySound().load_seek")
        if self.model.opt[POSITIONS][self.model.current_select][AUDIO] == RU:
            try:
                self.model.sound.stop()
                self.model.clock_action.cancel()
            except AttributeError:
                self.model.log.debug("WARNING: AttributeError self.app.sound.stop()")
            self.model.log.debug(f"self.app.chunk_current={self.model.chunk_current}")
            self.model.log.debug("self.app.opt[POSITIONS][self.app.current_select][CHUNK]=" +
                                 str(self.model.opt[POSITIONS][self.model.current_select][CHUNK]))
            self.model.sound = SoundLoader.load(
                self.model.current_select + self.model.conf.RUS_MP3). \
                load_seek(self.model.get_sound_pos())
            self.model.log.debug("Create Clock.schedule_interval(self.app.action.clock_action_time, 0.5)")
            self.model.clock_action = Clock.schedule_interval(self.model.action.clock_action_time, 0.5)
