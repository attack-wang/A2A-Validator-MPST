'''
combo.py
Parses card selections into valid Dou Dizhu combinations and
implements the pass-or-beat comparison logic.
'''
from collections import Counter
from combotype import ComboType
class Combo:
    def __init__(self, cards, ctype, main_rank, length):
        self.cards = list(cards)
        self.ctype = ctype
        self.main_rank = main_rank
        self.length = length  # number of "units" (straight length, airplane size, ...)
    def beats(self, other):
        if other is None:
            return True  # leading play: any valid combo is allowed
        if self.ctype == ComboType.ROCKET:
            return True
        if other.ctype == ComboType.ROCKET:
            return False
        if self.ctype == ComboType.BOMB:
            if other.ctype == ComboType.BOMB:
                return self.main_rank > other.main_rank
            return True
        if other.ctype == ComboType.BOMB:
            return False
        return (self.ctype == other.ctype
                and self.length == other.length
                and self.main_rank > other.main_rank)
    def __repr__(self):
        return 'Combo(%s, main=%d, len=%d)' % (self.ctype.name, self.main_rank, self.length)
def _find_airplane_with_wings(cnt, k, wing_kind):
    """Locate k consecutive triples (ranks <= A) whose removal leaves
    exactly k singles or k pairs as wings. Returns (main_rank,) or None."""
    triple_candidates = sorted(r for r, c in cnt.items() if c >= 3 and r <= 14)
    for start in range(len(triple_candidates) - k + 1):
        run = triple_candidates[start:start + k]
        if run[-1] - run[0] == k - 1:
            remaining = Counter(cnt)
            for r in run:
                remaining[r] -= 3
                if remaining[r] == 0:
                    del remaining[r]
            if wing_kind == 'singles':
                if sum(remaining.values()) == k:
                    return run[-1]
            else:
                if len(remaining) == k and all(c == 2 for c in remaining.values()):
                    return run[-1]
    return None