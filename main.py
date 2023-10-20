import os

os.environ["KIVY_AUDIO"] = "ffpyplayer"

from src.android import App
from src.model.model import Model
from src.view.android.view import AndroidView
from src.controller.android.controller import AndroidController

model = Model()
view = AndroidView(model)
controller = AndroidController(view)
application = App(controller)

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        "AndroidAppError: " +
        type(e).__name__ + ": " +
        e.__str__()
    )
