class Game:
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.castling_rights = {WHITE: {'K': True, 'Q': True}, BLACK: {'K': True, 'Q': True}}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history = []
        self.position_counts = {}
        self.result = None
        self.result_reason = ''
        # record initial position
        self.position_counts[self._position_key()] = 1