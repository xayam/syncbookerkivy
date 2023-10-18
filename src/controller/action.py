from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from src.model.utils import *


class Action:

    def __init__(self, app):
        self.app = app

    def touch_up_click(self, instance, event):
        self.app.log.debug("Enter to function 'touch_up_click'")
        pos = instance.cursor_index(instance.get_cursor_from_xy(*event.pos))
        if self.app.touch_pos == pos:
            return
        self.app.touch_pos = pos
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        self.app.log.debug(f"touch pos={pos}")
        try:
            if instance == self.app.table_label_left:
                sync = self.app.syncs[self.app.current_select].book1.sync
                chunk = self.app.syncs[self.app.current_select].chunks1
            else:
                sync = self.app.syncs[self.app.current_select].book2.sync
                chunk = self.app.syncs[self.app.current_select].chunks2

            for p in range(self.app.chunk_current):
                pos += len(chunk[p])

            for i in range(len(sync)):
                if sync[i][POS_START] > pos:
                    self.app.log.debug("self.app.sound stop and reload")
                    self.app.sound.stop()
                    self.app.opt[POSITIONS][self.app.current_select][POSI] = sync[i][TIME_START]
                    self.app.set_sound_pos(sync[i][TIME_START])
                    if instance == self.app.table_label_left:
                        self.app.sound = SoundLoader.load(
                            self.app.current_select + self.app.conf.ENG_AUDIO). \
                            load_seek(self.app.get_sound_pos())
                        self.app.opt[POSITIONS][self.app.current_select][AUDIO] = EN
                    else:
                        self.app.sound = SoundLoader.load(
                            self.app.current_select + self.app.conf.RUS_AUDIO). \
                            load_seek(self.app.get_sound_pos())
                        self.app.opt[POSITIONS][self.app.current_select][AUDIO] = RU
                    self.app.conf.save_options()
                    self.app.log.debug(f"create clock Clock.schedule_interval(self.clock_action_time)")
                    self.app.clock_action = Clock.schedule_interval(self.clock_action_time, 0.5)
                    return
        except KeyError:
            self.app.log.debug("WARNING, KeyError (ignored this)")
            self.app.touch_pos = 0
            self.app.container.switch_to(self.app.catalog)
            return

    def clock_action_time(self, _):
        self.app.log.debug("Enter to function 'clock_action_time()'")
        if self.app.opt[POSITIONS][self.app.current_select][AUDIO] == EN:
            text_area = self.app.table_label_left
            book_area = self.app.table_book_left
            text_area_other = self.app.table_label_right
            book_area_other = self.app.table_book_right
            chunk = self.app.syncs[self.app.current_select].chunks1
            chunk_other = self.app.syncs[self.app.current_select].chunks2
            sync = self.app.syncs[self.app.current_select].eng2rus
        else:
            text_area = self.app.table_label_right
            book_area = self.app.table_book_right
            text_area_other = self.app.table_label_left
            book_area_other = self.app.table_book_left
            chunk_other = self.app.syncs[self.app.current_select].chunks1
            chunk = self.app.syncs[self.app.current_select].chunks2
            sync = self.app.syncs[self.app.current_select].rus2eng
        pos = self.app.sound.get_pos()
        if self.app.sound._ffplayer.get_pts() + 0.5 >= \
                self.app.sound._ffplayer.get_metadata()['duration']:
            self.app.player.stop_button_click()
            self.app.opt[POSITIONS][self.app.current_select][POSI] = "0.0"
            self.app.opt[POSITIONS][self.app.current_select][CHUNK] = 0
            self.app.conf.save_options()
            return

        try:
            position = 0
            for current in range(len(self.app.syncs[self.app.current_select].chunks1)):
                position += len(chunk[current])
                if position > sync[str(int(pos))][0]:
                    if current != self.app.chunk_current:
                        self.app.chunk_current = current
                        self.app.opt[POSITIONS][self.app.current_select][CHUNK] = \
                            self.app.chunk_current
                        self.app.conf.save_options()
                        self.app.table_label_left.text = \
                            self.app.syncs[self.app.current_select].chunks1[self.app.chunk_current]
                        self.app.table_label_right.text = \
                            self.app.syncs[self.app.current_select].chunks2[self.app.chunk_current]
                        return
                    else:
                        break

            position = sync[str(int(pos))][0]
            for p in range(self.app.chunk_current):
                position -= len(chunk[p])
            self.app.log.debug(f"position={position}")

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

            position = sync[str(int(pos))][1]
            for p in range(self.app.chunk_current):
                position -= len(chunk_other[p])
            self.app.log.debug(f"position_other={position}")

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
        except KeyError as e:
            self.app.log.debug(f"KeyError: {e.__str__()} (ignore this)")
            return

        self.app.opt[POSITIONS][self.app.current_select][POSI] = str(pos)
        self.app.opt[POSITIONS][self.app.current_select][CHUNK] = self.app.chunk_current
        self.app.set_sound_pos(pos)
        self.app.conf.save_options()
