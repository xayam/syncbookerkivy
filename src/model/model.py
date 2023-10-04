import json

from .config import Config


class Model(Config):

    def __init__(self, app):
        self.app = app
        self.sound_pos = 0.0
        self.sound = None
        self.app.current_dir = self.app.FRAGMENT_BOOK_DIR
        Config.__init__(self, self.app)

    def set_sound_pos(self, value: float):
        self.sound_pos = value

    def get_sound_pos(self):
        return self.sound_pos

    def pre_load(self):
        with open(self.app.current_dir + self.RUS_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation = f.read() + "\n\n"
        with open(self.app.current_dir + self.ENG_ANNOT, mode="r", encoding="UTF-8") as f:
            self.app.annotation += f.read()

        with open(self.app.current_dir + self.ENG_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.eng_sync = json.load(f)
        with open(self.app.current_dir + self.RUS_SYNC, encoding="UTF-8", mode="r") as f:
            self.app.rus_sync = json.load(f)

        with open(self.app.current_dir + self.MICRO_JSON, encoding="UTF-8", mode="r") as f:
            self.app.micro = json.load(f)

        with open(self.app.current_dir + self.ENG_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.eng_book = txt.read()
            self.app.book = self.app.eng_book
        with open(self.app.current_dir + self.RUS_TXT, mode="r", encoding="UTF-8") as txt:
            self.app.rus_book = txt.read()
            self.app.book_other = self.app.rus_book
