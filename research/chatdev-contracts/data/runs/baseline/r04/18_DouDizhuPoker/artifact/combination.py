class Combination:
    def __init__(self, cards):
        self.cards = sorted(cards)
        self.n_cards = len(cards)
        self.type, self.main_rank = classify(cards)  # returns (CombinationType, main_rank or None)
    @property
    def is_valid(self): return self.type != CombinationType.INVALID