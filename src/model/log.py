
class Log:

    def __init__(self, debug=False):
        self.debug = debug

    def log(self, message):
        if self.debug:
            print("DEBUG: " + message)
