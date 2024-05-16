import Panel
import os
_popups = []

class Popup(Panel.Panel):

    def __init__(self, h, w, y, x, text, title:str=''):
        """
        text: Body text to take up majority of popup
        options: List of MenuOptions
        title: Optional title for popup
        """

        self.text = text
        for v in _popups:
            if v.title == title:
                raise Exception("Duplicate popup")

        # self.options = options

        super().__init__(h, w, y, x, title)

        _popups.append(self)


    def Draw(self):
        self.DrawBorder()

        self.content.addstr(0, 0, self.text)
        self.DrawContent()

    @staticmethod
    def Fullscreen(text, title:str=''):
        w, h = os.get_terminal_size()
        return Popup(h+1, w, 0, 0, text, title)
        
    @staticmethod
    def RemoveLast():
        _popups.pop()

    @staticmethod
    def RemoveByName(name):
        for i, v in enumerate(_popups):
            if v.title == name:
                _popups.pop(i)
                return

    @staticmethod
    def DrawPopups():
        for popup in _popups:
            popup.Draw()

    @staticmethod
    def Overlay(panel, text, title:str=''):
        '''Create a popup directly above an existing panel'''
        h, w, y, x = panel.h, panel.w, panel.y, panel.x
        Popup(h, w, y, x, text, title)
