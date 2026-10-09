def parse_combination(cards):
    if not cards:
        return Combination(ComboType.PASS, 0, 0, [])
    counts = Counter(c.rank for c in cards)
    n = len(cards)
    ranks = sorted(counts)
    rank_groups = {cnt: sorted(r for r, c in counts.items() if c == cnt) for cnt in (1, 2, 3, 4)}