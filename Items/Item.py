from dataclasses import dataclass

@dataclass
class Item:
    name:str

@dataclass(repr=False)
class Weapon(Item):
    # Non-defaults
    name:str
    rank:str
    weight:int
    might:int
    hit:int
    crit:int
    durability:int

    # Semi-defaults
    useRange:tuple

    # Defaults
    kind:str
    targetSame:bool = False # Target allies
    targetOther:bool = True # Target enemies
    cost:int = 0
    description:str = "No description"
    magical:bool=False

    def __post_init__(self):
        self.maxDurability = self.durability
    
    def __str__(self):
        return f"{self.name} {self.useRange}"

@dataclass
class Staff(Weapon):
    kind:str = "Staff"
    targetSame:bool = True
    targetOther:bool = False
    magical:bool=True

@dataclass
class Dark(Weapon):
    kind:str = "Dark"
    useRange:tuple = (1,2)
    magical:bool=True

@dataclass
class Light(Weapon):
    kind:str = "Light"
    useRange:tuple = (1,2)
    magical:bool=True

@dataclass
class Anima(Weapon):
    kind:str = "Anima"
    useRange:tuple = (1,2)
    magical:bool=True

@dataclass
class Sword(Weapon):
    kind:str = "Sword"
    useRange:tuple = (1,1)

@dataclass
class Lance(Weapon):
    kind:str = "Lance"
    useRange:tuple = (1,1)

@dataclass
class Axe(Weapon):
    kind:str = "Axe"
    useRange:tuple = (1,1)

@dataclass
class Bow(Weapon):
    kind:str = "Bow"
    useRange:tuple = (2,2)
