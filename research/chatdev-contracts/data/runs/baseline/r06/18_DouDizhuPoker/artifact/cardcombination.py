class CardCombination:
    def __init__(self, cards, ctype, main_rank, length, chain_length=1):
        self.cards = list(cards)
        self.type = ctype
        self.main_rank = main_rank
        self.length = length          # total number of cards
        self.chain_length = chain_length  # number of grouped units (e.g., triples in a plane)
    def beats(self, other):
        if other is None or other.type == ComboType.PASS:
            return True
        if self.type == ComboType.ROCKET:
            return other.type != ComboType.ROCKET
        if other.type == ComboType.ROCKET:
            return False
        if self.type == ComboType.BOMB:
            if other.type == ComboType.BOMB:
                return self.main_rank > other.main_rank
            return True
        if other.type == ComboType.BOMB:
            return False
        if self.type != other.type:
            return False
        if self.length != other.length:
            return False
        if self.chain_length != other.chain_length:
            return False
        return self.main_rank > other.main_rank
    def describe(self):
        ...