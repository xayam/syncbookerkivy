from .action import Action
from .player import Player
from ..view import View
from .mykivy import MyKivy


class AndroidView(View):

    def __init__(self, *args):
        super().__init__(*args)
        self.player = Player(app=self)
        self.action = Action(app=self)
        self.kivy = MyKivy(app=self)
