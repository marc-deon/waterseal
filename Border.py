from math import ceil, floor
def PrintBorder(x, y, title=""):
    """
    Generate a border for content of size (x, y) with an optional header title.
    Truncates title if longer than the width of the border.
    """

    # if title == None:
        # title = ""

    if title != "":
        title = "[" + title + "]"

    # Trim title if neccesary
    if len(title) > x:
        title = title[:x]

    # Total number of horizontal lines to fill with
    diff = x - len(title)
    left = ceil(diff/2)
    right = floor(diff/2)

    s = "╭" + "─" * left + title + "─" * right + "╮\n"
    for _ in range(y):
        s+="│" + " "*x + "│\n"
    s+="╰" + "─" * x + "╯"
    return s
