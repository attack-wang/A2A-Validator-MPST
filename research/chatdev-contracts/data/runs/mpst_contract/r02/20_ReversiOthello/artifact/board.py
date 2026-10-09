"""Board logic for Reversi (Othello)."""
SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


class Board:
    def __init__(self):
        self.grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.grid[3][3] = 'W'
        self.grid[3][4] = 'B'
        self.grid[4][3] = 'B'
        self.grid[4][4] = 'W'

    def in_bounds(self, r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def flips_for(self, player, r, c):
        """Return list of discs that would be flipped by playing at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != '.':
            return []
        opp = 'W' if player == 'B' else 'B'
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc) and self.grid[rr][cc] == opp:
                line.append((rr, cc))
                rr += dr
                cc += dc
            if line and self.in_bounds(rr, cc) and self.grid[rr][cc] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player):
        return [(r, c) for r in range(SIZE) for c in range(SIZE)
                if self.flips_for(player, r, c)]

    def apply_move(self, player, r, c):
        flips = self.flips_for(player, r, c)
        if not flips:
            return False
        self.grid[r][c] = player
        for rr, cc in flips:
            self.grid[rr][cc] = player
        return True

    def score(self):
        b = sum(row.count('B') for row in self.grid)
        w = sum(row.count('W') for row in self.grid)
        return b, w

    def is_full(self):
        return all(cell != '.' for row in self.grid for cell in row)

    def has_move(self, player):
        return bool(self.valid_moves(player))