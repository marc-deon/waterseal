from Logger import Logger
from Cursor import Cursor

class BattleManager:

    _instance = None

    # TODO: Static properties?
    @staticmethod
    def instance() -> "BattleManager":
        if BattleManager._instance == None:
            BattleManager([])
        return BattleManager._instance


    def __init__(self, parties:list=[]):
        self.parties = parties
        self.currentParty = 0
        self.turn = 0
        BattleManager._instance = self
        for party in parties:
            for unit in party:
                unit.moved = False


    def EndTurn(self):
        from Map import Map
        instance = Map.instance()

        for tile in instance:
            if tile and tile.kind.on_TurnEnd:
                tile.kind.on_TurnEnd(tile)

        result = instance.CheckConditions()

        if result != 0:
            return

        for unit in self.parties[self.currentParty]:
            unit.moved = False
        self.currentParty = (self.currentParty + 1) % len(self.parties)

        Logger.Log(f"Begin {BattleManager.instance().parties[self.currentParty].name} Turn")
        if self.currentParty == 0:
            self.turn+=1
        else:
            self.DoAiTurn()

        for tile in instance:
            if tile.kind.on_TurnStart:
                tile.kind.on_TurnStart(tile)


    def DoAiTurn(self):
        self.EndTurn()