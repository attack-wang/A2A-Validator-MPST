"""Core Gomoku game logic: board state, move validation, and win detection."""

BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
WIN_LENGTH = 5


class Board:
    """15x15 Gomoku board with move placement and win detection."""

    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        return self.grid[row][col] == EMPTY

    def place(self, row, col, player):
        """Place a stone; return True on success, False if the move is invalid."""
        if not self.in_bounds(row, col) or not self.is_empty(row, col):
            return False
        self.grid[row][col] = player
        return True

    def check_win(self, row, col):
        """Return the winning player if the stone at (row, col) completes five in a row."""
        player = self.grid[row][col]
        if player == EMPTY:
            return None
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while self.in_bounds(r, c) and self.grid[r][c] == player:
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= WIN_LENGTH:
                return player
        return None

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)