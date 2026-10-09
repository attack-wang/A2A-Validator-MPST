'''
chance.py: Chance card definitions and deck management.
'''
import random
class ChanceCard:
    """A single chance card with a human-readable description and an effect key."""
    def __init__(self, description, effect):
        """Store the card text and the machine-readable effect identifier."""
        self.description = description
        self.effect = effect
class ChanceDeck:
    """A shuffled deck of chance cards that reshuffles when exhausted."""
    def __init__(self):
        """Build the full card list and prepare a shuffled draw pile."""
        self._cards = [
            ChanceCard("Advance to GO and collect $200!", "go_to_go"),
            ChanceCard("Go directly to Jail. Do not pass GO, do not collect $200.", "go_to_jail"),
            ChanceCard("Bank pays you a dividend of $100.", "collect_100"),
            ChanceCard("Pay school fees of $75.", "pay_75"),
            ChanceCard("Speeding fine of $50 — the money goes to the Free Parking pot.", "fine_to_pot"),
            ChanceCard("You won a beauty contest! Collect $50.", "collect_50"),
            ChanceCard("Doctor's fee. Pay $50.", "pay_50"),
            ChanceCard("Building repairs: pay $40 per property you own.", "repairs"),
            ChanceCard("Get Out of Jail Free — keep this card until needed.", "jail_free_card"),
            ChanceCard("Take a stroll: advance 3 spaces.", "advance_3"),
            ChanceCard("Bank error in your favour: collect $150.", "collect_150"),
            ChanceCard("Pay tax of $100 to the Free Parking pot.", "tax_to_pot"),
        ]
        self._draw_pile = []
        self._reshuffle()
    def _reshuffle(self):
        """Rebuild the draw pile from all cards and shuffle it."""
        self._draw_pile = self._cards[:]
        random.shuffle(self._draw_pile)
    def draw(self):
        """Pop and return the top card, reshuffling first if the pile is empty."""
        if not self._draw_pile:
            self._reshuffle()
        return self._draw_pile.pop()