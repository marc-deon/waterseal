from MovementModifiers import MOVE_FOOT
from Unit import Unit
import Items

class Barth(Unit):
    def __init__(self):
        super().__init__("Barth", 0, Unit.Kind("Lord", "@", MOVE_FOOT), 25)

        self.AddItem(Items.Bows.IronBow())
        self.AddItem(Items.Swords.IronSword())
        self.AddItem(Items.Axes.HandAxe())
        self.AddItem(Items.Item.Item("Vulnerary"))
        self.AddItem(Items.Item.Item("Vulnerary"))