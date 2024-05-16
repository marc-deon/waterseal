import curses
from Panel import Panel, PrintBorder

class ColoredPanel(Panel):
    
    def __init__(self, h, w, y=0, x=0, title=None):
        self.lastBorderColor = curses.color_pair(1)
        super().__init__(h, w, y, x, title)

    def GenerateBorder(self):
        s = PrintBorder(self.w-3, self.h-3, self.title)
        self.border.addstr(0,0, s, curses.color_pair(1))
        self.DrawBorder()

    def Draw(self):
        if self.lastBorderColor != curses.color_pair(1):
            self.GenerateBorder()
        super().Draw()
        self.lastBorderColor = curses.color_pair(1)