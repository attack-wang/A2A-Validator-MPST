'''
cell.py
Defines the Cell class, the atomic unit of the Minesweeper board.
A Cell tracks its own state (mine, revealed, flagged) and the number of
mines in its neighborhood. All rendering-independent logic lives here.
'''
class Cell:
    '''Represents a single cell of the Minesweeper board.'''
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0  # Number of mines among the 8 neighbors.
    def reveal(self):
        '''Mark the cell as revealed. Returns True if the state changed.'''
        if self.is_revealed or self.is_flagged:
            return False
        self.is_revealed = True
        return True
    def toggle_flag(self):
        '''Toggle the flag on a covered cell. Returns True if state changed.'''
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    def has_mine(self):
        return self.is_mine
    def is_empty(self):
        '''A revealed cell with no adjacent mines (triggers flood fill).'''
        return self.adjacent_mines == 0 and not self.is_mine