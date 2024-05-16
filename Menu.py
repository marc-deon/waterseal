#region Imports
import curses
from dataclasses import dataclass
from functools import partial
from textwrap import dedent

import config
import Controls
import Unit
from Cursor import Cursor
from CursorMode import CursorMode
from Focus import Focus
from Focusable import Focusable
from Popup import Popup
from Map import Map
from Logger import Logger
from BattleManager import BattleManager

#endregion

_menus = []

@dataclass
class MenuOption:
    name:str
    callback:callable
    hover:callable = None
    unhover:callable = None


def DrawMenus():
    for m in _menus:
        m.Print()
        m.panel.Draw()


class Menu(Focusable):

    # Not every menu will use this, but it is common.
    def _endturn(self):
        Cursor.instance().PopFocus()
        BattleManager.instance().EndTurn()
        # self.Unregister()

    def __str__(self):
        return "Menu: " + self.panel.title

    def on_LoseFocus(self):
        self.panel.clear()
        self.panel.noutrefresh()
        # Logger.Log(f"Menu {self.panel.title} lost focus")


    # def Unregister(self):
    #     self.panel.erase()
    #     self.panel.menu = None
    #     if isinstance(Cursor.instance().top.target, Menu):
    #         self.panel.menu = Cursor.instance().top.target

    def Remove(self):
        _menus.remove(self)

    def on_Input(self, focus, inp):
        if inp == Controls.UP:
            self.Move(-1)
        elif inp == Controls.DOWN:
            self.Move(1)
        
        elif inp == Controls.CONFIRM:
            self.Unhover()
            self.Activate()

        elif inp == Controls.CANCEL:
            self.panel.erase()
            self.panel.noutrefresh()
            focus.cursor.PopFocus()
            # self.Unregister()
            self.Unhover()
            

    def __init__(self, loop=True, panel=None, *options):
        _menus.append(self)
        self.loop = loop
        self.panel = panel or config.menuPanel
        # self.panel.menu = self
        self.options = list(options)
        self.position = 0

    def Print(self):
        y = self.panel.getyx()[0]
        #w = self.panel.contentSize[1]
        self.panel.erase()

        for i, option in enumerate(self.options):
            lead = "> " if i == self.position else "  "
            color = (curses.color_pair(1) | curses.A_BOLD) if i == self.position else (curses.color_pair(0))
            #s = f"{lead + option.name:w<}"
            self.panel.addstr(i+y, 0, lead + option.name, color)
            #self.panel.addstr(i+y, 0, s, color)




        self.panel.move(y, 0)

    def AddOption(self, option):
        self.options.append(option)

        # Hover over our first option automatically, not just when we move off and back on
        if len(self.options) == 1:
            self.Hover()


    def Move(self, dir):
        if len(self.options) > 0:
            self.Unhover()
            self.position = (self.position + dir) % len(self.options)
            self.Hover()


    def Activate(self):
        if len(self.options) == 0:
            return

        if self.options[self.position].callback:
            return self.options[self.position].callback()


    def Hover(self):
        if len(self.options) == 0:
            return
            
        if self.options[self.position].hover:
            self.options[self.position].hover()


    def Unhover(self):
        if len(self.options) == 0:
            return
            
        if self.options[self.position].unhover:
            self.options[self.position].unhover()
        


# Menu with nothing in it
class EmptyMenu(Menu):
    pass

# Selected an empty tile
class TerrainMenu(Menu):

    def __init__(self):
        super().__init__()
        self.AddOption(MenuOption("End Turn", self._endturn))


###########
# Move unit -> Choose attack -> Choose weapon -> Choose target

# Moving unit to new map tile
class MoveMenu(Menu):
    def _attack(self):
        newMenu = WeaponMenu(self.unit)
        Cursor.instance().PushFocus(Focus(newMenu, CursorMode.MODE_MENU))

    def _item(self):
        # TODO: item menu
        pass

    def _wait(self):
        self.unit.MoveTo(self.unit.tentativeTile)
        # This feels slightly gross, but I think is okay?
        while Cursor.instance().top.mode != CursorMode.MODE_REGULAR:
            Cursor.instance().PopFocus()
            self.panel.erase()
        Map.instance().selectedUnit = None
        Cursor.instance().top.x = self.unit.x
        Cursor.instance().top.y = self.unit.y
        # self.Unregister()

    def __init__(self, unit):
        super().__init__()
        self.unit = unit

        if unit.currentWeapon:
            self.AddOption(MenuOption("Attack", self._attack))
        if len(unit.inventory) > 0:
            self.AddOption(MenuOption("Item", self._item))
        self.AddOption(MenuOption("Wait", self._wait))

    def on_Input(self, focus, inp):
        if inp == Controls.CANCEL:
            self.unit.tentativeTile = None
            self.panel.erase()
        super().on_Input(focus, inp)

