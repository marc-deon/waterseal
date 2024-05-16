from ColoredPanel import ColoredPanel
from Menu import Menu
from Panel import Panel
from Map import Map

# Feel free to set these as a user.

initial_statsSize   = 24, 17
initial_terrainSize = 24, 9
initial_logSize     = 32, -1
initial_menuSize    = 24, 13

# These are placeholders for global variables; don't touch them.
statsSize = initial_statsSize[0], initial_statsSize[1]
terrainSize = initial_terrainSize[0], initial_terrainSize[1]
logSize = initial_logSize[0], initial_logSize[1]
menuSize = initial_menuSize[0], initial_menuSize[1]
_screen = None

contentW = 0
contentH = 0
contentSize = 0,0

mapPanel = None
terrainPanel = None
statsPanel = None
logPanel = None
menuPanel = None
# actionMenu = None

panelColumns = []

def GetContentSize(screen, m):
    maxY,maxX = screen.getmaxyx()
    maxContentW = maxX - statsSize[0] - logSize[0] - 4
    maxContentH = maxY - 4
    contentW = min(maxContentW, m.x if m else 0)
    contentH = min(maxContentH, m.y if m else 0)
    contentSize = contentW+3, contentH+3
    return contentSize


def ResizeScreen(screen, m):
    global mapPanel, terrainPanel, statsPanel, logPanel, menuPanel
    global contentSize, statsSize, terrainSize, menuSize, logSize

    maxY,_ = screen.getmaxyx()

    # - 2 for stats border and log border
    contentSize = GetContentSize(screen, m)

    if initial_logSize[1] == -1:
        logSize = logSize[0], maxY-1

    mapPanel.Resize(contentSize[1], contentSize[0])
    terrainPanel.Resize(terrainSize[1], terrainSize[0])
    statsPanel.Resize(statsSize[1], statsSize[0])
    logPanel.Resize(logSize[1], logSize[0])
    menuPanel.Resize(menuSize[1], menuSize[0])

    AlignColumns()

def Update_Regular():
    pass
def Update_Unit():
    pass
def Update_Target():
    pass
def Update_Enemy():
    pass

def Config_Start(screen):

    Config_Size(screen)
    AlignColumns()

def Config_Size(screen=None):
    global logSize, contentSize, statsSize , terrainSize, menuSize
    global mapPanel, terrainPanel, statsPanel, logPanel, menuPanel
    # global actionMenu
    global _screen

    # The screen is the top level abstraction provided by curses.
    # Windows are section of the screen that can be edited invidually.
    #  They must be refreshed manually to display to the screen.
    # Pads are special windows that may be larger than the screen and
    #  Cropped or panned. This will be used for the main map.
    #
    # NOTE: All curses coordinates are in (y,x) and (height,width).

    # Map window size without border

    _screen = screen or _screen
    screen = _screen
    maxY, _ = screen.getmaxyx()

    m = Map.instance()

    contentSize = GetContentSize(screen, m)

    if initial_logSize[1] == -1:
        logSize = logSize[0], maxY+1

    mapPanel     = Panel(contentSize[1], contentSize[0], title="Map View")
    terrainPanel = Panel(terrainSize[1], terrainSize[0], title="Terrain")
    statsPanel   = ColoredPanel(statsSize[1]  , statsSize[0]  , title="Unit")
    logPanel     = Panel(logSize[1]    , logSize[0]    , title="Log")
    menuPanel    = Panel(menuSize[1]   , menuSize[0]   , title="Action")
    # actionMenu   = Menu(menuPanel.content)

def AlignColumns():
    global panelColumns
    _screen.erase()
    panelColumns = [
        [logPanel],
        [mapPanel],
        [statsPanel, terrainPanel],
        [menuPanel]
    ]

    accumulatedWidth = 0
    for column in panelColumns:
        maxWidth = 0
        accumulatedHeight = 0
        for panel in column:
            maxWidth = max(panel.w, maxWidth)
            panel.Move(accumulatedHeight, accumulatedWidth)
            accumulatedHeight += panel.h-1
        accumulatedWidth += maxWidth - 1
