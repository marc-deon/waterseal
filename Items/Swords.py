from dataclasses import dataclass
from Items.Item import Sword
# Stats from https://serenesforest.net/blazing-sword/
from dataclasses import dataclass


@dataclass
class IronSword(Sword):
    name:str = "Iron Sword"
    rank:str = "E"
    weight:int = 5
    might:int = 5
    hit:int = 90
    crit:int = 0
    durability:int = 46
    cost:int = 460
    description:str = "Rainy christmastide \\ A 20th iron fox sleeps \\ at the perfect sword"

@dataclass
class SlimSword(Sword):
    name:str = "Slim Sword"
    rank:str = "E"
    weight:int = 2
    might:int = 3
    hit:int = 100
    crit:int = 5
    durability:int = 30
    cost:int = 480
    description:str = "Dismal wintertime \\ A little, slim kitten squeaks \\ enjoying the sword"

@dataclass
class EmblemBlade(Sword):
    name:str = "Emblem Blade"
    rank:str = "E"
    weight:int = 5
    might:int = 5
    hit:int = 90
    crit:int = 0
    durability:int = 60
    cost:int = 0
    description:str = "Great warm up mountain \\ A single, emblem blade barks \\ watching the rabbit"

@dataclass
class PoisonSword(Sword):
    name:str = "Poison Sword"
    rank:str = "D"
    weight:int = 6
    might:int = 3
    hit:int = 70
    crit:int = 0
    durability:int = 40
    description:str = "Semiarid, leaping \\ A narrow poison sword runs \\ despite the spider"

@dataclass
class SteelSword(Sword):
    name:str = "Steel Sword"
    rank:str = "D"
    weight:int = 10
    might:int = 8
    hit:int = 75
    crit:int = 0
    durability:int = 30
    cost:int = 600
    description:str = "–"

@dataclass
class IronBlade(Sword):
    name:str = "Iron Blade"
    rank:str = "D"
    weight:int = 12
    might:int = 9
    hit:int = 70
    crit:int = 0
    durability:int = 35
    cost:int = 980
    description:str = "–"

@dataclass
class Armourslayer(Sword):
    name:str = "Armourslayer"
    rank:str = "D"
    weight:int = 11
    might:int = 8
    hit:int = 80
    crit:int = 0
    durability:int = 18
    cost:int = 1260
    description:str = "Effective against armoured units"

@dataclass
class Longsword(Sword):
    name:str = "Longsword"
    rank:str = "D"
    weight:int = 11
    might:int = 6
    hit:int = 85
    crit:int = 0
    durability:int = 18
    cost:int = 1260
    description:str = "Effective against horseback units"

@dataclass
class WoDao(Sword):
    name:str = "Wo Dao"
    rank:str = "D"
    weight:int = 5
    might:int = 8
    hit:int = 75
    crit:int = 35
    durability:int = 20
    cost:int = 1200
    description:str = "Myrmidon, Swordmaster, Blade Lord only"

@dataclass
class SteelBlade(Sword):
    name:str = "Steel Blade"
    rank:str = "C"
    weight:int = 14
    might:int = 11
    hit:int = 65
    crit:int = 0
    durability:int = 25
    cost:int = 1250
    description:str = "–"

@dataclass
class KillingEdge(Sword):
    name:str = "Killing Edge"
    rank:str = "C"
    weight:int = 7
    might:int = 9
    hit:int = 75
    crit:int = 30
    durability:int = 20
    cost:int = 1300
    description:str = "–"

@dataclass
class Wyrmslayer(Sword):
    name:str = "Wyrmslayer"
    rank:str = "C"
    weight:int = 5
    might:int = 7
    hit:int = 75
    crit:int = 0
    durability:int = 20
    cost:int = 3000
    description:str = "Effective against dragon units"

@dataclass
class Lancereaver(Sword):
    name:str = "Lancereaver"
    rank:str = "C"
    weight:int = 9
    might:int = 9
    hit:int = 75
    crit:int = 5
    durability:int = 15
    cost:int = 1800
    description:str = "Good against lances, bad against axes"

@dataclass
class BraveSword(Sword):
    name:str = "Brave Sword"
    rank:str = "B"
    weight:int = 12
    might:int = 9
    hit:int = 75
    crit:int = 0
    durability:int = 30
    cost:int = 3000
    description:str = "Allows 2 consecutive hits"


@dataclass
class SilverSword(Sword):
    name:str = "Silver Sword"
    rank:str = "A"
    weight:int = 8
    might:int = 13
    hit:int = 80
    crit:int = 0
    durability:int = 20
    cost:int = 1500
    description:str = "–"

@dataclass
class SilverBlade(Sword):
    name:str = "Silver Blade"
    rank:str = "A"
    weight:int = 13
    might:int = 14
    hit:int = 60
    crit:int = 0
    durability:int = 15
    cost:int = 1800
    description:str = "–"


@dataclass
class RegalBlade(Sword):
    name:str = "Regal Blade"
    rank:str = "S"
    weight:int = 9
    might:int = 20
    hit:int = 85
    crit:int = 0
    durability:int = 25
    cost:int = 15000
    description:str = "–"

@dataclass
class ManiKatti(Sword):
    name:str = "Mani Katti"
    rank:str = "X"
    weight:int = 3
    might:int = 8
    hit:int = 80
    crit:int = 20
    durability:int = 45
    description:str = "Lyn only, effective against armoured/mounted units"

@dataclass
class Rapier(Sword):
    name:str = "Rapier"
    rank:str = "X"
    weight:int = 5
    might:int = 7
    hit:int = 95
    crit:int = 10
    durability:int = 40
    cost:int = 6000
    description:str = "Eliwood only, effective against armoured/mounted units"

@dataclass
class Durandal(Sword):
    name:str = "Durandal"
    rank:str = "X"
    weight:int = 16
    might:int = 17
    hit:int = 90
    crit:int = 0
    durability:int = 20
    description:str = "Eliwood only, Str +5, effective against dragon units"

@dataclass
class SolKatti(Sword):
    name:str = "Sol Katti"
    rank:str = "X"
    weight:int = 14
    might:int = 12
    hit:int = 95
    crit:int = 25
    durability:int = 30
    description:str = "Lyn only, Res +5, effective against dragon units"

class LightBrand(Sword):
    rank:str = "C"
    useRange:tuple = (1,2)
    weight:int = 9
    might:int = 9
    hit:int = 70
    crit:int = 0
    durability:int = 25
    description:str = "Magic Sword (Light) at range"
class WindSword(Sword):
    rank:str = "B"
    useRange:tuple = (1,2)
    weight:int = 9
    might:int = 9
    hit:int = 70
    crit:int = 0
    durability:int = 40
    description:str = "Magic Sword (Anima), effective against flying units (Mario Kart: Double Dash!! bonus disk only)"
class Runesword(Sword):
    rank:str = "A"
    useRange:tuple = (1,2)
    weight:int = 11
    might:int = 12
    hit:int = 65
    crit:int = 0
    durability:int = 15
    description:str = "Magic Sword (Dark), drains HP from enemy"