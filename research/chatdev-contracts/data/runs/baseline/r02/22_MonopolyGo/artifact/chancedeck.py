class ChanceDeck:
    """A shuffled deck of simplified chance cards."""
    def __init__(self):
        self.cards = list(CHANCE_CARDS)
        random.shuffle(self.cards)
    def draw(self):
        if not self.cards:
            self.cards = list(CHANCE_CARDS)
            random.shuffle(self.cards)
        return self.cards.pop()