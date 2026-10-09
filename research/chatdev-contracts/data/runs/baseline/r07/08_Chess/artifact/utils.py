'''
Shared helper utilities for the chess game: color handling and
algebraic-coordinate (a1-h8) conversion functions used by every module.
'''
def opposite(color):
    """Return the opposite color ('w' <-> 'b')."""
    return 'b' if color == 'w' else 'w'
FILES = 'abcdefgh'
def file_char(col):
    """Convert a 0-based column index to its file letter ('a'-'h')."""
    return FILES[col]
def rank_char(row):
    """Convert a 0-based row index (0 = rank 1) to its rank digit."""
    return str(row + 1)
def square_name(sq):
    """Convert an internal (row, col) square to algebraic name, e.g. (0, 4) -> 'e1'."""
    return file_char(sq[1]) + rank_char(sq[0])
def parse_square(name):
    """Convert an algebraic square name such as 'e4' to internal (row, col)."""
    name = name.strip().lower()
    if len(name) != 2 or name[0] not in FILES or name[1] not in '12345678':
        return None
    return (int(name[1]) - 1, FILES.index(name[0]))