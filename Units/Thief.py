from MovementModifiers import MOVE_FOOT
from Unit import Unit
import Items

class Thief(Unit):
    def __init__(self):
        super().__init__("Thief", 2, Unit.Kind("Thief", "t", MOVE_FOOT), 15)

        self.AddItem(Items.Item.Item("Lockpick"))
        self.AddItem(Items.Bows.IronBow())