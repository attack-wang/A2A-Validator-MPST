class Piece:
    """A single checkers man or king."""
    def __init__(self, color):
        if color not in (RED, BLACK):
            raise ValueError(...)
        self.color = color
        self.is_king = False
    def promote(self):
        self.is_king = True
    @property
    def symbol(self):
        base = 'r' if self.color == RED else 'b'
        return base.upper() if self.is_king else base
    def __repr__(self):
        return f"Piece({self.color}{', king' if self.is_king else ''})"