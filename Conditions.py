from BattleManager import BattleManager
from Logger import Logger

# TODO: All of these need testing

class Condition:
    
    def Test(self, map:"Map"):
        raise NotImplementedError()

    def cb_onBegin(self):
        pass

    def __init__(self, *args):
        raise NotImplementedError(*args)


class VC_Rout(Condition):

    def Test(self, _:"Map"):
        if len(BattleManager.instance().parties[self.targetPartyIndex]) == 0:
            return True
        return False

    def cb_onBegin(self):
        pass

    def __init__(self, targetPartyIndex):
        self.targetPartyIndex = int(targetPartyIndex)


class VC_Seize(Condition):

    def Test(self, m:"Map"):
        # If a tile is seizable, but not yet seized, this will be false; otherwise null
        if m[self.x, self.y].unit and m[self.x, self.y].unit.partyIndex == 0:
            return True

        return False

    def cb_onBegin(self):
        pass

    def __init__(self, x, y):
            self.x = int(x)
            self.y = int(y)


class VC_Boss(Condition):

    def Test(self, _:"Map"):
        if not self.unit.tile:
            return True
        return False

    def cb_onBegin(self):
        for t in BattleManager.instance().parties:
            matches = list(filter(lambda x: x.name == self.unitName, t))
            if len(matches) > 0:
                self.unit = matches[0]
                return
        raise Exception(f"Could not find unit [{self.unitName}] in any of the parties")

    def __init__(self, unitName):
        self.unitName = unitName

class VC_Survive(Condition):
    
    def Test(self, _:"Map"):
        if BattleManager.instance().turn == self.turnCount:
            return True
        return False

    def cb_onBegin(self):
        pass

    def __init__(self, turnCount):
        self.turnCount = int(turnCount)


# For Lords
class LC_UnitDeath(Condition):

    def Test(self, _:"Map"):
        for u in self.units:
            if u not in BattleManager.instance().parties[u.partyIndex]:
                return True
        return False


    def cb_onBegin(self):
        for unitName in self.names:
            t:list = BattleManager.instance().parties[0]
            # This is a terrible abuse of language
            # Get the 1 Unit whose name matches our unitName
            self.units.add(next(filter(lambda x: x.name == unitName, t)))
        pass


    def __init__(self, *names):
        self.units = set()
        self.names = names


class LC_TurnCount(Condition):

    def Test(self, _:"Map"):
        return BattleManager.instance().turn + 1 >= self.maxTurns


    def cb_onBegin(self):
        pass

    def __init__(self, maxTurns):
        self.maxTurns = int(maxTurns)


class LC_DefendTile(Condition):

    def Test(self, m:"Map"):
        
        # If there's a unit, and it's on the red parties
        if m[self.x, self.y].unit != None and m[self.x, self.y].unit.parties == 1:
            return True

        return False

    def cb_onBegin(self):
        pass

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
