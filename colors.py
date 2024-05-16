import curses

CYAN_BLACK = 2
RED_BLACK = 3
GREEN_BLACK = 4
YELLOW_BLACK = 5
WHITE_BLACK = 6
COLOR_ERROR = 7
BLACK_WHITE = 8
RED_WHITE = 9
BLUE_BLACK = 10
BLACK_WHITE = 11

def InitColors():
    ## Changed at runtime

    # Current unit party
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    ## Static
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_GREEN)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)