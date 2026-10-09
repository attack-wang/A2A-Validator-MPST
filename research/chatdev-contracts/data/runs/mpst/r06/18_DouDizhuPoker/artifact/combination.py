class Combination:
    def __init__(self, cards):
        self.cards = list(cards)
        self.type, self.main_value, self.length = self._analyze()
    def is_valid(self):
        return self.type != 'invalid'
    def _analyze(self):
        ...