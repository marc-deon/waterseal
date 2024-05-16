from Map import Map
import curses
import random
from dataclasses import dataclass
from math import floor

from BattleManager import BattleManager
import config
from colors import BLACK_WHITE, CYAN_BLACK, RED_BLACK, RED_WHITE
# from Items.Item import *  # pylint: disable=unused-wildcard-import
import Items
from Logger import Logger
import MovementModifiers
import json

@dataclass
class StatBlock:
    strength:int
    magic:int
    defense:int
    accuracy:int
    speed:int
    luck:int
    resistance:int
    weight:int

ALIVE = 1
DEAD = 0

class Unit:

    def TakeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.Die()
            return DEAD
        return ALIVE


    def Heal(self, amount):
        self.hp = min(self.hp + amount, self.maxHp)


    def Die(self):
        self.tile.unit = None
        self.tile = None
        BattleManager.instance().parties[self.partyIndex].remove(self)
        Logger.Log(f"{self.name} has died!")


    # TODO: Limit weapon usage based on class and rank
    class Kind:
        name = "Classless"
        symbol = "?"

        def __init__(self, name, symbol, movementType):
            self.name = name
            self.symbol = symbol
            if isinstance(movementType, str):
                movementType = getattr(MovementModifiers, "MOVE_"+movementType.upper())
            self.movementType = movementType
            self.moveSpeed = 4 if movementType == MovementModifiers.MOVE_FOOT else 6

    def __repr__(self):
        return f"{self.name} ({self.x},{self.y})"

    @property
    def symbol(self):
        return self.kind.symbol

    @property
    def x(self):
        return self.tile.x

    @property
    def y(self):
        return self.tile.y

    # Used when ghosting over an uncofirmed move
    tentativeTile = None

    @property
    def tentativeX(self):
        if self.tentativeTile != None:
            return self.tentativeTile.x
        return None

    @property
    def tentativeY(self):
        if self.tentativeTile != None:
            return self.tentativeTile.y
        return None

    #region Stats
    @property
    def str(self):
        return self.statBlock.strength
    @property
    def mag(self):
        return self.statBlock.magic
    @property
    def dfn(self):
        return self.statBlock.defense
    @property
    def acc(self):
        return self.statBlock.accuracy
    @property
    def spd(self):
        return self.statBlock.speed
    @property
    def luk(self):
        return self.statBlock.luck
    @property
    def res(self):
        return self.statBlock.resistance
    @property
    def wei(self):
        return self.statBlock.weight

    # Derived stats
    @property
    def attackSpeed(self):
        if self.currentWeapon:
            return self.statBlock.speed - self.currentWeapon.weight
        return self.statBlock.speed

    @property
    def atk(self):
        wep = self.tentativeWeapon or self.currentWeapon or False

        if not wep:
            return 0

        stat = self.mag if wep.magical else self.str

        return stat + wep.might

    @property
    def crit(self):
        wep = self.tentativeWeapon or self.currentWeapon or False

        if not wep:
            return 0

        return floor(self.acc/2) + wep.crit

    @property
    def baseHit(self):
        wep = self.tentativeWeapon or self.currentWeapon or False
        if not wep:
            return 0

        return self.acc*2 + floor(self.luk/2) + wep.hit

    @property
    def avo(self):
        tile = self.tentativeTile or self.tile
        return self.spd*2 + self.luk + tile.avoidMod

    #endregion    

    @property
    def currentWeapon(self):
        return self.weapons[0] if len(self.weapons) != 0 else None

    @property
    def weapons(self):
        return [i for i in self.inventory if isinstance(i, Items.Weapon)]

    def __init__(self, partyIndex, name, kind, maxHp, stats, items=[]):
        self.partyIndex = partyIndex
        # BattleManager.instance().parties[partyIndex].AddActive(self)
        self.name = name
        self.kind = kind
        self.maxHp = maxHp
        self.hp = maxHp
        self.inventory = items
        self.rescue = None
        self.tile = None
        self.moved = False
        self.tentativeWeapon = None
        self.statBlock = stats

    @staticmethod
    def FromJson(path, partyIndex):
        obj = json.load(open(path, 'r'))
        name = obj["name"]
        kind = Unit.Kind(**obj["kind"])
        hp = obj["hp"]
        stats = StatBlock(**obj["stats"])
        items = [getattr(Items, item)() for item in obj["items"]]

        return Unit(partyIndex, name, kind, hp, stats, items)


    def EquipWeapon(self, weapon):
        assert weapon in self.inventory
        i = self.inventory.pop(self.inventory.index(weapon))
        self.inventory.insert(0, weapon)

    def MoveTo(self, tile):
        """Move unit to tile, leaving None and overwriting existing unit"""
        self.PlaceAt(tile)
        self.moved = True

    def PlaceAt(self, tile):
        """Move unit to tile without setting moved, leaving None and overwriting existing unit"""
        if self.tile:
            self.tile.unit = None
        self.tile = tile
        tile.unit = self
        self.tentativeTile = None

    def TentativeMoveTo(self, tile):
        self.tentativeTile = tile

    def CancelTentativeMove(self):
        self.tentativeTile = None


    def GetValidAttacks(self, map, weapon, noMove=False):

        if weapon == None:
            return []

        # Start with the tiles we can walk to if noMove is false, or with just our current tile if it's true
        validMoves = [self.tentativeTile if self.tentativeTile else self.tile] if noMove else self.GetValidMoves(map)[0]

        ##############
        validNodes = []
        minRange, maxRange = weapon.useRange


        for source in validMoves:
            frontier = set([map[source.x,source.y]])
            checked = set()
            distances = {map[source.x,source.y]: 0}

            while len(frontier) > 0:
                currentNode = frontier.pop()

                # Update frontier
                for neighbor in currentNode.neighbors:
                    if neighbor == None:
                        continue

                    # Set a large default distance if we haven't checked before
                    if neighbor not in distances:
                        distances[neighbor] = 6969

                    # (re-)evaluate distance, add to frontier if within range
                    if distances[currentNode]+1 < distances[neighbor]:
                        distances[neighbor] = distances[currentNode]+1
                        # Since we've (re-)evaluated thier distance, (re-)add to frontier
                        if distances[neighbor] <= maxRange:
                            frontier.add(neighbor)

                # Check if within range min and max
                if (distances[currentNode] >= minRange and distances[currentNode] <= maxRange):
                    validNodes.append(currentNode)
                checked.add(currentNode)
        #############
        return validNodes

    # TODO?: Fix terrain weights (or else check that Bagen is set to be affected as cav)
    def GetValidMoves(self, map):
        """Flood fill algorithm. Returns all valid:\nto-nodes and \nthrough-nodes."""
        throughNodes = []
        start = map[self.x,self.y]
        toNodes = [start]
        frontier = set([start])
        checked = set()
        distances = {start: 0}
        maxDistance = self.kind.moveSpeed

        while len(frontier) > 0:
            currentNode = frontier.pop()

            # Update frontier
            for neighbor in currentNode.neighbors:
                if (neighbor != None and
                    (
                        neighbor.unit == None or
                        neighbor.unit.partyIndex == self.partyIndex
                    ) and
                    not(self.kind.movementType & neighbor.kind.moveMod)
                ):

                    # Set a large default distance if we haven't checked before
                    if neighbor not in distances:
                        distances[neighbor] = 6969

                    # Add an extra cost if the tile is slow for our unit
                    moveMod = 1 if ((self.kind.movementType << 4) & currentNode.kind.moveMod) else 0

                    # (re-)evaluate distance, add to frontier if within range
                    if distances[currentNode]+1 + moveMod < distances[neighbor]:
                        distances[neighbor] = distances[currentNode]+1 + moveMod
                        # Since we've (re-)evaluated thier distance, (re-)add to frontier
                        if distances[neighbor] <= maxDistance:
                            frontier.add(neighbor)

            # Check if we can walk THROUGH here (including tiles with allies)
            if (not(self.kind.movementType & currentNode.kind.moveMod) and
                distances[currentNode] <= maxDistance #and
                #currentNode.unit == None
            ):
                throughNodes.append(currentNode)

            # Check to see if we can walk TO here (excluding tiles with allies)
            if (not(self.kind.movementType & currentNode.kind.moveMod) and
                distances[currentNode] <= maxDistance and
                currentNode.unit == None
            ):
                toNodes.append(currentNode)
            checked.add(currentNode)

        return toNodes, throughNodes


    def HighlightMovement(self, map, mapPad, cursor):
        """"Highlight valid movable spaces in cyan"""
        import Map
        focus = cursor.GetTopOfType(Map.Map)
        validNodes = self.GetValidMoves(map)[0]

        for node in validNodes:
            if node == self.tile:
                continue
            x, y = node.x, node.y
            s = map[x,y].kind.symbol
            color = curses.color_pair(CYAN_BLACK)
            mapPad.addstr(y,x,s, color | curses.A_REVERSE)
        mapPad.addstr(focus.y, focus.x, cursor.symbol, curses.color_pair(BLACK_WHITE) |
                curses.A_REVERSE)


    def HighlightAttacks(self, map, mapPad, cursor, noMove=False):
        """"Highlight valid movable spaces in cyan"""
        import Map
        focus = cursor.GetTopOfType(Map.Map)
        validNodes = self.GetValidAttacks(map, self.tentativeWeapon if self.tentativeWeapon else self.currentWeapon, noMove=noMove)

        for node in validNodes:
            if node == self.tile:
                continue
            x, y = node.x, node.y
            s = map[x,y].unit.kind.symbol if map[x,y].unit else map[x,y].kind.symbol
            color = curses.color_pair(RED_WHITE) if (map[x,y].unit != None) and (map[x,y].unit.partyIndex == self.partyIndex) else curses.color_pair(RED_BLACK)
            mapPad.addstr(y,x,s, color | curses.A_REVERSE)
        mapPad.addstr(focus.y, focus.x, cursor.symbol, curses.color_pair(RED_WHITE) |
                curses.A_REVERSE)

    
    def CanCounter(self, aggressor:"Unit") -> bool:
        if len(self.weapons) == 0:
            return False

        valid = self.GetValidAttacks(Map.instance(), self.currentWeapon, True)

        if aggressor.tile in valid:
            return True

        return False

    def AddItem(self, item):
    # TODO: Add bossom
        if len(self.inventory) >= 5:
            raise Exception("Inventory full")
        self.inventory.append(item)


