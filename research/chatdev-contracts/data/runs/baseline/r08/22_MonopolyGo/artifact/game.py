import sys
from board import Board
from chance import ChanceDeck
from dice import Dice
from player import Player
class Game:
    SALARY = 200
    JAIL_FINE = 50
    MAX_JAIL_TURNS = 3
    MAX_ROUNDS = 50
    def __init__(self, player_specs, board=None, rng=None, max_rounds=None, input_fn=input, output_fn=print):
        self.board = board if board is not None else Board()
        self.dice = Dice(rng=rng)
        self.chance_deck = ChanceDeck(rng=rng)  # hmm, ChanceDeck takes rng
        self.free_parking_pot = 0
        self.round_number = 0
        self.max_rounds = max_rounds if max_rounds is not None else Game.MAX_ROUNDS
        self.players = [Player(name, token) for name, token in player_specs]
        self.current_index = 0
        self._input = input_fn
        self._print = output_fn
        self.game_over = False