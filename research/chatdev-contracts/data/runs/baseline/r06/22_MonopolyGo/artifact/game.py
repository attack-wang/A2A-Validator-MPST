'''
game.py
Game engine: turn loop, movement, buying, rent, chance, jail, bankruptcy.
EOF-safe prompts use sensible defaults so automated runs complete cleanly.
'''
import random
from board import Board
from player import Player
from dice import Dice
from chance import ChanceDeck
import ui
GO_BONUS = 200
JAIL_FINE = 50
MAX_JAIL_TURNS = 3
MAX_DOUBLES = 3
class Game:
    def __init__(self, player_names, max_rounds=25, seed=None):
        self.rng = random.Random(seed) if seed is not None else random
        self.board = Board()
        self.players = [Player(n) for n in player_names]
        self.dice = Dice(rng=self.rng)
        self.chance_deck = ChanceDeck(rng=self.rng)
        self.round = 0
        self.max_rounds = max_rounds
        self.current = 0
    def active_players(self):
        return [p for p in self.players if not p.bankrupt]
    def play(self):
        ui.banner("Simplified Monopoly Go!")
        ui.show_message(f"Players: {', '.join(p.name for p in self.players)} | "
                        f"Game ends after {self.max_rounds} rounds or when one player remains.")
        while not self.game_over():
            self.play_round()
            ui.show_status(self.players, self.board, self.round, self.board.free_parking_pot)
        self.declare_winner()
    def game_over(self):
        if len(self.active_players()) <= 1:
            return True
        return self.round >= self.max_rounds
    def play_round(self):
        self.round += 1
        ui.show_message(f"\n=== Round {self.round} ===")
        for player in list(self.players):
            if player.bankrupt:
                continue
            self.play_turn(player)
            if len(self.active_players()) <= 1:
                return
    def play_turn(self, player):
        """Run one full turn, including doubles re-rolls and jail handling."""
        ui.turn_header(player, self.round, self.board)
        doubles_count = 0
        just_left_jail = False
        while True:
            if player.in_jail:
                if not self.handle_jail(player):
                    break  # still in jail, or move already resolved inside jail handling
                just_left_jail = True
            self.dice.roll()
            ui.show_roll(player, self.dice.last_roll)
            if self.dice.is_doubles:
                doubles_count += 1
                if doubles_count >= MAX_DOUBLES:
                    ui.show_message(f"{player.name} rolled doubles {MAX_DOUBLES} times in a row - straight to jail!")
                    self.send_to_jail(player)
                    break
            else:
                doubles_count = 0
            self.move_player(player, self.dice.total)
            self.resolve_space(player)
            if player.bankrupt or player.in_jail:
                break
            if not self.dice.is_doubles or just_left_jail:
                # No extra roll for doubles on the roll made right after leaving jail.
                break
            just_left_jail = False
            ui.show_message(f"{player.name} rolled doubles and takes another roll!")
    def handle_jail(self, player):
        """..."""
        options = [('roll', 'Roll for doubles (free)')]
        if player.can_afford(JAIL_FINE):
            options.insert(0, ('pay', f'Pay ${JAIL_FINE} fine and roll'))
        if player.get_out_of_jail_cards > 0:
            options.insert(0, ('card', 'Use a Get Out of Jail Free card'))
        choice = ui.prompt_choice(
            f"{player.name} is in jail (attempt {player.jail_turns + 1}/{MAX_JAIL_TURNS}). Choose:",
            options, default='roll')
        ...