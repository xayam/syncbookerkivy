import os

from kivy import platform

os.environ["KIVY_AUDIO"] = "ffpyplayer"


class App:
    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.view = controller.view

        self.init()

    def run(self):
        self.view.kivy.run()

    @staticmethod
    def init():
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET
                # Permission.READ_EXTERNAL_STORAGE,
                # Permission.WRITE_EXTERNAL_STORAGE,
                # Permission.MEDIA_CONTENT_CONTROL,
                # Permission.GLOBAL_SEARCH,
                # Permission.READ_MEDIA_AUDIO
            ])
