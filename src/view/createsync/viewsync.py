from src.view.createsync.mykivysync import MyKivySync


class ViewCreateSync(MyKivySync):

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        super().__init__(model=self.model)
