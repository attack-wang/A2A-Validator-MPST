'''
combos.py
Enumeration of every legal Dou Dizhu combination type.
'''
from enum import Enum
class ComboType(Enum):
    SINGLE = 'single'
    PAIR = 'pair'
    TRIPLE = 'triple'
    TRIPLE_ONE = 'triple_one'
    TRIPLE_PAIR = 'triple_pair'
    STRAIGHT = 'straight'
    DOUBLE_STRAIGHT = 'double_straight'
    TRIPLE_STRAIGHT = 'triple_straight'
    AIRPLANE_SINGLE = 'airplane_single'
    AIRPLANE_PAIR = 'airplane_pair'
    FOUR_TWO_SINGLE = 'four_two_single'
    FOUR_TWO_PAIR = 'four_two_pair'
    BOMB = 'bomb'
    ROCKET = 'rocket'