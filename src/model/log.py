from src.model.utils import DEBUG


class Log:

    def __init__(self):
        pass

    def log(self, message):
        if DEBUG:
            print("DEBUG: " + message)
