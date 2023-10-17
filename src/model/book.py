import json

from src.model.utils import *


class Book:

    def __init__(self, app, path, language):
        self.app = app
        self.path = path
        self.language = language
        self.pre_load()

    def pre_load(self):
        if self.language == EN:
            current = self.app.conf.BOOK_ENG_SCHEME
        else:
            current = self.app.conf.BOOK_RUS_SCHEME

        with open(self.path + current[ANNOT], mode="r", encoding="UTF-8") as f:
            self.annot = f.read() + "\n\n"
        with open(self.path + current[TXT], mode="r", encoding="UTF-8") as txt:
            self.txt = txt.read()
        with open(self.path + current[SYNC], mode="r", encoding="UTF-8") as f:
            self.sync = json.load(f)

        self.chunk_current = 0
        self.eng_chunks = []
        self.rus_chunks = []
