from src.controller.proxy import Proxy
from src.model.utils import *


class Player:

    def __init__(self, app):
        self.app = app

    def next_chunk(self):
        self.app.chunk_current += 1
        if self.app.chunk_current >= len(self.app.eng_chunks):
            self.app.chunk_current = 0
        Proxy.load_text_book(self,
                             self.app.table_label_left,
                             self.app.eng_chunks[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.rus_chunks[self.app.chunk_current])

    def prev_next(self):
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        try:
            if self.app.option[POSITIONS][self.app.current_select][AUDIO] == EN:
                sync = self.app.eng_sync
                chunk = self.app.eng_chunks
            else:
                sync = self.app.rus_sync
                chunk = self.app.rus_chunks
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
                             self.app.eng_chunks[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.rus_chunks[self.app.chunk_current])

    def prev_button_click(self, event=None):
        self.app.chunk_current -= 1
        if self.app.chunk_current < 0:
            self.app.chunk_current = len(self.app.eng_chunks) - 1
        self.prev_next()

    def next_button_click(self, event=None):
        self.app.chunk_current += 1
        if self.app.chunk_current >= len(self.app.eng_chunks):
            self.app.chunk_current = 0
        self.app.log(f"chunk_current={self.app.chunk_current}")
        self.app.log(f"len(eng_chunks)={len(self.app.eng_chunks)}")
        self.prev_next()

    def play_button_click(self, event=None):
        self.app.log("enter to function 'play_button_click'")
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
                             self.app.eng_chunks[self.app.chunk_current])
        Proxy.load_text_book(self,
                             self.app.table_label_right,
                             self.app.rus_chunks[self.app.chunk_current])

    def stop_button_click(self, event=None):
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        if not (self.app.sound is None):
            self.app.log("enter to function 'stop_button_click'")
            self.app.set_sound_pos(0.0)
            self.app.sound.stop()
            self.app.chunk_current = 0
            # self.app.table_label_left.text = ""
            # self.app.table_label_right.text = ""

    def pause_button_click(self, event=None):
        if not (self.app.clock_action is None):
            self.app.clock_action.cancel()
        if not (self.app.sound is None):
            self.app.log("enter to function 'pause_button_click'")
            self.app.set_sound_pos(self.app.sound.get_pos())
            self.app.sound.stop()
