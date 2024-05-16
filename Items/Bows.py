from Items.Item import Bow
from dataclasses import dataclass

@dataclass
class IronBow(Bow):
    name:str = "Iron Bow"	    
    rank:str = 'E'
    weight:int = 5
    might:int = 6
    hit:int = 85
    crit:int = 0
    durability:int = 45
    useRange:int = (2,2)
    cost:int = 40
    description:str = "-"
@dataclass
class EmblemBow(Bow):
    name:str = "Emblem Bow"	    
    rank:str = 'E'
    weight:int = 5
    might:int = 6
    hit:int = 85
    crit:int = 0
    durability:int = 60
    useRange:int = (2,2)
    cost:int = 0
    description:str = "Mario Kart: Double Dash!! bonus disk only)"
@dataclass
class Ballista(Bow):
    name:str = "Ballista"	    
    rank:str = 'E'
    weight:int = 20
    might:int = 8
    hit:int = 70
    crit:int = 0
    durability:int = 5
    useRange:int = (3,10)
    cost:int = 0
    description:str = "Cannot be countered"
@dataclass
class KillerBallista(Bow):
    name:str = "Killer Ballista"
    rank:str = 'E'
    weight:int = 20
    might:int = 12
    hit:int = 65
    crit:int = 10
    durability:int = 5
    useRange:int = (3,10)
    cost:int = 0
    description:str = "Cannot be countered"
@dataclass
class IronBallista(Bow):
    name:str = "Iron Ballista"	
    rank:str = 'E'
    weight:int = 20
    might:int = 13
    hit:int = 60
    crit:int = 0
    durability:int = 5
    useRange:int = (3,15)
    cost:int = 0
    description:str = "Cannot be countered"
@dataclass
class PoisonBow(Bow):
    name:str = "Poison Bow"	    
    rank:str = 'D'
    weight:int = 5
    might:int = 4
    hit:int = 65
    crit:int = 0
    durability:int = 40
    useRange:int = (2,2)
    cost:int = 0
    description:str = "Poisons on contact"
@dataclass
class ShortBow(Bow):
    name:str = "Short Bow"	    
    rank:str = 'D'
    weight:int = 3
    might:int = 5
    hit:int = 85
    crit:int = 10
    durability:int = 22
    useRange:int = (2,2)
    cost:int = 760
    description:str = "–"
@dataclass
class Longbow(Bow):
    name:str = "Longbow"	    
    rank:str = 'D'
    weight:int = 10
    might:int = 5
    hit:int = 65
    crit:int = 0
    durability:int = 20
    useRange:int = (2,3)
    cost:int = 100
    description:str = "–"
@dataclass
class SteelBow(Bow):
    name:str = "Steel Bow"	    
    rank:str = 'D'
    weight:int = 9
    might:int = 9
    hit:int = 70
    crit:int = 0
    durability:int = 30
    useRange:int = (2,2)
    cost:int = 200
    description:str = "–"
@dataclass
class KillerBow(Bow):
    name:str = "Killer Bow"	    
    rank:str = 'C'
    weight:int = 7
    might:int = 9
    hit:int = 75
    crit:int = 30
    durability:int = 20
    useRange:int = (2,2)
    cost:int = 400
    description:str = "–"
@dataclass
class BraveBow(Bow):
    name:str = "Brave Bow"	    
    rank:str = 'B'
    weight:int = 12
    might:int = 10
    hit:int = 70
    crit:int = 0
    durability:int = 30
    useRange:int = (2,2)
    cost:int = 500
    description:str = "Allows 2 consecutive hits"
@dataclass
class SilverBow(Bow):
    name:str = "Silver Bow"	    
    rank:str = 'A'
    weight:int = 6
    might:int = 13
    hit:int = 75
    crit:int = 0
    durability:int = 20
    useRange:int = (2,2)
    cost:int = 600
    description:str = "–"
@dataclass
class Rienfleche(Bow):
    name:str = "Rienfleche"	    
    rank:str = 'S'
    weight:int = 7
    might:int = 20
    hit:int = 80
    crit:int = 0
    durability:int = 25
    useRange:int = (2,2)
    cost:int = 5000
    description:str = "–"
