'''
cell.py — a single Minesweeper cell holding its state and flag behaviour.
'''
class Cell:
    """A single cell on the Minesweeper board."""
    __slots__ = ("is_mine", "is_revealed", "is_flagged", "adjacent_mines")
    def __init__(self):
        """Create a hidden, unflagged, mine-free cell."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def can_flag(self):
        """A flag can only be placed on an unrevealed cell."""
        return not self.is_revealed
    def toggle_flag(self):
        """Toggle the flag if allowed; return True when the state changed."""
        if self.can_flag():
            self.is_flagged = not self.is_flagged
            return True
        return False