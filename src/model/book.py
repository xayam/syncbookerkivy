import json

from src.model.utils import *


class Book:

    def __init__(self, app, path, language):
        self.app = app
        self.path = path
        self.language = language

        self.annot = None
        self.txt = None
        self.sync = None

        self.init()

    def init(self):
        self.app.log.debug("Enter to function 'Book.init()', " + self.language + " book")
        if self.language == EN:
            current = self.app.conf.BOOK_ENG_SCHEME
        else:
            current = self.app.conf.BOOK_RUS_SCHEME
        try:
            with open(self.path + current[ANNOT], mode="r", encoding="UTF-8") as f:
                self.annot = f.read() + "\n\n"
            with open(self.path + current[TXT], mode="r", encoding="UTF-8") as txt:
                self.txt = txt.read()
            with open(self.path + current[SYNC], mode="r", encoding="UTF-8") as f:
                self.sync = json.load(f)
        except Exception as e:
            self.app.log.debug(type(e).__name__ + ": " + e.__str__())
        try:
            self.app.chunk_current = \
                self.app.opt[POSITIONS][self.app.current_select][CHUNK]
        except KeyError as e:
            self.app.log.debug("KeyError: " + e.__str__())
            self.app.chunk_current = 0
