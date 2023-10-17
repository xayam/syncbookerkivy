from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button as MDRoundFlatButton
from kivy.uix.tabbedpanel import TabbedPanelItem

from src.model.utils import *
from src.controller.mysound import MySound

from .player import Player


class Table(TabbedPanelItem):
    def __init__(self, app):
        self.app = app
        self.app.clock_action = None
        self.clock_doseek = None
        self.sound_state = 0
        self.touch_pos = 0
        self.nonstop = False
        TabbedPanelItem.__init__(self,
                                 background_normal="img/table.png",
                                 background_down="img/table_pressed.png")
        self.app.player = Player(self.app)
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
                                               handle_image_left=self.app.DISABLE_MARKER,
                                               handle_image_right=self.app.DISABLE_MARKER,
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
        self.app.log("enter to function 'touch_up_click'")
        pos = instance.cursor_index(instance.get_cursor_from_xy(*event.pos))
        if self.touch_pos == pos:
            return
        self.touch_pos = pos
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        self.app.log(f"touch pos={pos}")
        try:
            if instance == self.app.table_label_left:
                sync = self.app.eng_sync
                chunk = self.app.eng_chunks
            else:
                sync = self.app.rus_sync
                chunk = self.app.rus_chunks

            for p in range(self.app.chunk_current):
                pos += len(chunk[p])

            for i in range(len(sync)):
                if sync[i][POS_START] > pos:
                    self.app.log("self.app.sound stop and reload")
                    self.app.sound.stop()
                    self.app.option[POSITIONS][self.app.current_select][POSI] = sync[i][TIME_START]
                    self.app.set_sound_pos(sync[i][TIME_START])
                    if instance == self.app.table_label_left:
                        self.app.sound = SoundLoader.load(
                            self.app.current_select + self.app.ENG_AUDIO). \
                            load_seek(self.app.get_sound_pos())
                        self.app.option[POSITIONS][self.app.current_select][AUDIO] = EN
                    else:
                        self.app.sound = SoundLoader.load(
                            self.app.current_select + self.app.RUS_AUDIO). \
                            load_seek(self.app.get_sound_pos())
                        self.app.option[POSITIONS][self.app.current_select][AUDIO] = RU
                    self.app.save_options()
                    self.app.log(f"create clock Clock.schedule_interval(self.clock_action_time)")
                    self.app.clock_action = Clock.schedule_interval(self.clock_action_time, 0.5)
                    return
        except AttributeError:
            self.app.log("WARNING, AttributeError (ignored this)")
            self.touch_pos = 0
            self.app.container.switch_to(self.app.catalog)
            return

    def clock_action_time(self, event=None):
        self.app.log("enter to function 'clock_action_time'")
        if self.app.option[POSITIONS][self.app.current_select][AUDIO] == EN:
            curr = R_POS
            curr_other = L_POS
            text_area = self.app.table_label_left
            book_area = self.app.table_book_left
            sync = self.app.eng_sync
            text_area_other = self.app.table_label_right
            book_area_other = self.app.table_book_right
            sync_other = self.app.rus_sync
            chunk = self.app.eng_chunks
            chunk_other = self.app.rus_chunks
        else:
            curr = L_POS
            curr_other = R_POS
            text_area = self.app.table_label_right
            book_area = self.app.table_book_right
            sync = self.app.rus_sync
            text_area_other = self.app.table_label_left
            book_area_other = self.app.table_book_left
            sync_other = self.app.eng_sync
            chunk = self.app.rus_chunks
            chunk_other = self.app.eng_chunks
        pos = self.app.sound.get_pos()
        if self.app.sound._ffplayer.get_pts() + 0.5 >= \
           self.app.sound._ffplayer.get_metadata()['duration']:
            self.app.player.stop_button_click()
            self.app.option[POSITIONS][self.app.current_select][POSI] = "0.0"
            self.app.save_options()
        for i in range(len(sync)):
            if sync[i][TIME_START] > pos:
                for k in range(len(self.app.micro)):
                    for j in range(len(self.app.micro[k])):
                        if self.app.micro[k][j][curr] > sync[i][POS_START]:
                            for z in range(len(sync_other)):
                                if self.app.micro[k][j][curr_other] > sync_other[z][POS_START]:
                                    self.app.pos_end = self.app.micro[k][j][curr]
                                    self.app.sync_i = i
                                    self.app.pos_end_other = self.app.micro[k][j][curr_other]
                                    self.app.sync_other_i = z
                                    self.app.start = sync[i][TIME_START]

                                    position = sync[i][POS_START]
                                    for p in range(self.app.chunk_current):
                                        position -= len(chunk[p])
                                    if position > len(chunk[self.app.chunk_current]):
                                        self.nonstop = True
                                        self.app.player.next_chunk()
                                        return
                                    try:
                                        text_area.select_text(0, position)
                                        y1 = text_area.get_cursor_from_index(
                                                text_area.selection_to)[1]
                                        text_area.cursor = (0, y1)
                                        y = text_area.cursor_pos[1] - book_area.height + \
                                            y1 * (text_area.line_height + text_area.line_spacing)
                                        if y >= text_area.cursor_pos[1] - book_area.height // 2:
                                            y = text_area.cursor_pos[1] - book_area.height // 2
                                        if y < 0:
                                            y = 0
                                        book_area.scroll_y = book_area. \
                                            convert_distance_to_scroll(0, y)[1]
                                    except Exception:
                                        return

                                    position = self.app.pos_end_other
                                    for p in range(self.app.chunk_current):
                                        position -= len(chunk_other[p])
                                    try:
                                        text_area_other.select_text(0, position)
                                        y1 = text_area_other.get_cursor_from_index(
                                            text_area_other.selection_to)[1]
                                        text_area_other.cursor = (0, y1)
                                        y = text_area_other.cursor_pos[1] - book_area_other.height + \
                                            y1 * (text_area_other.line_height + text_area_other.line_spacing)
                                        if y >= text_area_other.cursor_pos[1] - book_area_other.height // 2:
                                            y = text_area_other.cursor_pos[1] - book_area_other.height // 2
                                        if y < 0:
                                            y = 0
                                        book_area_other.scroll_y = book_area_other. \
                                            convert_distance_to_scroll(0, y)[1]
                                    except Exception:
                                        return
                                    self.app.option[POSITIONS][self.app.current_select][POSI] = \
                                        str(pos)
                                    self.app.set_sound_pos(pos)
                                    self.app.save_options()
                                    return

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
        self.app.clock_action = Clock.schedule_interval(self.clock_action_time, 0.5)

    def on_text_table_label_right(self, instance, value):
        Clock.schedule_once(self.update_table_label_right, 1)

    def update_table_label_right(self, *args):
        self.app.table_label_right.height = (len(self.app.table_label_right._lines) + 1) * \
                                            (self.app.table_label_right.line_height +
                                             self.app.table_label_right.line_spacing)
