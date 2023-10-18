import json
import os

from .book import Book
from .utils import *


class Sync:

    def __init__(self, app, current_path):
        self.app = app
        self.app.poses = {}
        self.current_path = current_path

        self.chunks1 = []
        self.chunks2 = []

        self.cover = self.current_path + self.app.conf.BOOK_SCHEME[COVER]
        self.valid = self.current_path + self.app.conf.BOOK_SCHEME[VALID]
        self.micro = []
        self.book1 = None
        self.book2 = None
        self.eng2rus = {}
        self.rus2eng = {}

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

        with open(self.current_path + self.app.conf.BOOK_SCHEME[ENG2RUS],
                  mode="r", encoding="UTF-8") as f:
            self.eng2rus = json.load(f)

        with open(self.current_path + self.app.conf.BOOK_SCHEME[RUS2ENG],
                  mode="r", encoding="UTF-8") as f:
            self.rus2eng = json.load(f)

        self.split_book()
        self.app.log.debug(f"len(self.chunks1)={len(self.chunks1)}")
        self.app.log.debug(f"len(self.chunks2)={len(self.chunks2)}")
        # self.set_markers()

    def split_book(self):
        self.app.log.debug("Enter function split_book()")
        begin2 = 0
        begin1 = 0
        page = 1
        for i in range(len(self.micro)):
            # self.app.log.debug(f"self.micro[i]={self.micro[i]}")
            if self.micro[i][L_POS] > page * self.app.chunk_width:
                text2 = self.book2.txt[begin2:self.micro[i][L_POS]]
                if text2 == "":
                    break
                self.chunks2.append(text2)
                begin2 = self.micro[i][L_POS]
                self.chunks1.append(
                    self.book1.txt[begin1:self.micro[i][R_POS]])
                begin1 = self.micro[i][R_POS]
                page += 1
        self.chunks2.append(
            self.book2.txt[begin2:len(self.book2.txt)])
        self.chunks1.append(
            self.book1.txt[begin1:len(self.book1.txt)])

    # def set_markers(self):
    #     if self.app.opt[POSITIONS][self.app.current_select][AUDIO] == EN:
    #         curr = R_POS
    #         curr_other = L_POS
    #         sync = self.app.syncs[self.app.current_select].book1.sync
    #         sync_other = self.app.syncs[self.app.current_select].book2.sync
    #     else:
    #         curr = L_POS
    #         curr_other = R_POS
    #         sync_other = self.app.syncs[self.app.current_select].book1.sync
    #         sync = self.app.syncs[self.app.current_select].book2.sync
    #
    #     for i in range(len(sync)):
    #         flag = False
    #         pos = sync[i][TIME_START]
    #         self.app.log.debug(f"pos={pos}")
    #         for j in range(len(self.app.syncs[self.app.current_select].micro)):
    #             if self.app.syncs[self.app.current_select].micro[j][curr] > sync[i][POS_START]:
    #                 for z in range(len(sync_other)):
    #                     if self.app.syncs[self.app.current_select].micro[j][curr_other] > \
    #                             sync_other[z][POS_START]:
    #                         self.app.poses[int(pos)] = {
    #                             "other": self.app.syncs[self.app.current_select].micro[j][curr_other],
    #                             "index": sync[i][POS_START]
    #                         }
    #                         flag = True
    #                         break
    #                 if flag:
    #                     break
    #     self.app.log.debug(f"len(self.app.poses)={len(self.app.poses)}")

