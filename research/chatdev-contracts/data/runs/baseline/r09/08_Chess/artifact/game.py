class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.move_history = []  # list of (san, move, record?) 
        self.position_counts = {}  # for threefold repetition
        self.game_over = False
        self.result = None  # e.g., "White wins by checkmate"
    def start(self): main loop
    def handle_input(self, text): parse commands or SAN
    def apply_move(self, move): make move, update history, repetition counts, halfmove clock (in board), switch turn, check end conditions
    def check_game_end(self): checkmate/stalemate/insufficient/50-move/threefold