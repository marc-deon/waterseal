from dataclasses import dataclass

from CursorMode import CursorMode
from Focusable import Focusable

@dataclass
class Focus:
    target:Focusable
    mode:CursorMode
    x:int = 0
    y:int = 0
    offsetX:int = 0
    offsetY:int = 0

    @property
    def pageY(self):
        return self.target.page[0]
    
    @property
    def pageX(self):
        return self.target.page[1]

    def __str__(self):
        return f"Focus: {self.target}"