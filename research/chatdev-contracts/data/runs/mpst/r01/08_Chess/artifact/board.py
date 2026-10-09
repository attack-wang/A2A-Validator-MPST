'''
board.py
8x8 chess board: initial setup, rendering, attack detection, and
make/undo move machinery used for legal-move simulation.
'''
import sys
from pieces import Piece
from move import Move
FILES = 'abcdefgh'
def square_to_coords(square): ...
def coords_to_square(row, col): ...
class Board:
    def __init__(self, empty=False):
        self.grid = [[None] * 8 for _ in range(8)]
        if not empty:
            self.setup_initial_position()
    def setup_initial_position(self):
        back = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col in range(8):
            self.grid[0][col] = Piece(back[col], 'b')
            self.grid[1][col] = Piece('P', 'b')
            self.grid[6][col] = Piece('P', 'w')
            self.grid[7][col] = Piece(back[col], 'w')
    def get_piece(self, row, col):
        return self.grid[row][col]
    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece
    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    def clone(self):
        new = Board(empty=True)
        new.grid = [[p.clone() if p else None for p in row] for row in self.grid]
        return new
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                p = self.grid[row][col]
                if p and p.type == 'K' and p.color == color:
                    return (row, col)
        return None
    def is_square_attacked(self, row, col, by_color):
        # Pawn attacks
        # White pawns attack upward (toward row-1); a white pawn on (r, c)
        # attacks (r-1, c-1) and (r-1, c+1).
        pawn_row = row + 1 if by_color == 'w' else row - 1
        for dc in (-1, 1):
            c = col + dc
            if 0 <= pawn_row < 8 and 0 <= c < 8:
                p = self.grid[pawn_row][c]
                if p and p.type == 'P' and p.color == by_color:
                    return True
        # Knight
        knight_offsets = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in knight_offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                p = self.grid[r][c]
                if p and p.type == 'N' and p.color == by_color:
                    return True
        # King adjacency
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    p = self.grid[r][c]
                    if p and p.type == 'K' and p.color == by_color:
                        return True
        # Sliding pieces: rooks/queens along ranks & files
        rook_dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in rook_dirs:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                p = self.grid[r][c]
                if p:
                    if p.color == by_color and p.type in ('R', 'Q'):
                        return True
                    break
                r += dr
                c += dc
        # Bishops/queens along diagonals
        bishop_dirs = [(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr, dc in bishop_dirs:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                p = self.grid[r][c]
                if p:
                    if p.color == by_color and p.type in ('B', 'Q'):
                        return True
                    break
                r += dr
                c += dc
        return False