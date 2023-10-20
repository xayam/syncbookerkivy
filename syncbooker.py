from src.model.model import Model
from src.view.windows.view import WindowsView
from src.controller.windows.controller import WindowsController
from src.android import App


model = Model()
view = WindowsView(model)
controller = WindowsController(view)
application = App(controller)

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        "WindowsAppError: " +
        type(e).__name__ + ": " +
        e.__str__()
    )
