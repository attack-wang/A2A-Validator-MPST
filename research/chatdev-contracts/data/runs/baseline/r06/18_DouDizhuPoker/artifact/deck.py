class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in range(3,16) for s in SUITS] + [Card(16), Card(17)]
    def shuffle(self)
    def deal(self): returns (hand1, hand2, hand3, bottom) each 17/17/17/3