from collections import Counter
from card import Card, RANK_VALUES, VALUE_TO_RANK
from combinations import ComboType
from combination import Combination
def is_consecutive(values):
    return all(values[i+1] - values[i] == 1 for i in range(len(values)-1))
def identify(cards):
    """Identify the combo type of a list of cards, or None if invalid."""
    n = len(cards)
    if n == 0:
        return None
    values = sorted(c.value for c in cards)
    counts = Counter(values)
    distinct = sorted(counts.keys())
    # Rocket: both jokers
    if n == 2 and values == [16, 17]:
        return Combination(ComboType.ROCKET, cards, main_value=17, size=2)
    # Single
    if n == 1:
        return Combination(ComboType.SINGLE, cards, main_value=values[0], size=1)
    # Pair
    if n == 2 and len(distinct) == 1:
        return Combination(ComboType.PAIR, cards, main_value=values[0], size=2)
    # Triple
    if n == 3 and len(distinct) == 1:
        return Combination(ComboType.TRIPLE, cards, main_value=values[0], size=3)
    # Bomb / Triple+Single
    if n == 4:
        if len(distinct) == 1:
            return Combination(ComboType.BOMB, cards, main_value=values[0], size=4)
        if len(distinct) == 2 and max(counts.values()) == 3:
            main_value = [v for v, c in counts.items() if c == 3][0]
            return Combination(ComboType.TRIPLE_ONE, cards, main_value=main_value, size=4)
        return None
    # Triple+Pair
    if n == 5:
        if len(distinct) == 2 and 3 in counts.values() and 2 in counts.values():
            main_value = [v for v, c in counts.items() if c == 3][0]
            return Combination(ComboType.TRIPLE_PAIR, cards, main_value=main_value, size=5)
    # Straight (5+ consecutive singles, no 2/jokers)
    if n >= 5 and len(distinct) == n and is_consecutive(distinct) and distinct[-1] <= 14:
        return Combination(ComboType.STRAIGHT, cards, main_value=distinct[-1], size=n)
    # Pair straight (3+ consecutive pairs, 6+ cards)
    if n >= 6 and n % 2 == 0 and all(c == 2 for c in counts.values()) and is_consecutive(distinct) and distinct[-1] <= 14:
        return Combination(ComboType.PAIR_STRAIGHT, cards, main_value=distinct[-1], size=n)
    # Pure airplane (2+ consecutive triples)
    if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts.values()) and is_consecutive(distinct) and distinct[-1] <= 14:
        return Combination(ComboType.AIRPLANE, cards, main_value=distinct[-1], size=n)
    # Airplane with singles: n == 4k, k consecutive triples + k kickers
    if n >= 8 and n % 4 == 0:
        k = n // 4
        body = _longest_triple_run(counts)
        if len(body) == k:
            leftover = {v: c - (3 if v in body else 0) for v, c in counts.items()}
            leftover = {v: c for v, c in leftover.items() if c > 0}
            if sum(leftover.values()) == k and max(leftover.values()) <= 3:
                # kickers cannot form a rocket (both jokers)? Actually with k>=2 kickers, if k==2 and leftover is {16:1, 17:1} that's rocket as wings — disallowed by standard rules
                if not (k == 2 and leftover.get(16) == 1 and leftover.get(17) == 1):
                    return Combination(ComboType.AIRPLANE_SINGLES, cards, main_value=body[-1], size=n)
    # Airplane with pairs: n == 5k, k consecutive triples + k pair wings
    if n >= 10 and n % 5 == 0:
        k = n // 5
        body = _longest_triple_run(counts)
        if len(body) == k:
            leftover = ...
            if all(c == 2 for c in leftover.values()):
                return Combination(ComboType.AIRPLANE_PAIRS, cards, main_value=body[-1], size=n)
    # Four with two singles: n == 6, quad + 2 kickers (kickers can't be both jokers)
    if n == 6:
        quads = [v for v, c in counts.items() if c == 4]
        if len(quads) == 1:
            rest = {v: c for v, c in counts.items() if v != quads[0]}
            if sum(rest.values()) == 2 and not (rest.get(16) == 1 and rest.get(17) == 1):
                return Combination(ComboType.FOUR_TWO_SINGLES, cards, main_value=quads[0], size=6)
    # Four with two pairs: n == 8, quad + 2 pairs
    if n == 8:
        quads = [v for v, c in counts.items() if c == 4]
        if len(quads) == 1:
            rest = [c for v, c in counts.items() if v != quads[0]]
            if rest == [2, 2]:
                return Combination(ComboType.FOUR_TWO_PAIRS, cards, main_value=quads[0], size=8)
    return None