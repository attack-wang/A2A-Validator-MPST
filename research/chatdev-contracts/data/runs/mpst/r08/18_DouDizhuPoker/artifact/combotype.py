from enum import Enum
class ComboType(Enum):
    SINGLE = 'single'
    PAIR = 'pair'
    TRIPLE = 'triple'
    TRIPLE_ONE = 'triple_one'
    TRIPLE_PAIR = 'triple_pair'
    STRAIGHT = 'straight'
    DOUBLE_STRAIGHT = 'double_straight'  # consecutive pairs
    TRIPLE_STRAIGHT = 'triple_straight'  # airplane without wings
    AIRPLANE_SINGLE = 'airplane_single'
    AIRPLANE_PAIR = 'airplane_pair'
    FOUR_TWO = 'four_two'  # four with two singles
    FOUR_TWO_PAIR = 'four_two_pair'
    BOMB = 'bomb'
    ROCKET = 'rocket'