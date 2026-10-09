'''
game.py
Core game engine for the simplified Monopoly Go! game.
The Game class manages players, turns, dice rolls, movement, buying
properties, rent collection, chance card effects, jail rules, the free
parking pot, bankruptcy and win detection, plus all console prompts.
'''
from board import Board, PropertySpace, TaxSpace, ChanceSpace, FreeParkingSpace, GoToJailSpace
from player import Player
from dice import Dice
from chance import ChanceDeck
from utils import ask_yes_no, ask_int, divider, press_enter, format_money
TOKENS = ["A", "B", "C", "D", "E", "F"]
class Game:
    """Turn-based game loop and rules for simplified Monopoly Go!."""
    MAX_ROUNDS = 50  # safety cap
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.players = []
        self.current_index = 0
        self.round_number = 1
        self.free_parking_pot = 0
        self.game_over = False
    # ---------- setup ----------
    def setup(self):
        print(divider("MONOPOLY GO! (Simplified)"))
        print("Roll the dice, buy properties, collect rent,")
        print("dodge jail, and grab the Free Parking pot!")
        while True:
            count = ask_int("How many players (2-4)? ", minimum=2, maximum=4)
            ...