# Unit is attacker: Decide weapon
class WeaponMenu(Menu):

    def _target(self, unit):
        newMenu = TargetMenu(unit, Map.instance())
        Cursor.instance().PushFocus(Focus(newMenu, CursorMode.MODE_MENU))
    
    def _hover(self, unit, wep):
        unit.tentativeWeapon = wep
        previewText = dedent(f"""\
        {wep.kind}
        Atk {unit.atk}
        Crt {unit.crit}
        Hit {unit.baseHit}
        Avo {unit.avo}
        """)
        Popup.Overlay(config.terrainPanel, previewText, title="Weapon")

    def _unhover(self):
        pass

    def on_Input(self, focus, inp):
        if inp == Controls.CANCEL:
            self.unit.tentativeWeapon = None
            Popup.RemoveByName("Weapon")
        
        if inp == Controls.CONFIRM:
            self.panel.erase()

        if (inp == Controls.UP) or (inp == Controls.DOWN):
            Popup.RemoveByName("Weapon")

        
        super().on_Input(focus, inp)

    def __init__(self, unit):
        super().__init__()
        self.unit = unit
        weapons = unit.weapons
        for w in weapons:
            hover = partial(self._hover, unit, w)
            select = partial(self._target, unit)
            dura = str(w.durability)
            width = len(w.name) + len(dura)
            # -2 for the borders, - 2 for the '> ', -1 for ?
            name = w.name + " " * (config.menuPanel.page[1]-5-width) + dura
            self.AddOption(MenuOption(name, select, hover=hover, unhover=self._unhover))

# Unit is attacker: decide target
class TargetMenu(Menu):

    def on_Input(self, focus, inp):
        if inp == Controls.CANCEL:
            Popup.RemoveByName("Combat")
        
        if inp == Controls.CONFIRM:
            Popup.RemoveByName("Combat")
            Popup.RemoveByName("Weapon")
        
        if (inp == Controls.UP) or (inp == Controls.DOWN):
            Popup.RemoveByName("Combat")

        super().on_Input(focus, inp)
        

    def _combat(self, unit, target):
        # self.Unregister()
        Logger.LogDebug(self.panel.title)
        unit.MoveTo(unit.tentativeTile)
        Map.instance().selectedUnit = None

        result = Unit.DoCombat(unit, target)

        # Combat resulted in map victory/loss
        if result:
            return
            
        # while Cursor.instance().top.mode != CursorMode.MODE_REGULAR:
        while not (
            type(Cursor.instance().top.target) == Map
            and Cursor.instance().top.mode == CursorMode.MODE_REGULAR
        ):
            Cursor.instance().PopFocus()
            self.panel.erase()
        Cursor.instance().top.x = unit.x
        Cursor.instance().top.y = unit.y

    def _hover(self, unit:Unit, target:Unit):

        # to show the counterattack, but only if we are in range of them
        targetWeapon = None        
        validAttacks = target.GetValidAttacks(Map.instance(), target.currentWeapon, True)
        for tile in validAttacks:
            if tile == unit.tentativeTile:
                targetWeapon = target.currentWeapon
                break

        targetDamage = Unit.Combat_Damage(target, unit)
        unitDamage = Unit.Combat_Damage(unit, target)

        # Todo: Brave weapons? Fists?
        unitDouble = "x2" if unit.attackSpeed - target.attackSpeed > 4 else ""
        targetDouble = "x2" if target.attackSpeed - unit.attackSpeed > 4 else ""

        previewText = dedent(f"""\
        {unit.name:>12}
        {target.hp:<4} HP   {unit.hp:>4}
        {targetDamage:<{4-len(targetDouble)}}{targetDouble} Atak {unitDamage:>{4-len(unitDouble)}}{unitDouble}
        {Unit.Combat_Hit(target, unit):<4} Hit  {Unit.Combat_Hit(unit, target):>4}
        {target.crit:<4} Crit {unit.crit:>4}
        {target.name}
        {targetWeapon if targetWeapon else "No Weapon"}
        """)
        Popup.Overlay(config.statsPanel, previewText, title="Combat")

    def _unhover(self):
        # Popup.RemoveLast()
        pass

    def __init__(self, unit, map):
        super().__init__()
        validTargets = [tile.unit for tile in unit.GetValidAttacks(map, unit.tentativeWeapon, noMove=True) if tile.unit != None]
        for target in validTargets:
            # TODO: Healing Staves should be able to target allies
            if target.partyIndex != unit.partyIndex:
                # TODO: Instead of this partial, make a combat preview window (maybe on hover?)
                select = partial(self._combat, unit, target)
                hover = partial(self._hover, unit, target)
                self.AddOption(MenuOption(f"{target}", select, hover=hover, unhover=self._unhover))
    pass


# Choosing item
class ItemMenu(Menu):
    pass

