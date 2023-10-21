import json

from .utils import *


class Conf:

    NAME = "SyncBooker"

    OPTIONS = "options.json"
    CONFIG = "config.sh"

    LICENSE = "LICENSE"
    CASES_HTML = os.getcwd() + "/cases.html"
    README_MD = os.getcwd() + "/README.md"
    FAQ_HTML = os.getcwd() + "/faq.html"
    DONATE = "https://yoomoney.ru/to/410014160363421"
    ICON_ICO = "res/img/icon.ico"
    ICON_PNG = "res/img/icon.png"

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
    ENG_MP3 = "eng.mp3"
    RUS_MP3 = "rus.mp3"
    COVER = "cover.jpg"
    VALID = "valid"

    RUS_ORIG = "rus.orig.html"
    ENG_ORIG = "eng.orig.html"
    RUS_MAP = "rus.map.json"
    ENG_MAP = "eng.map.json"
    RUS_WAV = "rus.wav"
    ENG_WAV = "eng.wav"
    RUS_FLAC = "rus.flac"
    ENG_FLAC = "eng.flac"

    BOOK_ENG_SCHEME = [
        ENG_ANNOT,
        ENG_TXT,
        ENG_FB2,
        ENG_MP3,
        ENG_SYNC
    ]
    BOOK_RUS_SCHEME = [
        RUS_ANNOT,
        RUS_TXT,
        RUS_FB2,
        RUS_MP3,
        RUS_SYNC
    ]
    BOOK_SCHEME = [
        COVER,
        MICRO,
        ENG2RUS,
        RUS2ENG,
        VALID
    ]

    DISABLE_MARKER = "res/img/marker.png"

    # Icon paths
    ICON_CATALOG = "res/img/catalog.png"
    ICON_CATALOG_PRESSED = "res/img/catalog_pressed.png"
    ICON_TABLE = "res/img/table.png"
    ICON_TABLE_PRESSED = "res/img/table_pressed.png"
    ICON_OPTIONS = "res/img/options.png"
    ICON_OPTIONS_PRESSED = "res/img/options_pressed.png"
    ICON_PREV = "res/img/prev.png"
    ICON_PREV_PRESSED = "res/img/prev_pressed.png"
    ICON_PLAY = "res/img/play.png"
    ICON_PLAY_PRESSED = "res/img/play_pressed.png"
    ICON_PAUSE = "res/img/pause.png"
    ICON_PAUSE_PRESSED = "res/img/pause_pressed.png"
    ICON_STOP = "res/img/stop.png"
    ICON_STOP_PRESSED = "res/img/stop_pressed.png"
    ICON_NEXT = "res/img/next.png"
    ICON_NEXT_PRESSED = "res/img/next_pressed.png"

    def __init__(self, app):
        self.app = app
        self.load_options()
        self.set_locale(self.app.opt[LOCALE])

    def set_locale(self, locale):
        self.locale = locale

    def load_options(self):
        if os.path.exists(self.OPTIONS):
            with open(self.OPTIONS, mode="r") as opt:
                self.app.opt = json.load(opt)
        else:
            self.save_options()

    def save_options(self):
        json_string = json.dumps(self.app.opt)
        with open(self.OPTIONS, mode="w") as opt:
            opt.write(json_string)
