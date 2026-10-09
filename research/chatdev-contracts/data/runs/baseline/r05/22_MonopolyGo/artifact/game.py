'''
game.py
Core game logic for the simplified Monopoly Go! game.
Runs the turn loop, resolves spaces, handles jail, chance cards,
rent, bankruptcy and the free-parking pot. All interactive prompts
are EOF-safe so the game never crashes in non-interactive runs.
'''
from dice import Dice
from board import Board, Property, GO_SALARY
from chance import (build_chance_deck, EFFECT_MONEY, EFFECT_MOVE_TO,
                    EFFECT_MOVE_BACK, EFFECT_GO_TO_JAIL,
                    EFFECT_GET_OUT_OF_JAIL, EFFECT_COLLECT_FROM_EACH,
                    EFFECT_PAY_EACH, EFFECT_PAY_PER_PROPERTY)
class Game:
    """Controller for a full game of simplified Monopoly Go!."""
    STARTING_MONEY = 1500
    GO_SALARY = GO_SALARY
    JAIL_FINE = 50
    MAX_JAIL_TURNS = 3
    MAX_DOUBLES = 3
    DEFAULT_MAX_ROUNDS = 20
    def __init__(self, player_names, max_rounds=DEFAULT_MAX_ROUNDS, seed=None):
        self.board = Board()
        self.dice = Dice(seed)
        self.players = [Player(name, self.STARTING_MONEY) for name in player_names]
        self.chance_deck = build_chance_deck()
        self.pot = 0
        self.round_number = 0
        self.max_rounds = max_rounds
        self.game_over = False
    # ------------------------------------------------------------------ #
    # EOF-safe interactive helpers                                       #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _pause(message="Press Enter to continue..."):
        """Never crash on EOF in non-interactive runs."""
        try:
            input(message)
        except (EOFError, KeyboardInterrupt):
            print()
    @staticmethod
    def _prompt(message, valid):
        """Ask until a valid choice; EOF falls back to the first valid option."""
        while True:
            try:
                choice = input(message).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                choice = valid[0]  # deterministic fallback for automation
            if choice in valid:
                return choice
            print(f"Please enter one of: {', '.join(valid)}")
    # ------------------------------------------------------------------ #
    # Main loop                                                          #
    # ------------------------------------------------------------------ #
    def play(self):
        """Run the game until it is over, then declare the winner."""
        print("=" * 60)
        print("Welcome to simplified MONOPOLY GO!")
        print(f"Each player starts with ${self.STARTING_MONEY}. "
              "Land on Free Parking to win the pot!")
        print("=" * 60)
        self.display_status()
        while not self.game_over:
            self.play_round()
            if not self.game_over:
                self.display_status()
        self._declare_winner()
    def play_round(self):
        """Give every active player one turn."""
        self.round_number += 1
        print(f"\n===== Round {self.round_number} =====")
        for player in self.players:
            if player.bankrupt or self.game_over:
                continue
            self.take_turn(player)
        self._check_game_over()
    def take_turn(self, player):
        """Handle one player's complete turn (including doubles re-rolls)."""
        print(f"\n--- {player.name}'s turn (money: ${player.money}, "
              f"at {self.board.get_space(player.position).name}) ---")
        if player.in_jail:
            moved = self._handle_jail_turn(player)
            if not moved:
                return
            self._resolve_space(player)
            return
        doubles_count = 0
        while True:
            self._pause("Press Enter to roll the dice...")
            d1, d2 = self.dice.roll()
            total = self.dice.last_total
            print(f"{player.name} rolled {d1} + {d2} = {total}")
            if self.dice.last_is_doubles:
                doubles_count += 1
                if doubles_count == self.MAX_DOUBLES:
                    print("Three doubles in a row! Off to jail with you.")
                    self._send_to_jail(player)
                    return
            self._move_player(player, total)
            self._resolve_space(player)
            if player.bankrupt or self.game_over:
                return
            if player.in_jail:
                return
            if self.dice.last_is_doubles:
                print(f"Doubles! {player.name} gets another roll.")
                continue
            break
    # ------------------------------------------------------------------ #
    # Movement & space resolution                                        #
    # ------------------------------------------------------------------ #
    def _move_player(self, player, steps, collect_go=True):
        """Advance the player `steps` spaces, paying GO salary when passing GO."""
        old = player.position
        new = (old + steps) % self.board.SIZE
        if collect_go and old + steps >= self.board.SIZE:
            player.receive(self.GO_SALARY)
            print(f"{player.name} collects ${self.GO_SALARY} salary for passing GO.")
        player.position = new
        print(f"{player.name} moved to {self.board.get_space(new).name} (space {new}).")
    def _move_to(self, player, target, collect_go=True):
        """Move the player forward to `target`, collecting GO salary if wrapped."""
        target %= self.board.SIZE
        if collect_go and target < player.position:
            player.receive(self.GO_SALARY)
            print(f"{player.name} collects ${self.GO_SALARY} salary for passing GO.")
        player.position = target
        print(f"{player.name} moved to {self.board.get_space(target).name} (space {target}).")
    def _move_back(self, player, steps):
        """Move the player backwards `steps` spaces (no GO salary)."""
        new = (player.position - steps) % self.board.SIZE
        player.position = new
        print(f"{player.name} moved back to {self.board.get_space(new).name} (space {new}).")
    def _resolve_space(self, player):
        """Apply the effect of the space the player landed on."""
        space = self.board.get_space(player.position)
        if isinstance(space, Property):
            self._resolve_property(player, space)
        elif space.kind == "chance":
            self._resolve_chance(player)
        elif space.kind == "go_to_jail":
            self._send_to_jail(player)
        elif space.kind == "tax":
            print(f"{player.name} pays ${space.amount} {space.name}.")
            self._charge(player, space.amount, to_pot=True)
        elif space.kind == "free_parking":
            if self.pot > 0:
                print(f"{player.name} lands on Free Parking and wins the ${self.pot} pot!")
                player.receive(self.pot)
                self.pot = 0
            else:
                print(f"{player.name} rests at Free Parking (pot is empty).")
        elif space.kind == "jail":
            if player.in_jail:
                print(f"{player.name} is in Jail.")
            else:
                print(f"{player.name} is just visiting Jail.")
        elif space.kind == "go":
            print(f"{player.name} is on GO.")
    def _resolve_property(self, player, prop):
        """Buy an unowned property or pay rent to its owner."""
        if not prop.is_owned():
            self._offer_purchase(player, prop)
        elif prop.owner is player:
            print(f"{player.name} rests at own property {prop.name}.")
        else:
            rent = prop.calculate_rent(self.board)
            print(f"{player.name} pays ${rent} rent to {prop.owner.name} for {prop.name}.")
            self._charge(player, rent, recipient=prop.owner)
    def _offer_purchase(self, player, prop):
        """Prompt the player to buy an unowned property (EOF -> decline)."""
        if not player.can_afford(prop.price):
            print(f"{player.name} cannot afford {prop.name} (${prop.price}).")
            return
        message = (f"{prop.name} costs ${prop.price} (rent ${prop.base_rent}). "
                   f"{player.name}, buy it? (y/n) ")
        choice = self._prompt(message, ("y", "n"))
        if choice == "y":
            self._charge(player, prop.price, to_pot=False)
            if not player.bankrupt:
                player.add_property(prop)
                prop.owner = player
                print(f"{player.name} bought {prop.name} for ${prop.price}!")
            else:
                print(f"{player.name} went bankrupt during the purchase; "
                      f"{prop.name} remains unowned.")
        else:
            print(f"{player.name} declined to buy {prop.name}.")
    # ------------------------------------------------------------------ #
    # Chance cards                                                       #
    # ------------------------------------------------------------------ #
    def _draw_chance(self):
        """Draw the top chance card, reshuffling the deck when empty."""
        if not self.chance_deck:
            self.chance_deck = build_chance_deck()
        return self.chance_deck.pop()
    def _resolve_chance(self, player):
        """Draw and apply one chance card."""
        card = self._draw_chance()
        print(f"{player.name} draws a Chance card: \"{card}\"")
        effect = card.effect
        if effect == EFFECT_MONEY:
            if card.amount >= 0:
                player.receive(card.amount)
                print(f"{player.name} receives ${card.amount}.")
            else:
                fine = -card.amount
                print(f"{player.name} must pay a ${fine} fine.")
                self._charge(player, fine, to_pot=True)
        elif effect == EFFECT_MOVE_TO:
            self._move_to(player, card.target)
            self._resolve_space(player)
        elif effect == EFFECT_MOVE_BACK:
            self._move_back(player, card.amount)
            self._resolve_space(player)
        elif effect == EFFECT_GO_TO_JAIL:
            self._send_to_jail(player)
        elif effect == EFFECT_GET_OUT_OF_JAIL:
            player.jail_free_cards += 1
            print(f"{player.name} keeps a Get Out of Jail Free card.")
        elif effect == EFFECT_COLLECT_FROM_EACH:
            total = 0
            for other in self.players:
                if other is not player and not other.bankrupt:
                    total += other.pay(card.amount)
            player.receive(total)
            print(f"{player.name} collects ${total} from the other players.")
        elif effect == EFFECT_PAY_EACH:
            for other in self.players:
                if other is player or other.bankrupt:
                    continue
                paid = player.pay(card.amount)
                other.receive(paid)
                if paid < card.amount:
                    self._declare_bankrupt(player, other)
                    break
        elif effect == EFFECT_PAY_PER_PROPERTY:
            count = len(player.properties)
            due = card.amount * count
            if count == 0:
                print(f"{player.name} owns no properties — nothing to pay.")
            else:
                print(f"{player.name} pays ${card.amount} x {count} properties = ${due}.")
                self._charge(player, due, to_pot=True)
    # ------------------------------------------------------------------ #
    # Jail                                                               #
    # ------------------------------------------------------------------ #
    def _send_to_jail(self, player):
        """Send the player directly to Jail."""
        print(f"{player.name} is sent to Jail!")
        player.position = self.board.JAIL_POSITION
        player.in_jail = True
        player.jail_turns = 0
    def _handle_jail_turn(self, player):
        """Offer jail-escape options; return True when the player moves afterwards."""
        player.jail_turns += 1
        print(f"{player.name} is in Jail (failed attempt {player.jail_turns}/"
              f"{self.MAX_JAIL_TURNS}).")
        options = []
        if player.can_afford(self.JAIL_FINE):
            options.append(("pay", f"pay the ${self.JAIL_FINE} fine"))
        options.append(("roll", "roll the dice for doubles"))
        if player.jail_free_cards > 0:
            options.append(("card",
                            f"use a Get Out of Jail Free card ({player.jail_free_cards} held)"))
        prompt_parts = [f"({i + 1}) {desc}" for i, (_, desc) in enumerate(options)]
        message = f"{player.name}, choose: " + " ".join(prompt_parts) + " "
        valid = tuple(str(i + 1) for i in range(len(options)))
        choice = self._prompt(message, valid)
        action = options[int(choice) - 1][0]
        if action == "pay":
            self._charge(player, self.JAIL_FINE, to_pot=True)
            if player.bankrupt:
                return False
            player.in_jail = False
            player.jail_turns = 0
            print(f"{player.name} pays the fine and leaves Jail.")
            return self._exit_jail_and_roll(player)
        if action == "card":
            player.jail_free_cards -= 1
            player.in_jail = False
            player.jail_turns = 0
            print(f"{player.name} uses a Get Out of Jail Free card!")
            return self._exit_jail_and_roll(player)
        # action == "roll": need doubles to get out
        self._pause("Press Enter to roll for doubles...")
        d1, d2 = self.dice.roll()
        print(f"{player.name} rolled {d1} + {d2}.")
        if self.dice.last_is_doubles:
            player.in_jail = False
            player.jail_turns = 0
            print(f"Doubles! {player.name} leaves Jail and moves {self.dice.last_total}.")
            self._move_player(player, self.dice.last_total)
            return True
        if player.jail_turns >= self.MAX_JAIL_TURNS:
            print(f"{player.name} failed {self.MAX_JAIL_TURNS} times — "
                  f"paying ${self.JAIL_FINE} and leaving Jail.")
            self._charge(player, self.JAIL_FINE, to_pot=True)
            if player.bankrupt:
                return False
            player.in_jail = False
            player.jail_turns = 0
            self._move_player(player, self.dice.last_total)
            return True
        print(f"{player.name} stays in Jail.")
        return False
    def _exit_jail_and_roll(self, player):
        """Roll the dice and move a freed player. Returns True (they moved)."""
        self._pause("Press Enter to roll the dice...")
        d1, d2 = self.dice.roll()
        print(f"{player.name} rolled {d1} + {d2} = {self.dice.last_total}.")
        self._move_player(player, self.dice.last_total)
        return True
    # ------------------------------------------------------------------ #
    # Money, bankruptcy & game-over                                      #
    # ------------------------------------------------------------------ #
    def _charge(self, player, amount, recipient=None, to_pot=False):
        """Take up to `amount` from the player and route it; declare bankruptcy if short."""
        paid = player.pay(amount)
        if to_pot:
            self.pot += paid
        elif recipient is not None:
            recipient.receive(paid)
        if paid < amount:
            shortfall = amount - paid
            print(f"{player.name} cannot pay the full ${amount} "
                  f"(short by ${shortfall}).")
            self._declare_bankrupt(player, recipient)
    def _declare_bankrupt(self, player, creditor=None):
        """Remove the player from the game; release properties (creditor may take them)."""
        player.bankrupt = True
        print(f"*** {player.name} is BANKRUPT and leaves the game! ***")
        for prop in list(player.properties):
            if creditor is not None and not creditor.bankrupt:
                creditor.add_property(prop)
                prop.owner = creditor
                print(f"  {prop.name} is transferred to {creditor.name}.")
            else:
                prop.owner = None
                print(f"  {prop.name} is returned to the bank.")
        player.properties = []
    def _check_game_over(self):
        """End the game when one player remains or the round limit is reached."""
        active = [p for p in self.players if not p.bankrupt]
        if len(active) <= 1:
            self.game_over = True
        elif self.round_number >= self.max_rounds:
            self.game_over = True
    def _declare_winner(self):
        """Announce the winner by net worth (or last player standing)."""
        print("\n" + "=" * 60)
        print("GAME OVER!")
        active = [p for p in self.players if not p.bankrupt]
        if len(active) == 1:
            print(f"The winner is {active[0].name}!")
        else:
            ranked = sorted(self.players, key=lambda p: p.net_worth(), reverse=True)
            winner = ranked[0]
            print(f"Time is up! Richest player: {winner.name} "
                  f"(net worth ${winner.net_worth()}).")
            for i, p in enumerate(ranked, 1):
                print(f"  {i}. {p.name}: net worth ${p.net_worth()}")
        print("=" * 60)
    # ------------------------------------------------------------------ #
    # Display                                                            #
    # ------------------------------------------------------------------ #
    def display_status(self):
        """Print a summary of every player's money, state and holdings."""
        print("-" * 60)
        print(f"Round {self.round_number} | Free Parking pot: ${self.pot}")
        for p in self.players:
            status = ("BANKRUPT" if p.bankrupt
                      else ("IN JAIL" if p.in_jail
                            else f"at {self.board.get_space(p.position).name}"))
            props = ", ".join(prop.name for prop in p.properties) or "none"
            print(f"  {p.name}: ${p.money} | {status} | properties: {props}")
        print("-" * 60)