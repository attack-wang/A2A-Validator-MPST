'''display.py — Terminal rendering: board grid, player status, message log.'''
def grid_coords(pos, total):
    """Map a board position onto (row, col) of a square perimeter grid.
    Derived from `total` so the display can never desync from the board:
    pos 0 sits at the bottom-right corner and movement is clockwise.
    """
    side = total // 4 + 1
    seg = total // 4
    last = side - 1
    if pos <= seg:
        return (last, last - pos)          # bottom row, right to left
    if pos <= 2 * seg:
        return (last - (pos - seg), 0)     # left column, bottom to top
    if pos <= 3 * seg:
        return (0, pos - 2 * seg)          # top row, left to right
    return (pos - 3 * seg, last)           # right column, top to bottom