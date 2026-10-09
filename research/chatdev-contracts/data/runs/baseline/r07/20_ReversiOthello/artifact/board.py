'''
board.py
Contains the Board class which represents the 8x8 Reversi (Othello) board.
It handles board state, valid move detection, disc flipping, and score counting.
'''
class Board:
    """Represents the 8x8 Reversi (Othello) game board and its rules."""
    SIZE = 8
    EMPTY = '.'
    BLACK = 'B'
    WHITE = 'W'
    # All 8 directions: up, down, left, right, and the 4 diagonals
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]
    def __init__(self):
        """Create an 8x8 grid and place the four starting discs."""
        self.grid = [[Board.EMPTY for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        # Standard starting position: white top-left of center, black top-right...
        center = Board.SIZE // 2  # 4
        self.grid[center - 1][center - 1] = Board.WHITE  # (3,3)
        self.grid[center - 1][center] = Board.BLACK      # (3,4)
        self.grid[center][center - 1] = Board.BLACK      # (4,3)
        self.grid[center][center] = Board.WHITE          # (4,4)
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < Board.SIZE and 0 <= col < Board.SIZE
    def opponent(self, player):
        """Return the opponent's color for the given player color."""
        return Board.WHITE if player == Board.BLACK else Board.BLACK
    def get_flips(self, row, col, player):
        """
        Return the list of (row, col) positions of opponent discs that would be
        flipped if `player` places a disc on (row, col).
        Returns an empty list if the move is not valid.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != Board.EMPTY:
            return []
        opp = self.opponent(player)
        flips = []
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            line = []
            # Walk in this direction while we see opponent discs.
            while self.in_bounds(r, c) and self.grid[r][c] == opp:
                line.append((r, c))
                r += dr
                c += dc
            # A valid capture requires the line to end on one of our own discs.
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flips.extend(line)
        return flips
    def is_valid_move(self, row, col, player):
        """Return True if `player` may place a disc on (row, col)."""
        return len(self.get_flips(row, col, player)) > 0
    def get_valid_moves(self, player):
        """Return a list of all valid (row, col) moves for `player`."""
        moves = []
        for r in range(Board.SIZE):
            for c in range(Board.SIZE):
                if self.is_valid_move(r, c, player):
                    moves.append((r, c))
        return moves
    def has_valid_moves(self, player):
        """Return True if `player` has at least one valid move."""
        return len(self.get_valid_moves(player)) > 0
    def apply_move(self, row, col, player):
        """
        Place a disc for `player` on (row, col), flip all captured discs and
        return True. Return False (without changing the board) if the move is
        not valid.
        """
        flips = self.get_flips(row, col, player)
        if not flips:
            return False
        self.grid[row][col] = player
        for r, c in flips:
            self.grid[r][c] = player
        return True
    def is_full(self):
        """Return True if every square is occupied."""
        for row in self.grid:
            for cell in row:
                if cell == Board.EMPTY:
                    return False
        return True
    def count_discs(self):
        """Return a tuple (black_count, white_count)."""
        black = 0
        white = 0
        for row in self.grid:
            for cell in row:
                if cell == Board.BLACK:
                    black += 1
                elif cell == Board.WHITE:
                    white += 1
        return black, white
    def display(self, valid_moves=None):
        """
        Print the board with column letters (A-H) and row numbers (1-8).
        Valid moves (if provided as a list of (row, col)) are marked with '*'.
        """
        valid = set(valid_moves) if valid_moves else set()
        header = '    ' + '   '.join(chr(ord('A') + c) for c in range(Board.SIZE))
        print('\n' + header)
        print('  +' + '---' * Board.SIZE + '+')
        for r in range(Board.SIZE):
            row_str = f'{r + 1} |'
            for c in range(Board.SIZE):
                if self.grid[r][c] == Board.EMPTY and (r, c) in valid:
                    row_str += ' * '
                else:
                    row_str += f' {self.grid[r][c]} '
            print(row_str + '|')
        print('  +' + '---' * Board.SIZE + '+')