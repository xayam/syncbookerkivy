from src.controller.proxy import Proxy
from src.model.utils import *

from .mysound import *

class Player:

    def __init__(self, app):
        self.app = app

    def next_chunk(self):
        self.app.chunk_current += 1
        if self.app.chunk_current >= len(self.app.syncs[self.app.current_select].chunks1):
            self.app.chunk_current = 0
        Proxy.load_text_book(self,
                             self.app.table_label_left,
                             self.app.syncs[self.app.current_select].
                             chunks1[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.syncs[self.app.current_select].
                             chunks2[self.app.chunk_current])

    def prev_next(self):
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        try:
            if self.app.opt[POSITIONS][self.app.current_select][AUDIO] == EN:
                sync = self.app.syncs[self.app.current_select].book1.sync
                chunk = self.app.syncs[self.app.current_select].chunks1
            else:
                sync = self.app.syncs[self.app.current_select].book2.sync
                chunk = self.app.syncs[self.app.current_select].chunks2
        except KeyError:
            return
        position = 0
        for p in range(self.app.chunk_current):
            position += len(chunk[p])
        for z in range(len(sync)):
            if sync[z][POS_START] > position:
                self.app.set_sound_pos(sync[z][TIME_START])
                break
        Proxy.load_text_book(self,
                             self.app.table_label_left,
                             self.app.syncs[self.app.current_select].
                             chunks1[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.syncs[self.app.current_select].
                             chunks2[self.app.chunk_current])

    def prev_button_click(self, event=None):
        self.app.chunk_current -= 1
        if self.app.chunk_current < 0:
            self.app.chunk_current = len(self.app.syncs[self.app.current_select].chunks1) - 1
        self.prev_next()

    def next_button_click(self, event=None):
        self.app.log.debug("Enter to function 'next_button_click'")
        self.app.chunk_current += 1
        if self.app.chunk_current >= len(self.app.syncs[self.app.current_select].chunks1):
            self.app.chunk_current = 0
        self.app.log.debug(f"chunk_current={self.app.chunk_current}")
        self.app.log.debug(f"len(eng_chunks)={len(self.app.syncs[self.app.current_select].chunks1)}")
        self.prev_next()

    def play_button_click(self, event=None):
        self.app.log.debug("Enter to function 'play_button_click'")
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        if self.app.sound is None:
            return
        self.app.sound.stop()
        Proxy.load_text_book(self,
                             self.app.table_label_left, "")
        Proxy.load_text_book(self,
                             self.app.table_label_right, "")
        Proxy.load_text_book(self,
                             self.app.table_label_left,
                             self.app.syncs[self.app.current_select].
                             chunks1[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.syncs[self.app.current_select].
                             chunks2[self.app.chunk_current])

    def stop_button_click(self, event=None):
        self.app.log.debug("Enter to function 'stop_button_click'")
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        if not (self.app.sound is None):
            self.app.set_sound_pos(0.0)
            self.app.sound.stop()
            self.app.chunk_current = 0
            self.app.opt[POSITIONS][self.app.current_select][POSI] = "0.0"
            self.app.opt[POSITIONS][self.app.current_select][CHUNK] = 0
            self.app.conf.save_options()

    def pause_button_click(self, event=None):
        self.app.log.debug("Enter to function 'pause_button_click'")
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        if not (self.app.sound is None):
            self.app.set_sound_pos(self.app.sound.get_pos())
            self.app.sound.stop()
            self.app.opt[POSITIONS][self.app.current_select][POSI] = \
                str(self.app.get_sound_pos())
            self.app.opt[POSITIONS][self.app.current_select][CHUNK] = \
                self.app.chunk_current
            self.app.conf.save_options()
