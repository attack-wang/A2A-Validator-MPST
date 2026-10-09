'''
board.py
Board module for the Tic-Tac-Toe game.
Defines the Board class: a 3x3 grid supporting labeled display, symbol
placement, win detection, draw detection, and empty-cell checks.
'''
class Board:
    """A 3x3 tic-tac-toe board with display and win/draw detection."""
    def __init__(self):
        """Create an empty 3x3 grid."""
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
    def display(self):
        """Print the board with 1-based row and column labels."""
        print("\n    1   2   3")
        for index, row in enumerate(self.grid, start=1):
            print(f"  {index} {row[0]} | {row[1]} | {row[2]}")
            if index < 3:
                print("   ---+---+---")
        print()
    def is_cell_empty(self, row: int, col: int) -> bool:
        """Return True if the cell at 0-based (row, col) is empty."""
        return self.grid[row][col] == ' '
    def make_move(self, row: int, col: int, symbol: str):
        """Place the given symbol at 0-based (row, col)."""
        self.grid[row][col] = symbol
    def is_full(self) -> bool:
        """Return True when every cell is occupied (draw condition)."""
        return all(cell != ' ' for row in self.grid for cell in row)
    def check_winner(self):
        """Return the winning symbol ('X' or 'O'), or None if no winner yet."""
        lines = []
        for i in range(3):
            lines.append(self.grid[i])                       # rows
            lines.append([self.grid[0][i], self.grid[1][i], self.grid[2][i]])  # columns
        lines.append([self.grid[0][0], self.grid[1][1], self.grid[2][2]])      # main diagonal
        lines.append([self.grid[0][2], self.grid[1][1], self.grid[2][0]])      # anti-diagonal
        for line in lines:
            if line[0] != ' ' and line[0] == line[1] == line[2]:
                return line[0]
        return None