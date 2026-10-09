class Combination:
    def __init__(self, ctype, cards, main_value, size):
        self.ctype = ctype
        self.cards = list(cards)
        self.main_value = main_value
        self.size = size
    def beats(self, other):
        if other is None: return True
        if self.ctype == ComboType.ROCKET: return True
        if other.ctype == ComboType.ROCKET: return False
        if self.ctype == ComboType.BOMB and other.ctype != ComboType.BOMB: return True
        if other.ctype == ComboType.BOMB and self.ctype != ComboType.BOMB: return False
        if self.ctype == other.ctype and self.size == other.size:
            return self.main_value > other.main_value
        return False
    def describe(self):
        return f"{self.ctype.value} (main rank: {VALUE_TO_RANK[self.main_value]})"