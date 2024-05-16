from functools import partial
from Cursor import Cursor
from CursorMode import CursorMode
import Popup, Menu
import os
from Focus import Focus
import Campaign

w = os.get_terminal_size()[0]

logo = """\
░    ░          ░             
░    ░   ░░░    ░    ░░░    ░░
░    ░      ░  ░░░  ░   ░  ░  
░ ░░ ░   ░░░░   ░   ░░░░░  ░  
░░  ░░  ░   ░   ░   ░      ░  
░    ░   ░░░░   ░░   ░░░   ░  

 ░░░░                ░
░       ░░░    ░░░   ░
 ░░░   ░   ░      ░  ░
    ░  ░░░░░   ░░░░  ░
    ░  ░      ░   ░  ░
░░░░    ░░░    ░░░░  ░
"""

# logo = logo.center(w)
lines = logo.split("\n")
logo = "\n".join([line.center(w-4) for line in lines])


def cb_onNew(titlemenu:Menu):
    titlemenu.Remove()
    Popup.Popup.RemoveLast()
    campaign = Campaign.Campaign("campaigns/fe7.json")
    campaign.Next()


def Title():
    titlePop = Popup.Popup.Fullscreen(logo)
    

    m = Menu.Menu(
        False,
        titlePop
    )
    for op in [
        Menu.MenuOption("", None),
        Menu.MenuOption("New", partial(cb_onNew, m)),
        Menu.MenuOption("Continue", None),
        Menu.MenuOption("Resetart Chapter", None),
        Menu.MenuOption("Settings", None),
        Menu.MenuOption("Exit", None)
    ]:
        m.AddOption(op)

    return m

# print(logo)