'''
move.py
Defines the Move class: an ordered path of board positions describing a
complete checkers move.
A move may be:
  * a simple diagonal step          -> path of two positions
  * a single jump                   -> path of two positions, 2 squares apart
  * a multi-jump capture sequence   -> path of three or more positions
Positions are (row, col) grid tuples with row 0 at the top of the board.
'''
class Move:
    """A full move path, e.g. [(5, 0), (3, 2)] or [(2, 1), (0, 3), (2, 5)]."""
    def __init__(self, positions):
        """Build a Move from an ordered list of (row, col) tuples."""
        if len(positions) < 2:
            raise ValueError("A move needs at least a start and an end position")
        self.positions = list(positions)
    @property
    def start(self):
        """Return the (row, col) square the moving piece leaves."""
        return self.positions[0]
    @property
    def end(self):
        """Return the (row, col) square where the move finishes."""
        return self.positions[-1]
    @property
    def is_jump(self):
        """True if any hop in the path covers two squares (i.e. a capture)."""
        return any(abs(r2 - r1) == 2 for (r1, _), (r2, _) in zip(self.positions, self.positions[1:]))
    def hops(self):
        """Yield consecutive (from_square, to_square) pairs along the path."""
        return list(zip(self.positions, self.positions[1:]))
    def __repr__(self):
        """Return the path in algebraic-ish form, e.g. 'b6-d8-f6'."""
        return '-'.join(f"{chr(ord('a') + c)}{8 - r}" for (r, c) in self.positions)