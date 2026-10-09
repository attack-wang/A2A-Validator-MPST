"""Reversi (Othello) game logic."""

SIZE = 8
EMPTY, BLACK, WHITE = 0, 1, 2
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1)]


class Reversi:
    def __init__(self):
        self.board = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK

    @staticmethod
    def opponent(color):
        return BLACK if color == WHITE else WHITE

    def flips_for(self, row, col, color):
        """Return discs flipped if color plays at (row, col); empty list if illegal."""
        if self.board[row][col] != EMPTY:
            return []
        opp = self.opponent(color)
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            while 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == opp:
                line.append((r, c))
                r += dr
                c += dc
            if line and 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == color:
                flips.extend(line)
        return flips

    def valid_moves(self, color):
        return [(r, c) for r in range(SIZE) for c in range(SIZE)
                if self.board[r][c] == EMPTY and self.flips_for(r, c, color)]

    def play(self, row, col):
        """Place current player's disc and flip; returns flips or None if illegal."""
        flips = self.flips_for(row, col, self.current)
        if not flips:
            return None
        self.board[row][col] = self.current
        for r, c in flips:
            self.board[r][c] = self.current
        self.current = self.opponent(self.current)
        return flips

    def pass_turn(self):
        self.current = self.opponent(self.current)

    def score(self):
        black = sum(row.count(BLACK) for row in self.board)
        white = sum(row.count(WHITE) for row in self.board)
        return black, white

    def over(self):
        return not self.valid_moves(BLACK) and not self.valid_moves(WHITE)