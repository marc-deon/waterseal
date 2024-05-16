from MovementModifiers import MOVE_FOOT, MOVE_HORSE
from Unit import Unit
from Items import Lances

class Bagen(Unit):
    def __init__(self):
        super().__init__("Bagen", 0, Unit.Kind("Paladin", "P", MOVE_HORSE), 40)

        self.AddItem(Lances.SilverLance())