from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanelItem

from src.model.utils import *


class Table(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        TabbedPanelItem.__init__(self,
                                 background_normal=self.app.conf.ICON_TABLE,
                                 background_down=self.app.conf.ICON_TABLE_PRESSED)
        self.table_gridlayout = GridLayout(cols=3)
        self.table_navigator = GridLayout(rows=5,
                                          size_hint_x=0.3)
        self.table_prev = Button(background_normal=self.app.conf.ICON_PREV,
                                 background_down=self.app.conf.ICON_PREV_PRESSED,
                                 on_release=self.app.player.prev_button_click)
        self.table_navigator.add_widget(self.table_prev)
        self.table_play = Button(background_normal=self.app.conf.ICON_PLAY,
                                 background_down=self.app.conf.ICON_PLAY_PRESSED,
                                 on_release=self.app.player.play_button_click)
        self.table_navigator.add_widget(self.table_play)
        self.table_pause = Button(background_normal=self.app.conf.ICON_PAUSE,
                                  background_down=self.app.conf.ICON_PAUSE_PRESSED,
                                  on_release=self.app.player.pause_button_click)
        self.table_navigator.add_widget(self.table_pause)
        self.table_stop = Button(background_normal=self.app.conf.ICON_STOP,
                                 background_down=self.app.conf.ICON_STOP_PRESSED,
                                 on_release=self.app.player.stop_button_click)
        self.table_navigator.add_widget(self.table_stop)
        self.table_next = Button(background_normal=self.app.conf.ICON_NEXT,
                                 background_down=self.app.conf.ICON_NEXT_PRESSED,
                                 on_release=self.app.player.next_button_click)
        self.table_navigator.add_widget(self.table_next)
        self.table_gridlayout.add_widget(self.table_navigator)
        self.app.table_book_left = ScrollView(do_scroll_x=False,
                                              do_scroll_y=True,
                                              bar_width=15)
        self.app.table_label_left = TextInput(size_hint=(1, None),
                                              focus=False,
                                              selection_color=self.app.opt[SEL],
                                              background_color=self.app.opt[BG],
                                              foreground_color=self.app.opt[FG],
                                              handle_image_left=self.app.conf.DISABLE_MARKER,
                                              handle_image_right=self.app.conf.DISABLE_MARKER,
                                              text="Select a book in the 'Catalog' section")
        self.app.table_label_left.is_focusable = False
        self.app.table_label_left.bind(text=self.on_text_table_label_left)
        self.app.table_label_left.bind(on_touch_up=self.app.action.touch_up_click)
        self.app.table_label_left.bind(on_double_tap=self.app.action.double_tap)
        self.app.table_label_left.height = max(self.app.table_label_left.minimum_height,
                                               self.app.table_book_left.height)
        self.app.table_book_left.add_widget(self.app.table_label_left)
        self.table_gridlayout.add_widget(self.app.table_book_left)
        self.app.table_book_right = ScrollView(do_scroll_x=False,
                                               do_scroll_y=True,
                                               bar_width=15)
        self.app.table_label_right = TextInput(size_hint=(1, None),
                                               focus=False,
                                               selection_color=self.app.opt[SEL],
                                               background_color=self.app.opt[BG],
                                               foreground_color=self.app.opt[FG],
                                               handle_image_left=self.app.conf.DISABLE_MARKER,
                                               handle_image_right=self.app.conf.DISABLE_MARKER,
                                               text="Выберите книгу в разделе 'Catalog'")
        self.app.table_label_right.is_focusable = False
        self.app.table_label_right.bind(text=self.on_text_table_label_right)
        self.app.table_label_right.bind(on_touch_up=self.app.action.touch_up_click)
        self.app.table_label_right.bind(on_double_tap=self.app.action.double_tap)
        self.app.table_label_right.height = max(self.app.table_label_right.minimum_height,
                                                self.app.table_book_right.height)
        self.app.table_book_right.add_widget(self.app.table_label_right)
        self.table_gridlayout.add_widget(self.app.table_book_right)
        self.add_widget(self.table_gridlayout)

    def on_text_table_label_left(self, instance, value):
        Clock.schedule_once(self.update_table_label_left, 1)

    def update_table_label_left(self, *args):
        self.app.log.debug("Enter to function 'update_table_label_left()'")
        self.app.table_label_left.height = (len(self.app.table_label_left._lines) + 1) * \
                                           (self.app.table_label_left.line_height +
                                            self.app.table_label_left.line_spacing)
        print("table_label_left.text[:10] = '" + self.app.table_label_left.text[:10] + "'")
        if self.app.table_label_left.text == " ":
            self.app.log.debug("True is self.app.table_label_left.text == ' '")
            return
        self.app.log.debug("MySound().load_seek")

        if self.app.nonstop:
            self.app.log.debug("True == self.app.nonstop")
            self.app.nonstop = False
            return
        try:
            self.app.sound.stop()
            self.app.clock_action.cancel()
        except AttributeError:
            self.app.log.debug("WARNING: AttributeError self.app.sound.stop()")
        if self.app.opt[POSITIONS][self.app.current_select][AUDIO] == EN:
            self.app.sound = SoundLoader.load(self.app.current_select + self.app.conf.ENG_AUDIO). \
                load_seek(self.app.get_sound_pos())
        else:
            self.app.sound = SoundLoader.load(self.app.current_select + self.app.conf.RUS_AUDIO). \
                load_seek(self.app.get_sound_pos())
        self.app.log.debug("Create Clock.schedule_interval(self.clock_action_time, timeout=0.5)")
        self.app.clock_action = Clock.schedule_interval(self.app.action.clock_action_time, 0.5)

    def on_text_table_label_right(self, instance, value):
        Clock.schedule_once(self.update_table_label_right, 1)

    def update_table_label_right(self, *args):
        self.app.log.debug("Enter to function 'update_table_label_right()'")
        self.app.table_label_right.height = (len(self.app.table_label_right._lines) + 1) * \
                                            (self.app.table_label_right.line_height +
                                             self.app.table_label_right.line_spacing)
