'''
board.py
Board state, move generation, move application and rendering.
...
'''
from pieces import Piece, RED, BLACK, FORWARD_DELTAS, ALL_DELTAS, KING_ROW, BOARD_SIZE
from move import Move, format_position
class Board:
    def __init__(self):
        self.grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._setup_pieces()
    def _setup_pieces(self):
        for row in range(3):
            for col in range(BOARD_SIZE):
                if self.is_playable(row, col):
                    self.grid[row][col] = Piece(RED)
        for row in range(5, 8):
            for col in range(BOARD_SIZE):
                if self.is_playable(row, col):
                    self.grid[row][col] = Piece(BLACK)
    @staticmethod
    def in_bounds(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    @staticmethod
    def is_playable(row, col):
        return (row + col) % 2 == 1
    def get_piece(self, row, col):
        return self.grid[row][col]
    def _find_simple_moves(self, row, col, piece):
        moves = []
        directions = ALL_DELTAS if piece.is_king else FORWARD_DELTAS[piece.color]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.in_bounds(r, c) and self.grid[r][c] is None:
                moves.append(Move(path=[(row, col), (r, c)], captures=[]))
        return moves
    def _find_jump_moves(self, row, col, piece):
        moves = []
        directions = ALL_DELTAS if piece.is_king else FORWARD_DELTAS[piece.color]
        start = (row, col)
        def extend(cur_row, cur_col, path, captures):
            continued = False
            for dr, dc in directions:
                mid = (cur_row + dr, cur_col + dc)
                land = (cur_row + 2 * dr, cur_col + 2 * dc)
                if not self.in_bounds(*land):
                    continue
                if mid in captures:
                    continue  # cannot jump the same piece twice
                mid_piece = self.grid[mid[0]][mid[1]]
                if mid_piece is None or mid_piece.color == piece.color:
                    continue
                land_piece = self.grid[land[0]][land[1]]
                if land_piece is not None and land != start:
                    continue  # landing square must be empty (start is vacated)
                new_path = path + [land]
                new_captures = captures + [mid]
                continued = True
                # A man reaching its king row must stop there and be crowned.
                if not piece.is_king and land[0] == KING_ROW[piece.color]:
                    moves.append(Move(new_path, new_captures))
                else:
                    extend(land[0], land[1], new_path, new_captures)
            if not continued and captures:
                moves.append(Move(path, captures))
        extend(row, col, [start], [])
        return moves