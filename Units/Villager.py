from MovementModifiers import MOVE_FOOT
from Unit import Unit

class Villager(Unit):
    def __init__(self):
        super().__init__("Villager", 3, Unit.Kind("Villager", "v", MOVE_FOOT), 15)