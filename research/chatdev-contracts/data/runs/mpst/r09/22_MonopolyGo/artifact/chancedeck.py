class ChanceDeck:
    def __init__(self):
        self._build()
    def _build(self):
        self._draw_pile = [ ... 8 cards ... ]
        random.shuffle(self._draw_pile)
        self._discard = []
        self._held = []  # GOOJF cards out of rotation
    def draw(self):
        if not self._draw_pile:
            self._draw_pile = self._discard
            self._discard = []
            random.shuffle(self._draw_pile)
        if not self._draw_pile:
            return None  # only possible if all remaining cards are held GOOJF
        card = self._draw_pile.pop()
        if card.effect_key == "jail_free":
            self._held.append(card)
        else:
            self._discard.append(card)
        return card
    def discard(self, card):
        """Return a normal card to the discard pile (after its effect resolves)."""
        if card not in self._discard and card not in self._held:
            self._discard.append(card)
    def restore_jail_free(self):
        """Return a used GOOJF card to the discard pile so it can be drawn again."""
        if self._held:
            card = self._held.pop()
            self._discard.append(card)
            return card
        return None