'''
Board module for the Gomoku game.
Contains the Board class, which manages the 15x15 grid, validates
moves, places stones, and detects wins (five or more stones in a row
horizontally, vertically or diagonally) as well as draws.
'''
class Board:
    """Represents the Gomoku board and implements its core rules."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    # Directions used for win checking: horizontal, vertical,
    # main diagonal and anti-diagonal.
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, size=15):
        """Create an empty board of the given size (default 15x15)."""
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.last_move = None
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[self.EMPTY for _ in range(self.size)]
                     for _ in range(self.size)]
        self.last_move = None
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the board and empty."""
        return self.in_bounds(row, col) and self.grid[row][col] == self.EMPTY
    def place_stone(self, row, col, player):
        """Place a stone for `player` at (row, col).
        Returns True if the move was legal and has been applied,
        otherwise False.
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        self.last_move = (row, col)
        return True
    def get_stone(self, row, col):
        """Return the value at (row, col); EMPTY when out of bounds."""
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return self.EMPTY
    def is_full(self):
        """Return True when no empty intersections remain (draw)."""
        for row in self.grid:
            if self.EMPTY in row:
                return False
        return True
    def _line_cells(self, row, col, dr, dc):
        """Collect consecutive same-colored cells through (row, col).
        Walks in direction (dr, dc) and its opposite starting from the
        stone at (row, col) and returns the list of coordinates, ordered
        from the negative end to the positive end.
        """
        player = self.grid[row][col]
        cells = [(row, col)]
        r, c = row + dr, col + dc
        while self.in_bounds(r, c) and self.grid[r][c] == player:
            cells.append((r, c))
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while self.in_bounds(r, c) and self.grid[r][c] == player:
            cells.insert(0, (r, c))
            r -= dr
            c -= dc
        return cells
    def check_win(self, row, col):
        """Return True if the stone just placed at (row, col) wins."""
        if self.grid[row][col] == self.EMPTY:
            return False
        for dr, dc in self.DIRECTIONS:
            if len(self._line_cells(row, col, dr, dc)) >= 5:
                return True
        return False
    def get_winning_line(self, row, col):
        """Return the coordinates of the winning five-in-a-row.
        Returns a list of (row, col) tuples (at least five cells) when
        the move at (row, col) completes a row of five, otherwise None.
        """
        if self.grid[row][col] == self.EMPTY:
            return None
        for dr, dc in self.DIRECTIONS:
            cells = self._line_cells(row, col, dr, dc)
            if len(cells) >= 5:
                return cells
        return None