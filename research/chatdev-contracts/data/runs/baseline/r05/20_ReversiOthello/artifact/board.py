'''
board.py
Board representation and Reversi rules for the 8x8 Othello game.
Defines the disc constants (EMPTY, BLACK, WHITE) and the Board class,
which stores the 8x8 grid, validates moves in all 8 directions, flips
captured discs, counts the score and renders the board as text.
'''
EMPTY = '.'
BLACK = 'B'
WHITE = 'W'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]
class Board:
    '''8x8 Reversi board with move validation and disc flipping.'''
    def __init__(self, size=8):
        '''Create an empty size x size board in the standard starting position.'''
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        mid = size // 2
        # Standard starting position: white at d4/e5, black at e4/d5.
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def is_full(self):
        '''Return True when no empty cells remain on the board.'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def count_discs(self, disc):
        '''Return how many discs of the given colour are on the board.'''
        return sum(row.count(disc) for row in self.grid)
    def _flips_in_direction(self, row, col, dr, dc, disc):
        '''Return discs flipped along (dr, dc), or [] if the line is not closed.'''
        opponent = WHITE if disc == BLACK else BLACK
        flips = []
        r, c = row + dr, col + dc
        while self.in_bounds(r, c) and self.grid[r][c] == opponent:
            flips.append((r, c))
            r += dr
            c += dc
        if flips and self.in_bounds(r, c) and self.grid[r][c] == disc:
            return flips
        return []
    def get_flips(self, row, col, disc):
        '''All opponent discs that would be flipped by placing `disc` at (row, col).'''
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        flips = []
        for dr, dc in DIRECTIONS:
            flips.extend(self._flips_in_direction(row, col, dr, dc, disc))
        return flips
    def get_valid_moves(self, disc):
        '''Return every (row, col) where `disc` may legally be placed.'''
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.get_flips(r, c, disc)]
    def has_any_valid_move(self, disc):
        '''Return True if `disc` has at least one legal move available.'''
        return any(self.get_flips(r, c, disc)
                   for r in range(self.size) for c in range(self.size))
    def place_disc(self, row, col, disc):
        '''Place a disc, flip captured discs, return the number flipped.'''
        flips = self.get_flips(row, col, disc)
        if not flips:
            raise ValueError(f'Invalid move at ({row}, {col}) for disc {disc!r}.')
        self.grid[row][col] = disc
        for r, c in flips:
            self.grid[r][c] = disc
        return len(flips)
    def display(self, valid_moves=None):
        '''Return the board as a string; valid moves are marked with "*".'''
        moves = set(valid_moves) if valid_moves else set()
        header = '    ' + ' '.join(str(c + 1) for c in range(self.size))
        lines = [header, '   ' + '-' * (2 * self.size)]
        for r in range(self.size):
            cells = ['*' if (r, c) in moves else self.grid[r][c]
                     for c in range(self.size)]
            lines.append(f'{r + 1} | ' + ' '.join(cells))
        return '\n'.join(lines)