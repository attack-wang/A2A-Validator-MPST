'''
board.py
Defines the Board class, which manages the 3x3 tic-tac-toe grid.
Responsibilities include move validation, placing marks, detecting
winning lines, and identifying draw conditions.
'''
class Board:
    """Manages the 3x3 tic-tac-toe board, its moves, and end-game detection."""
    EMPTY = " "
    def __init__(self):
        """Initialize an empty 3x3 grid."""
        self.grid = [[self.EMPTY for _ in range(3)] for _ in range(3)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[self.EMPTY for _ in range(3)] for _ in range(3)]
    def is_valid_move(self, row, col):
        """Return True if (row, col) lies inside the board and is empty."""
        return (
            0 <= row < 3
            and 0 <= col < 3
            and self.grid[row][col] == self.EMPTY
        )
    def make_move(self, row, col, player):
        """
        Place `player`'s mark at (row, col) when the move is valid.
        Returns:
            bool: True if the mark was placed, False otherwise.
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            return True
        return False
    def _winning_lines(self):
        """Yield every line (tuple of three cells) that can win the game."""
        for i in range(3):
            yield ((i, 0), (i, 1), (i, 2))   # row i
            yield ((0, i), (1, i), (2, i))   # column i
        yield ((0, 0), (1, 1), (2, 2))       # main diagonal
        yield ((0, 2), (1, 1), (2, 0))       # anti-diagonal
    def get_winning_line(self):
        """
        Find the line of three identical marks, if any.
        Returns:
            list[(int, int)] | None: the three (row, col) cells of the
            winning line, or None when there is no winner yet.
        """
        for line in self._winning_lines():
            marks = [self.grid[r][c] for r, c in line]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                return list(line)
        return None
    def check_winner(self):
        """
        Determine the winner of the current board, if any.
        Returns:
            str | None: "X" or "O" when someone has won, otherwise None.
        """
        line = self.get_winning_line()
        if line:
            row, col = line[0]
            return self.grid[row][col]
        return None
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        return all(cell != self.EMPTY for row in self.grid for cell in row)
    def get_available_moves(self):
        """Return a list of (row, col) tuples for all empty cells."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.grid[r][c] == self.EMPTY
        ]
    def display(self):
        """Return a human-readable string rendering of the board."""
        lines = ["    0   1   2", "  -------------"]
        for r in range(3):
            row = self.grid[r]
            lines.append(f"{r} | {row[0]} | {row[1]} | {row[2]} |")
            lines.append("  -------------")
        return "\n".join(lines)