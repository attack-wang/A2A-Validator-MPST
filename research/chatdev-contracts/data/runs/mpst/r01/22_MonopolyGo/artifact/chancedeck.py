class ChanceDeck:
    def __init__(self):
        self.cards = [...]
        random.shuffle
        self.index = 0
    def draw(self):
        card = self.cards[self.index]
        self.index = (self.index+1) % len
        return card