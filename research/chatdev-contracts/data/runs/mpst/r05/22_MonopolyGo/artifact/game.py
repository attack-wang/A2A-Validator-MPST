from board import Board
from chance import ChanceDeck, build_standard_deck
from dice import Dice
from player import Player
from ui import ask_yes_no, get_choice
class Game:
    GO_SALARY = 200
    JAIL_FINE = 50
    MAX_DOUBLES = 3
    MAX_ROUNDS = 100
    def __init__(self, player_names, max_rounds=MAX_ROUNDS):
        self.board = Board()
        self.dice = Dice()
        self.players = [Player(name) for name in player_names]
        self.chance_deck = ChanceDeck(build_standard_deck())
        self.round = 1
        self.max_rounds = max_rounds
        self.free_parking_pot = 0
        self.game_over = False
    # ---------- utilities ----------
    def log(self, message):
        print(f"    {message}")
    def active_players(self):
        return [p for p in self.players if not p.bankrupt]
    def get_choice(self, prompt, valid_options):
        return get_choice(prompt, valid_options)
    # ---------- main loop ----------
    def play(self):
        while not self.game_over and self.round <= self.max_rounds:
            self.play_round()
        self.declare_winner()
    def play_round(self):
        print(f"\n===== ROUND {self.round} =====")
        for player in list(self.players):
            if self.game_over:
                break
            if player.bankrupt:
                continue
            self.take_turn(player)
        self.round += 1
        if self.round > self.max_rounds:
            self.game_over = True
    def take_turn(self, player):
        self.display_status(player)
        if player.in_jail:
            self.handle_jail_turn(player)
        else:
            self.normal_turn(player)
    # ---------- movement ----------
    def normal_turn(self, player):
        doubles_count = 0
        while True:
            input(f"{player.name}, press Enter to roll the dice...")
            d1, d2, total, is_doubles = self.dice.roll()
            self.log(f"{player.name} rolled {d1} + {d2} = {total}" + (" (DOUBLES!)" if is_doubles else ""))
            if is_doubles:
                doubles_count += 1
                if doubles_count >= self.MAX_DOUBLES:
                    self.log("Three doubles in a row! Speeding — off to jail!")
                    self.send_to_jail(player)
                    break
            self.move_player(player, total)
            if self.game_over or player.bankrupt or player.in_jail:
                break
            if not is_doubles:
                break
            self.log(f"{player.name} rolled doubles and gets another roll!")
    def move_player(self, player, steps):
        old = player.position
        new = (old + steps) % len(self.board)
        if steps > 0 and new < old:
            player.receive(self.GO_SALARY)
            self.log(f"{player.name} passes GO and collects ${self.GO_SALARY}.")
        player.position = new
        space = self.board.get_space(new)
        self.log(f"{player.name} moves to {space} (position {new}).")
        space.land_on(player, self)
    def move_to(self, player, target, collect_go=True):
        target %= len(self.board)
        if collect_go and target < player.position:
            player.receive(self.GO_SALARY)
            self.log(f"{player.name} passes GO and collects ${self.GO_SALARY}.")
        player.position = target
        space = self.board.get_space(target)
        self.log(f"{player.name} moves to {space} (position {target}).")
        space.land_on(player, self)
    # ---------- money ----------
    def transfer(self, payer, payee, amount):
        paid = payer.pay(amount)
        if payee is not None:
            payee.receive(paid)
        if paid < amount:
            self.log(f"{payer.name} can only pay ${paid} of the ${amount} owed.")
            self.handle_bankruptcy(payer)
            return False
        return True
    def pay_to_pot(self, player, amount, reason):
        self.log(f"{player.name} pays ${amount} ({reason}) into the Free Parking pot.")
        paid = player.pay(amount)
        self.free_parking_pot += paid
        if paid < amount:
            self.log(f"{player.name} can only pay ${paid} of the ${amount} owed.")
            self.handle_bankruptcy(player)
            return False
        return True
    def collect_free_parking(self, player):
        self.log(f"{player.name} lands on Free Parking and collects the pot of ${self.free_parking_pot}!")
        player.receive(self.free_parking_pot)
        self.free_parking_pot = 0
    # ---------- properties ----------
    def offer_property_purchase(self, player, prop):
        if player.money < prop.price:
            self.log(f"{player.name} has only ${player.money} and cannot afford {prop.name} (${prop.price}).")
            return
        if ask_yes_no(f"Buy {prop.name} for ${prop.price}? (y/n): "):
            player.pay(prop.price)
            prop.owner = player
            player.properties.append(prop)
            self.log(f"{player.name} bought {prop.name} for ${prop.price}. Money left: ${player.money}.")
        else:
            self.log(f"{player.name} declined to buy {prop.name}.")
    def charge_rent(self, player, prop):
        owner = prop.owner
        self.log(f"{player.name} owes ${prop.rent} rent to {owner.name} for {prop.name}.")
        self.transfer(player, owner, prop.rent)
    # ---------- chance ----------
    def draw_chance(self, player):
        card = self.chance_deck.draw()
        self.log(f'{player.name} draws a Chance card: "{card.description}"')
        card.apply(player, self)
        if card.effect != "jail_free":
            self.chance_deck.discard(card)
    # ---------- jail ----------
    def send_to_jail(self, player):
        player.position = self.board.jail_position
        player.in_jail = True
        player.jail_turns = 0
        self.log(f"{player.name} is sent to JAIL!")
    def handle_jail_turn(self, player):
        self.log(f"{player.name} is in jail (attempt {player.jail_turns + 1} of 3).")
        options = ["r"]
        prompt = "Choose: [r] roll for doubles"
        if player.money >= self.JAIL_FINE:
            options.append("p")
            prompt += ", [p] pay $50 fine"
        if player.jail_free_cards:
            options.append("c")
            prompt += ", [c] use Get Out of Jail Free card"
        choice = get_choice(prompt + ": ", options)
        if choice == "c":
            card = player.jail_free_cards.pop()
            self.chance_deck.return_to_deck(card)
            player.in_jail = False
            player.jail_turns = 0
            self.log(f"{player.name} uses a Get Out of Jail Free card and leaves jail!")
            self.roll_and_move(player)
        elif choice == "p":
            if self.pay_to_pot(player, self.JAIL_FINE, "jail fine"):
                player.in_jail = False
                player.jail_turns = 0
                self.log(f"{player.name} pays the fine and leaves jail.")
                self.roll_and_move(player)
        else:
            d1, d2, total, is_doubles = self.dice.roll()
            self.log(f"{player.name} rolled {d1} + {d2} = {total}" + (" (DOUBLES!)" if is_doubles else ""))
            if is_doubles:
                player.in_jail = False
                player.jail_turns = 0
                self.log(f"{player.name} rolled doubles and leaves jail!")
                self.move_player(player, total)
            else:
                player.jail_turns += 1
                if player.jail_turns >= 3:
                    self.log("Third failed attempt — the fine must be paid.")
                    if self.pay_to_pot(player, self.JAIL_FINE, "jail fine"):
                        player.in_jail = False
                        player.jail_turns = 0
                        self.log(f"{player.name} leaves jail and moves {total} spaces.")
                        self.move_player(player, total)
                else:
                    self.log(f"{player.name} stays in jail.")
    def roll_and_move(self, player):
        input(f"{player.name}, press Enter to roll the dice...")
        d1, d2, total, is_doubles = self.dice.roll()
        self.log(f"{player.name} rolled {d1} + {d2} = {total}" + (" (DOUBLES!)" if is_doubles else ""))
        self.move_player(player, total)
    # ---------- bankruptcy / end ----------
    def handle_bankruptcy(self, player):
        player.bankrupt = True
        self.log(f"*** {player.name} is BANKRUPT and is out of the game! ***")
        for prop in list(player.properties):
            prop.owner = None
        player.properties = []
        if len(self.active_players()) <= 1:
            self.game_over = True
    def declare_winner(self):
        active = self.active_players()
        print("\n" + "*" * 50)
        if len(active) == 1:
            winner = active[0]
            reason = "last player standing"
        else:
            winner = max(self.players, key=lambda p: p.net_worth())
            reason = f"richest after {self.round - 1} rounds"
        print(f"GAME OVER! Winner: {winner.name} ({reason}) with net worth ${winner.net_worth()}.")
        print("*" * 50)
    # ---------- display ----------
    def display_status(self, player):
        print("\n" + "=" * 50)
        print(f"ROUND {self.round} | {player.name}'s turn")
        print("=" * 50)
        for p in self.players:
            status = ""
            if p.bankrupt:
                status = " (BANKRUPT)"
            elif p.in_jail:
                status = " (IN JAIL)"
            props = ", ".join(prop.name for prop in p.properties) if p.properties else "none"
            print(f"  {p.name}: ${p.money} | position {p.position} | properties: {props}{status}")
        print(f"  Free Parking pot: ${self.free_parking_pot}")
        self.board.display(self.players)