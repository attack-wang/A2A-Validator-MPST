def _find_groups(hand):
    """Return dict value -> list of cards with that value."""
    groups = {}
    for c in hand:
        groups.setdefault(c.value, []).append(c)
    return groups