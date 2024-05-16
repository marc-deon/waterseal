from Items.Item import Lance
from dataclasses import dataclass

@dataclass
class SilverLance(Lance):
    name:str = "Silver Lance"
    rank:str = 'A'
    useRange:tuple = (1,1)
    weight:int = 10
    might:int = 14
    hit:int = 75
    crit:int = 0
    durability:int = 20
    cost:int = 1200
    description:str = "-"