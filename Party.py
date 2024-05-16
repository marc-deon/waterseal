from BattleManager import BattleManager

class Party:

    def __init__(self, name, *units):

        self.name = name # Caelin, Black Fang, whatever
        self.activeUnits = list(units)
        self.reserveUnits = set()
        self.deadUnits = set()
        self.gold = 0
        self.convoy = set()

        BattleManager.instance().parties.append(self)


    def __len__(self):
        return len(self.activeUnits)


    def __getitem__(self, index):
        return list(self.reserveUnits.union(self.activeUnits))[index]


    def AddActive(self, unit):
        self.activeUnits.append(unit)


    def AddReserve(self, unit):
        self.reserveUnits.add(unit)


    def remove(self, unit):
        self.activeUnits.remove(unit)
        self.deadUnits.add(unit)

    # Not commenting this out for any real reason, I just don't think I'll need it?
    # def __setitem__(self, index, value):
    #     self.activeUnits[index] = value
