'''
game.py
Core game engine for the simplified Monopoly Go! game. Manages the turn
loop, dice rolling (with doubles rules), movement, property purchases,
rent payments, taxes, chance cards, jail handling, the Free Parking pot,
bankruptcy, and end-of-game results.
'''
from player import Player
from board import Board, Property, Railroad, Utility
from chance import ChanceDeck
from dice import Dice
class Game:
    GO_SALARY = 200
    MAX_DOUBLES = 3
    JAIL_FINE = 50
    MAX_JAIL_TURNS = 3
    UTILITY_RENT_MULTIPLIER = 4  # 4 x dice roll (10x if both utilities owned)
    def __init__(self, player_names, max_rounds=20):
        self.players = [Player(name) for name in player_names]
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.free_parking_pot = 0
        self.current_index = 0
        self.round = 1
        self.max_rounds = max_rounds
        self.game_over = False
        self.logs = []
    def log(self, message=""):
        print(message)
        self.logs.append(message)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        self.log("=" * 60)
        self.log("       WELCOME TO SIMPLIFIED MONOPOLY GO!")
        self.log("=" * 60)
        self.log(f"Players: {', '.join(p.name for p in self.players)}")
        self.log(f"Game length: {self.max_rounds} rounds (or last player standing)")
        self.log("\nInitial board:")
        self.log(self.board.render(self.players))
        while not self.game_over:
            player = self.players[self.current_index]
            if not player.bankrupt:
                self.play_turn(player)
            if self.check_game_over():
                break
            self.current_index = (self.current_index + 1) % len(self.players)
            if self.current_index == 0:
                self.round += 1
                if self.round > self.max_rounds:
                    self.game_over = True
                    self.log(f"\nMaximum of {self.max_rounds} rounds reached!")
        self.declare_results()