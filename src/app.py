from src.controller.controller import Controller


class App:
    def __init__(self):
        self.controller = Controller(app=self)
        self.view = self.controller.view
        self.model = self.controller.model

    def run(self):
        self.view.run()
