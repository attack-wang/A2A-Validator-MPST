'''
board.py
Reversi (Othello) board model: an 8x8 grid that stores the disc positions,
detects every legal move for a player, and automatically flips all opponent
discs that lie between a newly placed disc and an existing disc of the same
colour in any of the eight directions.
'''
EMPTY = 0
BLACK = 1
WHITE = 2
# The eight directions a line of discs can be captured in: (row_delta, col_delta).
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
class Board:
    """8x8 Reversi board with the standard starting position."""
    SIZE = 8
    def __init__(self):
        """Create an empty grid and place the four initial discs in the centre."""
        self.grid = [[EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        mid = self.SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the 8x8 grid."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    @staticmethod
    def opponent(player):
        """Return the colour opposite to `player`."""
        return WHITE if player == BLACK else BLACK
    def get_flippable_discs(self, player, row, col):
        """
        Return the list of opponent discs that would be flipped if `player`
        placed a disc on the empty square (row, col). An empty list means the
        move is illegal.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = self.opponent(player)
        flips = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            line = []
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flips.extend(line)
        return flips
    def get_valid_moves(self, player):
        """Return every legal move (row, col) currently available to `player`."""
        return [
            (r, c)
            for r in range(self.SIZE)
            for c in range(self.SIZE)
            if self.grid[r][c] == EMPTY and self.get_flippable_discs(player, r, c)
        ]
    def apply_move(self, player, row, col):
        """
        Place a disc for `player` on (row, col), flip every captured disc and
        return the list of flipped positions. Raises ValueError for illegal
        moves (defensive check; the UI only offers legal squares).
        """
        flips = self.get_flippable_discs(player, row, col)
        if not flips:
            raise ValueError(f"Illegal move ({row}, {col}) for player {player}.")
        self.grid[row][col] = player
        for r, c in flips:
            self.grid[r][c] = player
        return flips
    def is_full(self):
        """Return True when no empty square remains (a game-ending condition)."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def count_discs(self):
        """Return the current score as a tuple (black_count, white_count)."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white