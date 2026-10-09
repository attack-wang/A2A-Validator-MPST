'''
chance.py
Defines ChanceCard and ChanceDeck...
'''
import random
class ChanceCard:
    def __init__(self, description, effect_key, value=None):
        self.description = description
        self.effect_key = effect_key
        self.value = value
    def __str__(self):
        return self.description
class ChanceDeck:
    def __init__(self):
        self._draw_pile = [
            ChanceCard("Bank pays you a dividend of $50", "money", 50),
            ChanceCard("You win $100!", "money", 100),
            ChanceCard("Pay poor tax of $50 (goes to Free Parking pot)", "money", -50),
            ChanceCard("Advance to GO and collect $200", "move_to", 0),
            ChanceCard("Go directly to Jail! Do not pass GO.", "go_to_jail", None),
            ChanceCard("Get Out of Jail Free — keep this card", "jail_free", None),
            ChanceCard("Advance 3 spaces", "move", 3),
            ChanceCard("Go back 3 spaces", "move", -3),
        ]
        random.shuffle(self._draw_pile)
        self._discard = []
        self._held = []  # GOOJF cards currently out of rotation
    def draw(self):
        if not self._draw_pile:
            self._draw_pile = self._discard
            self._discard = []
            random.shuffle(self._draw_pile)
        if not self._draw_pile:
            return None
        card = self._draw_pile.pop()
        if card.effect_key == "jail_free":
            self._held.append(card)
        else:
            self._discard.append(card)
        return card
    def return_card(self, card):
        if card in self._held:
            self._held.remove(card)
        if card not in self._discard:
            self._discard.append(card)
    def cards_remaining(self):
        return len(self._draw_pile) + len(self._discard)