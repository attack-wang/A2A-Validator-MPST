import random
class ChanceCard:
    EFFECTS = ("money", "move_to", "move_back", "jail", "jail_free", "collect_each", "pay_each")
    def __init__(self, description, effect, amount=0, target=None):
        if effect not in ChanceCard.EFFECTS:
            raise ValueError(f"Unknown chance effect: {effect}")
        self.description = description
        self.effect = effect
        self.amount = amount
        self.target = target
    def apply(self, player, game):
        if self.effect == "money":
            if self.amount >= 0:
                player.receive(self.amount)
                game.log(f"{player.name} collects ${self.amount} from the bank.")
            else:
                game.pay_to_pot(player, -self.amount, "bank fee")
        elif self.effect == "move_to":
            game.move_to(player, self.target)
        elif self.effect == "move_back":
            game.move_player(player, -self.amount)
        elif self.effect == "jail":
            game.send_to_jail(player)
        elif self.effect == "jail_free":
            player.jail_free_cards.append(self)
            game.log(f"{player.name} keeps this card as a Get Out of Jail Free card.")
        elif self.effect == "collect_each":
            for other in game.active_players():
                if other is not player and not player.bankrupt:
                    game.log(f"{other.name} pays {player.name} ${self.amount}.")
                    game.transfer(other, player, self.amount)
        elif self.effect == "pay_each":
            for other in game.active_players():
                if other is not player and not player.bankrupt:
                    game.log(f"{player.name} pays {other.name} ${self.amount}.")
                    game.transfer(player, other, self.amount)
def build_standard_deck():
    return [
        ChanceCard("Advance to GO. Collect $200.", "move_to", target=0),
        ChanceCard("Go directly to Jail. Do not pass GO, do not collect $200.", "jail"),
        ChanceCard("The bank pays you a dividend of $50.", "money", amount=50),
        ChanceCard("Pay hospital fees of $100.", "money", amount=-100),
        ChanceCard("Speeding fine: pay $15.", "money", amount=-15),
        ChanceCard("You won second prize in a beauty contest. Collect $10.", "money", amount=10),
        ChanceCard("Go back 3 spaces.", "move_back", amount=3),
        ChanceCard("Take a walk to Boardwalk. Advance to Boardwalk.", "move_to", target=23),
        ChanceCard("Get Out of Jail Free. Keep this card until needed.", "jail_free"),
        ChanceCard("It's your birthday! Collect $10 from every player.", "collect_each", amount=10),
        ChanceCard("You owe each player $25. Pay up!", "pay_each", amount=25),
        ChanceCard("Advance to Free Parking.", "move_to", target=10),
    ]
class ChanceDeck:
    def __init__(self, cards):
        self.all_cards = list(cards)
        self.draw_pile = []
        self.discard_pile = []
        self.reset()
    def reset(self):
        self.draw_pile = list(self.all_cards)
        random.shuffle(self.draw_pile)
        self.discard_pile = []
    def draw(self):
        if not self.draw_pile:
            self.draw_pile = self.discard_pile
            self.discard_pile = []
            random.shuffle(self.draw_pile)
        if not self.draw_pile:
            self.draw_pile = [c for c in self.all_cards if c.effect != "jail_free"]
            random.shuffle(self.draw_pile)
        return self.draw_pile.pop()
    def discard(self, card):
        self.discard_pile.append(card)
    def return_to_deck(self, card):
        self.discard_pile.append(card)