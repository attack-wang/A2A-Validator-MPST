"""Reversi (Othello) core game logic."""

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
EMPTY, BLACK, WHITE = '.', 'B', 'W'


class Reversi:
    def __init__(self):
        self.board = [[EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK

    @staticmethod
    def opponent_of(player):
        return WHITE if player == BLACK else BLACK

    def flips_for(self, row, col, player):
        """Return list of discs that would be flipped by playing (row, col)."""
        if not (0 <= row < 8 and 0 <= col < 8) or self.board[row][col] != EMPTY:
            return []
        opp = self.opponent_of(player)
        flips = []
        for dr, dc in DIRS:
            line = []
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opp:
                line.append((r, c))
                r, c = r + dr, c + dc
            if line and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player=None):
        player = player or self.current
        return {(r, c) for r in range(8) for c in range(8)
                if self.flips_for(r, c, player)}

    def apply_move(self, row, col, player=None):
        player = player or self.current
        flips = self.flips_for(row, col, player)
        if not flips:
            return False
        self.board[row][col] = player
        for r, c in flips:
            self.board[r][c] = player
        return True

    def game_over(self):
        return not (self.valid_moves(BLACK) or self.valid_moves(WHITE))

    def score(self):
        b = sum(row.count(BLACK) for row in self.board)
        w = sum(row.count(WHITE) for row in self.board)
        return b, w

    def pass_turn(self):
        self.current = self.opponent_of(self.current)