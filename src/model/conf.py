import json
import os

from .utils import *


class Conf:
    OPTIONS_JSON = "options.json"
    DISABLE_MARKER = "img/marker.png"

    GITHUB_SYNCBOOKER = "https://github.com/xayam/syncbooker"
    UPDATE_URL = "https://github.com/xayam/syncbookerkivy/releases/download/SyncBookerKivy_v1.0/"
    # Copy here
    # UPDATE_URL = "https://cloud.mail.ru/public/rdBB/KHvCjQdaT/Android/"
    LIST_FILE = "list.zip"
    LIST_URL = UPDATE_URL + LIST_FILE
    SYNCBOOKER_CHAT = "https://t.me/syncbooker_chat"
    SYNCBOOKER_TELEGRAM = "@syncbooker_chat"
    EMAIL = "xayam@yandex.ru"

    RUS_ANNOT = "rus.annot.txt"
    ENG_ANNOT = "eng.annot.txt"
    RUS_SYNC = "rus.sync.json"
    ENG_SYNC = "eng.sync.json"
    MICRO = "micro2.json"
    ENG2RUS = "eng2rus.json"
    RUS2ENG = "rus2eng.json"
    ENG_FB2 = "eng.fb2"
    RUS_FB2 = "rus.fb2"
    ENG_TXT = "eng.txt"
    RUS_TXT = "rus.txt"
    ENG_AUDIO = "eng.mp3"
    RUS_AUDIO = "rus.mp3"
    COVER = "cover.jpg"
    VALID = "valid"

    BOOK_ENG_SCHEME = [
        ENG_ANNOT,
        ENG_TXT,
        ENG_FB2,
        ENG_AUDIO,
        ENG_SYNC
    ]
    BOOK_RUS_SCHEME = [
        RUS_ANNOT,
        RUS_TXT,
        RUS_FB2,
        RUS_AUDIO,
        RUS_SYNC
    ]
    BOOK_SCHEME = [
        COVER,
        MICRO,
        ENG2RUS,
        RUS2ENG,
        VALID
    ]

    # Icon paths
    ICON_CATALOG = "img/catalog.png"
    ICON_CATALOG_PRESSED = "img/catalog_pressed.png"
    ICON_TABLE = "img/table.png"
    ICON_TABLE_PRESSED = "img/table_pressed.png"
    ICON_PREV = "img/prev.png"
    ICON_PREV_PRESSED = "img/prev_pressed.png"
    ICON_PLAY = "img/play.png"
    ICON_PLAY_PRESSED = "img/play_pressed.png"
    ICON_PAUSE = "img/pause.png"
    ICON_PAUSE_PRESSED = "img/pause_pressed.png"
    ICON_STOP = "img/stop.png"
    ICON_STOP_PRESSED = "img/stop_pressed.png"
    ICON_NEXT = "img/next.png"
    ICON_NEXT_PRESSED = "img/next_pressed.png"

    def __init__(self, app=None):
        self.app = app
        self.app.opt = {
            FG: (0, 0, 0, 1),
            BG: (1, 1, 1, 1),
            SEL: (1, 1, 0, 0.4),
            POSITIONS: {
                i: {
                    POSI: "0.0", AUDIO: EN, CHUNK: 0
                } for i in []
            }
        }
        self.load_options()

    def load_options(self):
        if os.path.exists(self.OPTIONS_JSON):
            with open(self.OPTIONS_JSON, mode="r") as opt:
                self.app.opt = json.load(opt)
        else:
            self.save_options()

    def save_options(self):
        json_string = json.dumps(self.app.opt)
        with open(self.OPTIONS_JSON, mode="w") as opt:
            opt.write(json_string)
