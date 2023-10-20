from model.model import Model
from controller.controller import Controller
from view.view import View


class Application(Model, Controller, View):
    NAME = 'SyncBooker'
    VERSION = '4.0alpha'

    def __init__(self, debug=False):
        if not debug:
            Model.__init__(self, app=self)
            Controller.__init__(self, app=self)
            View.__init__(self, app=self)
