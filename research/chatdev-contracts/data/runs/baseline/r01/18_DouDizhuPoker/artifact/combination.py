'''
combination.py
Combination model: classifies played cards into Dou Dizhu types and
implements the pass-or-beat comparison logic.
'''
from collections import Counter
from constants import (SINGLE, PAIR, TRIO, TRIO_SINGLE, TRIO_PAIR, STRAIGHT,
                       PAIR_STRAIGHT, AIRPLANE, AIRPLANE_SINGLE, AIRPLANE_PAIR,
                       FOUR_TWO_SINGLES, FOUR_TWO_PAIRS, BOMB, ROCKET,
                       SMALL_JOKER_VALUE, BIG_JOKER_VALUE, MAX_STRAIGHT_VALUE)
class Combination:
    """A set of played cards with its detected type, main value and length."""
    def __init__(self, cards):
        if not cards:
            raise ValueError('A combination needs at least one card.')
        self.cards = sorted(cards, key=lambda c: c.value)
        self.type, self.main_value, self.length = self._classify()
    def _classify(self):
        """Detect the Dou Dizhu type; returns (type, main_value, length)."""
        n = len(self.cards)
        values = [c.value for c in self.cards]
        cnt = Counter(values)
        counts = sorted(cnt.values(), reverse=True)
        uniq = sorted(cnt)
        if n == 2 and values == [SMALL_JOKER_VALUE, BIG_JOKER_VALUE]:
            return ROCKET, BIG_JOKER_VALUE, 1
        if n == 4 and counts == [4]:
            return BOMB, uniq[0], 1
        if n == 1:
            return SINGLE, uniq[0], 1
        if n == 2 and counts == [2]:
            return PAIR, uniq[0], 1
        if n == 3 and counts == [3]:
            return TRIO, uniq[0], 1
        if n == 4 and counts == [3, 1]:
            return TRIO_SINGLE, [v for v, c in cnt.items() if c == 3][0], 1
        if n == 5 and counts == [3, 2]:
            return TRIO_PAIR, [v for v, c in cnt.items() if c == 3][0], 1
        if n >= 5 and counts == [1] * n and uniq[-1] <= MAX_STRAIGHT_VALUE \
                and uniq[-1] - uniq[0] == n - 1:
            return STRAIGHT, uniq[0], n
        if n >= 6 and n % 2 == 0 and counts == [2] * (n // 2) \
                and uniq[-1] <= MAX_STRAIGHT_VALUE \
                and uniq[-1] - uniq[0] == n // 2 - 1:
            return PAIR_STRAIGHT, uniq[0], n // 2
        if n == 6 and counts == [4, 1, 1]:
            return FOUR_TWO_SINGLES, [v for v, c in cnt.items() if c == 4][0], 1
        if n == 8 and counts == [4, 2, 2]:
            return FOUR_TWO_PAIRS, [v for v, c in cnt.items() if c == 4][0], 1
        trio_vals = sorted(v for v, c in cnt.items() if c == 3)
        if len(trio_vals) >= 2 and trio_vals[-1] <= MAX_STRAIGHT_VALUE \
                and trio_vals[-1] - trio_vals[0] == len(trio_vals) - 1:
            others = n - 3 * len(trio_vals)
            if others == 0:
                return AIRPLANE, trio_vals[0], len(trio_vals)
            if others == len(trio_vals):
                return AIRPLANE_SINGLE, trio_vals[0], len(trio_vals)
            if others == 2 * len(trio_vals) and \
                    all(c % 2 == 0 for v, c in cnt.items() if c != 3):
                return AIRPLANE_PAIR, trio_vals[0], len(trio_vals)
        raise ValueError('Invalid combination: ' + ', '.join(str(c) for c in self.cards))
    def beats(self, other):
        """Return True if this combination legally beats `other` (None = free lead)."""
        if other is None:
            return True
        if self.type == ROCKET:
            return True
        if other.type == ROCKET:
            return False
        if self.type == BOMB and other.type != BOMB:
            return True
        if other.type == BOMB and self.type != BOMB:
            return False
        if self.type == BOMB and other.type == BOMB:
            return self.main_value > other.main_value
        if (self.type == other.type and self.length == other.length
                and len(self.cards) == len(other.cards)):
            return self.main_value > other.main_value
        return False
    def __str__(self):
        return f"[{self.type}] " + ' '.join(str(c) for c in self.cards)
    __repr__ = __str__