from Menu import Menu, MenuOption

class PreparationsMenu(Menu):
    
    def _units(self):
        pass

    def _items(self):
        pass

    def _shop(self):
        pass

    def _support(self):
        # Don't implement this yet
        pass

    def _map(self):
        pass

    def _system(self):
        pass

    def _begin(self):
        pass

    def __init__(self):
        self.AddOption(MenuOption("Units", self._units))
        self.AddOption(MenuOption("Items", self._items))
        self.AddOption(MenuOption("Shop", self._shop))
        self.AddOption(MenuOption("Support", self._support))
        self.AddOption(MenuOption("Map", self._map))
        self.AddOption(MenuOption("System", self._system))
        self.AddOption(MenuOption("Begin", self._begin))

class PreparationsUnits(Menu):
    pass

class PreparationsSystem(Menu):

    def _save(self):
        pass
    def _load(self):
        pass
    def _settings(self):
        pass

    def __init__(self):
        self.AddOption(MenuOption("Save", self._save))
        self.AddOption(MenuOption("Load", self._load))
        self.AddOption(MenuOption("Settings", self._settings))