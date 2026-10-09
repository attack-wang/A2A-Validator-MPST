'''
constants.py
Shared board constants and coordinate/notation helpers used by every
module of the game. The board is an 8x8 grid; row 0 is rank 8 (top) and
column 0 is file 'a'. Playable (dark) squares satisfy (row + col) % 2 == 1,
which puts a red man on a1 as in standard English/American draughts.
'''
BOARD_SIZE = 8
FILES = "abcdefgh"
def in_bounds(row, col):
    """Return True if (row, col) lies inside the 8x8 board."""
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
def is_playable(row, col):
    """Return True if (row, col) is a dark, playable checkers square."""
    return in_bounds(row, col) and (row + col) % 2 == 1
def to_notation(row, col):
    """Convert board coordinates (row, col) to algebraic notation, e.g. (7, 0) -> 'a1'."""
    return f"{FILES[col]}{BOARD_SIZE - row}"
def format_move(move):
    """Convert a ((r1, c1), (r2, c2)) move tuple to notation, e.g. 'b6-a5'."""
    (r1, c1), (r2, c2) = move
    return f"{to_notation(r1, c1)}-{to_notation(r2, c2)}"