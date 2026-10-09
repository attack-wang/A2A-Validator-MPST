'''
card.py
Card model and 54-card deck construction for Dou Dizhu.
'''
from constants import RANK_ORDER, RANK_VALUE, SMALL_JOKER_VALUE, BIG_JOKER_VALUE
class Card:
    """A single playing card; jokers use rank 'joker' with suit 'small'/'big'."""
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    @property
    def value(self):
        """Numeric strength used for all comparisons (3..17)."""
        if self.rank == 'joker':
            return BIG_JOKER_VALUE if self.suit == 'big' else SMALL_JOKER_VALUE
        return RANK_VALUE[self.rank]
    def __str__(self):
        if self.rank == 'joker':
            return 'Joker(big)' if self.suit == 'big' else 'Joker(small)'
        return f"{self.rank}{self.suit}"
    __repr__ = __str__
    def __eq__(self, other):
        return isinstance(other, Card) and (self.value, self.suit) == (other.value, other.suit)
    def __hash__(self):
        return hash((self.value, self.suit))
    def __lt__(self, other):
        return self.value < other.value
def build_deck():
    """Build the standard 54-card Dou Dizhu deck (52 suited cards + 2 jokers)."""
    deck = [Card(r, s) for r in RANK_ORDER for s in ('♠', '♥', '♣', '♦')]
    deck.append(Card('joker', 'small'))
    deck.append(Card('joker', 'big'))
    return deck