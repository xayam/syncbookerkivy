import json
import os

from .utils import *
from .log import Log


class Config(Log):
    OPTIONS_JSON = "options.json"
    DISABLE_MARKER = "img/marker.png"
    # FRAGMENT_BOOK_DIR = "data/Kafka_Franz_-_The_Metamorphosis/"

    GITHUB_SYNCBOOKER = "https://github.com/xayam/syncbooker"
    UPDATE_URL = "https://cloud.mail.ru/public/rdBB/KHvCjQdaT/Android/"
    LIST_FILE = "list.zip"
    LIST_URL = UPDATE_URL + LIST_FILE
    SYNCBOOKER_CHAT = "https://t.me/syncbooker_chat"
    SYNCBOOKER_TELEGRAM = "@syncbooker_chat"
    EMAIL = "xayam@yandex.ru"

    RUS_ANNOT = "rus.annot.txt"
    ENG_ANNOT = "eng.annot.txt"
    RUS_SYNC = "rus.sync.json"
    ENG_SYNC = "eng.sync.json"
    MICRO_JSON = "micro.json"
    ENG_FB2 = "eng.fb2"
    RUS_FB2 = "rus.fb2"
    ENG_TXT = "eng.txt"
    RUS_TXT = "rus.txt"
    ENG_AUDIO = "eng.mp3"
    RUS_AUDIO = "rus.mp3"
    COVER = "cover.jpg"
    VALID = "valid"

    RUS_ORIG = "rus.orig.html"
    ENG_ORIG = "eng.orig.html"
    RUS_MAP = "rus.map.json"
    ENG_MAP = "eng.map.json"
    RUS_WAV = "rus.wav"
    ENG_WAV = "eng.wav"

    BOOK_SCHEME = [
        RUS_ANNOT, ENG_ANNOT, RUS_SYNC,
        ENG_SYNC, MICRO_JSON, ENG_FB2,
        RUS_FB2, ENG_TXT, RUS_TXT,
        ENG_AUDIO, RUS_AUDIO, COVER, VALID
    ]

    def __init__(self, app=None):
        self.app = app
        super(Config, self).__init__()
        self.books = []
        self.app.option = {FG: (0, 0, 0, 1),
                           BG: (1, 1, 1, 1),
                           SEL: (1, 1, 0, 0.4),
                           POSITIONS: {i: {POSI: "0.0", AUDIO: EN} for i in self.books}
                           }
        self.load_options()
        self.save_options()

    def load_options(self):
        if os.path.exists(self.OPTIONS_JSON):
            with open(self.OPTIONS_JSON, mode="r") as opt:
                self.app.option = json.load(opt)

    def save_options(self):
        json_string = json.dumps(self.app.option)
        with open(self.OPTIONS_JSON, mode="w") as opt:
            opt.write(json_string)

# if platform == 'android':
#     from android.permissions import request_permissions, Permission
#     request_permissions([Permission.INTERNET,
#                          Permission.READ_EXTERNAL_STORAGE,
#                          Permission.WRITE_EXTERNAL_STORAGE,
#                          Permission.MEDIA_CONTENT_CONTROL,
#                          # Permission.READ_HOME_APP_SEARCH_DATA,
#                          Permission.GLOBAL_SEARCH,
#                          # Permission.READ_ASSISTANT_APP_SEARCH_DATA
#                          Permission.READ_MEDIA_AUDIO
#                          ])
