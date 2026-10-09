BLACK, WHITE, EMPTY = 'B', 'W', '.'
DIRS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class Board:
    """Reversi board with move validation, disc flipping and scoring."""

    def __init__(self, size=8):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]
        mid = size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def flips_for(self, r, c, player):
        """Return the discs that would be flipped by placing `player` at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != EMPTY:
            return []
        opponent = WHITE if player == BLACK else BLACK
        flips = []
        for dr, dc in DIRS:
            line = []
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc) and self.grid[rr][cc] == opponent:
                line.append((rr, cc))
                rr += dr
                cc += dc
            if line and self.in_bounds(rr, cc) and self.grid[rr][cc] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player):
        return {(r, c) for r in range(self.size) for c in range(self.size)
                if self.flips_for(r, c, player)}

    def apply_move(self, r, c, player):
        """Place `player` at (r, c), flip captured discs, return the flipped list."""
        flips = self.flips_for(r, c, player)
        if not flips:
            return []
        self.grid[r][c] = player
        for rr, cc in flips:
            self.grid[rr][cc] = player
        return flips

    def score(self):
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)