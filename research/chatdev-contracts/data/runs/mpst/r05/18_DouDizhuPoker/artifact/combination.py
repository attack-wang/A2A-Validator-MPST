'''
combination.py
Combination detection and comparison for Dou Dizhu.
detect(cards) -> (CombinationType, primary_value, length)
    Returns (None, None, None) for an illegal set of cards.
primary_value is the "strength" of the combination:
    - the rank value for SINGLE/PAIR/TRIPLE/BOMB
    - the highest rank value for sequences (straights, pair straights, airplanes)
    - the rank value of the triple/quad for kicker combinations
length is the number of "sets" in sequence types (e.g. a 7-card straight has
length 7, a 3-triple airplane has length 3); it is 1 for non-sequence types.
Two combinations of a sequence type may only be compared when their lengths
are equal.
beats(other) implements the pass-or-beat rule:
    - a combination can only beat the same type with equal length and a
      higher primary value, or
    - a BOMB beats every non-bomb (and higher bombs), and
    - the ROCKET beats everything.
'''
from collections import Counter
from constants import (ACE, BIG_JOKER, SMALL_JOKER, CombinationType,
                       SEQUENCE_TYPES)
def detect(cards):
    """Classify a list of cards. Returns (type, primary_value, length)."""
    n = len(cards)
    if n == 0:
        return None, None, None
    counts = Counter(c.value for c in cards)
    values = sorted(counts)
    # Rocket: small joker + big joker
    if n == 2 and values == [SMALL_JOKER, BIG_JOKER]:
        return CombinationType.ROCKET, BIG_JOKER, 1
    if n == 1:
        return CombinationType.SINGLE, values[0], 1
    if n == 2 and len(counts) == 1:
        return CombinationType.PAIR, values[0], 1
    if n == 3 and len(counts) == 1:
        return CombinationType.TRIPLE, values[0], 1
    if n == 4 and len(counts) == 1:
        return CombinationType.BOMB, values[0], 1
    # triple + single
    if n == 4:
        triples = [v for v, c in counts.items() if c == 3]
        if len(triples) == 1:
            return CombinationType.TRIPLE_SINGLE, triples[0], 1
        return None, None, None
    # triple + pair
    if n == 5:
        triples = [v for v, c in counts.items() if c == 3]
        pairs = [v for v, c in counts.items() if c == 2]
        if len(triples) == 1 and len(pairs) == 1:
            return CombinationType.TRIPLE_PAIR, triples[0], 1
        # fall through to straight check below
    # straight: >=5 distinct consecutive ranks, all <= ACE (no 2, no jokers)
    if n >= 5 and len(counts) == n and values[-1] <= ACE \
            and values[-1] - values[0] == n - 1:
        return CombinationType.STRAIGHT, values[-1], n
    # pair straight: >=3 consecutive pairs, all <= ACE
    if n >= 6 and n % 2 == 0 and all(c == 2 for c in counts.values()) \
            and values[-1] <= ACE and values[-1] - values[0] == n // 2 - 1:
        return CombinationType.PAIR_STRAIGHT, values[-1], n // 2
    # pure airplane: >=2 consecutive triples, all <= ACE
    if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts.values()) \
            and values[-1] <= ACE and values[-1] - values[0] == n // 3 - 1:
        return CombinationType.AIRPLANE, values[-1], n // 3
    # four with two singles (n == 6): one quad + any two other cards
    if n == 6:
        quads = [v for v, c in counts.items() if c == 4]
        if len(quads) == 1:
            return CombinationType.FOUR_TWO_SINGLE, quads[0], 1
        return None, None, None
    # four with two pairs (n == 8): one quad + exactly two pairs
    if n == 8:
        quads = [v for v, c in counts.items() if c == 4]
        if len(quads) == 1:
            others = {v: c for v, c in counts.items() if v != quads[0]}
            if all(c == 2 for c in others.values()) and len(others) == 2:
                return CombinationType.FOUR_TWO_PAIR, quads[0], 1
        # fall through to airplane-with-wings checks
    # airplane with wings
    res = _detect_airplane_wings(counts, values, n)
    if res:
        return res
    return None, None, None