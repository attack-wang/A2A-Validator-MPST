class Game:
    def __init__(self, player_names, max_rounds=MAX_ROUNDS):
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.players = [Player(name, STARTING_MONEY) for name in player_names]
        self.free_parking_pot = 0
        self.round_number = 0
        self.max_rounds = max_rounds
        self.current_player_index = 0
        self.game_over = False
        self.consecutive_doubles = 0  # hmm, per-turn or per-player?