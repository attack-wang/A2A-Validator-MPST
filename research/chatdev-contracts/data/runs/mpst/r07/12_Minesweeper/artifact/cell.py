'''
cell.py
Cell model for Minesweeper: a single grid square with its mine,
reveal, flag and adjacency state.
'''
class Cell:
    """One square of the Minesweeper board."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.exploded = False      # True only for the mine the player clicked
        self.wrong_flag = False    # True for flagged cells that held no mine
    def reveal(self):
        """Mark this cell as uncovered."""
        self.is_revealed = True
    def toggle_flag(self):
        """Flag/unflag this cell; revealed cells can never be flagged."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
    def reset(self):
        """Restore the cell to its pristine, face-down state."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.exploded = False
        self.wrong_flag = False