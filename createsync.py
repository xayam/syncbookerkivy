from src.model.utils import *
from src.app import App

APP = APP_CREATESYNC

application = App(app={APP_NAME: APP})

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        APP + "Error: " +
        type(e).__name__ + ": " +
        e.__str__()
    )
