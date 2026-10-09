'''
combination.py: Combination types and pass-or-beat comparison logic.
'''
# Combination type constants
SINGLE = 'single'
PAIR = 'pair'
TRIO = 'trio'
TRIO_SINGLE = 'trio_single'
TRIO_PAIR = 'trio_pair'
STRAIGHT = 'straight'
PAIR_STRAIGHT = 'pair_straight'
AIRPLANE = 'airplane'
AIRPLANE_SINGLE = 'airplane_single'
AIRPLANE_PAIR = 'airplane_pair'
FOUR_TWO_SINGLES = 'four_two_singles'
FOUR_TWO_PAIRS = 'four_two_pairs'
BOMB = 'bomb'
ROCKET = 'rocket'
COMBINATION_NAMES = {
    SINGLE: '单牌 Single', PAIR: '对子 Pair', TRIO: '三张 Trio',
    TRIO_SINGLE: '三带一 Trio+Single', TRIO_PAIR: '三带二 Trio+Pair',
    STRAIGHT: '顺子 Straight', PAIR_STRAIGHT: '连对 Pair-Straight',
    AIRPLANE: '飞机 Airplane', AIRPLANE_SINGLE: '飞机带单 Airplane+Singles',
    AIRPLANE_PAIR: '飞机带对 Airplane+Pairs',
    FOUR_TWO_SINGLES: '四带二 Four+Two Singles', FOUR_TWO_PAIRS: '四带两对 Four+Two Pairs',
    BOMB: '炸弹 Bomb', ROCKET: '王炸 Rocket',
}
class Combination:
    """A played combination: type, key value, chain length and the cards used."""
    def __init__(self, ctype, cards, main_value, chain_length=1):
        """Store the type, the cards played, the ranking value and chain length."""
        self.ctype = ctype
        self.cards = list(cards)
        self.main_value = main_value
        self.chain_length = chain_length
    def beats(self, other):
        """Return True if this combination may be played on top of `other`."""
        if other is None:
            return True  # free lead
        if self.ctype == ROCKET:
            return True
        if other.ctype == ROCKET:
            return False
        if self.ctype == BOMB and other.ctype != BOMB:
            return True
        if other.ctype == BOMB and self.ctype != BOMB:
            return False
        if self.ctype != other.ctype:
            return False
        if self.chain_length != other.chain_length:
            return False
        return self.main_value > other.main_value
    def __repr__(self):
        """Debug representation showing type, main value and chain length."""
        return f"<{COMBINATION_NAMES.get(self.ctype, self.ctype)} main={self.main_value} len={self.chain_length}>"