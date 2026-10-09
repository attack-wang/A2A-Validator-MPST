class ComboType(Enum): SINGLE, PAIR, TRIPLE, TRIPLE_SINGLE, TRIPLE_PAIR, STRAIGHT, PAIR_STRAIGHT, TRIPLE_STRAIGHT (airplane), AIRPLANE_SINGLE, AIRPLANE_PAIR, FOUR_TWO_SINGLE, FOUR_TWO_PAIR, BOMB, ROCKET
class Combination:
    def __init__(self, cards, combo_type, main_rank)
    def beats(self, other) -> bool
    @staticmethod parse(cards) -> Combination or None