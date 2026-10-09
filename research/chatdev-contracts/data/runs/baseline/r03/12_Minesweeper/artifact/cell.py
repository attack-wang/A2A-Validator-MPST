'''
Defines the Cell class, the atomic unit of the Minesweeper board.
A Cell keeps track of:
  * whether it hides a mine,
  * whether it has been revealed,
  * whether the player flagged it,
  * how many mines are located in the 8 neighbouring cells.
'''
class Cell:
    """Represents a single square of the Minesweeper grid."""
    __slots__ = ("is_mine", "is_revealed", "is_flagged", "adjacent_mines")
    def __init__(self):
        """Create a hidden, empty (mine-less, unflagged) cell."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------
    def reveal(self):
        """Mark the cell as revealed. Returns True if the state changed."""
        if self.is_revealed or self.is_flagged:
            return False
        self.is_revealed = True
        return True
    def toggle_flag(self):
        """Flag / unflag the cell. Only hidden cells can be flagged.
        Returns True if the flag state changed.
        """
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return True
    def reset(self):
        """Restore the cell to its initial hidden state."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    @property
    def is_empty(self):
        """True when the cell holds no mine and no adjacent mines."""
        return not self.is_mine and self.adjacent_mines == 0
    @property
    def is_safe(self):
        """True when the cell does not hide a mine."""
        return not self.is_mine
    def __repr__(self):
        state = "M" if self.is_mine else str(self.adjacent_mines)
        flags = []
        if self.is_revealed:
            flags.append("revealed")
        if self.is_flagged:
            flags.append("flagged")
        suffix = " ({})".format(", ".join(flags)) if flags else ""
        return "Cell[{}{}]".format(state, suffix)