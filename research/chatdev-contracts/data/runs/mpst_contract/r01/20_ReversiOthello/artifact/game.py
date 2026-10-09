"""Reversi (Othello) core game logic."""
SIZE = 8
EMPTY, BLACK, WHITE = '.', 'B', 'W'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1)]


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * SIZE for _ in range(SIZE)]
        mid = SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def flips_for(self, player, r, c):
        """Return discs that would be flipped if `player` plays at (r, c)."""
        if not self.in_bounds(r, c) or self.grid[r][c] != EMPTY:
            return []
        opponent = WHITE if player == BLACK else BLACK
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

    def valid_moves(self, player):
        moves = {}
        for r in range(SIZE):
            for c in range(SIZE):
                if self.grid[r][c] == EMPTY:
                    flips = self.flips_for(player, r, c)
                    if flips:
                        moves[(r, c)] = flips
        return moves

    def apply_move(self, player, r, c):
        flips = self.flips_for(player, r, c)
        if not flips:
            return False
        self.grid[r][c] = player
        for rr, cc in flips:
            self.grid[rr][cc] = player
        return True

    def score(self):
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def has_any_move(self, player):
        return bool(self.valid_moves(player))