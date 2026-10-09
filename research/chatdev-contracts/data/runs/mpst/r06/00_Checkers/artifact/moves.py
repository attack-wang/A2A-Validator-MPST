'''
moves.py
Move representation and legal-move generation for checkers:
simple diagonal moves, (multi-)jump sequences, and the
compulsory-capture rule.
'''
from board import Board, BOARD_SIZE
from pieces import PieceColor
# All four diagonal directions as (dr, dc).
DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
def forward_directions(color):
    '''Return the two diagonal directions a non-king of `color` may move.'''
    return ((1, -1), (1, 1)) if color == PieceColor.RED else ((-1, -1), (-1, 1))
class Move:
    '''A legal move: an ordered path of squares plus captured squares.'''
    def __init__(self, path, captures=()):
        self.path = tuple(path)          # e.g. ((2, 2), (4, 4), (6, 6))
        self.captures = tuple(captures)  # midpoints of each jump
    @property
    def start(self):
        '''First square of the path.'''
        return self.path[0]
    @property
    def end(self):
        '''Last square of the path.'''
        return self.path[-1]
    @property
    def is_capture(self):
        '''True if this move captures at least one enemy piece.'''
        return bool(self.captures)
    @property
    def notation(self):
        '''Human-readable notation, e.g. "c3-d4" or "c3xe5xg7".'''
        arrow = 'x' if self.is_capture else '-'
        return arrow.join(chr(ord('a') + c) + str(r + 1) for (r, c) in self.path)
    def __repr__(self):
        return f"Move({self.notation})"
def get_simple_moves(board, row, col):
    '''Return all one-step diagonal moves from (row, col) to empty squares.'''
    piece = board.get_piece(row, col)
    result = []
    directions = DIRECTIONS if piece.is_king else forward_directions(piece.color)
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if Board.is_valid_square(nr, nc) and board.get_piece(nr, nc) is None:
            result.append(Move([(row, col), (nr, nc)]))
    return result
def get_jump_sequences(board, row, col):
    '''Return every maximal jump sequence starting at (row, col).
    Uses DFS with board simulation (apply/undo). Only terminal sequences
    are returned: if further jumps exist from a landing square, the chain
    MUST continue (compulsory multi-jump). A man that lands on its crowning
    row stops there and is crowned; it does not keep jumping as a king.
    '''
    piece = board.get_piece(row, col)
    results = []
    def dfs(r, c, path, captures):
        # A man that just jumped onto its king row must stop (it gets crowned).
        if not piece.is_king and captures and Board.is_king_row(piece.color, r):
            results.append(Move(path, captures))
            return
        directions = DIRECTIONS if piece.is_king else forward_directions(piece.color)
        extended = False
        for dr, dc in directions:
            mid = (r + dr, c + dc)
            land = (r + 2 * dr, c + 2 * dc)
            if not Board.is_valid_square(*land):
                continue
            mid_piece = board.get_piece(*mid)
            if mid_piece is None or mid_piece.color == piece.color:
                continue                      # nothing to capture / own piece
            if board.get_piece(*land) is not None:
                continue                      # landing square occupied
            # --- simulate the jump ---
            board.remove_piece(r, c)
            board.remove_piece(*mid)
            board.place_piece(land[0], land[1], piece)
            dfs(land[0], land[1], path + [land], captures + [mid])
            # --- undo the jump ---
            board.remove_piece(land[0], land[1])
            board.place_piece(mid[0], mid[1], mid_piece)
            board.place_piece(r, c, piece)
            extended = True
        if not extended and captures:
            results.append(Move(path, captures))
    dfs(row, col, [(row, col)], [])
    return results
def get_single_jumps(board, row, col):
    '''Return single-jump segments (Move objects with path length 2)
    from (row, col). Used for interactive chain-jump continuation.'''
    piece = board.get_piece(row, col)
    result = []
    directions = DIRECTIONS if piece.is_king else forward_directions(piece.color)
    for dr, dc in directions:
        mid = (row + dr, col + dc)
        land = (row + 2 * dr, col + 2 * dc)
        if not Board.is_valid_square(*land):
            continue
        mid_piece = board.get_piece(*mid)
        if mid_piece is None or mid_piece.color == piece.color:
            continue
        if board.get_piece(*land) is not None:
            continue
        result.append(Move([(row, col), land], [mid]))
    return result
def get_all_moves(board, color):
    '''All legal moves for `color`. If any capture exists, ONLY captures
    are legal (compulsory capture rule).'''
    jumps, simple = [], []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece(row, col)
            if piece is None or piece.color != color:
                continue
            jumps.extend(get_jump_sequences(board, row, col))
            simple.extend(get_simple_moves(board, row, col))
    return jumps if jumps else simple