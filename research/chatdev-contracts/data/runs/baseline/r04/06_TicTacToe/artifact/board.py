'''
Board module for the Tic-Tac-Toe game.
This module defines the Board class, which manages the state of the
standard 3x3 grid. It is responsible for rendering the board, validating
and applying moves, detecting winning lines, and checking whether the
board is full (draw condition).
'''
class Board:
    """Represents the 3x3 Tic-Tac-Toe board and its rules."""
    def __init__(self):
        """Initialize an empty 3x3 grid filled with blank spaces."""
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
    def display(self):
        """Print the current board with row and column coordinates."""
        print()
        print("      1   2   3")
        print("    +---+---+---+")
        for row_index, row in enumerate(self.grid, start=1):
            print(f"  {row_index} | {row[0]} | {row[1]} | {row[2]} |")
            print("    +---+---+---+")
        print()
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the grid and still empty."""
        return (
            0 <= row < 3
            and 0 <= col < 3
            and self.grid[row][col] == " "
        )
    def make_move(self, row, col, symbol):
        """Place the given symbol on the board if the move is valid.
        Returns True when the move was applied, False otherwise.
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = symbol
            return True
        return False
    def check_winner(self):
        """Return the winning symbol ('X' or 'O'), or None if no winner yet.
        Checks all rows, all columns, and both diagonals.
        """
        # Check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        # Check columns
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != " ":
                return self.grid[0][col]
        # Check main diagonal (top-left to bottom-right)
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
            return self.grid[0][0]
        # Check anti-diagonal (top-right to bottom-left)
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
            return self.grid[0][2]
        return None
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        return all(cell != " " for row in self.grid for cell in row)