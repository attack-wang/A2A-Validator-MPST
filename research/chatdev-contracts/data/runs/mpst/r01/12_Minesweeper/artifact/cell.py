'''
cell.py
Defines the Cell class, representing a single square on the Minesweeper
board. Each cell tracks whether it hides a mine, whether it has been
revealed or flagged, and how many mines are adjacent to it.
'''
class Cell:
    """A single square of the Minesweeper board."""
    __slots__ = ("row", "col", "is_mine", "is_revealed", "is_flagged",
                 "adjacent_mines")
    def __init__(self, row, col):
        """Create a hidden, empty (mine-free) cell at the given position."""
        self.row = row
        self.col = col
        self.reset()
    def reset(self):
        """Restore the cell to its initial hidden, mine-free state."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def reveal(self):
        """Mark the cell as revealed. Returns True if it was hidden before."""
        if self.is_revealed:
            return False
        self.is_revealed = True
        return True
    def toggle_flag(self):
        """Toggle the flag on a hidden cell. Flags on revealed cells are ignored.
        Returns True if the flag state changed.
        """
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    @property
    def is_empty(self):
        """True when the cell is revealed and has no adjacent mines."""
        return self.is_revealed and self.adjacent_mines == 0 and not self.is_mine
    def __repr__(self):
        state = "M" if self.is_mine else str(self.adjacent_mines)
        flags = "F" if self.is_flagged else ("R" if self.is_revealed else "H")
        return f"Cell({self.row},{self.col},{state},{flags})"