'''
card.py
The Card class. A card has a rank ('3'..'2', 'joker', 'JOKER') and a suit
('♠', '♥', '♣', '♦') or None for jokers.
Cards are ordered primarily by their Dou Dizhu value (3 < ... < 2 < jokers),
ties broken by suit so that every card in the deck is unique and sortable.
'''
from functools import total_ordering
from constants import RANK_VALUES, RANK_NAMES
@total_ordering
class Card:
    """A single playing card."""
    def __init__(self, rank, suit=None):
        if rank not in RANK_VALUES:
            raise ValueError(f'Unknown rank: {rank!r}')
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]
    @property
    def is_joker(self):
        return self.suit is None
    @property
    def display(self):
        """Human readable name, e.g. '♠A' or 'Big Joker'."""
        if self.is_joker:
            return RANK_NAMES.get(self.rank, self.rank)
        return f'{self.suit}{self.rank}'
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value and self.suit == other.suit
    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return (self.value, str(self.suit)) < (other.value, str(other.suit))
    def __hash__(self):
        return hash((self.value, self.suit))
    def __repr__(self):
        return f'Card({self.display})'
    def __str__(self):
        return self.display