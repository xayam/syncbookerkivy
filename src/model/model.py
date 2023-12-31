from .log import Log
from .conf import Conf
from .storage import Storage
from .utils import *


class Model:

    def __init__(self, controller=None):
        self.controller = controller
        self.app = None if self.controller is None else controller.app

        self.opt = None
        self.clock_action = None
        self.count_action = 0
        self.pts_action = 0
        self.sound_state = 0
        self.touch_pos = 0
        self.nonstop = False
        self.sound = None
        self.sound_pos = 0.0
        self.chunk_width = 4000 if ANDROID else 20000
        self.chunk_current = 0
        self.syncs = {}
        self.current_select = None
        self.log = Log()
        self.reset_opt()
        self.conf = Conf(model=self)
        self.stor = Storage(model=self)
        self.stor.list()

    def set_sound_pos(self, value: float):
        self.sound_pos = value

    def get_sound_pos(self):
        return self.sound_pos

    def reset_opt(self):
        self.opt = {
            DHT: False,
            PRELOAD: False,
            LOCALE: EN,
            FG: (0, 0, 0, 1),
            BG: (1, 1, 1, 1),
            SEL: (1, 1, 0, 0.4),
            FONT: "Arial",
            FONTSIZESCALE: "1.0",
            SPEED: "1.0",
            POSITIONS: {
                path: {
                    POSI: "0.0", AUDIO: EN, CHUNK: 0
                } for path in []
            }
        }
