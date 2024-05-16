#!/usr/bin/env python3

#region Imports
import os

if os.get_terminal_size()[0] < 80 or os.get_terminal_size()[1] < 24:
        print("Water Seal requires a minimum of 80x24 character display. Please seek a computer from 1980 or newer.")

import curses
from sys import stdout

import colors
import config
from Items.Item import Weapon
import Titlescreen
from BattleManager import BattleManager
from config import Config_Start, ResizeScreen
from Cursor import Cursor
from CursorMode import CursorMode
from Focus import Focus
from Map import Map
import Menu
# from Menu import *
from Popup import Popup

import gc


#endregion

#region Temporary initialization
BattleManager()
cursor = Cursor()
#endregion

def Main_Init():
    if os.get_terminal_size()[0] < 80 or os.get_terminal_size()[1] < 24:
        # print("Water Seal requires a minimum of 24x80 character display. Please seek a computer from 1980 or newer.")
        return False

    stdout.write("\x1b]2;Water Seal\x07")
    curses.curs_set(0)
    curses.halfdelay(1)
    colors.InitColors()
    return True

def Update_Draw_Battle():
    currentMap = Map.instance()

    terrainSize = config.terrainSize
    mapPanel = config.mapPanel
    terrainPanel = config.terrainPanel
    statsPanel = config.statsPanel
    logPanel = config.logPanel
    menuPanel = config.menuPanel
    hoveredUnit = currentMap.hoveredUnit
    hoveredTile = currentMap.hoveredTile

    # Draw Map, including cursor
    currentMap.Print(mapPanel)

    statsPanel.erase()

    # Change UI content and colors
    if currentMap.hoveredTile.unit:
        if currentMap.hoveredTile.unit.partyIndex == 0:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        elif currentMap.hoveredTile.unit.partyIndex == 1:
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        elif currentMap.hoveredTile.unit.partyIndex == 2:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        elif currentMap.hoveredTile.unit.partyIndex == 3:
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        # Stats panel
        statsPanel.addstr(0,0, hoveredUnit.name, curses.color_pair(1))
        statsPanel.addstr(1,0, hoveredUnit.kind.name)
        statsPanel.addstr(2,0, "Moved" if hoveredUnit.moved else f"Movement: {hoveredUnit.kind.moveSpeed}")
        statsPanel.addstr(3,0, f"HP {hoveredUnit.hp}/{hoveredUnit.maxHp}")
        statsPanel.addstr(10,0, f"Rescuing: {hoveredUnit.rescue}")
        statsPanel.addstr(11,0,"Status effects")
        statsPanel.addstr(12,0,"go")
        statsPanel.addstr(13,0,"here")

        mapPanel.addstr(hoveredUnit.y, hoveredUnit.x, hoveredUnit.kind.symbol, curses.color_pair(colors.BLACK_WHITE))

        for i, item in enumerate(hoveredUnit.inventory):
            s = item.name
            if isinstance(item, Weapon):
                s+= f" ({item.durability}/{item.maxDurability})"
            statsPanel.addstr(4+i, 0, s)

    # Show map highlights, prioritizing selected > hovered > none
    unit = currentMap.selectedUnit if currentMap.selectedUnit \
           else currentMap.hoveredTile.unit if currentMap.hoveredTile.unit \
           else None

    if unit and not unit.moved:
        if unit.tentativeWeapon:
            unit.HighlightAttacks(currentMap, mapPanel, cursor, noMove=True)
        else:
            unit.HighlightAttacks(currentMap, mapPanel, cursor)
            unit.HighlightMovement(currentMap, mapPanel, cursor)

            
    else:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    logPanel.content.scrollok(True)

    terrainPanel.erase()
    terrainPanel.addstr(0,0,hoveredTile.name)
    posString = f"({hoveredTile.x}, {hoveredTile.y})"
    # Show the tile coords on the right side of the panel
    terrainPanel.addstr(0,terrainSize[0]-len(posString)-3, posString)
    terrainPanel.addstr(1,0,f"{hoveredTile.defenseMod:<2d} DEF\n")
    terrainPanel.addstr(2,0,f"{hoveredTile.avoidMod:<2d} AVO\n")
    if hoveredTile.unit:
        terrainPanel.addstr(3,0,f"Unit: {hoveredTile.unit.name}\n",
                curses.color_pair(hoveredTile.unit.partyIndex+2))
    else:
        pass
    terrainPanel.addstr(4,0,hoveredTile.kind.description)

    for panel in [mapPanel, terrainPanel, statsPanel, logPanel, menuPanel]:
        panel.Draw()


def Update_Draw():

    if Map.instance():
        Update_Draw_Battle()

    Popup.DrawPopups()
    Menu.DrawMenus()
    curses.doupdate()

def Main(screen):

    if not Main_Init():
        return

    currentMap = Map.instance()
    Config_Start(screen)

    cursor.PushFocus(Focus(Titlescreen.Title(), CursorMode.MODE_MENU))

    while True:
        ## Get Input
        inp = -1
        try:
            inp = screen.getch()
        except:
            pass

        ## Process input
        if inp == curses.KEY_RESIZE:
            ResizeScreen(screen, currentMap)

        if inp == curses.KEY_END:
            break

        quit = cursor.Input(inp)
        if quit:
            break


        # gc.collect()
        # foo = gc.get_referrers(Menu._menus[-1])
        ## Draw Graphics
        Update_Draw()
        

curses.wrapper(Main)
