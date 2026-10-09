'''
combination.py
The Combination class stores a validated play and implements the
pass-or-beat comparison logic (beats()).
'''
from combos import ComboType
class Combination:
    def __init__(self, ctype, cards, main_value, length):
        self.type = ctype
        self.cards = list(cards)
        self.main_value = main_value   # decisive rank value used for comparison
        self.length = length           # number of "units" for sequences; 1 otherwise
    def __str__(self):
        cards_str = ' '.join(str(c) for c in self.cards)
        return f"{self.type.value} [{cards_str}]"
    def beats(self, other):
        '''Return True if this combination beats `other` (pass-or-beat rule).'''
        if other is None:
            return True  # leading a fresh trick: any valid combination is allowed
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
        return (self.type == other.type
                and self.length == other.length
                and self.main_value > other.main_value)