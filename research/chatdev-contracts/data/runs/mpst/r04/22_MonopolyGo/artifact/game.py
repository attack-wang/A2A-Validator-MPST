'''game.py — Game engine: turn loop, movement, buying, rent, chance, jail, bankruptcy.'''
import random
from dice import Dice
from player import Player
from board import Board, Property
from chancedeck import ChanceDeck
import display
GO_SALARY = 200
MAX_DOUBLES = 3
class Game:
    def __init__(self, player_names, max_rounds=50, seed=None):
        rng = random.Random(seed)
        self.board = Board()
        self.dice = Dice(rng=rng)
        self.chance_deck = ChanceDeck(rng=rng)  # shared rng keeps runs reproducible
        tokens = ["@", "#", "$", "&"]
        self.players = [Player(name, tokens[i % len(tokens)]) for i, name in enumerate(player_names)]
        self.round = 0
        self.max_rounds = max_rounds
        self.free_parking_pot = 0
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
    # ---------- helpers ----------
    def active_players(self):
        return [p for p in self.players if not p.bankrupt]
    def announce(self, msg):
        print(msg)
    def prompt(self, msg, options):
        """Prompt until a valid choice index is given."""
        while True:
            raw = input("{} {}".format(msg, options)).strip().lower()
            if raw.isdigit():
                idx = int(raw)
                if 0 <= idx < len(options):
                    return idx
            self.announce("  -> please enter a valid option number.")
    ...