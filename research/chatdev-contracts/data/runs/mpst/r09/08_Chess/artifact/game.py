class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.castling_rights = {'w': {'K': True, 'Q': True}, 'b': {'K': True, 'Q': True}}
        self.en_passant_target = None  # (row, col) of the square that can be captured en passant
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []  # list of SAN strings
        self.position_history = []  # for threefold repetition: position keys