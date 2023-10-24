from kivy.uix.textinput import TextInput


class MyTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(
            padding=(10, 10),
            focus=False,
            use_bubble=False,
            use_handles=False,
            **kwargs
        )
        self.is_focusable = False
        self.lines = self._lines
