from kivy.clock import Clock

from src.model.utils import *


class Player:

    def __init__(self, app):
        self.app = app

    def next_chunk(self):
        self.app.model.log.debug("Enter to function 'next_chunk()'")
        self.app.model.chunk_current += 1
        if self.app.model.chunk_current >= len(self.app.model.syncs[self.app.model.current_select].chunks1):
            self.app.model.chunk_current = 0
        Clock.schedule_once(self.delay_run, timeout=0)

    def prev_next(self):
        self.app.model.log.debug("Enter to function 'prev_next()'")
        if not (self.app.model.clock_action is None):
            self.app.model.clock_action.cancel()
        try:
            if self.app.model.opt[POSITIONS][self.app.model.current_select][AUDIO] == EN:
                sync = self.app.model.syncs[self.app.model.current_select].book1.sync
                chunk = self.app.model.syncs[self.app.model.current_select].chunks1
            else:
                sync = self.app.model.syncs[self.app.model.current_select].book2.sync
                chunk = self.app.model.syncs[self.app.model.current_select].chunks2
        except KeyError:
            self.app.model.log.debug("KeyError: self.app.model.opt[POSITIONS][self.app.model.current_select]")
            return
        position = 0
        for p in range(self.app.model.chunk_current):
            position += len(chunk[p])
        for i in range(len(sync)):
            if sync[i][POS_START] > position:
                self.app.model.log.debug(f"Set sound pos, self.app.model.set_sound_pos({sync[i][TIME_START]})")
                self.app.model.log.debug(f"Index i={i}, length of sync={len(sync)}")
                self.app.model.set_sound_pos(sync[i][TIME_START])
                break
        Clock.schedule_once(self.delay_run, timeout=0)

    def delay_run(self, _):
        self.app.model.log.debug("Enter to function 'delay_run()'")
        self.app.table_label_left.text = \
            self.app.model.syncs[self.app.model.current_select].chunks1[self.app.model.chunk_current]
        self.app.table_label_right.text = \
            self.app.model.syncs[self.app.model.current_select].chunks2[self.app.model.chunk_current]

    def prev_button_click(self, _):
        self.app.model.log.debug("Enter to function 'prev_button_click()'")
        self.app.model.chunk_current -= 1
        if self.app.model.chunk_current < 0:
            try:
                self.app.model.chunk_current = len(self.app.model.syncs[self.app.model.current_select].chunks1) - 1
            except KeyError:
                self.app.model.log.debug("KeyError: self.app.model.syncs[self.app.model.current_select].chunks1")
                self.app.model.chunk_current = 0
                return
        self.app.model.log.debug(f"Current page chunk_current={self.app.model.chunk_current}")
        self.prev_next()

    def next_button_click(self, _):
        self.app.model.log.debug("Enter to function 'next_button_click()'")
        self.app.model.chunk_current += 1
        try:
            if self.app.model.chunk_current >= len(self.app.model.syncs[self.app.model.current_select].chunks1):
                self.app.model.chunk_current = 0
        except KeyError:
            self.app.model.chunk_current = 0
            return
        self.app.model.log.debug(f"Current page chunk_current={self.app.model.chunk_current}")
        self.app.model.log.debug(f"Length of chunks1={len(self.app.model.syncs[self.app.model.current_select].chunks1)}")
        self.prev_next()

    def play_button_click(self, _):
        self.app.model.log.debug("Enter to function 'play_button_click()'")
        if not (self.app.model.clock_action is None):
            self.app.model.clock_action.cancel()
        if self.app.model.sound is None:
            return
        self.app.model.sound.stop()
        self.app.table_label_left.text = "\n" * 50
        self.app.table_label_right.text = "\n" * 50
        Clock.schedule_once(self.delay_run, timeout=1)

    def stop_button_click(self, _=None):
        self.app.model.log.debug("Enter to function 'stop_button_click()'")
        if not (self.app.model.clock_action is None):
            self.app.model.clock_action.cancel()
        if not (self.app.model.sound is None):
            self.app.model.set_sound_pos(0.0)
            self.app.model.sound.stop()
            self.app.model.chunk_current = 0
            self.app.model.opt[POSITIONS][self.app.model.current_select][POSI] = "0.0"
            self.app.model.opt[POSITIONS][self.app.model.current_select][CHUNK] = 0
            self.app.model.conf.save_options()

    def pause_button_click(self, _=None):
        self.app.model.log.debug("Enter to function 'pause_button_click()'")
        if not (self.app.model.clock_action is None):
            self.app.model.clock_action.cancel()
        if not (self.app.model.sound is None):
            self.app.model.set_sound_pos(self.app.model.sound.get_pos())
            self.app.model.sound.stop()
            self.app.model.opt[POSITIONS][self.app.model.current_select][POSI] = \
                str(self.app.model.get_sound_pos())
            self.app.model.opt[POSITIONS][self.app.model.current_select][CHUNK] = \
                self.app.model.chunk_current
            self.app.model.conf.save_options()
