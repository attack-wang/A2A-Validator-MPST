class ChanceCard:
    def __init__(self, text, effect, amount=0, target=None):
        ...
class ChanceDeck:
    def __init__(self):
        self.cards = [...]
        self.jail_card_in_deck = True  # the jail card is only drawn while in deck
    def draw(self):
        available = [c for c in self.cards if c.effect != "jail_card" or self.jail_card_in_deck]
        card = random.choice(available)
        if card.effect == "jail_card":
            self.jail_card_in_deck = False
        return card
    def return_jail_card(self):
        self.jail_card_in_deck = True