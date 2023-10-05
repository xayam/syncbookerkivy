
class Proxy:

    @staticmethod
    def load_text_book(self, receiver, message):
        if receiver.text != message:
            receiver.text = message
