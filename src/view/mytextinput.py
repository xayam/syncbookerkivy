from kivy.uix.textinput import TextInput


class MyTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = self._lines
