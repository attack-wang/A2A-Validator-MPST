'''
move.py
Representation and parsing of checkers moves.
A Move is a sequence of board squares (row, column) describing the
complete path of a piece: two squares for a simple diagonal step, or
three or more squares for a (possibly multi) jump. Captured pieces sit
on the intermediate squares between consecutive path positions.
Moves are entered in coordinate notation such as:
    b6-c5          simple move
    b6-d4-f2       double jump
    b6 d4          separators may be spaces, commas or the word "to"
'''
import re
from board import BOARD_SIZE
_FILES = "abcdefgh"
# "b6-c5" -> tokens ["b6", "c5"]; separators may be "-", spaces, commas,
# or the word "to" (case-insensitive).
_TOKEN_RE = re.compile(r"[\s,\-]+|\bto\b", re.IGNORECASE)
_SQUARE_RE = re.compile(r"^([a-hA-H])([1-8])$")
class Move:
    """A complete move path: a list of (row, col) squares."""
    def __init__(self, path):
        self._path = list(path)
    @property
    def path(self):
        """The ordered squares the piece travels through."""
        return list(self._path)
    @property
    def start(self):
        return self._path[0]
    @property
    def end(self):
        return self._path[-1]
    @property
    def is_capture(self):
        """A move is a capture when it covers more than two squares."""
        return len(self._path) > 2
    @property
    def captured_squares(self):
        """Midpoints between consecutive path squares = captured pieces."""
        return [
            ((self._path[i][0] + self._path[i + 1][0]) // 2,
             (self._path[i][1] + self._path[i + 1][1]) // 2)
            for i in range(len(self._path) - 1)
        ]
    @classmethod
    def parse(cls, text):
        """
        Parse user input into a Move, or return None if malformed.
        Accepts "b6-c5", "b6 d4", "b6-d4-f2", "c3 to d4", etc.
        """
        if not isinstance(text, str):
            return None
        tokens = [t for t in _TOKEN_RE.split(text.strip()) if t]
        path = []
        for token in tokens:
            match = _SQUARE_RE.match(token)
            if not match:
                return None
            file_ch, rank_ch = match.groups()
            col = _FILES.index(file_ch.lower())
            row = BOARD_SIZE - int(rank_ch)
            path.append((row, col))
        if len(path) < 2:
            return None
        return cls(path)
    def to_notation(self):
        """Render the move back into coordinate notation."""
        return "-".join(self._square_name(p) for p in self._path)
    @staticmethod
    def _square_name(pos):
        row, col = pos
        return f"{_FILES[col]}{BOARD_SIZE - row}"
    def __eq__(self, other):
        return isinstance(other, Move) and self._path == other._path
    def __hash__(self):
        return hash(tuple(self._path))
    def __repr__(self):
        return f"Move({self.to_notation()})"