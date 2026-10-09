"""Core Reversi (Othello) game logic: board, valid moves, flips, scoring."""

EMPTY, BLACK, WHITE = '.', 'B', 'W'
SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


class ReversiGame:
    def __init__(self):
        self.board = [[EMPTY] * SIZE for _ in range(SIZE)]
        # Standard starting position (center four discs).
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK  # Black moves first.

    @staticmethod
    def opponent(player):
        return WHITE if player == BLACK else BLACK

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < SIZE and 0 <= c < SIZE

    def _flips(self, r, c, player):
        """Return all discs that would be flipped if `player` plays at (r, c)."""
        if not self.in_bounds(r, c) or self.board[r][c] != EMPTY:
            return []
        opp = self.opponent(player)
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc) and self.board[rr][cc] == opp:
                line.append((rr, cc))
                rr += dr
                cc += dc
            if line and self.in_bounds(rr, cc) and self.board[rr][cc] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player=None):
        """Map of (r, c) -> list of flipped discs for every legal move."""
        player = player or self.current
        moves = {}
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == EMPTY:
                    flips = self._flips(r, c, player)
                    if flips:
                        moves[(r, c)] = flips
        return moves

    def is_valid_move(self, r, c, player=None):
        player = player or self.current
        return self.in_bounds(r, c) and bool(self._flips(r, c, player))

    def apply_move(self, r, c, player=None):
        """Place a disc, flip captured lines, return True if the move was legal."""
        player = player or self.current
        flips = self._flips(r, c, player)
        if not flips:
            return False
        self.board[r][c] = player
        for rr, cc in flips:
            self.board[rr][cc] = player
        return True

    def has_valid_move(self, player):
        return bool(self.valid_moves(player))

    def score(self):
        b = sum(row.count(BLACK) for row in self.board)
        w = sum(row.count(WHITE) for row in self.board)
        return b, w

    def board_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def game_over(self):
        return self.board_full() or not (
            self.has_valid_move(BLACK) or self.has_valid_move(WHITE))

    def switch_player(self):
        self.current = self.opponent(self.current)