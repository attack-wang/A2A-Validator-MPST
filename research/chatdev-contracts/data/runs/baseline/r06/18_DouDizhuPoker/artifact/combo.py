'''
combo.py
Single source of truth for ComboType and CardCombination...
'''
from enum import Enum
class ComboType(Enum):
    PASS = 'pass'
    SINGLE = 'single'
    PAIR = 'pair'
    TRIPLE = 'triple'
    TRIPLE_ONE = 'triple_one'
    TRIPLE_PAIR = 'triple_pair'
    STRAIGHT = 'straight'
    PAIR_STRAIGHT = 'pair_straight'
    PLANE = 'plane'
    PLANE_SINGLE = 'plane_single'
    PLANE_PAIR = 'plane_pair'
    FOUR_TWO = 'four_two'
    FOUR_TWO_PAIR = 'four_two_pair'
    BOMB = 'bomb'
    ROCKET = 'rocket'
    INVALID = 'invalid'