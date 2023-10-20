from .log import Log
from .conf import Conf
from .storage import Storage
from .utils import *


class Model:

    def __init__(self):
        self.clock_action = None
        self.sound_state = 0
        self.touch_pos = 0
        self.nonstop = False
        self.sound = None
        self.sound_pos = 0.0
        self.chunk_width = 4000
        self.chunk_current = 0
        self.syncs = {}
        self.current_select = None

        self.log = Log()
        self.opt = {
            FG: (0, 0, 0, 1),
            BG: (1, 1, 1, 1),
            SEL: (1, 1, 0, 0.4),
            POSITIONS: {
                i: {
                    POSI: "0.0", AUDIO: EN, CHUNK: 0
                } for i in []
            }
        }
        self.conf = Conf(app=self)
        self.stor = Storage(app=self)
        self.stor.list()

    def set_sound_pos(self, value: float):
        self.sound_pos = value

    def get_sound_pos(self):
        return self.sound_pos
