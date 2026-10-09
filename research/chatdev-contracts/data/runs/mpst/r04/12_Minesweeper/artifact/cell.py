'''
cell.py
Defines the Cell class: the state of a single square on the
Minesweeper board (mine, revealed, flagged, adjacent mine count).
'''
class Cell:
    """Represents a single cell on the Minesweeper board."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0