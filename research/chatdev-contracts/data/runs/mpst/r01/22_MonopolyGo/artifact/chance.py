'''
chance.py
Simplified chance cards and the deck used to draw them.
Each card carries an effect key that the Game class interprets.
'''
import random
class ChanceCard:
    """One chance card with a text description and an effect."""
    def __init__(self, text, effect, amount=0, target=None):
        self.text = text
        self.effect = effect  # see Game._apply_chance_card
        self.amount = amount
        self.target = target
    def __str__(self):
        return self.text
class ChanceDeck:
    """A shuffled, endlessly cycling deck of chance cards."""
    def __init__(self):
        self.cards = self._build()
        random.shuffle(self.cards)
        self._index = 0
    def _build(self):
        return [
            ChanceCard("Advance to GO! Collect $200.", "goto", 200, 0),
            ChanceCard("Bank error in your favor — collect $75.", "collect", 75),
            ChanceCard("Bank pays you a dividend of $50.", "collect", 50),
            ChanceCard("Go directly to Jail. Do not pass GO, do not collect $200.", "goto_jail"),
            ChanceCard("Speeding fine: pay $15.", "fine", 15),
            ChanceCard("You won the beauty contest! Collect $100.", "collect", 100),
            ChanceCard("It's your birthday! Collect $10 from every player.", "collect_from_each", 10),
            ChanceCard("Charity donation: pay $25 to every player.", "pay_each", 25),
            ChanceCard("Get Out of Jail Free! Keep this card until you need it.", "jail_free"),
            ChanceCard("Take a stroll to Free Parking.", "goto", 0, 9),
            ChanceCard("Go back 3 spaces.", "move_back", 3),
            ChanceCard("Street repairs: pay $40 per property you own.", "repairs", 40),
        ]
    def draw(self):
        card = self.cards[self._index]
        self._index = (self._index + 1) % len(self.cards)
        return card