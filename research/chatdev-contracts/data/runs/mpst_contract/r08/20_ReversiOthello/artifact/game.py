"""Reversi (Othello) game logic: board state, valid moves, disc flipping, scoring."""

SIZE = 8
EMPTY, BLACK, WHITE = '.', 'B', 'W'
DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class Reversi:
    """8x8 Reversi board with turn handling for two players."""

    def __init__(self):
        self.board = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK
        self.passes = 0

    @staticmethod
    def opponent(player):
        return WHITE if player == BLACK else BLACK

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def flips_for(self, r, c, player):
        """Discs that would be flipped if `player` plays at (r, c); [] if illegal."""
        if not self.in_bounds(r, c) or self.board[r][c] != EMPTY:
            return []
        opp = self.opponent(player)
        flips = []
        for dr, dc in DIRECTIONS:
            line, rr, cc = [], r + dr, c + dc
            while self.in_bounds(rr, cc) and self.board[rr][cc] == opp:
                line.append((rr, cc))
                rr, cc = rr + dr, cc + dc
            if line and self.in_bounds(rr, cc) and self.board[rr][cc] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player):
        """All legal moves for `player` as (row, col) tuples."""
        return [(r, c) for r in range(SIZE) for c in range(SIZE)
                if self.flips_for(r, c, player)]

    def apply_move(self, r, c, player):
        """Place a disc and flip all captured lines. Returns True on success."""
        flips = self.flips_for(r, c, player)
        if not flips:
            return False
        self.board[r][c] = player
        for rr, cc in flips:
            self.board[rr][cc] = player
        self.passes = 0
        self.current = self.opponent(player)
        return True

    def pass_turn(self):
        self.passes += 1
        self.current = self.opponent(self.current)

    def score(self):
        black = sum(row.count(BLACK) for row in self.board)
        white = sum(row.count(WHITE) for row in self.board)
        return black, white

    def is_over(self):
        """Board full or neither side can move (two consecutive passes)."""
        if self.passes >= 2:
            return True
        return not (self.valid_moves(BLACK) or self.valid_moves(WHITE))