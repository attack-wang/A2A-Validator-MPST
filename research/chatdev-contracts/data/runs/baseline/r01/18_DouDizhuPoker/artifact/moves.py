'''
moves.py
Move generation: enumerates every legal Combination for a hand and
filters the ones that beat the current table combination.
'''
from collections import Counter
from itertools import combinations
from card import Card
from combination import Combination
from constants import (SMALL_JOKER_VALUE, BIG_JOKER_VALUE, MAX_STRAIGHT_VALUE)
def _group(hand):
    """Group hand cards by value; returns (values sorted asc, {value: [cards]})."""
    by_value = {}
    for c in hand:
        by_value.setdefault(c.value, []).append(c)
    for cards in by_value.values():
        cards.sort(key=lambda c: c.value)
    return sorted(by_value), by_value
def _consecutive_runs(values, min_len, max_len, need):
    """Yield lists of `need` consecutive values with length in [min_len, max_len]."""
    ...