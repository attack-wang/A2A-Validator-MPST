'''
game.py
Core game engine for the simplified Monopoly Go! game.
Manages turns, dice rolls, movement, property purchases, rent,
chance cards, jail rules and bankruptcy until a winner emerges.
'''
import sys
from player import Player
from board import Board
from dice import Dice
from chance import ChanceDeck
import ui
class Game:
    """Runs the simplified Monopoly Go! match."""
    MAX_JAIL_TURNS = 3
    DOUBLES_LIMIT = 3  # three doubles in a row sends you to jail
    def __init__(self, player_names, max_rounds=20):
        self.board = Board()
        self.dice = Dice()
        self.chance_deck = ChanceDeck()
        self.players = [Player(name) for name in player_names]
        self.max_rounds = max_rounds
        self.round_num = 0
        self.game_over = False
    # ----- main loop ----------------------------------------------
    def play(self):
        """Run the game until one player remains or rounds run out."""
        ui.banner()
        ui.show_message(f"Starting a {self.max_rounds}-round game with {len(self.players)} players.")
        while not self.game_over:
            self.round_num += 1
            ui.show_round(self.round_num, self.max_rounds)
            ui.show_player_summary(self.players)
            for player in list(self.players):
                if self.game_over:
                    break
                if not player.is_active:
                    continue
                self.take_turn(player)
            if self.round_num >= self.max_rounds:
                self.game_over = True
            if self._active_players_count() <= 1:
                self.game_over = True
        return self._determine_winner()
    def _active_players_count(self):
        return sum(1 for p in self.players if p.is_active)
    def _determine_winner(self):
        active = [p for p in self.players if p.is_active]
        if len(active) == 1:
            return active[0]
        if not active:
            return None
        return max(active, key=lambda p: p.net_worth())
    # ----- turn handling ------------------------------------------
    def take_turn(self, player):
        ui.show_turn_header(player)
        if player.in_jail:
            if not self._handle_jail_turn(player):
                return
        doubles_count = 0
        while True:
            ui.prompt(f"{player.name}, press Enter to roll the dice...")
            die1, die2 = self.dice.roll()
            total = die1 + die2
            is_doubles = self.dice.is_doubles(die1, die2)
            ui.show_dice_roll(die1, die2, total, is_doubles)
            self._move_player(player, total)
            self._resolve_landing(player)
            if player.bankrupt or player.in_jail:
                return
            if is_doubles:
                doubles_count += 1
                if doubles_count >= self.DOUBLES_LIMIT:
                    ui.show_message("Three doubles in a row! Go directly to Jail.")
                    player.send_to_jail(self.board.JAIL_POS)
                    return
                ui.show_message("Doubles! Roll again.")
                continue
            break
    def _handle_jail_turn(self, player):
        """Return True when the player leaves jail and takes a normal turn."""
        if player.has_jail_free_card() and ui.prompt_yes_no(f"{player.name}, use your Get Out of Jail Free card?"):
            player.use_jail_free_card()
            player.release_from_jail()
            ui.show_message(f"{player.name} used a Get Out of Jail Free card!")
            return True
        if player.can_afford(Player.JAIL_BAIL) and ui.prompt_yes_no(f"{player.name}, pay $50 bail to leave jail?"):
            player.pay(Player.JAIL_BAIL)
            player.release_from_jail()
            ui.show_message(f"{player.name} paid $50 bail.")
            return True
        die1, die2 = self.dice.roll()
        is_doubles = self.dice.is_doubles(die1, die2)
        ui.show_dice_roll(die1, die2, die1 + die2, is_doubles)
        player.jail_turns += 1
        if is_doubles:
            player.release_from_jail()
            ui.show_message(f"{player.name} rolled doubles and leaves jail!")
            return True
        if player.jail_turns >= self.MAX_JAIL_TURNS:
            ui.show_message(f"{player.name} served the maximum jail time and pays $50 bail.")
            player.pay(Player.JAIL_BAIL)
            player.release_from_jail()
            return True
        ui.show_message(f"{player.name} stays in jail (turn {player.jail_turns} of {self.MAX_JAIL_TURNS}).")
        return False
    def _move_player(self, player, steps):
        collected = self.board.move_forward(player, steps)
        if collected:
            ui.show_message(f"{player.name} passed GO and collected $200.")
        ui.show_message(f"{player.name} moved to {self.board.get_space(player.position).name}.")
    def _resolve_landing(self, player):
        space = self.board.get_space(player.position)
        if space.type == "property":
            self._handle_property(player, space)
        elif space.type == "chance":
            card = self.chance_deck.draw()
            ui.show_card(card)
            self._apply_chance_card(player, card)
        elif space.type == "go_to_jail":
            ui.show_message(f"{player.name} is sent directly to Jail!")
            player.send_to_jail(self.board.JAIL_POS)
        elif space.type == "free_parking":
            ui.show_message(f"{player.name} rests at Free Parking. Nothing happens.")
        elif space.type == "jail":
            ui.show_message(f"{player.name} is just visiting the jail.")
        elif space.type == "go":
            ui.show_message(f"{player.name} landed on GO.")
        ui.show_board(self.board, self.players)
    def _handle_property(self, player, prop):
        if not prop.is_owned():
            ui.show_property_card(prop)
            if player.can_afford(prop.price) and ui.prompt_yes_no(f"{player.name}, buy {prop.name} for ${prop.price}?"):
                player.pay(prop.price)
                prop.purchase(player)
                ui.show_message(f"{player.name} bought {prop.name} for ${prop.price}.")
            elif not player.can_afford(prop.price):
                ui.show_message(f"{player.name} cannot afford {prop.name}.")
        elif prop.is_owned_by(player):
            ui.show_message(f"{player.name} owns {prop.name}. Welcome home!")
        else:
            rent = prop.rent
            ui.show_message(f"{player.name} pays ${rent} rent to {prop.owner.name}.")
            paid = player.pay(rent)
            prop.owner.receive(paid)
            if paid < rent:
                ui.show_message(f"{player.name} could only pay ${paid}!")
            self._check_bankruptcy(player)
    # ----- chance effects -----------------------------------------
    def _apply_chance_card(self, player, card):
        effect = card.effect
        if effect == "collect":
            player.receive(card.amount)
            ui.show_message(f"{player.name} collects ${card.amount}.")
        elif effect == "fine":
            paid = player.pay(card.amount)
            ui.show_message(f"{player.name} pays a ${card.amount} fine.")
            self._check_bankruptcy(player)
        elif effect == "goto":
            target = card.target if card.target is not None else self.board.GO_POS
            if target == self.board.GO_POS:
                player.receive(self.board.GO_BONUS)
                ui.show_message(f"{player.name} advances to GO and collects $200.")
            else:
                ui.show_message(f"{player.name} advances to {self.board.get_space(target).name}.")
            player.position = target
            self._resolve_landing(player)
        elif effect == "goto_jail":
            ui.show_message(f"{player.name} goes directly to Jail!")
            player.send_to_jail(self.board.JAIL_POS)
        elif effect == "collect_from_each":
            total = 0
            for other in self.players:
                if other is player or not other.is_active:
                    continue
                total += other.pay(card.amount)
                self._check_bankruptcy(other)
            player.receive(total)
            ui.show_message(f"{player.name} collects ${total} from the other players.")
        elif effect == "pay_each":
            for other in self.players:
                if other is player or not other.is_active:
                    continue
                paid = player.pay(card.amount)
                other.receive(paid)
            ui.show_message(f"{player.name} pays ${card.amount} to each player.")
            self._check_bankruptcy(player)
        elif effect == "jail_free":
            player.jail_free_cards += 1
            ui.show_message(f"{player.name} keeps a Get Out of Jail Free card.")
        elif effect == "move_back":
            self.board.move_backward(player, card.amount)
            ui.show_message(f"{player.name} moves back {card.amount} spaces to {self.board.get_space(player.position).name}.")
            self._resolve_landing(player)
        elif effect == "repairs":
            cost = card.amount * len(player.properties)
            if cost > 0:
                paid = player.pay(cost)
                ui.show_message(f"{player.name} pays ${paid} for repairs on {len(player.properties)} properties.")
                self._check_bankruptcy(player)
            else:
                ui.show_message(f"{player.name} owns no properties, so repairs cost nothing.")
    def _check_bankruptcy(self, player):
        if player.money <= 0 and not player.bankrupt:
            player.bankrupt = True
            released = player.release_properties()
            ui.show_message(f"{player.name} is BANKRUPT! {len(released)} properties returned to the bank.")