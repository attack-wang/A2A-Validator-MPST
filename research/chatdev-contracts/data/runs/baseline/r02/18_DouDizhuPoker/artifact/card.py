"""Card and Deck classes for the Dou Dizhu game."""
import random
from constants import RANKS, RANK_VALUE, SUITS, SUIT_SYMBOLS
class Card:
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUE[rank]
    @property
    def is_joker(self):
        return self.suit is None
    def __str__(self):
        if self.is_joker:
            return self.rank
        return f"{SUIT_SYMBOLS[self.suit]}{self.rank}"
    __repr__ = __str__
    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))
    def __lt__(self, other):
        if self.value != other.value:
            return self.value < other.value
        return (self.suit or '') < (other.suit or '')
class Deck:
    """Standard 54-card deck."""
    def __init__(self):
        self.cards = []
        for rank in RANKS:
            if RANK_VALUE[rank] >= 16:
                self.cards.append(Card(rank, None))
            else:
                for suit in SUITS:
                    self.cards.append(Card(rank, suit))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        """Return (hand1, hand2, hand3, bottom): 17/17/17 + 3 bottom cards."""
        self.shuffle()
        return self.cards[:17], self.cards[17:34], self.cards[34:51], self.cards[51:]