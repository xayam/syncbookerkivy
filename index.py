from src.model.model import Model
from src.view.web.view import WebView
from src.controller.web.controller import WebController
from src.web import App


model = Model()
view = WebView(model)
controller = WebController(view)
application = App(controller)

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        "WebAppError: " +
        type(e).__name__ + ": " +
        e.__str__()
    )
