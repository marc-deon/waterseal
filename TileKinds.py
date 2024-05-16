
from Tile import TileKind
from MovementModifiers import * # pylint: disable=unused-wildcard-import
from colors import WHITE_BLACK, GREEN_BLACK, CYAN_BLACK, BLACK_WHITE

def tile_heal(tile):
    if tile.unit:
        tile.unit.Heal(5)

# We'll likely need no more than 32 tile types (and potentially, some of those
# could be doubled at as 'palette swaps,' but that's probably more trouble than it's worth)

PLAIN    = TileKind("Plain",    " ", WHITE_BLACK, 0, 0,  "Neutral terrain"                            , NONE_IMPASS)
WALL     = TileKind("Wall",     "▣", WHITE_BLACK, 0, 0,  "Impassible except by flyers"                , GROUND_IMPASS)
CRACK    = TileKind("Crack",    "⊠", WHITE_BLACK, 0, 0,  "A weakened wall"                            , GROUND_IMPASS)
WOODS    = TileKind("Woods",    "░", GREEN_BLACK, 0, 10, "Hard for cavalry to move through."          , HORSE_SLOW | MECHA_IMPASS)
HILL     = TileKind("Hill",     "n", WHITE_BLACK, 1, 10, "Hard for non-flying units to move through." , GROUND_SLOW | MECHA_IMPASS)
RIVER    = TileKind("River",    "~", CYAN_BLACK , 0,-10, "Hard for non-flying units to move through." , GROUND_SLOW | MECHA_IMPASS)
MOUNTAIN = TileKind("Mountain", "▲", WHITE_BLACK, 3, 10, "Impassible except by flyers."               , GROUND_IMPASS)
CLIFF    = TileKind("Cliff",    "\\",WHITE_BLACK, 0, 0,  "Impassible except by flyers."               , GROUND_IMPASS)
OCEAN    = TileKind("Ocean",    "≈", CYAN_BLACK , 0, 0,  "Impassible except by flyers."               , GROUND_IMPASS)
BRIDGE   = TileKind("Bridge",   "=", WHITE_BLACK, 0, 0,  "Neutral terrain"                            , NONE_IMPASS)
HOUSE    = TileKind("House",    "H", WHITE_BLACK, 0,10,  "Somebody's home"                            , NONE_IMPASS)
DOOR     = TileKind("Door",     "▯", WHITE_BLACK, 0, 0,  "Can open with a key"                        ,IMPASS)
THRONE   = TileKind("Throne",   "h", WHITE_BLACK, 2,20,  "Chair for important people"                 ,NONE_IMPASS)
FORT     = TileKind("Fort",     "F", WHITE_BLACK, 2,20,  "Heals you every turn"                       ,NONE_IMPASS, on_TurnStart=tile_heal)
PILLAR   = TileKind("Pillar",   "I", WHITE_BLACK, 1,20,  "Holds the roof up?"                         ,NONE_IMPASS)
PEAK     = TileKind("Peak",     "^", WHITE_BLACK, 2,40,  "Holds the sky up?"                          ,HORSE_IMPASS)

# kinds = [PLAIN, WALL, WOODS, HILL, RIVER, MOUNTAIN, CLIFF, OCEAN, BRIDGE]
# 0 Plain
# 1 Wall
# 2 Woods
# 3 Hill
# 4 River
# 5 Mounta
# 6 Cliff
# 7 Ocean
# 8 Bridge