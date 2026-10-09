'''
board.py
Defines the Board class, which encapsulates the state and logic of the
tic-tac-toe playing grid.
Responsibilities:
    * Store the 3x3 grid of cell values ('X', 'O', or ' ').
    * Validate and apply player moves.
    * Detect win conditions (rows, columns, diagonals).
    * Detect draw conditions (board full with no winner).
    * Provide the coordinates of the winning line so the UI can highlight it.
    * Reset the board for a new round.
'''
class Board:
    """Represents the 3x3 tic-tac-toe board and its game logic."""
    SIZE = 3  # Board is a standard 3x3 grid.
    def __init__(self):
        """Create an empty 3x3 board."""
        self.reset()
    def reset(self):
        """Clear the board so a new round can begin."""
        self.grid = [[' ' for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the board and still empty."""
        return (
            0 <= row < self.SIZE
            and 0 <= col < self.SIZE
            and self.grid[row][col] == ' '
        )
    def make_move(self, row, col, symbol):
        """
        Place `symbol` at (row, col) if the move is legal.
        Returns:
            True  -> the move was applied.
            False -> the move was rejected (out of range or cell occupied).
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = symbol
        return True
    def is_full(self):
        """Return True when every cell has been played (draw condition)."""
        return all(self.grid[r][c] != ' ' for r in range(self.SIZE) for c in range(self.SIZE))
    def get_available_moves(self):
        """Return a list of (row, col) tuples for all empty cells."""
        return [
            (r, c)
            for r in range(self.SIZE)
            for c in range(self.SIZE)
            if self.grid[r][c] == ' '
        ]
    def check_winner(self):
        """
        Determine whether either symbol has completed a line.
        Returns:
            'X' or 'O' if that symbol has a winning line, otherwise None.
        """
        for line in self._all_lines():
            symbols = [self.grid[r][c] for (r, c) in line]
            if symbols[0] != ' ' and symbols[0] == symbols[1] == symbols[2]:
                return symbols[0]
        return None
    def get_winning_line(self):
        """
        Return the coordinates of the completed line, if any.
        Returns:
            A list of three (row, col) tuples describing the winning line,
            or None when no player has won yet.
        """
        for line in self._all_lines():
            symbols = [self.grid[r][c] for (r, c) in line]
            if symbols[0] != ' ' and symbols[0] == symbols[1] == symbols[2]:
                return line
        return None
    def _all_lines(self):
        """Yield every possible winning line on the board (8 total)."""
        lines = []
        # Rows
        for r in range(self.SIZE):
            lines.append([(r, c) for c in range(self.SIZE)])
        # Columns
        for c in range(self.SIZE):
            lines.append([(r, c) for r in range(self.SIZE)])
        # Diagonals
        lines.append([(i, i) for i in range(self.SIZE)])
        lines.append([(i, self.SIZE - 1 - i) for i in range(self.SIZE)])
        return lines