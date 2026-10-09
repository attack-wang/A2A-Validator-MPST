'''
board.py
Board module: represents the 3x3 tic-tac-toe grid, validates moves,
and detects winning lines.
'''
EMPTY_CELL = " "
class Board:
    """A 3x3 tic-tac-toe board: stores marks, validates moves, finds wins."""
    def __init__(self):
        # Build the empty 3x3 grid via reset() so init and new rounds share one code path.
        self.reset()
    def reset(self):
        """Clear the board to a 3x3 grid of empty cells."""
        self.grid = [[EMPTY_CELL for _ in range(3)] for _ in range(3)]
    def make_move(self, row, col, symbol):
        """
        Place `symbol` at (row, col).
        Returns True if the move is legal (in bounds and cell empty) and was applied;
        returns False for out-of-range coordinates or an already-occupied cell.
        """
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self.grid[row][col] != EMPTY_CELL:
            return False
        self.grid[row][col] = symbol
        return True
    def is_full(self):
        """Return True when all nine cells are occupied (draw condition)."""
        return all(self.grid[r][c] != EMPTY_CELL for r in range(3) for c in range(3))
    def get_winning_line(self, symbol):
        """Return the list of (row, col) cells forming a winning line for symbol, or None."""
        # Check rows
        for r in range(3):
            if all(self.grid[r][c] == symbol for c in range(3)):
                return [(r, c) for c in range(3)]
        # Check columns
        for c in range(3):
            if all(self.grid[r][c] == symbol for r in range(3)):
                return [(r, c) for r in range(3)]
        # Check main diagonal
        if all(self.grid[i][i] == symbol for i in range(3)):
            return [(i, i) for i in range(3)]
        # Check anti-diagonal
        if all(self.grid[i][2 - i] == symbol for i in range(3)):
            return [(i, 2 - i) for i in range(3)]
        return None