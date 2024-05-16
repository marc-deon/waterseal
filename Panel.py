import curses
import itertools
from Logger import Logger

#import config
from Border import PrintBorder

class Panel:

    @property
    def contentSize(self):
        return self.h, self.w

    @property
    def page(self):
        return self.contentSize

    def __init__(self, h, w, y=0, x=0, title=None):
        """A pad with 1 character border on every side, and a title.\
\nNote that the given height and width are for the border size.\
Content size will be 2 less in each direction, so h, w must be > 2.\
\n\nY and x should generally be left at zero unless this is a popup.
"""

        assert h > 2
        assert w > 2

        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.title = title

        # self.menu = None

        self.content = curses.newpad(h-2, w-2)
        self.border = curses.newpad(h, w)

        self.GenerateBorder()

    def GenerateBorder(self):
        s = PrintBorder(self.w-3, self.h-3, self.title)
        self.border.addstr(0,0, s)
        self.DrawBorder()

    def Rename(self, title):
        self.title = title
        self.GenerateBorder()

    def Draw(self):
        """Draw the border+title and content of this panel"""
        # Seperated into two different functions for the sake of child classes
        
        # Args A, B: 'camera position' top left
        # Args C, D: 'screen position' top left
        # Args E, F: 'screen position' bottom right
        self.DrawBorder()
        self.DrawContent()


    def noutrefresh(self):
        self.DrawBorder()
        self.DrawContent()

    def DrawBorder(self):
        """Draw the border and title of this panel"""
        self.border.noutrefresh(0, 0, self.y, self.x, self.h+self.y-2, self.w+self.x-2)

    def DrawContent(self):
        """Draw the content of this panel"""
        # if self.menu:
        #     self.menu.Print()
        self.content.noutrefresh(0, 0, self.y+1, self.x+1, self.h+self.y-3, self.w+self.x-3)

    def Move(self, y, x):
        """Move the vertical and horizontal position of this panel by y and x"""
        self.y, self.x = y, x

    def move(self, y, x):
        """Move the content cursor position to (y,x)"""
        self.content.move(y, x)

    def Resize(self, h, w):
        """Set the height and width of this panel to h and w"""
        import config
        self.h = h
        self.w = w
        self.content.resize(h-2, w-2)
        self.border.resize(h, w)
        config.AlignColumns()

        self.GenerateBorder()

    def Grow(self, dy=0, dx=0):
        """Change the height and width of this Panel by dy and dx"""
        import config
        self.h+=dy
        self.w+=dx
        self.content.resize(self.h-2, self.w-2)
        self.border.resize(self.h, self.w)
        config.AlignColumns()

        self.GenerateBorder()

    def addstr(self, *args):
        """
        Add a string to a curses window. If mode is given 
        (e.g. curses.A_BOLD), then format text accordingly. We do very 
        rudimentary wrapping on word boundaries.

        Raise WindowFullException if we run out of room.
        """
        height, width = self.content.getmaxyx()
        height = height-1 # what?

        y, x = self.content.getyx() # Coords of cursor
        s = ""
        mode = 0
        

        # String given without mode
        if len(args) == 1:
            s = args[0]

        # String given with mode
        elif len(args) == 2:
            s = args[0]
            mode = args[1]

        # y, x, and string given
        elif len(args) == 3:
            y = args[0]
            x = args[1]
            s = args[2]

        # y, x, string, mode given
        elif len(args) == 4:
            y = args[0]
            x = args[1]
            s = args[2]
            mode = args[3]

        if y >= height:
            self.Grow(1, 0)
            self.addstr(*args)
            return


        # If the whole string fits on the current line, just add it all at once
        if len(s) + x < width:
            self.content.addstr(y, x, s, mode)

        # Otherwise, split on word boundaries and write each token individually
        else:
            for word in words_and_spaces(s):
                if len(word) + x < width:
                    self.content.addstr(y, x, word, mode)
                else:
                    if y == height:
                        # Can't go down another line
                        raise Exception(f"{self.title} panel full")
                        # self.Grow(1, 0)
                    self.content.addstr(y+1, 0, word, mode)
                (y, x) = self.content.getyx()

    def erase(self):
        self.content.erase()

    def clear(self):
        self.content.clear()
        # Logger.Log(f"{self.title} cleared")

    def getyx(self):
        return self.content.getyx()

def words_and_spaces(s):
    """
    >>> words_and_spaces('spam eggs ham')
    ['spam', ' ', 'eggs', ' ', 'ham']
    """
    # Inspired by http://stackoverflow.com/a/8769863/262271

    # Split only on spaces; leave tabs and newlines
    s = s.split(' ')

    # Chain together words and spaces (now as invidual elements, rather than characters in a string)
    s = zip(s, itertools.repeat(' '))

    # Words and spaces have been paired off into 2tuples; flatten them
    s = itertools.chain.from_iterable(s)

    # Bake into a list and drop the last space
    return list(s)[:-1]


#addstr, words_and_spaces taken with modification from http://colinmorris.github.io/blog/word-wrap-in-pythons-curses-library
