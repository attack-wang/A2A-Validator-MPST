class Piece:
    def __init__(self, color, piece_type):
        self.color = color  # 'w' or 'b'
        self.piece_type = piece_type  # 'K','Q','R','B','N','P'
    def __repr__(self): ...