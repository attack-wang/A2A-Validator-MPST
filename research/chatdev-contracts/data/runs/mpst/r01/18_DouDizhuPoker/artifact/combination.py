'''
Combination module: parse card sets into valid Dou Dizhu combinations and compare them.
'''
from enum import Enum, auto
from collections import Counter
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
    FOUR_TWO_SINGLE = auto()
    FOUR_TWO_PAIR = auto()
    BOMB = auto()
    ROCKET = auto()
MAX_SEQUENCE_VALUE = 14  # 'A'; '2' and jokers may not appear in sequences
class Combination:
    def __init__(self, cards, ctype, main_value, length):
        self.cards = sorted(cards, key=lambda c: c.value)
        self.ctype = ctype
        self.main_value = main_value
        self.length = length
    @staticmethod
    def _is_consecutive(values):
        values = sorted(values)
        return all(values[i + 1] - values[i] == 1 for i in range(len(values) - 1))
    @classmethod
    def parse(cls, cards):
        cards = sorted(cards, key=lambda c: c.value)
        n = len(cards)
        if n == 0:
            return None
        counts = Counter(c.value for c in cards)
        distinct = sorted(counts)
        # Rocket
        if n == 2 and counts.get(16, 0) == 1 and counts.get(17, 0) == 1:
            return cls(cards, CombType.ROCKET, 17, 1)
        # Single
        if n == 1:
            return cls(cards, CombType.SINGLE, cards[0].value, 1)
        # Pair
        if n == 2 and len(counts) == 1:
            return cls(cards, CombType.PAIR, cards[0].value, 1)
        # Triple
        if n == 3 and len(counts) == 1:
            return cls(cards, CombType.TRIPLE, cards[0].value, 1)
        # Bomb
        if n == 4 and len(counts) == 1:
            return cls(cards, CombType.BOMB, cards[0].value, 1)
        # Triple + single
        if n == 4 and len(counts) == 2 and 3 in counts.values():
            triple = [v for v, c in counts.items() if c == 3][0]
            return cls(cards, CombType.TRIPLE_SINGLE, triple, 1)
        # Triple + pair
        if n == 5 and sorted(counts.values()) == [2, 3]:
            triple = [v for v, c in counts.items() if c == 3][0]
            return cls(cards, CombType.TRIPLE_PAIR, triple, 1)
        # Straight
        if n >= 5 and len(counts) == n and max(distinct) <= MAX_SEQUENCE_VALUE and cls._is_consecutive(distinct):
            return cls(cards, CombType.STRAIGHT, max(distinct), n)
        # Pair straight
        if n >= 6 and n % 2 == 0 and len(counts) == n // 2 and all(c == 2 for c in counts.values()) \
                and max(distinct) <= MAX_SEQUENCE_VALUE and cls._is_consecutive(distinct):
            return cls(cards, CombType.PAIR_STRAIGHT, max(distinct), n // 2)
        # Four with two singles
        if n == 6 and 4 in counts.values():
            quads = [v for v, c in counts.items() if c == 4]
            if len(quads) == 1:
                rest = {v: c for v, c in counts.items() if v != quads[0]}
                if sum(rest.values()) == 2 and all(c <= 2 for c in rest.values()):
                    return cls(cards, CombType.FOUR_TWO_SINGLE, quads[0], 1)
        # Four with two pairs
        if n == 8 and sorted(counts.values()) == [2, 2, 4]:
            quad = [v for v, c in counts.items() if c == 4][0]
            return cls(cards, CombType.FOUR_TWO_PAIR, quad, 1)
        # Airplane (pure)
        if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts.values()) \
                and max(distinct) <= MAX_SEQUENCE_VALUE and cls._is_consecutive(distinct):
            return cls(cards, CombType.AIRPLANE, max(distinct), n // 3)
        # Airplane with single wings
        if n >= 8 and n % 4 == 0:
            combo = cls._parse_airplane_wings(counts, n // 4, 1)
            if combo is not None:
                return combo
        # Airplane with pair wings
        if n >= 10 and n % 5 == 0:
            combo = cls._parse_airplane_wings(counts, n // 5, 2)
            if combo is not None:
                return combo
        return None
    @classmethod
    def _parse_airplane_wings(cls, counts, k, wing_size):
        if k < 2:
            return None
        triple_values = sorted(v for v, c in counts.items() if c >= 3 and v <= MAX_SEQUENCE_VALUE)
        for start in range(len(triple_values) - k + 1):
            run = triple_values[start:start + k]
            if not cls._is_consecutive(run):
                continue
            remaining = Counter(counts)
            for v in run:
                remaining[v] -= 3
            if all(c == wing_size for c in remaining.values()) and sum(remaining.values()) == k * wing_size:
                return None  # placeholder — need cards
        return None