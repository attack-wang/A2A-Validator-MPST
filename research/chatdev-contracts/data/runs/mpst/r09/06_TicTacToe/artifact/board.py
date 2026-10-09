'''
board.py
Defines the Board class, which manages the 3x3 tic-tac-toe grid.
Responsibilities:
  * storing the state of the nine cells,
  * validating and applying moves,
  * detecting win / draw / ongoing states,
  * providing a text rendering of the board (useful for logs and tests).
'''
class Board:
    """Represents the 3x3 tic-tac-toe board and its rules."""
    EMPTY = " "
    # All eight lines that win the game: 3 rows, 3 columns, 2 diagonals.
    WINNING_LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    )
    def __init__(self):
        """Create an empty 3x3 board."""
        self.cells = [self.EMPTY] * 9
    def reset(self):
        """Clear every cell so a new round can start."""
        self.cells = [self.EMPTY] * 9
    def is_valid_move(self, index):
        """Return True if `index` is inside the board and the cell is empty."""
        return 0 <= index < len(self.cells) and self.cells[index] == self.EMPTY
    def make_move(self, index, symbol):
        """
        Place `symbol` ("X" or "O") in cell `index`.
        Returns True when the move was applied, False when the cell was
        already taken or the index was out of range.
        """
        if not self.is_valid_move(index):
            return False
        self.cells[index] = symbol
        return True
    def check_winner(self):
        """
        Evaluate the board.
        Returns a tuple (status, symbol, line) where
          status -- "win", "draw" or "ongoing",
          symbol -- the winning mark (None unless status == "win"),
          line   -- the three winning cell indices (None unless status == "win").
        """
        for line in self.WINNING_LINES:
            a, b, c = line
            if (self.cells[a] != self.EMPTY
                    and self.cells[a] == self.cells[b] == self.cells[c]):
                return "win", self.cells[a], line
        if self.is_full():
            return "draw", None, None
        return "ongoing", None, None
    def is_full(self):
        """Return True when all nine cells are occupied."""
        return all(cell != self.EMPTY for cell in self.cells)
    def available_moves(self):
        """Return the indices of all empty cells."""
        return [i for i, cell in enumerate(self.cells) if cell == self.EMPTY]
    def display(self):
        """Return a human-readable picture of the board."""
        lines = []
        for row in range(3):
            cells = self.cells[row * 3:(row + 1) * 3]
            lines.append(" " + " | ".join(cells) + " ")
            if row < 2:
                lines.append("---+---+---")
        return "\n".join(lines)