'''
game.py
Core game engine for the simplified Monopoly Go!: turn handling,
space resolution, jail rules, chance cards, bankruptcy and win checks.
'''
from board import Board
from chance import ChanceDeck
from dice import Dice
from player import Player
from utils import ask_yes_no, ask_int
class Game:
    """Runs the simplified Monopoly Go! game loop."""
    GO_SALARY = 200
    STARTING_MONEY = 1500
    BAIL_AMOUNT = 50
    MAX_JAIL_ATTEMPTS = 3
    TAX_AMOUNT = 100
    MAX_CHAIN = 4  # safety limit for chained chance movements
    def __init__(self):
        self.board = Board()
        self.chance_deck = ChanceDeck()
        self.players = []
        self.pot = 0
        self.round_number = 0
        self.current_log = []
    # ------------------------------------------------------------------
    # Logging helpers
    # ------------------------------------------------------------------
    def log(self, message):
        """Append a message to the current turn's log."""
        self.current_log.append(message)
    def flush_log(self):
        """Print and clear the current turn's log."""
        for line in self.current_log:
            print(line)
        self.current_log = []
    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def setup(self):
        """Ask for the number of players (2-4) and their names."""
        print("=== Welcome to Monopoly Go! (simplified) ===")
        count = ask_int("How many players (2-4)? ", 2, 4)
        for i in range(1, count + 1):
            name = ""
            while not name.strip():
                name = input(f"Enter name for Player {i}: ").strip()
                if not name:
                    print("Name cannot be empty.")
            self.players.append(Player(name, self.STARTING_MONEY))
        print(f"\n{count} players ready. Each starts with ${self.STARTING_MONEY}.")
        print("Board layout preview:")
        for idx, space in enumerate(self.board.spaces):
            print(f"  {idx:2d}: {space.describe()}")
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Set up and run the game until only one player remains."""
        self.setup()
        game_over = False
        while not game_over:
            self.round_number += 1
            print(f"\n===== Round {self.round_number} =====")
            for player in list(self.players):
                if player.bankrupt:
                    continue
                print()
                self.take_turn(player)
                if self.check_game_over():
                    game_over = True
                    break
        self.announce_winner()
    def announce_winner(self):
        """Declare the winner (last non-bankrupt player) or richest player."""
        survivors = [p for p in self.players if not p.bankrupt]
        if len(survivors) == 1:
            print(f"\n*** {survivors[0].name} wins Monopoly Go! ***")
        else:
            best = max(self.players, key=lambda p: p.net_worth())
            print(f"\n*** Game over! {best.name} wins with the highest net worth (${best.net_worth()}). ***")
    def check_game_over(self):
        """Return True when fewer than two players are still solvent."""
        active = [p for p in self.players if not p.bankrupt]
        return len(active) <= 1
    # ------------------------------------------------------------------
    # Turn handling
    # ------------------------------------------------------------------
    def take_turn(self, player):
        """Execute one full turn for the given player."""
        self.current_log = []
        self.display_player(player)
        # Jail handling
        if player.in_jail:
            turn_over = self.handle_jail_turn(player)
            if turn_over or player.bankrupt:
                self.flush_log()
                return
        # Roll dice (doubles grant extra rolls; three doubles -> jail)
        doubles_count = 0
        steps = 0
        while True:
            input(f"{player.name}, press Enter to roll the dice...")
            d1, d2 = Dice.roll()
            steps += d1 + d2
            self.log(f"{player.name} rolls {d1} + {d2} = {d1 + d2}.")
            if d1 == d2:
                doubles_count += 1
                if doubles_count == 3:
                    self.log(f"{player.name} rolled doubles three times in a row!")
                    self.send_to_jail(player)
                    self.flush_log()
                    return
                self.log(f"{player.name} rolled doubles and rolls again!")
                continue
            break
        # Move and resolve
        passed_go = player.move(steps, self.board.SIZE)
        if passed_go:
            player.receive(self.GO_SALARY)
            self.log(f"{player.name} passed GO and collects ${self.GO_SALARY}.")
        self.log(f"{player.name} moves {steps} spaces to {self.board.spaces[player.position].name}.")
        self.resolve_space(player)
        self.flush_log()