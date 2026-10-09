"""Board logic for Reversi (Othello)."""

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Board:
    SIZE = 8
    EMPTY, BLACK, WHITE = 0, 1, 2

    def __init__(self):
        self.grid = [[self.EMPTY] * self.SIZE for _ in range(self.SIZE)]
        mid = self.SIZE // 2
        self.grid[mid - 1][mid - 1] = self.WHITE
        self.grid[mid][mid] = self.WHITE
        self.grid[mid - 1][mid] = self.BLACK
        self.grid[mid][mid - 1] = self.BLACK

    def in_bounds(self, r, c):
        return 0 <= r < self.SIZE and 0 <= c < self.SIZE

    def discs_flipped(self, player, r, c):
        """Return list of (r, c) discs that would be flipped by placing player's disc at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != self.EMPTY:
            return []
        opponent = 3 - player
        flipped = []
        for dr, dc in DIRECTIONS:
            line = []
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc) and self.grid[nr][nc] == opponent:
                line.append((nr, nc))
                nr, nc = nr + dr, nc + dc
            if line and self.in_bounds(nr, nc) and self.grid[nr][nc] == player:
                flipped.extend(line)
        return flipped

    def valid_moves(self, player):
        """Return dict mapping (r, c) -> list of discs flipped for each valid move."""
        moves = {}
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == self.EMPTY:
                    flips = self.discs_flipped(player, r, c)
                    if flips:
                        moves[(r, c)] = flips
        return moves

    def apply_move(self, player, r, c):
        """Place a disc and flip captured discs. Returns True if the move was valid."""
        flips = self.discs_flipped(player, r, c)
        if not flips:
            return False
        self.grid[r][c] = player
        for fr, fc in flips:
            self.grid[fr][fc] = player
        return True

    def is_full(self):
        return all(cell != self.EMPTY for row in self.grid for cell in row)

    def score(self):
        black = sum(row.count(self.BLACK) for row in self.grid)
        white = sum(row.count(self.WHITE) for row in self.grid)
        return black, white