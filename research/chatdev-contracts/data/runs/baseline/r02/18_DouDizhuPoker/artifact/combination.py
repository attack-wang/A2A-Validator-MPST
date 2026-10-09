def _counts(cards):
    counts = {}
    for c in cards:
        counts[c.value] = counts.get(c.value, 0) + 1
    return counts
def _is_run(values):
    """True if values form a consecutive ascending run that tops out at A (14)."""
    return (values == list(range(values[0], values[-1] + 1)) and values[-1] <= MAX_STRAIGHT_VALUE)
def identify(cards):
    n = len(cards)
    if n == 0:
        return CombType.INVALID, 0
    counts = _counts(cards)
    values = sorted(counts)
    count_values = sorted(counts.values())
    # Rocket: both jokers
    if n == 2 and set(values) == {16, 17}:
        return CombType.ROCKET, 17
    # Bomb: four of a kind
    if n == 4 and len(values) == 1:
        return CombType.BOMB, values[0]
    # Single
    if n == 1:
        return CombType.SINGLE, values[0]
    # Pair (jokers can't pair: only one of each exists, so len(values)==1 with joker impossible)
    if n == 2 and len(values) == 1:
        return CombType.PAIR, values[0]
    # Triple
    if n == 3 and len(values) == 1:
        return CombType.TRIPLE, values[0]
    # Triple + single
    if n == 4 and count_values == [1, 3]:
        triple = [v for v, c in counts.items() if c == 3][0]
        return CombType.TRIPLE_ONE, triple
    # Triple + pair
    if n == 5 and count_values == [2, 3]:
        triple = [v for v, c in counts.items() if c == 3][0]
        return CombType.TRIPLE_PAIR, triple
    # Straight: >=5 distinct consecutive values, max <= A
    if n >= 5 and len(values) == n and _is_run(values):
        return CombType.STRAIGHT, values[-1]
    # Pair straight: >=3 consecutive pairs
    if n >= 6 and n % 2 == 0 and set(counts.values()) == {2} and _is_run(values):
        return CombType.PAIR_STRAIGHT, values[-1]
    # Pure airplane: >=2 consecutive triples
    if n >= 6 and n % 3 == 0 and set(counts.values()) == {3} and _is_run(values):
        return CombType.AIRPLANE, values[-1]
    # Airplane with single wings: k triples + k singles, n = 4k
    if n >= 8 and n % 4 == 0:
        k = n // 4
        result = _find_airplane_wings(counts, k, wing_size=1)
        if result is not None:
            return CombType.AIRPLANE_SINGLE, result
    # Airplane with pair wings: k triples + k pairs, n = 5k
    if n >= 10 and n % 5 == 0:
        k = n // 5
        result = _find_airplane_wings(counts, k, wing_size=2)
        if result is not None:
            return CombType.AIRPLANE_PAIR, result
    # Four + two singles
    if n == 6 and 4 in counts.values():
        quad = [v for v, c in counts.items() if c == 4][0]
        return CombType.FOUR_TWO, quad
    # Four + two pairs
    if n == 8 and 4 in counts.values():
        rest = {v: c for v, c in counts.items() if c != 4}
        if sum(rest.values()) == 4 and all(c % 2 == 0 for c in rest.values()):
            quad = [v for v, c in counts.items() if c == 4][0]
            return CombType.FOUR_TWO_PAIR, quad
    return CombType.INVALID, 0