'''
board.py
Board representation and move mechanics for the checkers game.
'''
from piece import Piece
BOARD_SIZE = 8
COLS = 'abcdefgh'
class Board:
    '''8x8 checkers board: piece placement, rendering and move helpers.'''
    def __init__(self):
        '''Create the board and place the 24 starting pieces.'''
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.setup()
    def setup(self):
        '''Put 12 black men on the top three playable rows and 12 red men
        on the bottom three playable rows (standard starting position).'''
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.is_playable(r, c):
                    if r <= 2:
                        self.grid[r][c] = Piece('black')
                    elif r >= 5:
                        self.grid[r][c] = Piece('red')
    @staticmethod
    def is_playable(r, c):
        '''Dark squares (the only squares pieces may occupy) satisfy
        (r + c) % 2 == 1; e.g. a1 -> (7, 0) is playable.'''
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and (r + c) % 2 == 1
    def in_bounds(self, r, c):
        '''Return True if (r, c) lies on the board.'''
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE
    def get_piece(self, r, c):
        '''Return the piece at (r, c), or None if the square is empty.'''
        return self.grid[r][c]
    def count_pieces(self, color):
        '''Return how many pieces of the given color remain on the board.'''
        return sum(1 for row in self.grid for p in row if p is not None and p.color == color)
    def _directions(self, piece):
        '''Diagonal directions a piece may travel. Men move forward only
        (red moves up the grid, black moves down); kings move both ways.'''
        if piece.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.color == 'red':
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]
    def get_steps_from(self, r, c):
        '''Return all simple (non-capturing) destination squares for the
        piece standing on (r, c) as a list of (row, col) tuples.'''
        piece = self.grid[r][c]
        if piece is None:
            return []
        steps = []
        for dr, dc in self._directions(piece):
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.grid[nr][nc] is None:
                steps.append((nr, nc))
        return steps
    def _capture_hops(self, r, c, piece, grid):
        '''Yield (landing_r, landing_c, victim_r, victim_c) for every single
        capture hop available to `piece` standing on (r, c) of `grid`.'''
        for dr, dc in self._directions(piece):
            mr, mc = r + dr, c + dc            # victim square
            lr, lc = r + 2 * dr, c + 2 * dc    # landing square
            if not self.in_bounds(lr, lc):
                continue
            victim = grid[mr][mc]
            if victim is not None and victim.color != piece.color and grid[lr][lc] is None:
                yield (lr, lc, mr, mc)
    def get_capture_sequences_from(self, r, c):
        '''Return all maximal capture paths available to the piece standing
        on (r, c). Each path is a list of (row, col) tuples starting with
        (r, c). A path is extended while further jumps exist; per English
        draughts rules a man that lands on its king row is crowned and the
        move ends immediately.'''
        piece = self.grid[r][c]
        if piece is None:
            return []
        king_row = 0 if piece.color == 'red' else BOARD_SIZE - 1
        results = []
        def helper(cur_r, cur_c, grid, path):
            # A man that just jumped onto its king row stops here (crowned).
            if not piece.is_king and cur_r == king_row and len(path) > 1:
                results.append(path)
                return
            extended = False
            for lr, lc, mr, mc in self._capture_hops(cur_r, cur_c, piece, grid):
                extended = True
                new_grid = [row[:] for row in grid]
                new_grid[cur_r][cur_c] = None
                new_grid[mr][mc] = None          # remove the captured piece
                new_grid[lr][lc] = piece
                helper(lr, lc, new_grid, path + [(lr, lc)])
            if not extended and len(path) > 1:
                results.append(path)
        helper(r, c, self.grid, [(r, c)])
        return results
    def apply_path(self, path):
        '''Apply a validated move path to the board: move the piece, remove
        every captured victim, crown a man finishing on its king row, and
        return the (possibly newly crowned) piece.'''
        start = path[0]
        piece = self.grid[start[0]][start[1]]
        self.grid[start[0]][start[1]] = None
        for (fr, fc), (tr, tc) in zip(path, path[1:]):
            if abs(tr - fr) == 2:                # a jump: remove the victim
                self.grid[(fr + tr) // 2][(fc + tc) // 2] = None
        end = path[-1]
        self.grid[end[0]][end[1]] = piece
        if not piece.is_king and end[0] == (0 if piece.color == 'red' else BOARD_SIZE - 1):
            piece.crown()
        return piece
    def display(self):
        '''Render the board with file letters a-h and rank numbers 8..1.
        Red men are "r", black men "b"; kings use the uppercase letter.'''
        lines = ['    a b c d e f g h', '    ----------------']
        for r in range(BOARD_SIZE):
            cells = []
            for c in range(BOARD_SIZE):
                piece = self.grid[r][c]
                cells.append(piece.symbol if piece is not None else '.')
            lines.append(f'  {BOARD_SIZE - r} ' + ' '.join(cells))
        return '\n'.join(lines)