# Return list of combat steps
def Combat_GetSteps(attacker:Unit, defender:Unit) -> list:

    canCounter = defender.CanCounter(attacker)

    # Attacker hits; defender counterattacks
    steps = [(attacker, defender)]
    if canCounter:
        steps.append((defender, attacker))

    if attacker.attackSpeed - defender.attackSpeed > 4:
        # Attacker gets an extra step
        steps.append((attacker, defender))
    
    elif defender.attackSpeed - attacker.attackSpeed > 4 and canCounter:
        # defender gets an extra step
        steps.append((defender, attacker))

    return steps


def clamp(val, maxi, mini):
    return max(mini, min(val, maxi))


def Combat_DoStep(attacker, defender):
    ch = Combat_Hit(attacker, defender)

    # Roll 2d100; success if either is less than hit
    hit = (ch - random.randint(0, 100) > 0) or (ch - random.randint(0, 100) > 0)

    if hit:
        # roll 1d100; compare with luck+crit. Double damage if the roll is low.
        crit = 1 + (random.randint(1, 100) < attacker.luk + attacker.currentWeapon.crit)
        
        damage = Combat_Damage(attacker, defender)

        # Avoid negative damage, apply crit 2x as appropriate
        damage = max(damage, 0) * crit

        Logger.Log(f"{attacker} {'BASHES' if crit==2 else 'strikes'} {defender} for {damage}!")
        died = not defender.TakeDamage(damage)
        if died:
            return DEAD
    else:
        Logger.Log(f"{attacker} Misses {defender}!")
    
    return ALIVE


def Combat_Hit(attacker, defender):
    return max(attacker.baseHit - defender.avo, 0)


def Combat_Damage(attacker:Unit, defender:Unit):
    res = defender.res if attacker.currentWeapon.magical else defender.dfn
    return max(attacker.atk - res, 0)


# Return combat data, perhaps later with a setting for monte carlo sims?
def SimulateCombat(attacker, defender, monte=False) -> tuple:
    return ()
    

def DoCombat(attacker, defender):
    map:Map = attacker.tile.map

    attacker.EquipWeapon(attacker.tentativeWeapon)
    attacker.tentativeWeapon = None
    steps = Combat_GetSteps(attacker, defender)
    for step in steps:
        result = Combat_DoStep(*step)
        if result == DEAD:
            break
    
    return map.CheckConditions()