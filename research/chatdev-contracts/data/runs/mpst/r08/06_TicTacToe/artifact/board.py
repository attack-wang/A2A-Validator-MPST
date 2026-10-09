'''
board.py
Defines the Board class, which manages the 3x3 tic-tac-toe grid.
Responsibilities:
  - Store and reset the grid state
  - Validate and apply moves
  - Detect a winning line (rows, columns, diagonals)
  - Detect a full board (draw condition)
  - Report empty cells
'''
class Board:
    """Represents the 3x3 tic-tac-toe board and its core game logic."""
    def __init__(self):
        """Initialize an empty 3x3 grid."""
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the grid and currently empty."""
        return 0 <= row < 3 and 0 <= col < 3 and self.grid[row][col] == " "
    def make_move(self, row, col, symbol):
        """
        Place `symbol` at (row, col) if the move is valid.
        Returns:
            True if the move was applied, False otherwise.
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False
    def check_winner(self):
        """
        Determine whether either symbol has completed a line.
        Returns:
            "X" or "O" if there is a winner, otherwise None.
        """
        lines = self._all_lines()
        for (r1, c1, r2, c2, r3, c3) in lines:
            if (
                self.grid[r1][c1] != " "
                and self.grid[r1][c1] == self.grid[r2][c2] == self.grid[r3][c3]
            ):
                return self.grid[r1][c1]
        return None
    def get_winning_line(self):
        """
        Return the (row, col) tuples forming the winning line, or None.
        Useful for highlighting the winning cells in the UI.
        """
        lines = self._all_lines()
        for (r1, c1, r2, c2, r3, c3) in lines:
            if (
                self.grid[r1][c1] != " "
                and self.grid[r1][c1] == self.grid[r2][c2] == self.grid[r3][c3]
            ):
                return [(r1, c1), (r2, c2), (r3, c3)]
        return None
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        return all(cell != " " for row in self.grid for cell in row)
    def get_empty_cells(self):
        """Return a list of (row, col) tuples for all empty cells."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.grid[r][c] == " "
        ]
    @staticmethod
    def _all_lines():
        """Return all 8 possible winning lines as coordinate tuples."""
        lines = []
        # Rows
        for r in range(3):
            lines.append((r, 0, r, 1, r, 2))
        # Columns
        for c in range(3):
            lines.append((0, c, 1, c, 2, c))
        # Diagonals
        lines.append((0, 0, 1, 1, 2, 2))
        lines.append((0, 2, 1, 1, 2, 0))
        return lines