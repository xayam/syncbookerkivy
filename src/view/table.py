from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button as MDRoundFlatButton
from kivy.uix.tabbedpanel import TabbedPanelItem

from src.model.utils import *
from src.controller.mysound import MySound

from .action import Action
from .player import Player


class Table(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.app.clock_action = None
        self.clock_doseek = None
        self.sound_state = 0
        self.app.touch_pos = 0
        self.nonstop = False
        TabbedPanelItem.__init__(self,
                                 background_normal="img/table.png",
                                 background_down="img/table_pressed.png")
        self.app.player = Player(self.app)
        self.app.action = Action(self.app)
        self.table_gridlayout = GridLayout(cols=3)
        self.table_navigator = GridLayout(rows=5,
                                          size_hint_x=0.3)
        self.table_prev = MDRoundFlatButton(background_normal="img/prev.png",
                                            background_down="img/prev_pressed.png",
                                            on_release=self.app.player.prev_button_click)
        self.table_navigator.add_widget(self.table_prev)

        self.table_play = MDRoundFlatButton(background_normal="img/play.png",
                                            background_down="img/play_pressed.png",
                                            on_release=self.app.player.play_button_click)
        self.table_navigator.add_widget(self.table_play)

        self.table_pause = MDRoundFlatButton(background_normal="img/pause.png",
                                             background_down="img/pause_pressed.png",
                                             on_release=self.app.player.pause_button_click)
        self.table_navigator.add_widget(self.table_pause)

        self.table_stop = MDRoundFlatButton(background_normal="img/stop.png",
                                            background_down="img/stop_pressed.png",
                                            on_release=self.app.player.stop_button_click)
        self.table_navigator.add_widget(self.table_stop)

        self.table_next = MDRoundFlatButton(background_normal="img/next.png",
                                            background_down="img/next_pressed.png",
                                            on_release=self.app.player.next_button_click)
        self.table_navigator.add_widget(self.table_next)

        self.table_gridlayout.add_widget(self.table_navigator)

        self.app.table_book_left = ScrollView(do_scroll_x=False,
                                              do_scroll_y=True,
                                              bar_width=15)

        self.app.table_label_left = TextInput(size_hint=(1, None),
                                              focus=False,
                                              selection_color=self.app.option[SEL],
                                              background_color=self.app.option[BG],
                                              foreground_color=self.app.option[FG],
                                              handle_image_left=self.app.DISABLE_MARKER,
                                              handle_image_right=self.app.DISABLE_MARKER,
                                              text="Select a book in the 'Catalog' section")
        self.app.table_label_left.is_focusable = False
        self.app.table_label_left.bind(text=self.on_text_table_label_left)
        self.app.table_label_left.bind(on_touch_up=self.app.action.touch_up_click)

        self.app.table_label_left.height = max(self.app.table_label_left.minimum_height,
                                               self.app.table_book_left.height)
        self.app.table_book_left.add_widget(self.app.table_label_left)
        self.table_gridlayout.add_widget(self.app.table_book_left)
        self.app.table_book_right = ScrollView(do_scroll_x=False,
                                               do_scroll_y=True,
                                               bar_width=15)
        self.app.table_label_right = TextInput(size_hint=(1, None),
                                               focus=False,
                                               selection_color=self.app.option[SEL],
                                               background_color=self.app.option[BG],
                                               foreground_color=self.app.option[FG],
                                               handle_image_left=self.app.DISABLE_MARKER,
                                               handle_image_right=self.app.DISABLE_MARKER,
                                               text="Выберите книгу в разделе 'Catalog'")
        self.app.table_label_right.is_focusable = False
        self.app.table_label_right.bind(text=self.on_text_table_label_right)
        self.app.table_label_right.bind(on_touch_up=self.app.action.touch_up_click)
        self.app.table_label_right.height = max(self.app.table_label_right.minimum_height,
                                                self.app.table_book_right.height)
        self.app.table_book_right.add_widget(self.app.table_label_right)
        self.table_gridlayout.add_widget(self.app.table_book_right)
        self.add_widget(self.table_gridlayout)

    def on_text_table_label_left(self, instance, value):
        Clock.schedule_once(self.update_table_label_left, 1)

    def update_table_label_left(self, *args):
        self.app.table_label_left.height = (len(self.app.table_label_left._lines) + 1) * \
                                           (self.app.table_label_left.line_height +
                                            self.app.table_label_left.line_spacing)
        if self.app.table_label_left.text == "":
            return
        self.app.log("MySound().load_seek")
        try:
            if self.nonstop:
                self.app.log("self.nonstop is True")
                self.nonstop = False
                return
            self.app.sound.stop()
            self.app.clock_action.cancel()
        except AttributeError:
            pass
        if self.app.option[POSITIONS][self.app.current_select][AUDIO] == EN:
            self.app.sound = SoundLoader.load(self.app.current_select + self.app.ENG_AUDIO). \
                         load_seek(self.app.get_sound_pos())
        else:
            self.app.sound = SoundLoader.load(self.app.current_select + self.app.RUS_AUDIO). \
                         load_seek(self.app.get_sound_pos())
        self.app.log("Clock.schedule_interval(self.clock_action_time)")
        self.app.clock_action = Clock.schedule_interval(self.app.action.clock_action_time, 0.5)

    def on_text_table_label_right(self, instance, value):
        Clock.schedule_once(self.update_table_label_right, 1)

    def update_table_label_right(self, *args):
        self.app.table_label_right.height = (len(self.app.table_label_right._lines) + 1) * \
                                            (self.app.table_label_right.line_height +
                                             self.app.table_label_right.line_spacing)
