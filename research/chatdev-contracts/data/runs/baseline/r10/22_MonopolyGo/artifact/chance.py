"""Chance module: defines chance cards and the deck."""
import random
from constants import CHANCE_CARDS
class ChanceCard:
    """A single chance card with an effect."""
    def __init__(self, description, effect, value):
        self.description = description
        self.effect = effect  # 'money', 'move_to', 'move_back', 'go_to_jail', 'get_out_of_jail'
        self.value = value
class ChanceDeck:
    """Deck of chance cards; draw randomly (reshuffle when empty)."""
    def __init__(self):
        self.cards = [ChanceCard(*c) for c in CHANCE_CARDS]
        self.deck = []
    def draw(self):
        if not self.deck:
            self.deck = self.cards[:]
            random.shuffle(self.deck)
        return self.deck.pop()