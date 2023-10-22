import src.controller.init

from src.model.model import Model
from src.view.view import View


class Controller(Model, View):

    def __init__(self, app):
        self.app = app

        self.model = Model.__init__(self, app=self)
        self.view = View.__init__(self, app=self.model)

        self.init()

    def init(self):
        pass
        # if self.app.android:
        #     from android.permissions import request_permissions, Permission
        #     request_permissions([
        #         Permission.INTERNET
        #         # Permission.READ_EXTERNAL_STORAGE,
        #         # Permission.WRITE_EXTERNAL_STORAGE,
        #         # Permission.MEDIA_CONTENT_CONTROL,
        #         # Permission.GLOBAL_SEARCH,
        #         # Permission.READ_MEDIA_AUDIO
        #     ])
