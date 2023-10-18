from kivy import platform

from src.model.model import Model
from src.controller.controller import Controller
from src.view.view import View


class App(Model, Controller, View):
    def __init__(self):
        Model.__init__(self, app=self)
        Controller.__init__(self, app=self)
        View.__init__(self, app=self)

        self.init()

    @staticmethod
    def init():
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET
                                 # Permission.READ_EXTERNAL_STORAGE,
                                 # Permission.WRITE_EXTERNAL_STORAGE,
                                 # Permission.MEDIA_CONTENT_CONTROL,
                                 # Permission.GLOBAL_SEARCH,
                                 # Permission.READ_MEDIA_AUDIO
                                 ])
