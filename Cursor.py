from Focus import Focus
from Focusable import Focusable
import Menu

class Cursor:

    _instance = None

    @staticmethod
    def instance() -> "Cursor":
        return Cursor._instance

    def __init__(self):
        Cursor._instance = self
        self.focuses = []

    def Input(self, input):
        self.focuses[-1].target.on_Input(self.focuses[-1], input)

    @property
    def symbol(self):
        # Return differently based on mode?
        return "X"

    @property
    def top(self):
        return self.focuses[-1]

    # Get the focus with target of given type closest to the top of the stack
    def GetTopOfType(self, type):
        return next((f for f in self.focuses[::-1] if isinstance(f.target, type)), None)

    def PushFocus(self, focus:Focus):
        assert type(focus) == Focus
        focus.cursor = self
        if self.focuses:
            self.focuses[-1].target.on_LoseFocus()
        self.focuses.append(focus)

    def PopFocus(self):
        foc = self.focuses.pop()
        foc.target.on_LoseFocus()
        return foc
