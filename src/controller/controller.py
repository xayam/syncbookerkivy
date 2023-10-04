

class Controller:

    def __init__(self, app):
        self.app = app
        self.init()

    def init(self):
        with open(self.app.FRAGMENT_BOOK_DIR + self.app.ENG_TXT, mode="r", encoding="UTF-8") as f:
            self.app.eng_txt = f.read()
        with open(self.app.FRAGMENT_BOOK_DIR + self.app.RUS_TXT, mode="r", encoding="UTF-8") as f:
            self.app.rus_txt = f.read()
