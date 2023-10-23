from .mykivy import MyKivy
from .action import Action
from .player import Player


class View(MyKivy):

    def __init__(self, model, **kwargs):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app
        
        self.controller.player = Player(model=self.model)
        self.controller.action = Action(model=self.model)
        super().__init__(model=self.model, **kwargs)
