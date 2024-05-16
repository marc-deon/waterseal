from dataclasses import dataclass
from Items.Item import Axe

@dataclass
class IronAxe(Axe):
    name:str = "Iron Axe"
    rank:str = 'E'
    weight:int = 10
    might:int = 8
    hit:int = 75
    crit:int = 0
    durability:int = 45
    cost:int = 270
    description:int = "–"
@dataclass
class EmblemAxe(Axe):
    name:str = "Emblem Axe"
    rank:str = 'E'
    weight:int = 10
    might:int = 8
    hit:int = 75
    crit:int = 0
    durability:int = 60
    cost:int = 0
    description:int =  "(Mario Kart: Double Dash!! bonus disk only)"
@dataclass
class SteelAxe(Axe):
    name:str = "Steel Axe"
    rank:str = 'E'
    weight:int = 15
    might:int = 11
    hit:int = 65
    crit:int = 0
    durability:int = 30
    cost:int = 360
    description:int = "–"
@dataclass
class DevilAxe(Axe):
    name:str = "Devil Axe"
    rank:str = 'E'
    weight:int = 18
    might:int = 18
    hit:int = 55
    crit:int = 0
    durability:int = 20
    cost:int = 900
    description:int = "May damage user"
@dataclass
class PoisonAxe(Axe):
    name:str = "Poison Axe"
    rank:str = 'D'
    weight:int = 10
    might:int = 4
    hit:int = 60
    crit:int = 0
    durability:int = 40
    cost:int = 0
    description:int = "Poisons on contact"
@dataclass
class Halberd(Axe):
    name:str = "Halberd"
    rank:str = 'D'
    weight:int = 15
    might:int = 10
    hit:int = 60
    crit:int = 0
    durability:int = 18
    cost:int = 810
    description:int = "Effective against horseback units"
@dataclass
class Hammer(Axe):
    name:str = "Hammer"
    rank:str = 'D'
    weight:int = 15
    might:int = 10
    hit:int = 55
    crit:int = 0
    durability:int = 20
    cost:int = 800
    description:int = "Effective against armoured units"
@dataclass
class DragonAxe(Axe):
    name:str = "Dragon Axe"
    rank:str = 'C'
    weight:int = 11
    might:int = 10
    hit:int = 60
    crit:int = 0
    durability:int = 40
    cost:int = 6000
    description:int = "Effective against dragon units (Mario Kart: Double Dash!! bonus disk only)"
@dataclass
class KillerAxe(Axe):
    name:str = "Killer Axe"
    rank:str = 'C'
    weight:int = 11
    might:int = 11
    hit:int = 65
    crit:int = 30
    durability:int = 20
    cost:int = 1000
    description:int = "–"
@dataclass
class Swordreaver(Axe):
    name:str = "Swordreaver"
    rank:str = 'C'
    weight:int = 13
    might:int = 11
    hit:int = 65
    crit:int = 5
    durability:int = 15
    cost:int = 2100
    description:int = "Good against swords, bad against lances"
@dataclass
class Swordslayer(Axe):
    name:str = "Swordslayer"
    rank:str = 'C'
    weight:int = 13
    might:int = 11
    hit:int = 80
    crit:int = 5
    durability:int = 20
    cost:int = 2000
    description:int = "Good against swords, bad against lances, effective against Mercenaries, Heroes, Myrmidons, Swordmasters and Blade Lords"
@dataclass
class BraveAxe(Axe):
    name:str = "Brave Axe"
    rank:str = 'B'
    weight:int = 16
    might:int = 10
    hit:int = 65
    crit:int = 0
    durability:int = 30
    cost:int = 2250
    description:int = "Allows 2 consecutive hits"
@dataclass
class SilverAxe(Axe):
    name:str = "Silver Axe"
    rank:str = 'A'
    weight:int = 12
    might:int = 15
    hit:int = 70
    crit:int = 0
    durability:int = 20
    cost:int = 1000
    description:int = "–"
@dataclass
class Basilikos(Axe):
    name:str = "Basilikos"
    rank:str = 'S'
    weight:int = 13
    might:int = 22
    hit:int = 75
    crit:int = 0
    durability:int = 25
    cost:int = 15000
    description:int = "–"
@dataclass
class WolfBeil(Axe):
    name:str = "WolfBeil"
    rank:str = 'X'
    weight:int = 10
    might:int = 10
    hit:int = 75
    crit:int = 5
    durability:int = 30
    cost:int = 6000
    description:int = "Hector only, effective against armoured and horseback units"
@dataclass
class Armads(Axe):
    name:str = "Armads"
    rank:str = 'X'
    weight:int = 18
    might:int = 18
    hit:int = 85
    crit:int = 0
    durability:int = 25
    cost:int = 0
    description:int = "Hector only, Def +5, effective against dragon units"
@dataclass
class Tomahawk(Axe):
    name:str = "Tomahawk"
    rank:str = 'A'
    weight:int = 14
    might:int = 13
    hit:int = 65
    crit:int = 0
    durability:int = 15
    useRange:tuple = (1,2)
    cost:int = 3000
    description:int = "–"
@dataclass
class HandAxe(Axe):
    name:str = "Hand Axe"
    rank:str = 'E'
    weight:int = 12
    might:int = 7
    hit:int = 60
    crit:int = 0
    durability:int = 20
    useRange:tuple = (1,2)
    cost:int = 300
    description:int = "–"
