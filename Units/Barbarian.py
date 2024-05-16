from MovementModifiers import MOVE_FOOT
from Unit import Unit
from Items import Axes

class Barbarian(Unit):
    def __init__(self):
        super().__init__("Barbarian", 1, Unit.Kind("Barbarian", "b", MOVE_FOOT), 20)

        self.AddItem(Axes.IronAxe())
        