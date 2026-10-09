"""Reversi (Othello) core game logic."""

EMPTY, BLACK, WHITE = ".", "B", "W"

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1), (0, 1),
              (1, -1), (1, 0), (1, 1)]


class ReversiGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK
        self.game_over = False

    @staticmethod
    def opponent(player):
        return WHITE if player == BLACK else BLACK

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def flips_for(self, r, c, player):
        """Return list of discs flipped if player plays at (r, c)."""
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
        player = player or self.current
        moves = {}
        for r in range(8):
            for c in range(8):
                flips = self.flips_for(r, c, player)
                if flips:
                    moves[(r, c)] = flips
        return moves

    def is_valid_move(self, r, c, player=None):
        player = player or self.current
        return bool(self.flips_for(r, c, player))

    def apply_move(self, r, c, player=None):
        player = player or self.current
        flips = self.flips_for(r, c, player)
        if not flips:
            return False
        self.board[r][c] = player
        for fr, fc in flips:
            self.board[fr][fc] = player
        self.advance_turn()
        return True

    def advance_turn(self):
        opp = self.opponent(self.current)
        if self.valid_moves(opp):
            self.current = opp
        elif not self.valid_moves(self.current):
            self.game_over = True

    def score(self):
        b = sum(row.count(BLACK) for row in self.board)
        w = sum(row.count(WHITE) for row in self.board)
        return b, w

    def is_over(self):
        if self.game_over:
            return True
        return all(cell != EMPTY for row in self.board for cell in row)