import json

from .log import Log
from .conf import Conf
from .storage import Storage
from .utils import *


class Model:

    def __init__(self, app):
        self.app = app
        self.app.clock_action = None
        self.app.sound_state = 0
        self.app.touch_pos = 0
        self.app.nonstop = False
        self.app.sound = None
        self.app.sound_pos = 0.0
        self.app.chunk_width = 4000
        self.app.chunk_current = 0
        self.app.syncs = {}
        self.app.current_select = None

        self.app.log = Log()
        self.app.conf = Conf(self.app)
        self.app.stor = Storage(self.app)
        self.app.stor.list()

    def set_sound_pos(self, value: float):
        self.sound_pos = value

    def get_sound_pos(self):
        return self.sound_pos