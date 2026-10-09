import random, itertools
from card import Card
from combination import Combination, CombType
from player import Player
from move_generator import generate_all_moves, find_responses
class Game:
    BOTTOM_COUNT = 3
    HAND_SIZE = 17
    def __init__(self):
        self.players = [Player('You (P1)', human), Player('AI West'), Player('AI East')]
        self.landlord = None
        self.bottom_cards = []
        self.current_bid = 0
        self.bid_winner = None
    def build_deck(self): 54 cards
    def deal(self): shuffle, 17 each, bottom 3
    def bidding(self): 
        # One round: each player in turn bids 0-3 (must be > current or 0=pass)
        # If all pass → redeal (return False)
        # Highest bidder becomes landlord, gets bottom cards
        # Standard: bidding ends early if someone bids 3
    def start(self): loop: deal → bidding (redeal if all pass) → play → show result → play again?
    def play(self):
        current_player_idx = landlord index
        current_combo = None
        last_player = None
        pass_count = 0
        while True:
            player = players[idx]
            if pass_count >= 2: current_combo = None (free lead, reset)
            move = get_move(player, current_combo)
            if move is None:  # pass
                pass_count += 1
                announce
            else:
                remove cards, announce, current_combo = move, last_player = player, pass_count = 0
                if not player.hand: break → winner
            idx = (idx+1) % 3
        determine result: winner.is_landlord → landlord wins else farmers win
        scoring