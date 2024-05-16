from CursorMode import CursorMode
from Focus import Focus
from Unit import Unit
from Party import Party
from BattleManager import BattleManager
from Cursor import Cursor
from Map import Map
import json

class Campaign():


    _instance = None

    @staticmethod
    def instance() -> "Campaign":
        return Campaign._instance


    @property
    def event(self) -> dict:
        return self.events[self.step]


    def __init__(self, path:str, step:int=0):
        Campaign._instance = self
        self.events = json.load(open(path, 'r'))["events"]
        self.step = step
        self.playerParty = Party("Player")


    def Next(self):
        event:dict = self.event

        if event["type"] == "dialogue":
            # raise NotImplementedError("dialogue")
            self.step+=1
            self.Next()
            return

        elif event["type"] == "combat":
            m = Map.ReadFromJson(event["file"])
            focus = Focus(m, CursorMode.MODE_REGULAR)
            Cursor.instance().PushFocus(focus)
            m.Begin()

        elif event["type"] == "preparation":
            raise NotImplementedError("preparation")

        elif event["type"] == "item":
            raise NotImplementedError("item")

        elif event["type"] == "recruit":
            u = Unit.FromJson(f"Units/{event['target']}.json", 0)
            self.playerParty.AddReserve(u)

        elif event["type"] == "promotion":
            raise NotImplementedError("promotion")

        elif event["type"] == "move":
            raise NotImplementedError("move")


        else:
            raise TypeError()

        self.step += 1
        # TODO: Imeplenet non-silent recruits, remove 'or'
        if event.get("silent", False) or event["type"] == "recruit":
            self.Next()



# def ReadFromJson(path:str, step:int=0) -> Campagin:

#     c = Campagin()
#     c.step = step

#     return c