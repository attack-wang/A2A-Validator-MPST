'''
ai.py
Simple heuristic AI for Dou Dizhu: bidding evaluation and play selection.
'''
from collections import Counter
from combo import Combo, parse_combo
from combotype import ComboType
def hand_points(hand):
    points = 0
    cnt = Counter(c.rank for c in hand)
    if cnt.get(17, 0) > 0:
        points += 3
    if cnt.get(16, 0) > 0:
        points += 2
    points += 2 * cnt.get(15, 0)
    points += 1 * cnt.get(14, 0)
    bombs = sum(1 for c in cnt.values() if c == 4)
    points += 3 * bombs
    return points
def decide_bid(hand, highest_bid):
    points = hand_points(hand)
    if points >= 8:
        bid = 3
    elif points >= 5:
        bid = 2
    elif points >= 3:
        bid = 1
    else:
        bid = 0
    return bid if bid > highest_bid else 0  # 0 = pass