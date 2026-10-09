"""Game engine for the simplified Monopoly Go! console game.
Implements the turn loop, dice rolling, movement, property purchase,
rent collection, chance cards, jail rules and bankruptcy handling.
"""
import random
import sys
from config import (
    BOARD_SIZE, GO_SALARY, GO_POSITION, JAIL_POSITION,
    FREE_PARKING_POSITION, GO_TO_JAIL_POSITION, JAIL_FINE, JAIL_MAX_TURNS,
    TAX_AMOUNT, FREE_PARKING_POT_ENABLED, DOUBLES_LIMIT,
    MIN_PLAYERS, MAX_PLAYERS, PLAYER_TOKENS,
    TYPE_GO, TYPE_PROPERTY, TYPE_CHANCE, TYPE_JAIL,
    TYPE_FREE_PARKING, TYPE_TAX, TYPE_GO_TO_JAIL, BOARD_LAYOUT,
    CHANCE_GAIN, CHANCE_LOSE, CHANCE_MOVE, CHANCE_GOTO, CHANCE_GOTO_JAIL,
)
from board import Board
from player import Player
from chancedeck import ChanceDeck
def roll_dice():
    """Roll two six-sided dice. Returns (d1, d2, is_doubles)."""
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    return d1, d2, d1 == d2
class Game:
    """Coordinates players, the board and the rules of the game."""
    def __init__(self, tokens):
        self.board = Board()
        self.players = [Player(t) for t in tokens]
        self.deck = ChanceDeck()
        self.pot = 0          # free-parking pot
        self.round = 0
    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------
    @staticmethod
    def prompt(text, valid=None):
        """Keep prompting until the answer is acceptable."""
        while True:
            answer = input(text).strip().lower()
            if valid is None or answer in valid:
                return answer
            print(f"  Invalid input — please choose one of: {', '.join(valid)}")
    @classmethod
    def ask_yes_no(cls, text):
        """Ask a yes/no question; returns True for 'y'."""
        return cls.prompt(text, ["y", "n"]) == "y"
    # ------------------------------------------------------------------
    # Turn handling
    # ------------------------------------------------------------------
    def play(self):
        """Main game loop; runs until one player remains solvent."""
        print("=== Simplified Monopoly Go! ===")
        self.board.render(self.players)
        active = [p for p in self.players if not p.bankrupt]
        turn_index = 0
        while len([p for p in self.players if not p.bankrupt]) > 1:
            player = self.players[turn_index % len(self.players)]
            turn_index += 1
            if player.bankrupt:
                continue
            self.round += 1
            print(f"\n--- Round {self.round}: {player.token} "
                  f"(${player.money}) at {self.board.describe_space(player.position)} ---")
            self.take_turn(player)
        winner = next((p for p in self.players if not p.bankrupt), None)
        if winner:
            print(f"\n*** {winner.token} wins with ${winner.money}! ***")
    def take_turn(self, player):
        """Play one full turn for `player`."""
        doubles_count = 0
        while True:
            if player.in_jail:
                if not self.handle_jail(player):
                    return
            input(f"  {player.token}, press Enter to roll the dice...")
            d1, d2, is_doubles = roll_dice()
            print(f"  {player.token} rolls {d1} + {d2} = {d1 + d2}"
                  + (" (doubles!)" if is_doubles else ""))
            if is_doubles:
                doubles_count += 1
                if doubles_count >= DOUBLES_LIMIT:
                    print(f"  Three doubles in a row — {player.token} goes to jail!")
                    self.send_to_jail(player)
                    return
            else:
                doubles_count = 0
            self.move_player(player, d1 + d2)
            if player.in_jail:      # sent to jail by the space just landed on
                return
            self.resolve_space(player)
            if player.bankrupt:
                return
            if not is_doubles:
                return
            print(f"  Doubles — {player.token} rolls again!")