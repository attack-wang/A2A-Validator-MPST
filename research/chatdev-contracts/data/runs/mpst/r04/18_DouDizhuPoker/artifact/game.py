class GamePhase(Enum):
    BIDDING = 0
    PLAYING = 1
    OVER = 2
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.hand = []
        self.is_human = is_human
        self.is_landlord = False
        self.bid = 0
class DouDizhuGame:
    def __init__(self, player_names, human_index=0):
        ...
    def new_round(self):
        # deal cards, sort hands, phase = BIDDING, bidding starts at rotating dealer
    def make_bid(self, player_idx, bid):
        # bid in 0..3, must be > current highest
        # all pass -> redeal
        # bid == 3 -> immediate landlord
    def finish_bidding(self):
        # set landlord, give bottom cards, phase PLAYING, current = landlord
    def play_cards(self, player_idx, cards):
        # validate turn, parse combo, validate beat, remove from hand, record, check win
    def pass_turn(self, player_idx):
        # validate turn; pass_count += 1; if pass_count == 2: clear last_play
    def advance_turn(self):
        ...