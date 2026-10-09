'''Combination module: detection, comparison, and candidate generation for Dou Dizhu combos.'''
from collections import Counter
from enum import Enum
class ComboType(Enum):
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    TRIPLE_ONE = 4
    TRIPLE_PAIR = 5
    STRAIGHT = 6
    PAIR_STRAIGHT = 7
    PLANE = 8
    PLANE_SINGLE = 9
    PLANE_PAIR = 10
    FOUR_TWO = 11
    FOUR_TWO_PAIR = 12
    BOMB = 13
    ROCKET = 14
class Combo:
    def __init__(self, ctype, main_value, length, cards):
        self.type = ctype
        self.main_value = main_value
        self.length = length
        self.cards = list(cards)
    def size(self):
        return len(self.cards)
    def describe(self):
        # human-readable description
        ...
    def beats(self, other):
        if other is None:
            return True
        if self.type == ComboType.ROCKET:
            return True
        if other.type == ComboType.ROCKET:
            return False
        if self.type == ComboType.BOMB:
            if other.type == ComboType.BOMB:
                return self.main_value > other.main_value
            return True
        if other.type == ComboType.BOMB:
            return False
        return (self.type == other.type and self.length == other.length 
                and self.main_value > other.main_value)