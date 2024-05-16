from Panel import Panel
import curses
from os import error
from typing import Union

import sys

import config
import Controls
import Menu
import TileKinds
from BattleManager import BattleManager
from Cursor import Cursor
from CursorMode import CursorMode
from Focus import Focus
from Focusable import Focusable
from Logger import Logger
from Popup import Popup
import Tile
import json
import Unit
from Party import Party
import Conditions

class Map(Focusable):

    _instance = None

    @property
    def page(self):
        return config.mapPanel.contentSize


    def Begin(self):
        """Player has started battle"""
        
        config.Config_Size()
        config.AlignColumns()

        # Deploy all units

        # Initialize all conditions (some require deployed units... maybe bad? Probably fine)
        for cond in self.lossConditions:
            cond.cb_onBegin()
        for cond in self.victoryConditions:
            cond.cb_onBegin()


    def Move_Unit(self, x, y, unit, focus, confirm, cancel):
        assert unit != None
        valid = unit.GetValidMoves(self)[1]
        target = self[focus.x + x, focus.y + y]
        if target in valid:
            self.Move_Shared(x, y, focus)

        if confirm:
            # Filter to only the valid to-moves
            if self.hoveredTile in self.selectedUnit.GetValidMoves(self)[0]:
                self.selectedUnit.TentativeMoveTo(self.hoveredTile)
                newMenu = Menu.MoveMenu(unit)
                newMenu.cursor = focus.cursor
                focus.cursor.PushFocus(Focus(newMenu, CursorMode.MODE_MENU))

        if cancel:
            self.selectedUnit = None
            Cursor.instance().PopFocus()
            

    def Move_Target(self, x, y, unit, focus, confirm, cancel):
        pass
            

    def Move_Shared(self, x, y, focus):
        """Scrolling the map"""
        ## Move cursor
        # Cap focus within map size
        if focus.x + x < self.x and focus.x + x >= 0:
            focus.x += x
        if focus.y + y < self.y and focus.y + y >= 0:
            focus.y += y

        # Vector to adjust camera by
        v = [0,0]

        # Scroll right if necesary
        if focus.x >= focus.pageX + focus.offsetX:
            v[0] = focus.x - (focus.pageX + focus.offsetX)
        # Scroll left
        if focus.x < focus.offsetX:
            v[0] = focus.offsetX - focus.x
        # Scroll up
        if focus.y < focus.offsetY:
            v[1] = focus.offsetY - focus.y
        # Scroll down
        if focus.y >= focus.pageY + focus.pageY:
            v[1] = focus.y - (focus.pageY + focus.offsetY)
        
        focus.offsetX += v[0]
        focus.offsetY += v[1]
      
    def Move_Regular(self, x, y, focus, confirm, cancel):
        """Move the map cursor without any restraints"""          
        # Scroll camera if neccesary
        self.Move_Shared(x, y, focus)

        # Confirm/Cancel
        if confirm:
            hoveredUnit = self.hoveredUnit

            # Hovering over a unit that hasn't moved yet
            if hoveredUnit and (self.selectedUnit == None) and not hoveredUnit.moved:
                if hoveredUnit.partyIndex == BattleManager.instance().currentParty:
                    self.selectedUnit = hoveredUnit
                    focus.cursor.PushFocus(
                        Focus(self, CursorMode.MODE_UNIT,
                            focus.x, focus.y,
                            focus.offsetX, focus.offsetY
                        )
                    )
            # Hovering over just terrain
            elif not hoveredUnit:
                # End turn/settings/etc
                newMenu = Menu.TerrainMenu()
                focus.cursor.PushFocus(
                    Focus(newMenu, CursorMode.MODE_MENU, 
                        1, len(newMenu.options)
                    )
                )

    def on_Input(self, focus, inp):
        y = 0
        x = 0

        if inp == Controls.UP:
            y = -1
        elif inp == Controls.DOWN:
            y = 1
        if inp == Controls.LEFT:
            x = -1
        elif inp == Controls.RIGHT:
            x = 1

        confirm = inp == Controls.CONFIRM
        cancel = inp == Controls.CANCEL


        if focus.mode == CursorMode.MODE_UNIT:
            unit = self.selectedUnit
            self.Move_Unit(x, y, unit, focus, confirm, cancel)

        elif focus.mode == CursorMode.MODE_TARGET:
            unit = self.selectedUnit
            self.Move_Target(x, y, unit, focus, confirm, cancel)

        elif focus.mode == CursorMode.MODE_REGULAR:
            unit = self[focus.x, focus.y].unit
            self.Move_Regular(x, y, focus, confirm, cancel)


    def __getitem__(self, index):
        if isinstance(index, int):
            y = int(index / len(self.tiles[0]))
            x = index % len(self.tiles[0])
        else:
            x, y = index

        if (x < 0) or (x >= self.x) or (y < 0) or (y >= self.y):
            # return None
            raise IndexError()
        return self.tiles[y][x]


    def __setitem__(self, indices, value):
        x,y = indices
        self.tiles[y][x] = value


    @property
    def x(self):
        return self.size[0]
    @property
    def y(self):
        return self.size[1]

    @property
    def hoveredTile(self):
        inst = Cursor.instance()
        return self[inst.top.x, inst.top.y]

    @property
    def hoveredUnit(self):
        return self.hoveredTile.unit

    @staticmethod
    def instance():
        return Map._instance

    def __init__(self, x, y, victoryConditions=[], lossConditions=[]):
        Map._instance = self

        # lol list comprehensions :^)))))
        self.tiles = [[Tile.Tile(TileKinds.PLAIN, self, i, j) for i in range(x)] for j in range(y)]
        # list[Tile -> Unit dictionary]
        self.spawns = []
        self.size = x, y
        self.cameraOffset = [0, 0]
        self.selectedUnit = None
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self[x,y].x = x
                self[x,y].y = y

        self.victoryConditions = victoryConditions
        self.lossConditions = lossConditions

        
    # Returns 1 on win, -1 on loss, 0 otherwise
    def CheckConditions(self):
        result = 0
        for cond in self.victoryConditions:
            # Logger.Log("Checking vc", cond, cond.)
            if cond.Test(self):

                # Remove all foci up to and including the map
                while not isinstance(Cursor.instance().PopFocus().target, Map):
                    pass
                    
                # Create the victory popup, with continue option that kills the popup

                def _continue():
                    Popup.RemoveLast()
                    Cursor.instance().PopFocus()

                    # Load the next campaign event (e.g. focus on the next map)
                    from Campaign import Campaign
                    Campaign.instance().Next()
                    


                p = Popup.Fullscreen("Victory!\n","VICTORY!")
                menu = Menu.Menu(
                    False,
                    p,
                    Menu.MenuOption("Continue", _continue)
                    )

                # focus on the popup
                f = Focus(menu, CursorMode.MODE_MENU)
                Cursor.instance().PushFocus(f)

                result = 1
                break

        if not result:       
            for cond in self.lossConditions:
                if cond.Test(self):
                    
                    Logger.Log("loss due to", cond)
                    result = -1
                    
                    Popup.Fullscreen("Max cringe",[],"DEFEAT")
                    break


        return result

    def Print(self, mapPad, showTerrain=False, **vargs):
        # assert type(cursor) == Cursor
        cursor = Cursor.instance()
        focus = cursor.GetTopOfType(Map)
        # Logger.Log("focus is", focus)

        # assert type(focus) == Focus
        # assert type(focus.target) == Map
        if type(focus) != Focus:
            return
        if not focus.target:
            return
        if type(focus.target) != Map:
            return


        y = 0
        for row in self.tiles:
            mapPad.move(y,0)

            x = 0
            for tile in row:

                s = str(tile)
                party = 0
                bold = False

                if showTerrain or tile.unit == None:
                    s = str(tile)
                    party = 0 if tile.kind.color == None else tile.kind.color
                else:
                    s = tile.unit.symbol
                    party = tile.unit.partyIndex+2
                    bold = not tile.unit.moved


                # Add the character with the proper party (or terrain) color. Reverse FG and BG if this is the cursor position.
                mapPad.addstr(s, curses.color_pair(party) | (curses.A_REVERSE * (x == focus.x and y
                    == focus.y)) | (curses.A_BOLD * bold) )
                x+=1
            y+=1


    @staticmethod
    def ReadFromJson(path):

        data:dict = json.load(open(path, 'r'))
        
        charKey = data["key"]
        x = len(data["map"][0])
        y = len(data["map"])

        BattleManager.instance().parties = BattleManager.instance().parties[:1]

        for partyName in data["partyNames"][1:]:
            Party(partyName)

        vc, lc = [], []
        for ctype, args in data["conditions"].items():
            
            # For single arguments, wrap them in a list
            if type(args) != list:
                args = [args]

            # Get the Python condition from string
            cond = getattr(Conditions, ctype)
            # Instantiate with arguments
            cond = cond(*args)

            if ctype.startswith("VC"):
                vc.append(cond)
            elif ctype.startswith("LC"):
                lc.append(cond)

        map = Map(x, y, vc, lc)

        for j, line in enumerate(data["map"]):
            for i, c in enumerate(line):
                map[i,j].kind = Tile.nameKey[charKey[c]]


        Logger.LogDebug("Beginning spawns...")

        for spawn in data.get("spawns", []):
            # Add to that dict every spawn tile
            x, y = spawn
            map.spawns.append(map[x,y])

        Logger.LogDebug("Finished deployment locations")

        for i, team in enumerate(data.get("predeploy", [])):
            for name, xy in team.items():
                x, y = xy
                name = name.split("_")[0]

                unit = None

                # If this is the player party...
                if i == 0:
                    # If the unit already exists, get it; otherwise, spawn with default stats
                    ru:set = BattleManager.instance().parties[i].reserveUnits
                    unit = next(filter(lambda x: x.name == name, ru), None)
                    unit = unit or Unit.Unit.FromJson(f"Units/{name}.json", i)
                    unit.moved = False
                # Enemy party will always spawn with default stats
                else:
                    unit = Unit.Unit.FromJson(f"Units/{name}.json", i)
                
                BattleManager.instance().parties[i].activeUnits.append(unit)
                unit.PlaceAt(map[x,y])
        
        Logger.LogDebug("Finished predeployed units")
        return map
























