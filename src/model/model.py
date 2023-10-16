import json

from .config import Config
from .utils import *


class Model(Config):

    def __init__(self, app):
        self.app = app
        self.sound = None
        self.sound_pos = 0.0
        self.chunk_width = 4000
        self.chunk_current = 0
        self.eng_chunks = []
        self.rus_chunks = []
        self.current_select = None
        Config.__init__(self, self.app)

    def set_sound_pos(self, value: float):
        self.sound_pos = value

    def get_sound_pos(self):
        return self.sound_pos

    def pre_load(self):
        with open(self.current_select + self.RUS_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation = f.read() + "\n\n"
        with open(self.current_select + self.ENG_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation += f.read()

        with open(self.current_select + self.ENG_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.eng_sync = json.load(f)
        with open(self.current_select + self.RUS_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.rus_sync = json.load(f)

        with open(self.current_select + self.MICRO_JSON, encoding="UTF-8", mode="r") as f:
            self.app.micro = json.load(f)

        with open(self.current_select + self.ENG_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.eng_book = txt.read()
            self.app.book = self.app.eng_book
        with open(self.current_select + self.RUS_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.rus_book = txt.read()
            self.app.book_other = self.app.rus_book

        self.chunk_current = 0
        self.eng_chunks = []
        self.rus_chunks = []
        self.split_book()

    def split_book(self):
        rus_begin = 0
        eng_begin = 0
        page = 1
        for i in range(len(self.app.micro)):
            for j in range(len(self.app.micro[i])):
                if self.app.micro[i][j][L_POS] > page * self.chunk_width:
                    rus_text = self.app.rus_book[rus_begin:self.app.micro[i][j][L_POS]]
                    if rus_text == "":
                        break
                    self.rus_chunks.append(rus_text)
                    rus_begin = self.app.micro[i][j][L_POS]
                    self.eng_chunks.append(
                        self.app.eng_book[eng_begin:self.app.micro[i][j][R_POS]])
                    eng_begin = self.app.micro[i][j][R_POS]
                    page += 1
                    break
        self.rus_chunks.append(
            self.app.rus_book[rus_begin:len(self.app.rus_book)])
        self.eng_chunks.append(
            self.app.eng_book[eng_begin:len(self.app.eng_book)])
