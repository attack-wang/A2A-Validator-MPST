"""Reversi (Othello) core game logic."""

BLACK, WHITE, EMPTY = 'X', 'O', '.'
DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))


class Reversi:
    """8x8 Reversi board with move validation, flipping and scoring."""

    def __init__(self):
        self.board = [[EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current = BLACK

    @staticmethod
    def opponent(player):
        return WHITE if player == BLACK else BLACK

    def flips_for(self, row, col, player):
        """Return the list of discs flipped if `player` plays at (row, col)."""
        if not (0 <= row < 8 and 0 <= col < 8) or self.board[row][col] != EMPTY:
            return []
        foe = self.opponent(player)
        flips = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            line = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == foe:
                line.append((r, c))
                r += dr
                c += dc
            if line and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                flips.extend(line)
        return flips

    def valid_moves(self, player=None):
        """Map {(row, col): [flipped discs]} for every legal move."""
        player = self.current if player is None else player
        moves = {}
        for r in range(8):
            for c in range(8):
                flips = self.flips_for(r, c, player)
                if flips:
                    moves[(r, c)] = flips
        return moves

    def apply_move(self, row, col):
        """Place the current player's disc, flip captured lines, switch turn."""
        moves = self.valid_moves()
        if (row, col) not in moves:
            return False
        self.board[row][col] = self.current
        for r, c in moves[(row, col)]:
            self.board[r][c] = self.current
        self.current = self.opponent(self.current)
        return True

    def pass_turn(self):
        self.current = self.opponent(self.current)

    def has_any_move(self, player):
        return any(self.flips_for(r, c, player)
                   for r in range(8) for c in range(8))

    def game_over(self):
        return not (self.has_any_move(BLACK) or self.has_any_move(WHITE))

    def score(self):
        black = sum(row.count(BLACK) for row in self.board)
        white = sum(row.count(WHITE) for row in self.board)
        return black, white