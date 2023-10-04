from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader

from src.model.utils import *


class Table(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.clock_action = None
        TabbedPanelItem.__init__(self, text="Table")
        self.table_gridlayout = GridLayout(cols=3)

        self.table_navigator = GridLayout(rows=5, size_hint_x=0.3)

        self.table_prev = Button(text="Prev")
        self.table_navigator.add_widget(self.table_prev)

        self.table_play = Button(text="Play",
                                 on_press=self.play_button_click)
        self.table_navigator.add_widget(self.table_play)

        self.table_pause = Button(text="Pause",
                                  on_press=self.pause_button_click)
        self.table_navigator.add_widget(self.table_pause)

        self.table_stop = Button(text="Stop",
                                 on_press=self.stop_button_click)
        self.table_navigator.add_widget(self.table_stop)

        self.table_next = Button(text="Next")
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
                                              text="Choice book in 'Catalog'")
        self.app.table_label_left.is_focusable = False
        self.app.table_label_left.bind(text=self.on_text_table_label_left)
        self.app.table_label_left.bind(on_touch_up=self.touch_up_click)

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
                                               text="Выберите книгу в разделе 'Catalog'")
        self.app.table_label_right.is_focusable = False
        self.app.table_label_right.bind(text=self.on_text_table_label_right)
        self.app.table_label_right.bind(on_touch_up=self.touch_up_click)
        self.app.table_label_right.height = max(self.app.table_label_right.minimum_height,
                                                self.app.table_book_right.height)
        self.app.table_book_right.add_widget(self.app.table_label_right)

        self.table_gridlayout.add_widget(self.app.table_book_right)
        self.add_widget(self.table_gridlayout)

    def touch_up_click(self, instance, event):
        if not (self.clock_action is None):
            self.clock_action.cancel()
        pos = instance.cursor_index(instance.get_cursor_from_xy(*event.pos))
        if instance == self.app.table_label_left:
            sync = self.app.eng_sync
        else:
            sync = self.app.rus_sync
        for i in range(len(sync)):
            if sync[i][POS_START] > pos:
                try:
                    if instance == self.app.table_label_left:
                        # if self.app.option[POSITIONS][self.app.current_select][AUDIO] != EN:
                        self.app.sound.stop()
                        self.app.sound = SoundLoader.load(self.app.current_select + self.app.ENG_FLAC)
                        self.app.option[POSITIONS][self.app.current_select][AUDIO] = EN
                    else:
                        # if self.app.option[POSITIONS][self.app.current_select][AUDIO] != RU:
                        self.app.sound.stop()
                        self.app.sound = SoundLoader.load(self.app.current_select + self.app.RUS_FLAC)
                        self.app.option[POSITIONS][self.app.current_select][AUDIO] = RU
                except AttributeError:
                    self.app.container.switch_to(self.app.catalog)
                    return
                self.app.option[POSITIONS][self.app.current_select][POSI] = sync[i][TIME_START]
                self.app.set_sound_pos(sync[i][TIME_START])
                self.app.save_options()
                Clock.schedule_once(self.play_button_click, 2)
                return

    def clock_action_time(self, event=None):
        self.table_next.text = f"T:{self.app.get_sound_pos():0.1f}"
        self.table_prev.text = f"A:{self.app.sound.get_pos():0.1f}"
        if self.app.option[POSITIONS][self.app.current_select][AUDIO] == EN:
            curr = R_POS
            curr_other = L_POS
            text_area = self.app.table_label_left
            book_area = self.app.table_book_left
            sync = self.app.eng_sync
            text_area_other = self.app.table_label_right
            book_area_other = self.app.table_book_right
            sync_other = self.app.rus_sync
        else:
            curr = L_POS
            curr_other = R_POS
            text_area = self.app.table_label_right
            book_area = self.app.table_book_right
            sync = self.app.rus_sync
            text_area_other = self.app.table_label_left
            book_area_other = self.app.table_book_left
            sync_other = self.app.eng_sync
        pos = max([self.app.get_sound_pos(), self.app.sound.get_pos()])
        for i in range(len(sync)):
            if sync[i][TIME_START] > pos:
                for k in range(len(self.app.micro)):
                    for j in range(len(self.app.micro[k])):
                        if self.app.micro[k][j][curr] >= sync[i][POS_START]:
                            for z in range(len(sync_other)):
                                if self.app.micro[k][j][curr_other] >= sync_other[z][POS_START]:
                                    self.app.pos_end = self.app.micro[k][j][curr]
                                    self.app.sync_i = i
                                    self.app.pos_end_other = self.app.micro[k][j][curr_other]
                                    self.app.sync_other_i = z
                                    self.app.start = sync[i][TIME_START]

                                    if sync[i][POS_START] < len(text_area.text) - 1:
                                        text_area.select_text(0, sync[i][POS_START])
                                        text_area.cursor = (0, text_area. \
                                                            get_cursor_from_index(
                                                            text_area.selection_to)[1])
                                        y = text_area.cursor_pos[1] - book_area.height // 2
                                        book_area.scroll_y = book_area. \
                                            convert_distance_to_scroll(0, y)[1]

                                    if self.app.pos_end_other < len(text_area_other.text) - 1:
                                        text_area_other.select_text(0, self.app.pos_end_other)
                                        text_area_other.cursor = (0, text_area_other. \
                                                                  get_cursor_from_index(
                                                                  text_area_other.selection_to)[1])
                                        y = text_area_other.cursor_pos[1] - book_area_other.height // 2
                                        book_area_other.scroll_y = book_area_other. \
                                            convert_distance_to_scroll(0, y)[1]

                                    self.app.option[POSITIONS][self.app.current_select][POSI] = \
                                        str(pos)
                                    self.app.set_sound_pos(pos)
                                    self.app.save_options()
                                    return

    def play_button_click(self, event=None):
        if not (self.app.sound is None):
            if not (self.clock_action is None):
                self.clock_action.cancel()
            if self.app.sound.state != 'play':
                self.app.sound.play()
            Clock.schedule_once(self.do_seek, 0)

    def stop_button_click(self, event=None):
        if not (self.app.sound is None):
            if not (self.clock_action is None):
                self.clock_action.cancel()
            self.app.set_sound_pos(0.0)
            self.app.sound.stop()
            self.app.option[POSITIONS][self.app.current_select][POSI] = "0"
            self.app.save_options()

    def do_seek(self, event=None):
        if self.app.get_sound_pos() > 0.0:
            self.app.sound.seek(self.app.get_sound_pos())
        self.clock_action = Clock.schedule_interval(self.clock_action_time, 0.5)

    def pause_button_click(self, event=None):
        if not (self.app.sound is None):
            if not (self.clock_action is None):
                self.clock_action.cancel()
            self.app.set_sound_pos(self.app.sound.get_pos())
            self.app.sound.stop()

    def on_text_table_label_left(self, instance, value):
        self.clock_left = Clock.schedule_interval(self.update_table_label_left, 3)

    def update_table_label_left(self, *args):
        self.app.table_label_left.height = (len(self.app.table_label_left._lines) + 1) * \
                                           self.app.table_label_left.line_height
        self.clock_left.cancel()
        Clock.schedule_once(self.play_button_click, 2)

    def on_text_table_label_right(self, instance, value):
        self.clock_right = Clock.schedule_interval(self.update_table_label_right, 3)

    def update_table_label_right(self, *args):
        self.app.table_label_right.height = (len(self.app.table_label_right._lines) + 1) * \
                                            self.app.table_label_right.line_height
        self.clock_right.cancel()
