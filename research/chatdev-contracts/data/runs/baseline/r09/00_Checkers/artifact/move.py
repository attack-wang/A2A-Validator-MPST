'''
move.py
Move representation: a from-square, a to-square, and metadata about
whether the move is a jump (capture) and which enemy piece is captured.
'''
class Move:
    def __init__(self, start, end, captured=None):
        self.start = start      # (row, col)
        self.end = end          # (row, col)
        self.captured = captured  # (row, col) of captured piece or None
        self.is_jump = captured is not None
    @property
    def start_row(self):
        return self.start[0]
    @property
    def start_col(self):
        return self.start[1]
    @property
    def end_row(self):
        return self.end[0]
    @property
    def end_col(self):
        return self.end[1]
    def __repr__(self):
        return f"Move({self.start}->{self.end}, captured={self.captured})"