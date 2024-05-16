from dataclasses import dataclass
from Items.Item import Item

@dataclass
class Vulnerary(Item):
    name:str = "Vulnerary"
    durability:int = 3
    description:str = "Pillz here"