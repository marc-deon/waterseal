from enum import Flag
class CursorMode(Flag):
    MODE_OFF     = 0 # During enemy turn
    MODE_REGULAR = 1 # Your turn, no unit selected
    MODE_UNIT    = 2 # Choosing where to move
    MODE_MENU    = 3 # Chosing a target, menu options, or in a popup
    MODE_TARGET  = 4 # Chosing who to target/heal/rescue/trade