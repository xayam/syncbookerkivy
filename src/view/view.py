from .mykivy import MyKivy
from .action import Action
from .player import Player


class View(MyKivy):

    def __init__(self, model, **kwargs):
        self.model = model
        print(str(self.model))
        self.model.player = Player(model=self.model)
        self.model.action = Action(model=self.model)
        super().__init__(model=self.model, **kwargs)
