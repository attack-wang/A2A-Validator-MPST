'''
Chess board: setup, move generation, legality, SAN parsing, rendering.
'''
import re
from piece import Piece, SlidingPiece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
SAN_PATTERN = re.compile(
    r'^([KQRBN])?([a-h])?([1-8])?(x)?([a-h][1-8])(?:=([QRBN]))?$'
)
FILES = 'abcdefgh'
def square_name(file, rank):
    return f"{FILES[file]}{rank + 1}"
def parse_square(text):
    f = FILES.index(text[0])
    r = int(text[1]) - 1
    return (f, r)
PROMOTION_CLASSES = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.turn = 'w'
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.position_counts = {}
        self.move_log = []
    def setup(self):
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for f in range(8):
            self.grid[0][f] = back[f]('w')
            self.grid[1][f] = Pawn('w')
            self.grid[6][f] = Pawn('b')
            self.grid[7][f] = back[f]('b')
        self.turn = 'w'
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.position_counts = {}
        self.move_log = []
        self.position_counts[self.position_key()] = 1