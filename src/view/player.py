from kivy.clock import Clock

from src.model.utils import *


class Player:

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller

    def next_chunk(self):
        self.model.log.debug("Enter to function 'next_chunk()'")
        self.model.chunk_current += 1
        if self.model.chunk_current >= len(self.model.syncs[self.model.current_select].chunks1):
            self.model.chunk_current = 0
        Clock.schedule_once(self.delay_run, timeout=0)

    def prev_next(self):
        self.model.log.debug("Enter to function 'prev_next()'")
        if not (self.model.clock_action is None):
            self.model.clock_action.cancel()
        try:
            if self.model.opt[POSITIONS][self.model.current_select][AUDIO] == EN:
                sync = self.model.syncs[self.model.current_select].book1.sync
                chunk = self.model.syncs[self.model.current_select].chunks1
            else:
                sync = self.model.syncs[self.model.current_select].book2.sync
                chunk = self.model.syncs[self.model.current_select].chunks2
        except KeyError:
            self.model.log.debug("KeyError: self.app.opt[POSITIONS][self.app.current_select]")
            return
        position = 0
        for p in range(self.model.chunk_current):
            position += len(chunk[p])
        for i in range(len(sync)):
            if sync[i][POS_START] > position:
                self.model.log.debug(f"Set sound pos, self.app.set_sound_pos({sync[i][TIME_START]})")
                self.model.log.debug(f"Index i={i}, length of sync={len(sync)}")
                self.model.set_sound_pos(sync[i][TIME_START])
                break
        Clock.schedule_once(self.delay_run, timeout=0)

    def delay_run(self, _):
        self.model.log.debug("Enter to function 'delay_run()'")
        self.controller.table_label_left.text = \
            self.model.syncs[self.model.current_select].chunks1[self.model.chunk_current]
        self.controller.table_label_right.text = \
            self.model.syncs[self.model.current_select].chunks2[self.model.chunk_current]

    def prev_button_click(self, _):
        self.model.log.debug("Enter to function 'prev_button_click()'")
        self.model.chunk_current -= 1
        if self.model.chunk_current < 0:
            try:
                self.model.chunk_current = len(self.model.syncs[self.model.current_select].chunks1) - 1
            except KeyError:
                self.model.log.debug("KeyError: self.app.syncs[self.app.current_select].chunks1")
                self.model.chunk_current = 0
                return
        self.model.log.debug(f"Current page chunk_current={self.model.chunk_current}")
        self.prev_next()

    def next_button_click(self, _):
        self.model.log.debug("Enter to function 'next_button_click()'")
        self.model.chunk_current += 1
        try:
            if self.model.chunk_current >= len(self.model.syncs[self.model.current_select].chunks1):
                self.model.chunk_current = 0
        except KeyError:
            self.model.chunk_current = 0
            return
        self.model.log.debug(f"Current page chunk_current={self.model.chunk_current}")
        self.model.log.debug(f"Length of chunks1={len(self.model.syncs[self.model.current_select].chunks1)}")
        self.prev_next()

    def play_button_click(self, _):
        self.model.log.debug("Enter to function 'play_button_click()'")
        if not (self.model.clock_action is None):
            self.model.clock_action.cancel()
        if self.model.sound is None:
            return
        self.model.sound.stop()
        self.controller.table_label_left.text = "\n" * 100
        self.controller.table_label_right.text = "\n" * 100
        Clock.schedule_once(self.delay_run, timeout=1)

    def stop_button_click(self, _=None):
        self.model.log.debug("Enter to function 'stop_button_click()'")
        if not (self.model.clock_action is None):
            self.model.clock_action.cancel()
        if not (self.model.sound is None):
            self.model.set_sound_pos(0.0)
            self.model.sound.stop()
            self.model.chunk_current = 0
            self.model.opt[POSITIONS][self.model.current_select][POSI] = "0.0"
            self.model.opt[POSITIONS][self.model.current_select][CHUNK] = 0
            self.model.conf.save_options()

    def pause_button_click(self, _=None):
        self.model.log.debug("Enter to function 'pause_button_click()'")
        if not (self.model.clock_action is None):
            self.model.clock_action.cancel()
        if not (self.model.sound is None):
            self.model.set_sound_pos(self.model.sound.get_pos())
            self.model.sound.stop()
            self.model.opt[POSITIONS][self.model.current_select][POSI] = \
                str(self.model.get_sound_pos())
            self.model.opt[POSITIONS][self.model.current_select][CHUNK] = \
                self.model.chunk_current
            self.model.conf.save_options()
