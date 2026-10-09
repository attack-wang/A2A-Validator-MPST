class Combination:
    KINDS = {...}
    def __init__(self, kind, main_rank, length, cards):
        self.kind = kind
        self.main = main_rank
        self.length = length
        self.cards = list(cards)
    def beats(self, current):
        if current is None:
            return True
        if self.kind == 'rocket':
            return True
        if current.kind == 'rocket':
            return False
        if self.kind == 'bomb':
            if current.kind == 'bomb':
                return self.main > current.main
            return True  # current is non-bomb non-rocket
        if current.kind == 'bomb':
            return False
        # both non-bomb, non-rocket
        return self.kind == current.kind and self.length == current.length and self.main > current.main
    def describe(self):
        ...