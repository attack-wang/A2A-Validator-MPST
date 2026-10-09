'''
board.py
This module defines the Board class for the Gomoku game.
The board is a standard 15x15 grid. Each cell is either empty or holds
a stone belonging to the Black or White player. The Board is responsible
for:
* storing and resetting the grid state,
* validating candidate moves (bounds + occupancy),
* placing stones,
* detecting a win (five or more unbroken stones of the same colour in a
  horizontal, vertical or diagonal direction) starting from the last
  placed stone,
* extracting the exact winning line (used to highlight it in the UI),
* detecting a draw (board completely full),
* rendering a plain-text representation of the board for console play.
'''
# Cell / player constants shared across the whole application.
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {
    BLACK: "Black",
    WHITE: "White",
}
# Symbols used by the console interface ('.' for empty cells).
PLAYER_SYMBOLS = {
    EMPTY: ".",
    BLACK: "X",
    WHITE: "O",
}
class Board:
    """A 15x15 Gomoku board that stores stones and detects wins."""
    SIZE = 15
    # The four directions that a five-in-a-row line can lie along.
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    def __init__(self, size=SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def is_valid_position(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_empty(self, row, col):
        """Return True if the cell at (row, col) contains no stone."""
        return self.grid[row][col] == EMPTY
    def is_valid_move(self, row, col):
        """Return True if a stone may be placed at (row, col)."""
        return self.is_valid_position(row, col) and self.is_empty(row, col)
    def get_stone(self, row, col):
        """Return the contents of the cell at (row, col)."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is outside the board.")
        return self.grid[row][col]
    def place_stone(self, row, col, player):
        """Place a stone for `player` at (row, col).
        Raises ValueError if the position is occupied or outside the board.
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is outside the board.")
        if not self.is_empty(row, col):
            raise ValueError(f"Position ({row}, {col}) is already occupied.")
        self.grid[row][col] = player
    def remove_stone(self, row, col):
        """Remove any stone at (row, col) (used by the undo feature)."""
        if self.is_valid_position(row, col):
            self.grid[row][col] = EMPTY
    def is_full(self):
        """Return True when every cell holds a stone (draw condition)."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def check_win(self, row, col):
        """Return the player who has five-in-a-row through (row, col), else None.
        Only the lines passing through the most recently placed stone need
        to be inspected, because a win can only be created by the last move.
        """
        player = self.grid[row][col]
        if player == EMPTY:
            return None
        for dr, dc in self.DIRECTIONS:
            count = 1
            count += self._count_direction(row, col, dr, dc, player)
            count += self._count_direction(row, col, -dr, -dc, player)
            if count >= 5:
                return player
        return None
    def get_winning_line(self, row, col):
        """Return the list of (row, col) cells forming the winning line."""
        player = self.grid[row][col]
        if player == EMPTY:
            return []
        for dr, dc in self.DIRECTIONS:
            line = [(row, col)]
            line += self._collect_direction(row, col, dr, dc, player)
            line += self._collect_direction(row, col, -dr, -dc, player)
            if len(line) >= 5:
                # Return the cells ordered along the line.
                line.sort()
                return line
        return []
    def _count_direction(self, row, col, dr, dc, player):
        """Count consecutive `player` stones from (row, col) along (dr, dc)."""
        count = 0
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.grid[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count
    def _collect_direction(self, row, col, dr, dc, player):
        """Collect consecutive `player` stones from (row, col) along (dr, dc)."""
        cells = []
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.grid[r][c] == player:
            cells.append((r, c))
            r += dr
            c += dc
        return cells
    def display(self):
        """Return a plain-text picture of the board for console play."""
        header = "    " + "  ".join(chr(ord("A") + i) for i in range(self.size))
        lines = [header]
        for r in range(self.size):
            label = f"{r + 1:>2}  "
            cells = "  ".join(PLAYER_SYMBOLS[self.grid[r][c]] for c in range(self.size))
            lines.append(label + cells)
        return "\n".join(lines)