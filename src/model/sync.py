import json
import os

from .book import Book
from .utils import *


class Sync:

    def __init__(self, app, current_path):
        self.app = app
        self.current_path = current_path

        self.chunks1 = []
        self.chunks2 = []

        self.cover = self.current_path + self.app.conf.BOOK_SCHEME[COVER]
        self.valid = self.current_path + self.app.conf.BOOK_SCHEME[VALID]
        self.micro = None
        self.book1 = None
        self.book2 = None

    def loads(self):
        self.app.log.debug("Enter function Sync.loads()")
        if not os.path.exists(self.valid):
            path = self.app.conf.UPDATE_URL + "/" + self.current_path[5:-1] + ".zip"
            self.app.log.debug(f"Try download '{path}'")
            self.app.stor.storage_book(path)
        self.book1 = Book(app=self.app, path=self.current_path, language=EN)
        self.book2 = Book(app=self.app, path=self.current_path, language=RU)
        with open(self.current_path + self.app.conf.BOOK_SCHEME[MICRO_JSON],
                  mode="r", encoding="UTF-8") as f:
            self.micro = json.load(f)
        self.split_book()

    def split_book(self):
        self.app.log.debug("Enter function split_book()")
        begin2 = 0
        begin1 = 0
        page = 1
        for i in range(len(self.micro)):
            for j in range(len(self.micro[i])):
                if self.micro[i][j][L_POS] > page * self.app.chunk_width:
                    text2 = self.book2.txt[begin2:self.micro[i][j][L_POS]]
                    if text2 == "":
                        break
                    self.chunks2.append(text2)
                    begin2 = self.micro[i][j][L_POS]
                    self.chunks1.append(
                        self.book1.txt[begin1:self.micro[i][j][R_POS]])
                    begin1 = self.micro[i][j][R_POS]
                    page += 1
                    break
        self.chunks2.append(
            self.book2.txt[begin2:len(self.book2.txt)])
        self.chunks1.append(
            self.book1.txt[begin1:len(self.book1.txt)])
