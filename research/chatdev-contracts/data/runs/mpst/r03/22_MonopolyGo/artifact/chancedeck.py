class ChanceDeck:
    def __init__(self):
        self._cards = [ChanceCard(desc, effect), ...]
        self._draw_pile = []
        self._reshuffle()
    def _reshuffle(self):
        self._draw_pile = self._cards[:]
        random.shuffle(self._draw_pile)
    def draw(self):
        if not self._draw_pile:
            self._reshuffle()
        return self._draw_pile.pop()