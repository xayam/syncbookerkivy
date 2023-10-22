from src.controller.controller import Controller


class App:
    def __init__(self):
        self.controller = Controller()
        self.view = self.controller.view

    def run(self):
        self.view.run()
