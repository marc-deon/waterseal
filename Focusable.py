# Focusables are components of the game that the player directly interacts with
# e.x. menus, popups, and the main map window. A focusable may have its focus
# stolen from it: this is handled by the Focus struct of the cursor.

class NotImplementError(Exception):
    pass

class Focusable():
    def on_Input(self, focus, inp):
        raise NotImplementedError("on_Input not implemented")

    def on_GetFocus(self):
        raise NotImplementedError("on_GetFocus not implemented")

    def on_LoseFocus(self):
        # raise NotImplementedError("on_LoseFocus not implemented")
        pass

    # Recommended methods to be called from on_Input

    def on_Up(self):
        pass

    def on_Down(self):
        pass

    def on_Left(self):
        pass

    def on_Right(self):
        pass

    def on_Confirm(self):
        pass

    def on_Cancel(self):
        pass

    @property
    def page(self):
        '''pageY, pageX'''
        raise NotImplementedError("page not implemented")