from src.controller.controller import Controller


class App:
    def __init__(self):
        self.controller = Controller(app=self)

    def run(self):
        self.controller.view.run()
