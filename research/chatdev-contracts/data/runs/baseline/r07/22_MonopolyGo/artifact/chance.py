'''
chance.py
Chance card mechanics for the simplified Monopoly Go! game.
Defines the simplified chance card effects and the deck that shuffles
and draws them, including the "Get Out of Jail Free" card.
'''
import random
class ChanceCard:
    """One simplified chance card with a description and an effect key."""
    def __init__(self, description, effect, value=0):
        self.description = description
        self.effect = effect
        self.value = value
class ChanceDeck:
    """Shuffled deck of chance cards; draws cycle through the deck."""
    def __init__(self):
        self.cards = self._build()
        self.draw_pile = []
        self.shuffle()
    def _build(self):
        return [
            ChanceCard("Advance to GO! Collect $200.", "go_to_go"),
            ChanceCard("The bank pays you a dividend of $50.", "gain", 50),
            ChanceCard("You won a beauty contest! Collect $100.", "gain", 100),
            ChanceCard("It's your birthday! Collect $25 from every player.", "collect_from_all", 25),
            ChanceCard("Pay school fees of $50.", "pay", 50),
            ChanceCard("Speeding fine! Pay $15.", "pay", 15),
            ChanceCard("Doctor's fee! Pay $100.", "pay", 100),
            ChanceCard("Go directly to JAIL! Do not pass GO.", "go_to_jail"),
            ChanceCard("Go back 3 spaces.", "go_back", 3),
            ChanceCard("Take a stroll to Free Parking.", "go_to_free_parking"),
            ChanceCard("Building repairs: pay $20 for each property you own.", "pay_per_property", 20),
            ChanceCard("GET OUT OF JAIL FREE! Keep this card for later.", "jail_free"),
        ]
    def shuffle(self):
        self.draw_pile = self.cards[:]
        random.shuffle(self.draw_pile)
    def draw(self):
        """Draw the top card, reshuffling when the pile runs dry."""
        if not self.draw_pile:
            self.shuffle()
        return self.draw_pile.pop()