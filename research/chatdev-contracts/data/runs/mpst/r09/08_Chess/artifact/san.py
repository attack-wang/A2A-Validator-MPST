class Move:
    __slots__ = ('from_row', 'from_col', 'to_row', 'to_col', 'promotion', 'is_castle', 'is_en_passant', 'captured', 'piece')
    def __init__(self, from_row, from_col, to_row, to_col, promotion=None, is_castle=None, is_en_passant=False):
        ...