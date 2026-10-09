class ComboType(Enum):
    SINGLE, PAIR, TRIPLE, TRIPLE_ONE, TRIPLE_PAIR, STRAIGHT, PAIR_STRAIGHT, PLANE, PLANE_SINGLE, PLANE_PAIR, FOUR_TWO_SINGLES, FOUR_TWO_PAIRS, BOMB, ROCKET, INVALID, PASS
class Combination:
    def __init__(self, cards, combo_type, main_value, length)
    @property is_bomb / is_rocket
    def beats(other) -> bool
def identify(cards) -> Combination or None:
    # analyze the list of cards and return a Combination if valid