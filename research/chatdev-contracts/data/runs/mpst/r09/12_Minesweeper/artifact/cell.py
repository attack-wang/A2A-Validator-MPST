"""
Cell model for the Minesweeper game.
A Cell holds all state for a single square on the board: whether it hides
a mine, whether it has been revealed, whether the player flagged it, and
how many mines are adjacent to it.
"""
class Cell:
    """Represents a single square of the Minesweeper board."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.reset()
    def reset(self):
        """Restore the cell to its initial, unrevealed state."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def can_reveal(self):
        """A cell can be revealed only if it is hidden and not flagged."""
        return not self.is_revealed and not self.is_flagged
    def reveal(self):
        """Mark the cell as revealed. Returns True if the state changed."""
        if not self.can_reveal():
            return False
        self.is_revealed = True
        return True
    def toggle_flag(self):
        """Toggle the flag on a hidden cell. Returns True if state changed."""
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    def __repr__(self):
        return "Cell(row={}, col={}, mine={}, revealed={}, flagged={}, adj={})".format(
            self.row, self.col, self.is_mine, self.is_revealed,
            self.is_flagged, self.adjacent_mines)