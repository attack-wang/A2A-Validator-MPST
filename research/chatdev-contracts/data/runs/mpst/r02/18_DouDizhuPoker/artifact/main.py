def enumerate_moves(hand):
    '''Return a list of all legal combinations playable from `hand`.'''
    moves = []
    counts = Counter(c.rank for c in hand)
    by_rank = {r: [c for c in hand if c.rank == r] for r in counts}
    # singles
    for r, cards in by_rank.items():
        moves.append(cards[:1])
    # pairs
    for r, cards in by_rank.items():
        if len(cards) >= 2:
            moves.append(cards[:2])
    # triples
    for r, cards in by_rank.items():
        if len(cards) >= 3:
            moves.append(cards[:3])
    # bombs
    for r, cards in by_rank.items():
        if len(cards) == 4:
            moves.append(cards[:4])
    # rocket
    if 'SJ' in counts and 'BJ' in counts:
        moves.append(by_rank['SJ'][:1] + by_rank['BJ'][:1])
    # triple + kickers
    triples = [r for r, c in counts.items() if c >= 3]
    singles_avail = ... # kickers
    for r in triples:
        for kicker_rank in counts:
            if kicker_rank != r:
                moves.append(by_rank[r][:3] + by_rank[kicker_rank][:1])  # triple_one
        # triple_pair: need a pair kicker
        for kicker_rank, c in counts.items():
            if kicker_rank != r and c >= 2:
                moves.append(by_rank[r][:3] + by_rank[kicker_rank][:2])
    # straights (length 5..12)
    ...
    # double straights
    ...
    # triple straights
    ...
    # airplanes with wings
    ...
    # four-two
    ...
    return moves