from kivy.core.audio import SoundLoader


class Proxy:

    @staticmethod
    def load_text_book(self, receiver, message):
        receiver.text = message

    @staticmethod
    def load_sound(self, receiver, message):
        receiver.sound = SoundLoader.load(message)
        # receiver.table.play_button_click()
