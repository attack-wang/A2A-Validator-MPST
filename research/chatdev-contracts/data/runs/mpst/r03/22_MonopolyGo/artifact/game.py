'''
game.py: core game engine — turn loop, movement, money transfers, jail and chance resolution.
'''
import random
from board import Board
from dice import Dice
from player import Player, GO_SALARY, JAIL_FINE
from chance import ChanceDeck
from tiles import PropertyTile
class Game:
    """Coordinates the board, players, dice and chance deck to run the game."""
    def __init__(self, player_names):
        """Set up the board, dice, chance deck and one Player per name."""
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.players = [Player(name) for name in player_names]
        self.free_parking_pot = 0
        self.current_index = 0
        self.game_over = False
    # ------------------------------------------------------------------
    # Money handling
    # ------------------------------------------------------------------
    def transfer(self, payer, payee, amount):
        """Move `amount` from payer to payee. Handles liquidation & bankruptcy."""
        if amount <= 0:
            return
        # Ensure payer can pay; liquidate if needed
        if payer.money < amount:
            needed = amount - payer.money
            self.liquidate_player(payer, needed)
        if payer.money >= amount:
            payer.pay(amount)
            if payee is not None:
                payee.receive(amount)
            if payee is None:
                print(f"  ${amount} goes to the bank.")
        else:
            # Bankrupt: pay what remains, then declare bankruptcy
            paid = payer.money
            if paid > 0:
                payer.pay(paid)
                if payee is not None:
                    payee.receive(paid)
            self.declare_bankrupt(payer)
    def liquidate_player(self, player, needed):
        """Sell properties back to the bank at half price until money >= needed."""
        for prop in list(player.properties):
            if player.money >= needed:
                break
            sell_price = prop.price // 2
            prop.owner = None
            player.properties.remove(prop)
            player.receive(sell_price)
            print(f"  {player.name} sells {prop.name} to the bank for ${sell_price}.")
    def pay_to_pot(self, player, amount):
        """Take `amount` from `player` and add what was actually paid to the pot."""
        before = player.money
        self.transfer(player, None, amount)
        self.free_parking_pot += min(amount, before)
        print(f"  Free Parking pot is now ${self.free_parking_pot}.")
    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def move_player(self, player, steps):
        """Advance `player` by `steps`, paying the GO salary when passing GO."""
        if player.bankrupt:
            return
        start = player.position
        player.position = (player.position + steps) % self.board.size
        steps_taken = (player.position - start) % self.board.size
        if steps_taken > 0 and start + steps >= self.board.size:
            player.receive(GO_SALARY)
            print(f"  {player.name} passed GO and collects ${GO_SALARY} salary.")
    def send_player_to_jail(self, player):
        """Teleport `player` to the jail square and mark them as jailed."""
        player.position = self.board.jail_position
        player.in_jail = True
        player.jail_turns = 0
        print(f"  {player.name} is now in jail (position {player.position}).")
    # ------------------------------------------------------------------
    # Buying / chance
    # ------------------------------------------------------------------
    def prompt_buy_property(self, player, tile):
        """Offer an unowned property to the landing player."""
        if player.money < tile.price:
            print(f"  {player.name} cannot afford {tile.name} (${tile.price}).")
            return
        answer = input(f"  {player.name}, buy {tile.name} for ${tile.price}? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            if player.pay(tile.price):
                tile.owner = player
                player.properties.append(tile)
                print(f"  {player.name} now owns {tile.name}.")
        else:
            print(f"  {player.name} declines to buy {tile.name}.")
    def draw_chance(self, player):
        """Draw a chance card and apply its effect to `player`."""
        card = self.chance_deck.draw()
        print(f"  CHANCE: {card.description}")
        effect = card.effect
        if effect == "go_to_go":
            player.position = 0
            player.receive(200)
        elif effect == "go_to_jail":
            self.send_player_to_jail(player)
        elif effect == "collect_100":
            player.receive(100)
        elif effect == "pay_75":
            self.transfer(player, None, 75)
        elif effect == "fine_to_pot":
            self.pay_to_pot(player, 50)
        elif effect == "collect_50":
            player.receive(50)
        elif effect == "pay_50":
            self.transfer(player, None, 50)
        elif effect == "repairs":
            total = 40 * len(player.properties)
            if total > 0:
                print(f"  {player.name} owns {len(player.properties)} properties: ${total} due.")
                self.transfer(player, None, total)
            else:
                print(f"  {player.name} owns no properties, so no repair costs.")
        elif effect == "jail_free_card":
            player.get_out_of_jail_cards += 1
            print(f"  {player.name} keeps the card ({player.get_out_of_jail_cards} held).")
        elif effect == "advance_3":
            self.move_player(player, 3)
            self.resolve_landing(player)
        elif effect == "collect_150":
            player.receive(150)
        elif effect == "tax_to_pot":
            self.pay_to_pot(player, 100)
        else:
            print(f"  Unknown chance effect: {effect}")
    # ------------------------------------------------------------------
    # Jail
    # ------------------------------------------------------------------
    def handle_jail_turn(self, player):
        """Handle a jailed player's options. Returns (escaped, preset_roll)."""
        print(f"{player.name} is in jail (turn {player.jail_turns + 1} of 3).")
        options = ["r"]  # roll for doubles
        if player.money >= JAIL_FINE:
            options.append("p")
        if player.get_out_of_jail_cards > 0:
            options.append("c")
        while True:
            choice = input(f"  {player.name}, choose: (r)oll doubles, (p)ay ${JAIL_FINE} fine, (c)use card: ").strip().lower()
            if choice in options:
                break
            print("  Invalid choice, try again.")
        if choice == "p":
            if player.pay(JAIL_FINE):
                player.in_jail = False
                player.jail_turns = 0
                print(f"  {player.name} pays the fine and is free!")
            return True, None
        if choice == "c":
            player.get_out_of_jail_cards -= 1
            player.in_jail = False
            player.jail_turns = 0
            print(f"  {player.name} uses a Get Out of Jail Free card!")
            return True, None
        # choice == "r": roll for doubles
        input(f"  {player.name}, press Enter to roll for doubles...")
        d1, d2 = self.dice.roll()
        print(f"  {player.name} rolls {d1} + {d2} = {d1 + d2}.")
        if d1 == d2:
            player.in_jail = False
            player.jail_turns = 0
            print(f"  Doubles! {player.name} escapes jail and moves {d1 + d2}.")
            return True, d1 + d2
        player.jail_turns += 1
        if player.jail_turns >= 3:
            # Third failed attempt: must pay fine and move
            print(f"  {player.name} failed 3 times and must pay the ${JAIL_FINE} fine.")
            if player.pay(JAIL_FINE):
                player.in_jail = False
                player.jail_turns = 0
                return True, None  # normal roll next... hmm
            else:
                self.declare_bankrupt(player)
                return False, None
        print(f"  {player.name} stays in jail.")
        return False, None