"""Reversi (Othello) board logic: valid moves, disc flipping, scoring."""

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
EMPTY, BLACK, WHITE = 0, 1, 2


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * 8 for _ in range(8)]
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def flips_for(self, r, c, player):
        """Return list of discs flipped if player plays at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != EMPTY:
            return []
        opp = 3 - player
        flips = []
        for dr, dc in DIRS:
            line = []
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc) and self.grid[nr][nc] == opp:
                line.append((nr, nc))
                nr += dr
                nc += dc
            if line and self.in_bounds(nr, nc) and self.grid[nr][nc] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player):
        return [(r, c) for r in range(8) for c in range(8)
                if self.flips_for(r, c, player)]

    def place(self, r, c, player):
        flips = self.flips_for(r, c, player)
        if not flips:
            return False
        self.grid[r][c] = player
        for fr, fc in flips:
            self.grid[fr][fc] = player
        return True

    def score(self):
        b = sum(row.count(BLACK) for row in self.grid)
        w = sum(row.count(WHITE) for row in self.grid)
        return b, w

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def game_over(self):
        return self.is_full() or not (self.valid_moves(BLACK)
                                      or self.valid_moves(WHITE))