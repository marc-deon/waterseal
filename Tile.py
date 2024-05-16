nameKey = {}

class TileKind:
    def __init__(self, name, symbol, color, defenseMod, avoidMod, description, moveMod,
                 on_UnitEnter=None, on_UnitExit=None,
                 on_TurnStart=None, on_TurnEnd=None,
                 on_Attack=None, on_Activate=None):
        self.name = name
        self.symbol = symbol
        self.color = color
        self.defenseMod = defenseMod
        self.avoidMod = avoidMod
        self.description = description
        self.moveMod = moveMod

        self.on_UnitEnter = on_UnitEnter or (lambda tile, unit : None)
        self.on_UnitExit  = on_UnitExit  or (lambda tile, unit : None)
        self.on_TurnStart = on_TurnStart or (lambda tile : None)
        self.on_TurnEnd   = on_TurnEnd   or (lambda tile : None)
        self.on_Attack    = on_Attack    # Not visible in menu if None
        self.on_Activate  = on_Activate  # Not visible in menu if None

        nameKey[name] = self

class Tile:

    @property
    def defenseMod(self):
        return self.kind.defenseMod

    @property
    def avoidMod(self):
        return self.kind.avoidMod

    @property
    def name(self):
        return self.kind.name

    @property
    def neighbors(self):
        return [
            None if self.y == 0             else self.map[self.x, self.y-1], # North
            None if self.x == self.map.x-1  else self.map[self.x+1, self.y], # East
            None if self.y == self.map.y-1  else self.map[self.x, self.y+1], # South
            None if self.x == 0             else self.map[self.x-1, self.y]  # West
        ]

    def __init__(self, kind:TileKind, m, x, y):
        self.kind = kind
        self.unit = None
        self.map = m
        self.x = x
        self.y = y

    def __str__(self):
        return self.kind.symbol

    def __repr__(self):
        return self.name if self.name else "?"
