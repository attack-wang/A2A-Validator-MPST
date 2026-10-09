'''
game.py
Game module for the simplified Monopoly Go! game.
Drives the turn-based game loop and enforces all rules: dice movement,
buying properties, collecting rent, chance cards, jail, and free parking.
'''
from board import Board
from chance import ChanceDeck
from dice import Dice
from player import Player, GO_SALARY, JAIL_FINE
DEFAULT_MAX_ROUNDS = 25
MAX_JAIL_TURNS = 3
class Game:
    """Drives the simplified Monopoly Go! game loop and all rules."""
    def __init__(self, player_names, max_rounds=DEFAULT_MAX_ROUNDS,
                 input_fn=input, print_fn=print):
        self.board = Board.build_default_board()
        self.players = [Player(name) for name in player_names]
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.round_number = 0
        self.max_rounds = max_rounds
        self.free_parking_pot = 0
        self._input = input_fn
        self._print = print_fn
    # ------------------------------------------------------------------
    # Input / output helpers
    # ------------------------------------------------------------------
    def ask_yes_no(self, prompt):
        """Prompt until the user answers yes or no. Returns True/False."""
        while True:
            answer = self._input(f"{prompt} (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            self._print("Please answer 'y' or 'n'.")
    def ask_choice(self, prompt, options):
        """Prompt until the user picks one of `options` (list of keys)."""
        valid = [str(o).lower() for o in options]
        while True:
            answer = self._input(f"{prompt} [{'/'.join(valid)}]: ").strip().lower()
            if answer in valid:
                return answer
            self._print(f"Please choose one of: {', '.join(valid)}.")
    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------
    def display_board(self):
        """Print an overview of every space on the board."""
        self._print("\n=== BOARD ===")
        for i, space in enumerate(self.board.spaces):
            self._print(f"[{i:>2}] {space}")
    def display_players(self):
        """Print each player's cash, position, holdings and status."""
        self._print("\n=== PLAYERS ===")
        for p in self.players:
            status = ""
            if p.in_jail:
                status += " (IN JAIL)"
            if p.bankrupt:
                status += " (BANKRUPT)"
            props = ", ".join(prop.name for prop in p.properties) or "none"
            self._print(f"{p.name}: ${p.money}{status} | "
                        f"at {self.board.get_space(p.position).name} | owns: {props}")
        self._print(f"Free Parking pot: ${self.free_parking_pot}")
    def display_space(self, position):
        """Print details of the space at `position`."""
        self._print(f"-> Landed on: {self.board.get_space(position)}")
    # ------------------------------------------------------------------
    # Money helpers
    # ------------------------------------------------------------------
    def transfer(self, payer, amount, recipient=None, to_pot=False):
        """Make `payer` pay `amount` to a recipient, the free-parking pot,
        or the bank. Handles partial payment and bankruptcy."""
        cash_available = payer.money
        paid_full = payer.pay(amount)
        gained = amount if paid_full else cash_available
        if recipient is not None:
            recipient.receive(gained)
        elif to_pot:
            self.free_parking_pot += gained
        if not paid_full:
            self.release_properties(payer)
            self._print(f"*** {payer.name} cannot pay ${amount} — BANKRUPT! ***")
        return paid_full
    def release_properties(self, player):
        """Return all of a bankrupt player's properties to the bank."""
        for prop in player.properties:
            prop.owner = None
        player.properties = []
    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def move_player(self, player, steps):
        """Move a player forward, paying GO salary when GO is passed."""
        if player.move(steps, self.board.size):
            player.receive(GO_SALARY)
            self._print(f"{player.name} passed GO and collected ${GO_SALARY}.")
        self.display_space(player.position)
    def send_to_jail(self, player):
        """Send a player directly to jail (no GO salary is collected)."""
        player.send_to_jail(self.board.jail_position())
        self._print(f"{player.name} was sent to Jail!")
    # ------------------------------------------------------------------
    # Landing resolution
    # ------------------------------------------------------------------
    def resolve_landing(self, player):
        """Apply the effect of the space the player landed on."""
        space = self.board.get_space(player.position)
        if space.kind == "property":
            self.handle_property(player, space)
        elif space.kind == "chance":
            card = self.chance_deck.draw()
            self._print(f"{player.name} drew a Chance card: \"{card}\"")
            self.handle_chance(player, card)
        elif space.kind == "go_to_jail":
            self.send_to_jail(player)
        elif space.kind == "free_parking":
            if self.free_parking_pot > 0:
                player.receive(self.free_parking_pot)
                self._print(f"{player.name} collected ${self.free_parking_pot} "
                            f"from the Free Parking pot!")
                self.free_parking_pot = 0
            else:
                self._print(f"{player.name} is resting on Free Parking.")
        elif space.kind == "jail":
            self._print(f"{player.name} is just visiting Jail.")
        elif space.kind == "go":
            self._print(f"{player.name} is on GO.")
    def handle_property(self, player, prop):
        """Buy an unowned property, or pay rent if someone else owns it."""
        if prop.owner is None:
            if player.can_afford(prop.price):
                if self.ask_yes_no(
                        f"{player.name}, do you want to buy {prop.name} "
                        f"for ${prop.price}?"):
                    player.buy(prop)
                    self._print(f"{player.name} bought {prop.name} "
                                f"for ${prop.price}.")
                else:
                    self._print(f"{player.name} declined to buy {prop.name}.")
            else:
                self._print(f"{player.name} cannot afford {prop.name} "
                            f"(${prop.price}).")
        elif prop.owner is player:
            self._print(f"{player.name} owns {prop.name}. Welcome home!")
        else:
            rent = prop.rent
            self._print(f"{player.name} pays ${rent} rent to "
                        f"{prop.owner.name} for {prop.name}.")
            self.transfer(player, rent, recipient=prop.owner)
    # ------------------------------------------------------------------
    # Chance cards
    # ------------------------------------------------------------------
    def handle_chance(self, player, card):
        """Apply the effect of a drawn chance card."""
        effect = card.effect
        if effect == "COLLECT":
            player.receive(card.amount)
            self._print(f"{player.name} collected ${card.amount}.")
        elif effect == "PAY":
            self.transfer(player, card.amount, to_pot=True)
        elif effect == "MOVE":
            self._print(f"{player.name} advances {card.steps} spaces.")
            self.move_player(player, card.steps)
            self.resolve_landing(player)
        elif effect == "MOVE_BACK":
            self._print(f"{player.name} moves back {card.steps} spaces.")
            player.position = (player.position - card.steps) % self.board.size
            space = self.board.get_space(player.position)
            self._print(f"{player.name} moved back to {space.name} "
                        f"(space {player.position}).")
            self.resolve_landing(player)
        elif effect == "GO_TO":
            if card.target == "go":
                go_index = self.board.go_position()
                player.position = go_index
                player.receive(GO_SALARY)
                self._print(f"{player.name} advanced to GO and "
                            f"collected ${GO_SALARY}!")
        elif effect == "GO_TO_JAIL":
            self.send_to_jail(player)
    # ------------------------------------------------------------------
    # Jail handling
    # ------------------------------------------------------------------
    def handle_jail_turn(self, player):
        """Handle a turn for a player currently in jail.
        Returns the dice roll that freed the player (when doubles were
        rolled), otherwise None (still jailed, freed by paying the fine,
        or bankrupt).
        """
        choice = self.ask_choice(
            f"{player.name}, you are in jail. Pay ${JAIL_FINE} fine or "
            f"try to roll doubles?",
            ["pay", "roll"])
        if choice == "pay":
            if self.transfer(player, JAIL_FINE):
                player.leave_jail()
                self._print(f"{player.name} paid the fine and is free.")
                return None  # freed by paying; a fresh roll happens below
            return None  # bankrupt
        # Try to roll doubles
        roll = self.dice.roll()
        self._print(f"{player.name} {Dice.describe(roll)}")
        if self.dice.is_doubles(roll):
            player.leave_jail()
            self._print(f"{player.name} rolled doubles and leaves jail!")
            return roll  # the freeing roll is also used for movement
        player.jail_turns += 1
        if player.jail_turns >= MAX_JAIL_TURNS:
            # Forced to pay the fine after three failed attempts
            self._print(f"{player.name} failed {MAX_JAIL_TURNS} times and "
                        f"must pay the ${JAIL_FINE} fine.")
            if self.transfer(player, JAIL_FINE):
                player.leave_jail()
            return None
        self._print(f"{player.name} stays in jail "
                    f"(attempt {player.jail_turns}/{MAX_JAIL_TURNS}).")
        return None
    # ------------------------------------------------------------------
    # Turn / game loop
    # ------------------------------------------------------------------
    def take_turn(self, player):
        """Play one full turn for `player`."""
        self._print(f"\n--- {player.name}'s turn ---")
        freeing_roll = None
        if player.in_jail:
            freeing_roll = self.handle_jail_turn(player)
            if freeing_roll is None and player.in_jail:
                # Still in jail (failed to roll doubles) or went bankrupt
                # while trying to pay the fine: the turn ends here.
                return
        # Use the roll that freed the player from jail (doubles), or roll
        # normally (fresh roll after paying the fine / never in jail).
        roll = freeing_roll if freeing_roll is not None else self.dice.roll()
        self._print(f"{player.name} {Dice.describe(roll)}")
        steps = self.dice.total(roll)
        self.move_player(player, steps)
        self.resolve_landing(player)
    def active_players(self):
        """Players who are not bankrupt."""
        return [p for p in self.players if not p.bankrupt]
    def check_game_over(self):
        """Return True when only one active player remains."""
        return len(self.active_players()) <= 1
    def declare_winner(self):
        """Announce the winner (or leader by net worth at round limit)."""
        active = self.active_players()
        if len(active) == 1:
            self._print(f"\n*** {active[0].name} WINS! "
                        f"Everyone else went bankrupt. ***")
        else:
            leader = max(active, key=lambda p: p.net_worth())
            self._print(f"\n*** Game over after {self.max_rounds} rounds. "
                        f"{leader.name} wins with a net worth of "
                        f"${leader.net_worth()}! ***")
    def play(self):
        """Run the game until a winner is decided or rounds run out."""
        self._print("Welcome to simplified Monopoly Go!")
        self.display_board()
        self.display_players()
        while self.round_number < self.max_rounds:
            self.round_number += 1
            self._print(f"\n========== ROUND {self.round_number} "
                        f"of {self.max_rounds} ==========")
            for player in self.players:
                if player.bankrupt:
                    continue
                self.take_turn(player)
                self.display_players()
                if self.check_game_over():
                    self.declare_winner()
                    return
        self.declare_winner()