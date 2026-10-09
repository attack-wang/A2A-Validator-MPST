'''
card.py
Defines the Card class used throughout the Dou Dizhu game.
Rank values:
    3-10  -> face value 3..10
    J     -> 11, Q -> 12, K -> 13, A -> 14, 2 -> 15
    Small Joker -> 16, Big Joker -> 17
'''
import functools
@functools.total_ordering
class Card:
    """A single playing card for Dou Dizhu."""
    RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    RANK_VALUES = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                   '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
    SUITS = ['♠', '♥', '♣', '♦']
    def __init__(self, rank, suit=None):
        """rank: one of RANK_ORDER or 'SJOKER'/'BJOKER'; suit: one of SUITS (None for jokers)."""
        if rank in ('SJOKER', 'BJOKER'):
            self.rank = rank
            self.suit = None
        else:
            if rank not in self.RANK_VALUES:
                raise ValueError(f"Invalid rank: {rank}")
            if suit not in self.SUITS:
                raise ValueError(f"Invalid suit: {suit}")
            self.rank = rank
            self.suit = suit
    @property
    def rank_value(self):
        """Numerical strength of the card (jokers 16/17, '2' = 15)."""
        if self.rank == 'SJOKER':
            return 16
        if self.rank == 'BJOKER':
            return 17
        return self.RANK_VALUES[self.rank]
    def is_joker(self):
        return self.rank in ('SJOKER', 'BJOKER')
    def __eq__(self, other):
        return isinstance(other, Card) and self.rank_value == other.rank_value
    def __lt__(self, other):
        return self.rank_value < other.rank_value
    def __hash__(self):
        return hash((self.rank_value, self.rank))
    def __str__(self):
        if self.is_joker():
            return '小王' if self.rank == 'SJOKER' else '大王'
        return f"{self.rank}{self.suit}"
    def __repr__(self):
        return str(self)