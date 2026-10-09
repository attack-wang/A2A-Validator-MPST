def classify(cards):
    n = len(cards)
    if n == 0:
        return None
    values = sorted(c.value for c in cards)
    counts = Counter(values)
    # Rocket
    if n == 2 and counts[SMALL_JOKER] == 1 and counts[BIG_JOKER] == 1:
        return Combination(ROCKET, BIG_JOKER, 1, cards)
    # Single
    if n == 1:
        return Combination(SINGLE, values[0], 1, cards)
    # Pair
    if n == 2 and len(counts) == 1:
        return Combination(PAIR, values[0], 1, cards)
    # Trio
    if n == 3 and len(counts) == 1:
        return Combination(TRIO, values[0], 1, cards)
    # Bomb
    if n == 4 and len(counts) == 1:
        return Combination(BOMB, values[0], 1, cards)
    # Trio + single
    if n == 4 and len(counts) == 2 and 3 in counts.values():
        trio_val = [v for v, c in counts.items() if c == 3][0]
        return Combination(TRIO_SINGLE, trio_val, 1, cards)
    # Trio + pair
    if n == 5 and len(counts) == 2 and sorted(counts.values()) == [2, 3]:
        trio_val = [v for v, c in counts.items() if c == 3][0]
        return Combination(TRIO_PAIR, trio_val, 1, cards)
    # Straight: >= 5 consecutive, all counts == 1, max <= 14 (A)
    if n >= 5 and len(counts) == n and max(values) <= 14 and values[-1] - values[0] == n - 1:
        return Combination(STRAIGHT, values[0], n, cards)
    # Pair straight: >= 3 consecutive pairs, all counts == 2, max <= 14
    if n >= 6 and n % 2 == 0 and len(counts) == n // 2 and all(c == 2 for c in counts.values()) and max(values) <= 14:
        vals = sorted(counts.keys())
        if vals[-1] - vals[0] == len(vals) - 1:
            return Combination(PAIR_STRAIGHT, vals[0], len(vals), cards)
    # Airplane (pure trios): >= 2 consecutive trios
    if n >= 6 and n % 3 == 0 and len(counts) == n // 3 and all(c == 3 for c in counts.values()) and max(values) <= 14:
        vals = sorted(counts.keys())
        if vals[-1] - vals[0] == len(vals) - 1:
            return Combination(AIRPLANE, vals[0], len(vals), cards)
    # Airplane + singles: k trios consecutive + k singles
    # Airplane + pairs: k trios consecutive + k pairs
    # Four + 2 singles
    if n == 6 and 4 in counts.values():
        four_val = [v for v, c in counts.items() if c == 4][0]
        # the remaining 2 cards: could be 2 singles or 1 pair
        # Standard: four + 2 singles. If remaining is a pair, some rules treat as four+2 singles too.
        # I'll allow both interpretations? No - four+2singles requires 2 distinct singles OR a pair counts as two singles in some rules.
        # To keep it simple: remaining 2 cards must not be a rocket (both jokers).
        rest = [v for v, c in counts.items() if v != four_val]
        if len(rest) == 2:  # two distinct singles
            if set(rest) == {SMALL_JOKER, BIG_JOKER}:
                return None  # rocket can't be kicker
            return Combination(FOUR_TWO_SINGLES, four_val, 1, cards)
        elif len(rest) == 1 and counts[rest[0]] == 2:
            # pair as kicker - ambiguous; some rules allow as four+2 singles
            # I'll treat as four+2 singles (common online rule)
            return Combination(FOUR_TWO_SINGLES, four_val, 1, cards)
    # Four + 2 pairs
    if n == 8:
        four_val = [v for v, c in counts.items() if c == 4]
        if len(four_val) == 1:
            others = {v: c for v, c in counts.items() if v != four_val[0]}
            if all(c == 2 for c in others.values()) and len(others) == 2:
                return Combination(FOUR_TWO_PAIRS, four_val[0], 1, cards)
    # Airplane with wings - need more complex logic
    # k consecutive trios + k singles (n = 4k) or k pairs (n = 5k)
    ...