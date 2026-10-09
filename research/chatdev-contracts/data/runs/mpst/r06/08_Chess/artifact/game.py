class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history = []  # list of (move, san)
        self.snapshots = []  # for undo
        self.position_counts = {}  # for threefold repetition