# pieces.py
class Color:
    WHITE = 'w'
    BLACK = 'b'
class Piece:
    def __init__(self, color, kind):
        self.color = color
        self.kind = kind  # 'K','Q','R','B','N','P'
    @property
    def letter(self):
        return self.kind if self.color == 'w' else self.kind.lower()