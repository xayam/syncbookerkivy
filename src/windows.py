

class App:
    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.view = controller.view


    def run(self):
        self.view.run()
