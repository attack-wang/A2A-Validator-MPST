'''
combination.py
Parsing and comparison of Dou Dizhu card combinations.
A Combination classifies a set of cards into a ComboType, computes its
main value and sequence length, and knows whether it beats another combo.
'''
from collections import Counter
from enum import Enum
from cards import RANK_VALUE, VALUE_RANK, MAX_STRAIGHT_VALUE
class ComboType(Enum):
    SINGLE = 'single'
    PAIR = 'pair'
    TRIPLE = 'triple'
    TRIPLE_SINGLE = 'triple_single'
    TRIPLE_PAIR = 'triple_pair'
    STRAIGHT = 'straight'
    PAIR_STRAIGHT = 'pair_straight'
    AIRPLANE = 'airplane'
    AIRPLANE_SINGLE = 'airplane_single'
    AIRPLANE_PAIR = 'airplane_pair'
    FOUR_TWO_SINGLE = 'four_two_single'
    FOUR_TWO_PAIR = 'four_two_pair'
    BOMB = 'bomb'
    ROCKET = 'rocket'
    INVALID = 'invalid'
class Combination:
    """A played set of cards, classified per standard Dou Dizhu rules."""
    def __init__(self, cards):
        self.cards = list(cards)
        self.type, self.main_value, self.sequence_length = self._analyze()
    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _is_consecutive(values):
        return all(b - a == 1 for a, b in zip(values, values[1:]))
    @staticmethod
    def _rank_of_count(counts, wanted):
        """Return the (unique) rank holding exactly `wanted` copies."""
        for rank, cnt in counts.items():
            if cnt == wanted:
                return rank
        raise ValueError('no rank with that count')
    def _analyze(self):
        ...