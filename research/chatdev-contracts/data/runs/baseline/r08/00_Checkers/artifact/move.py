class Move:
    def __init__(self, from_row, from_col, to_row, to_col, captured=None):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.captured = captured  # (row, col) of jumped piece or None
    def is_capture(self):
        return self.captured is not None
    def __eq__(self, other):
        return (isinstance(other, Move) and
                self.from_row == other.from_row and
                self.from_col == other.from_col and
                self.to_row == other.to_row and
                self.to_col == other.to_col)
    def __hash__(self):
        return hash((self.from_row, self.from_col, self.to_row, self.to_col))
    def __repr__(self):
        fr = 8 - self.from_row
        tr = 8 - self.to_row
        fc = chr(ord('a') + self.from_col)
        tc = chr(ord('a') + self.to_col)
        sep = 'x' if self.is_capture() else '-'
        return f"{fc}{fr}{sep}{tc}{tr}"