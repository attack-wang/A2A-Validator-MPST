'''
move.py
Move representation and notation parsing for the checkers game.
A move is a path of squares; a simple step has two squares, a jump
chain lists every landing square in order.  Squares use algebraic
notation such as 'b6' (column letter a-h, rank number 1-8).
'''
import re
_SQUARE_RE = re.compile(r'^[a-h][1-8]$')
def notation_to_square(text):
    """Convert algebraic notation like 'b6' into (row, col) board indices."""
    text = text.strip().lower()
    if not _SQUARE_RE.match(text):
        raise ValueError(f"'{text}' is not a valid square (expected e.g. 'b6').")
    col = ord(text[0]) - ord('a')
    row = 8 - int(text[1])   # rank 1 is the bottom row (index 7)
    return (row, col)
def square_to_notation(square):
    """Convert a (row, col) board index back into algebraic notation."""
    row, col = square
    return f"{chr(ord('a') + col)}{8 - row}"
class Move:
    """A path of squares describing a simple step or a jump chain."""
    def __init__(self, path):
        if len(path) < 2:
            raise ValueError("A move needs at least a start and an end square.")
        self._path = tuple(path)
    @property
    def path(self):
        return self._path
    @property
    def start(self):
        return self._path[0]
    @property
    def end(self):
        return self._path[-1]
    @property
    def steps(self):
        """Number of square-to-square hops in the move."""
        return len(self._path) - 1
    def hop(self, index):
        """Return (from_square, to_square) for hop number `index`."""
        return self._path[index], self._path[index + 1]
    def is_jump(self):
        """True if any hop in the path covers two squares (a capture)."""
        return any(abs(to_r - from_r) == 2
                   for (from_r, from_c), (to_r, to_c)
                   in zip(self._path, self._path[1:]))
    def captured_squares(self):
        """Midpoints of every capturing hop, in order."""
        squares = []
        for i in range(len(self._path) - 1):
            (fr, fc), (tr, tc) = self._path[i], self._path[i + 1]
            if abs(tr - fr) == 2:
                squares.append(((fr + tr) // 2, (fc + tc) // 2))
        return squares
    def __eq__(self, other):
        return isinstance(other, Move) and self._path == other._path
    def __hash__(self):
        return hash(self._path)
    def __str__(self):
        return '-'.join(square_to_notation(sq) for sq in self._path)
def parse_move(text):
    """Parse 'b6-a5', 'b6xa5', 'b6-d4-f2', or 'b6 to a5' into a Move."""
    normalized = text.strip().lower()
    normalized = normalized.replace('->', '-').replace(' to ', '-')
    tokens = [t for t in re.split(r'[\s\-x]+', normalized) if t]
    if len(tokens) < 2:
        raise ValueError("A move needs at least a start and an end square, e.g. 'b6-a5'.")
    return Move(tuple(notation_to_square(t) for t in tokens))