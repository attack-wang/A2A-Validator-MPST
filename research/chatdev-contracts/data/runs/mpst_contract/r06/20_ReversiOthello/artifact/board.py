DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

EMPTY, BLACK, WHITE = 0, 1, 2


class Board:
    """8x8 Reversi board with move validation and disc flipping."""

    def __init__(self):
        self.size = 8
        self.reset()

    def reset(self):
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def discs_flipped(self, r, c, player):
        """Return the list of discs that would be flipped by a move at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != EMPTY:
            return []
        opponent = 3 - player
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc) and self.grid[rr][cc] == opponent:
                line.append((rr, cc))
                rr += dr
                cc += dc
            if line and self.in_bounds(rr, cc) and self.grid[rr][cc] == player:
                flips.extend(line)
        return flips

    def is_valid_move(self, r, c, player):
        return bool(self.discs_flipped(r, c, player))

    def valid_moves(self, player):
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.is_valid_move(r, c, player)]

    def place(self, r, c, player):
        flips = self.discs_flipped(r, c, player)
        if not flips:
            return False
        self.grid[r][c] = player
        for rr, cc in flips:
            self.grid[rr][cc] = player
        return True

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def score(self):
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white