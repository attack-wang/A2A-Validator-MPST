'''
board.py
Defines the Reversi (Othello) board: disc constants, move parsing,
valid-move detection, disc placement with flipping, score counting
and console rendering of the 8x8 grid.
'''
BLACK = 'X'
WHITE = 'O'
EMPTY = ' '
BLACK_SYMBOL = 'X'
WHITE_SYMBOL = 'O'
EMPTY_SYMBOL = '.'
VALID_MOVE_SYMBOL = '*'
COLUMNS = 'abcdefgh'
class Board:
    '''An 8x8 Reversi board with the standard starting position.'''
    SIZE = 8
    def __init__(self):
        '''Create an empty grid and place the four initial discs.'''
        self.grid = [[EMPTY for _ in range(self.SIZE)]
                     for _ in range(self.SIZE)]
        mid = self.SIZE // 2
        self.grid[mid - 1][mid - 1] = WHITE   # d4
        self.grid[mid - 1][mid] = BLACK       # e4
        self.grid[mid][mid - 1] = BLACK       # d5
        self.grid[mid][mid] = WHITE           # e5
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def _flipped_discs(self, color, row, col):
        '''Return the list of opponent discs that would be flipped if
        `color` placed a disc on the empty cell (row, col).'''
        if self.grid[row][col] != EMPTY:
            return []
        opponent = WHITE if color == BLACK else BLACK
        flipped = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue
                path = []
                r, c = row + drow, col + dcol
                while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                    path.append((r, c))
                    r, c = r + drow, c + dcol
                if path and self.in_bounds(r, c) and self.grid[r][c] == color:
                    flipped.extend(path)
        return flipped
    def get_valid_moves(self, color):
        '''Return a list of all legal (row, col) moves for `color`.'''
        return [(row, col)
                for row in range(self.SIZE)
                for col in range(self.SIZE)
                if self.grid[row][col] == EMPTY
                and self._flipped_discs(color, row, col)]
    def place_disc(self, color, row, col):
        '''Place a disc for `color` at (row, col), flip all bracketed
        opponent discs and return the number of discs flipped.'''
        flipped = self._flipped_discs(color, row, col)
        if not flipped:
            raise ValueError(f'Illegal move for {color} at ({row}, {col}).')
        self.grid[row][col] = color
        for r, c in flipped:
            self.grid[r][c] = color
        return len(flipped)
    def count_discs(self):
        '''Return a (black_count, white_count) tuple.'''
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white
    def is_full(self):
        '''Return True when no empty cell remains on the board.'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def display(self, valid_moves=None):
        '''Print the board to the console. If `valid_moves` is given,
        those empty cells are highlighted with "*".'''
        move_set = set(valid_moves) if valid_moves else set()
        print('    ' + ' '.join(COLUMNS))
        print('  +' + '-' * (2 * self.SIZE + 1) + '+')
        for row in range(self.SIZE):
            cells = []
            for col in range(self.SIZE):
                cell = self.grid[row][col]
                if cell == BLACK:
                    cells.append(BLACK_SYMBOL)
                elif cell == WHITE:
                    cells.append(WHITE_SYMBOL)
                elif (row, col) in move_set:
                    cells.append(VALID_MOVE_SYMBOL)
                else:
                    cells.append(EMPTY_SYMBOL)
            print(f'{row + 1:>2}| ' + ' '.join(cells) + ' |')
        print('  +' + '-' * (2 * self.SIZE + 1) + '+')
def parse_move(text):
    '''Convert user input into a (row, col) tuple with 0-based indexes.
    Accepts algebraic notation such as "d3" (column letter + row number)
    or numeric notation such as "4 3" / "4,3" (row then column, 1-based).
    Returns None when the input cannot be interpreted as a board cell.'''
    if text is None:
        return None
    text = text.strip().lower()
    if not text:
        return None
    # Algebraic notation, e.g. "d3".
    if len(text) == 2 and text[0] in COLUMNS and text[1].isdigit():
        row = int(text[1]) - 1
        col = COLUMNS.index(text[0])
        if 0 <= row < Board.SIZE:
            return (row, col)
        return None
    # Numeric notation, e.g. "4 3" or "4,3".
    parts = text.replace(',', ' ').split()
    if len(parts) == 2 and all(part.isdigit() for part in parts):
        row, col = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= row < Board.SIZE and 0 <= col < Board.SIZE:
            return (row, col)
    return None