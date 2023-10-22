from .mykivy import MyKivy

from .action import Action
from .player import Player
from .mykivy import MyKivy


class View(MyKivy):

    def __init__(self, app, **kwargs):
        self.app = app
        self.player = Player(app=self)
        self.action = Action(app=self)
        super().__init__(app=self, **kwargs)
