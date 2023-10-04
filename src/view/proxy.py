from kivy.core.audio import SoundLoader


class Proxy:

    @staticmethod
    def load_text_book(self, receiver, message):
        receiver.text = message
