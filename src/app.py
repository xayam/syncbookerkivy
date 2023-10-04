from src.model.model import Model
from src.controller.controller import Controller
from src.view.view import View


class App(Model, Controller, View):
    def __init__(self):
        Model.__init__(self, app=self)
        Controller.__init__(self, app=self)
        View.__init__(self, app=self)
