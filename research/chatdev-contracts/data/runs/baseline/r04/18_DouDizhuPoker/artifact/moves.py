def generate_moves(hand, target=None):
    """hand: list of Card; target: Combination or None. Returns list of card-lists."""
    counts = Counter(c.rank for c in hand)
    by_rank = {r: [c for c in hand if c.rank == r] for r in counts}
    moves = []
    if target is None:
        # all lead moves
        for each type...:
        # singles, pairs, triples, triple+1, triple+2, straights, pair straights, airplanes, bombs, rocket, four+2
    else:
        if target.type == ROCKET: return []
        # same type matching
        # bombs
        # rocket
    return moves