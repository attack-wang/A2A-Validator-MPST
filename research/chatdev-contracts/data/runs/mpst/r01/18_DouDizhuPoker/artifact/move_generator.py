'''
Move generator: enumerate all valid leading combinations and all valid responses
that beat a given combination for a player's hand.
'''
from collections import Counter
from card import Card
from combination import Combination, CombType
MAX_SEQ = 14  # 'A'
def _buckets(hand):
    b = {}
    for c in hand:
        b.setdefault(c.value, []).append(c)
    return b
def _mk(cards, ctype, main_value, length):
    return Combination(cards, ctype, main_value, length)
def all_singles(hand):
    b = _buckets(hand)
    return [_mk([b[v][0]], CombType.SINGLE, v, 1) for v in sorted(b)]
def all_pairs(hand):
    b = _buckets(hand)
    return [_mk(b[v][:2], CombType.PAIR, v, 1) for v in sorted(b) if len(b[v]) >= 2]
def all_triples(hand):
    b = _buckets(hand)
    return [_mk(b[v][:3], CombType.TRIPLE, v, 1) for v in sorted(b) if len(b[v]) >= 3]
def all_bombs(hand):
    b = _buckets(hand)
    return [_mk(b[v][:4], CombType.BOMB, v, 1) for v in sorted(b) if len(b[v]) == 4]
def rocket(hand):
    b = _buckets(hand)
    if 16 in b and 17 in b:
        return [_mk([b[16][0], b[17][0]], CombType.ROCKET, 17, 1)]
    return []
def all_straights(hand):
    b = _buckets(hand)
    moves = []
    for length in range(5, 13):
        for start in range(3, MAX_SEQ - length + 2):
            values = range(start, start + length)
            if all(v in b for v in values):
                cards = [b[v][0] for v in values]
                moves.append(_mk(cards, CombType.STRAIGHT, start + length - 1, length))
    return moves
def all_pair_straights(hand):
    b = _buckets(hand)
    moves = []
    for length in range(3, 11):  # number of pairs
        for start in range(3, MAX_SEQ - length + 2):
            values = range(start, start + length)
            if all(len(b.get(v, [])) >= 2 for v in values):
                cards = []
                for v in values:
                    cards.extend(b[v][:2])
                moves.append(_mk(cards, CombType.PAIR_STRAIGHT, start + length - 1, length))
    return moves
def all_airplanes(hand):
    b = _buckets(hand)
    moves = []
    triple_values = [v for v in sorted(b) if len(b[v]) >= 3 and v <= MAX_SEQ]
    # pure airplanes and airplanes with wings
    for k in range(2, 7):
        for i in range(len(triple_values) - k + 1):
            run = triple_values[i:i + k]
            if run[-1] - run[0] != k - 1:
                continue
            main = run[-1]
            cards = []
            for v in run:
                cards.extend(b[v][:3])
            moves.append(_mk(list(cards), CombType.AIRPLANE, main, k))
            # with single wings
            wings = _pick_kickers(b, run, k, 1)
            if wings is not None:
                moves.append(_mk(cards + wings, CombType.AIRPLANE_SINGLE, main, k))
            # with pair wings
            wings = _pick_kickers(b, run, k, 2)
            if wings is not None:
                moves.append(_mk(cards + wings, CombType.AIRPLANE_PAIR, main, k))
    return moves