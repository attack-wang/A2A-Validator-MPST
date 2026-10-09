'''
game.py
Core game engine for the simplified Monopoly Go! game. Contains the Game
class which manages players, the board, turns, transactions, chance cards,
jail rules and the console-based user interface.
'''
from board import Board, Property, ChanceSpace, JailSpace, GoToJailSpace, FreeParkingSpace, GoSpace
from player import Player
from dice import Dice
from chance import ChanceDeck
class Game:
    '''Controls the full game loop and all console interaction.'''
    GO_SALARY = 200
    JAIL_FINE = 50
    MAX_CONSECUTIVE_DOUBLES = 3
    def __init__(self, player_names, starting_money=1500, max_rounds=20):
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.players = [Player(name, starting_money) for name in player_names]
        self.round_number = 1
        self.max_rounds = max_rounds
        self.free_parking_pot = 0
        self.game_over = False
    def active_players(self):
        return [p for p in self.players if not p.is_bankrupt()]
    def play(self):
        self.print_welcome()
        while not self.game_over:
            for player in list(self.players):
                if self.game_over:
                    break
                if player.is_bankrupt():
                    continue
                self.take_turn(player)
                self.check_game_over()
            if not self.game_over:
                self.round_number += 1
                if self.round_number > self.max_rounds:
                    self.game_over = True
        self.announce_winner()
    def print_welcome(self):
        print("=" * 60)
        print("        WELCOME TO SIMPLIFIED MONOPOLY GO!")
        print("=" * 60)
        print("Rules:")
        print(" - Roll two dice and move around the board.")
        print(" - Land on an unowned property: you may buy it.")
        print(" - Land on an owned property: pay rent to the owner.")
        print(" - Roll doubles to roll again; three doubles in a row -> jail!")
        print(" - Chance spaces draw a card with a random effect.")
        print(f" - Go To Jail sends you to jail; pay ${self.JAIL_FINE} or roll doubles to leave.")
        print(" - Free Parking pays out the collected fine pot.")
        print(f" - Game ends after {self.max_rounds} rounds or when one player remains.")
        print("=" * 60)
    def take_turn(self, player):
        print("\n" + "-" * 60)
        print(f"Round {self.round_number} | {player.name}'s turn")
        self.show_player_status(player)
        doubles_count = 0
        while True:
            if player.in_jail:
                if not self.handle_jail(player):
                    break
            input(f"  {player.name}, press Enter to roll the dice...")
            die1, die2, total, is_doubles = self.dice.roll()
            print(f"  {player.name} rolled {die1} + {die2} = {total}"
                  + (" (DOUBLES!)" if is_doubles else ""))
            if is_doubles:
                doubles_count += 1
                if doubles_count >= self.MAX_CONSECUTIVE_DOUBLES:
                    print(f"  Three doubles in a row! {player.name} goes to jail.")
                    self.send_to_jail(player)
                    break
            self.move_player(player, total)
            self.handle_landing(player)
            if player.is_bankrupt() or player.in_jail:
                break
            if not is_doubles:
                break
            print(f"  Doubles! {player.name} rolls again.")
        self.show_player_status(player)
        self.display_board()
    def handle_jail(self, player):
        '''Handle a player's turn while incarcerated.
        Returns True if released and may roll normally, False if turn ends.'''
        print(f"  {player.name} is in jail (attempt {player.jail_turns + 1}/{Player.MAX_JAIL_TURNS}).")
        choice = ""
        while choice not in ("pay", "roll"):
            choice = input(f"  Pay ${self.JAIL_FINE} fine or roll for doubles? (pay/roll): ").strip().lower()
        if choice == "pay" and player.can_afford(self.JAIL_FINE):
            paid = player.pay(self.JAIL_FINE)
            self.free_parking_pot += paid
            player.release_from_jail()
            print(f"  {player.name} paid a ${paid} fine and is released (may roll normally).")
            return True
        if choice == "pay":
            print(f"  {player.name} cannot afford the fine and must roll for doubles.")
        die1, die2, total, is_doubles = self.dice.roll()
        print(f"  Jail roll: {die1} + {die2} = {total}" + (" (DOUBLES!)" if is_doubles else ""))
        if is_doubles:
            player.release_from_jail()
            print(f"  {player.name} rolls doubles and leaves jail!")
            self.move_player(player, total)
            self.handle_landing(player)
            return False
        player.jail_turns += 1
        if player.jail_turns >= Player.MAX_JAIL_TURNS:
            paid = player.pay(self.JAIL_FINE)
            self.free_parking_pot += paid
            player.release_from_jail()
            print(f"  Third failed attempt: {player.name} pays ${paid} and is released (no move).")
        else:
            print(f"  No doubles. {player.name} stays in jail.")
        return False
    def move_player(self, player, steps):
        old = player.position
        player.position = (player.position + steps) % self.board.size()
        if old + steps >= self.board.size():
            player.receive(self.GO_SALARY)
            print(f"  {player.name} passed GO and collects ${self.GO_SALARY}.")
        print(f"  {player.name} moved to space {player.position}: {self.board.get_space(player.position)}")
    def move_player_to(self, player, target):
        target = target % self.board.size()
        if target < player.position:
            player.receive(self.GO_SALARY)
            print(f"  {player.name} passed GO and collects ${self.GO_SALARY}.")
        player.position = target
        print(f"  {player.name} moved to space {player.position}: {self.board.get_space(player.position)}")
    def move_player_back(self, player, steps):
        player.position = (player.position - steps) % self.board.size()
        print(f"  {player.name} moved back to space {player.position}: {self.board.get_space(player.position)}")
    def send_to_jail(self, player):
        player.send_to_jail(self.board.JAIL_POSITION)
        print(f"  {player.name} is sent directly to JAIL!")
    def handle_landing(self, player):
        space = self.board.get_space(player.position)
        if isinstance(space, Property):
            self.handle_property(player, space)
        elif isinstance(space, ChanceSpace):
            self.handle_chance(player)
        elif isinstance(space, GoToJailSpace):
            self.send_to_jail(player)
        elif isinstance(space, FreeParkingSpace):
            self.handle_free_parking(player)
        elif isinstance(space, JailSpace):
            print(f"  {player.name} is just visiting jail.")
        elif isinstance(space, GoSpace):
            print(f"  {player.name} rests on GO.")
    def handle_property(self, player, prop):
        if not prop.is_owned():
            if player.can_afford(prop.price):
                choice = input(f"  {prop.name} is unowned (price ${prop.price}, rent ${prop.rent}). Buy it? (yes/no): ").strip().lower()
                if choice in ("yes", "y"):
                    player.pay(prop.price)
                    player.add_property(prop)
                    prop.owner = player
                    print(f"  {player.name} bought {prop.name} for ${prop.price}.")
                else:
                    print(f"  {player.name} declined to buy {prop.name}.")
            else:
                print(f"  {player.name} cannot afford {prop.name} (${prop.price}).")
        elif prop.is_owned_by(player):
            print(f"  {player.name} owns {prop.name}. No rent due.")
        else:
            paid = player.pay(prop.rent)
            prop.owner.receive(paid)
            print(f"  {player.name} pays ${paid} rent to {prop.owner.name} for {prop.name}.")
            if player.is_bankrupt():
                self.handle_bankruptcy(player)
    def handle_chance(self, player):
        card = self.chance_deck.draw()
        print(f"  {player.name} draws a Chance card: \"{card.description}\"")
        if card.effect == "money":
            if card.amount >= 0:
                player.receive(card.amount)
                print(f"  {player.name} receives ${card.amount}.")
            else:
                paid = player.pay(-card.amount)
                self.free_parking_pot += paid
                print(f"  {player.name} pays ${paid}.")
                if player.is_bankrupt():
                    self.handle_bankruptcy(player)
        elif card.effect == "advance_to_go":
            self.move_player_to(player, 0)
        elif card.effect == "move_to":
            self.move_player_to(player, card.amount)
            self.handle_landing(player)
        elif card.effect == "move_back":
            self.move_player_back(player, card.amount)
            self.handle_landing(player)
        elif card.effect == "go_to_jail":
            self.send_to_jail(player)
    def handle_free_parking(self, player):
        if self.free_parking_pot > 0:
            player.receive(self.free_parking_pot)
            print(f"  {player.name} lands on Free Parking and collects the pot of ${self.free_parking_pot}!")
            self.free_parking_pot = 0
        else:
            print(f"  {player.name} lands on Free Parking. The pot is empty.")
    def handle_bankruptcy(self, player):
        released = player.remove_properties()
        print(f"  {player.name} is BANKRUPT and leaves the game! "
              f"{len(released)} property(ies) returned to the bank.")
    def check_game_over(self):
        if len(self.active_players()) <= 1:
            self.game_over = True
    def announce_winner(self):
        print("\n" + "=" * 60)
        print("GAME OVER!")
        alive = self.active_players()
        if len(alive) == 1:
            print(f"The winner is {alive[0].name} with ${alive[0].money} in cash!")
        else:
            ranked = sorted(self.players, key=lambda p: p.net_worth(), reverse=True)
            print("Round limit reached. Final standings by net worth:")
            for i, p in enumerate(ranked, 1):
                print(f"  {i}. {p.name}: ${p.net_worth()} (cash ${p.money})")
            print(f"Leader: {ranked[0].name}!")
        print("=" * 60)
    def show_player_status(self, player):
        space = self.board.get_space(player.position)
        print(f"  [{player.name}] Money: ${player.money} | Position: {player.position} ({space}) | Properties: {player.property_names()}")
    def display_board(self):
        print("\n" + "=" * 60)
        print("==================== GAME BOARD ====================")
        for i, space in enumerate(self.board.spaces):
            line = f" {i:2d}. {space.name:<24}"
            if isinstance(space, Property):
                owner = space.owner.name if space.owner else "Bank"
                line += f"| ${space.price}, Rent ${space.rent} | Owner: {owner:<10}"
            else:
                line += "| " + " " * 38
            here = [p.name for p in self.players if p.position == i and not p.is_bankrupt()]
            line += "| Players: " + (", ".join(here) if here else "-")
            print(line)
        print(f" Free Parking pot: ${self.free_parking_pot}")
        print("=" * 60)