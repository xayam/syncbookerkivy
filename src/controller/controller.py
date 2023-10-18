from .action import Action
from .player import Player


class Controller:

    def __init__(self, app):
        self.app = app

        self.app.player = Player(self.app)
        self.app.action = Action(self.app)
