'''
parser.py
Validates a set of cards as a legal Dou Dizhu combination and returns a
Combination object, or None when the cards do not form a legal play.
'''
from collections import Counter
from cards import RANK_VALUE
from combos import ComboType
from combination import Combination
# Straights / planes may only use ranks 3..A (values 3..14); '2' and jokers excluded.
STRAIGHT_MAX = RANK_VALUE['A']
def _consecutive(values):
    return all(b - a == 1 for a, b in zip(values, values[1:]))
def _parse_airplane_single(counts, n):
    '''k consecutive triples + k single kickers (n == 4k, k >= 2).'''
    if n < 8 or n % 4 != 0:
        return None
    k = n // 4
    candidates = sorted(RANK_VALUE[r] for r, c in counts.items() if c >= 3 and RANK_VALUE[r] <= STRAIGHT_MAX)
    best = None
    for i in range(len(candidates) - k + 1):
        run = candidates[i:i + k]
        if _consecutive(run):
            best = run  # keep the highest-valued valid run (strongest reading)
    if best is None:
        return None
    return Combination(ComboType.AIRPLANE_SINGLE, ..., best[-1], k)