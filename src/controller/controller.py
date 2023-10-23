from src.model.model import Model
from src.model.utils import *
from src.view.view import ViewSyncBooker
from src.view.createsync.viewsync import ViewCreateSync


class Controller:

    def __init__(self, app):

        self.app = app
        self.model = Model(controller=self)
        if self.app[APP_NAME] == APP_CREATESYNC:
            self.view = ViewCreateSync(model=self.model)
        else:
            self.view = ViewSyncBooker(model=self.model)

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
