from src.controller.controller import Controller


class App:
    def __init__(self, app):
        self.app = app
        self.controller = Controller(app=self.app)
        self.view = self.controller.view
        self.model = self.controller.model

    def run(self):
        self.view.run()
