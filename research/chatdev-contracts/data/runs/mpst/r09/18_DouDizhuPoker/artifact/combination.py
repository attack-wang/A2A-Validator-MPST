'''
combination.py
Defines combination types and the Combination class that parses a set of
cards into a valid Dou Dizhu combination and compares it against others.
'''
from enum import Enum, auto
from card import RANK_NAMES
class CombType(Enum):
    SINGLE = auto()
    PAIR = auto()
    TRIPLE = auto()
    TRIPLE_SINGLE = auto()
    TRIPLE_PAIR = auto()
    STRAIGHT = auto()
    PAIR_STRAIGHT = auto()
    AIRPLANE = auto()
    AIRPLANE_SINGLE = auto()
    AIRPLANE_PAIR = auto()
    FOUR_TWO_SINGLES = auto()
    FOUR_TWO_PAIRS = auto()
    BOMB = auto()
    ROCKET = auto()
class Combination:
    def __init__(self, cards):
        self.cards = sorted(cards, key=lambda c: c.rank)
        self.type = None
        self.rank = 0  # main rank used for comparison
        self.length = 0  # number of units for sequences
        self._parse()
    def _parse(self):
        # count ranks
        from collections import Counter
        counts = Counter(c.rank for c in self.cards)
        n = len(self.cards)
        ...